"""Blueprint relativa all'autenticazione dell'api."""

from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from flask import Blueprint, Request, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
    get_jwt,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError

from flask_project_demo.db import Session
from flask_project_demo.models import User
from flask_project_demo.plugins import jwt_manager

auth = Blueprint("auth", __name__, url_prefix="/auth")


@jwt_manager.user_identity_loader
def user_identity_lookup(user: User):
    """Set the user identity in the JWT token."""
    return {"email": user.email, "id": user.id, "name": user.name}


@jwt_manager.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """Get the user from the JWT token."""
    identity = jwt_data["sub"]
    with Session() as session:
        return session.query(User).filter(User.email == identity["email"]).one_or_none()


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
        return {"message": e.messages}, HTTPStatus.BAD_REQUEST

    with Session() as session:
        user = session.query(User).filter(User.email == email).one_or_none()

    if user and user.verify_password(password):
        access_token = create_access_token(
            user,
            fresh=timedelta(minutes=60),
            expires_delta=timedelta(days=1),
        )
        refresh_token = create_refresh_token(
            user,
            expires_delta=timedelta(days=30),
        )
        response = jsonify(access_token=access_token, refresh_token=refresh_token)
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, HTTPStatus.OK

    return {"message": "Invalid email or password."}, HTTPStatus.UNAUTHORIZED


@auth.get("/logout")
@jwt_required()
def logout():
    """User logout.

    Delete the JWT token cookie.
    """
    response = jsonify({"message": "Logout successful."})
    unset_jwt_cookies(response)

    return response, HTTPStatus.OK


@auth.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    """Refresh the JWT token."""
    current_user = get_jwt()
    access_token = create_access_token(identity=current_user, fresh=True)
    response = jsonify({"message": "Token refreshed."})
    set_access_cookies(response, access_token)

    return response, HTTPStatus.OK


def refresh_expiring_token(response):
    """Refresh the JWT token.

    This callback is called before every request to check if the
    JWT token is about to expire and refresh it.
    """
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            set_access_cookies(response, access_token)

        return response
    except (RuntimeError, KeyError):
        return response
