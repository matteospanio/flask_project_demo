from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flask_project_demo.db import Session
from flask_project_demo.models import User
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_project_demo.typing import LoginSchema
from marshmallow.exceptions import ValidationError

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.post("/login")
def login():
    """User login.

    Authenticate a user and returns a JWT token.
    """
    data = request.get_json()
    try:
        email, password = LoginSchema.validate_request(data)
    except ValidationError as e:
        print(e.messages)
        return {"message": e.messages}, HTTPStatus.BAD_REQUEST

    with Session() as session:
        user = session.query(User).filter(User.email == email).one_or_none()

    if user and user.verify_password(password):
        access_token = create_access_token(identity=user.email)
        refresh_token = create_refresh_token(identity=user.email)

        return (
            jsonify(access_token=access_token, refresh_token=refresh_token),
            HTTPStatus.OK,
        )

    return {"message": "Invalid email or password."}, HTTPStatus.UNAUTHORIZED
