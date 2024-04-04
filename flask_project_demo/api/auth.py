"""Blueprint relativa all'autenticazione dell'api."""

from http import HTTPStatus

from flask import Blueprint, Request, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError

from flask_project_demo.db import Session
from flask_project_demo.models import User

auth = Blueprint("auth", __name__, url_prefix="/auth")


class LoginSchema(Schema):
    """Schema per validare il Login."""

    email = fields.String(required=True)
    password = fields.String(required=True)

    @classmethod
    def validate_request(cls, request: Request) -> tuple[str, str]:
        """Validate the request.

        Parameters
        ----------
        request : Request
            The URL request

        Returns
        -------
        tuple[str, str]
            The parsed request

        Raises
        ------
        ValidationError
            if the request is invalid.
        """
        data: dict = cls().load(request.get_json())  # type: ignore
        return data["email"], data["password"]


@auth.post("/login")
def login():
    """User login.

    Authenticate a user and returns a JWT token.
    """
    try:
        email, password = LoginSchema.validate_request(request)
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
