from flask import Blueprint, jsonify, request
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from marshmallow import ValidationError
from flask_project_demo.db import Session
from flask_project_demo.models.user import (
    User,
    UserPostSchema,
    UserPatchSchema,
)
from flask_project_demo.typing import UserQuerySchema

users = Blueprint("users", __name__)


@users.get("/")
@jwt_required()
def get_users():
    """Get all users.

    Query the `users` table filtering by name or email.
    """
    try:
        req = UserQuerySchema.validate_request(request)
    except ValidationError as e:
        return {"message": e.messages}, HTTPStatus.BAD_REQUEST

    with Session() as session:
        query = select(User)

        if req.email:
            query = query.where(User.email.like(f"%{req.email}%"))

        if req.name:
            query = query.where(User.name.like(f"%{req.name}%"))

        query = query.limit(req.limit).offset(req.offset)

        if req.order:
            query = query.order_by(User.id if req.order == "asc" else User.id.desc())

        result = session.scalars(query).all()

    return jsonify(result), HTTPStatus.OK


@users.get("/<int:id>")
@jwt_required()
def get_user(id: int):
    """Get a user by ID."""
    with Session() as session:
        result = session.scalars(select(User).where(User.id == id)).one_or_none()

    return jsonify(result), HTTPStatus.OK


@users.post("/")
def create_user():
    """Create a new user."""
    data = request.get_json()
    try:
        UserPostSchema().load(data)
    except ValidationError:
        return {"message": "Invalid data in request."}, HTTPStatus.BAD_REQUEST

    new_user = User(
        name=data["name"],
        email=data["email"],
        hashed_password=generate_password_hash(data["password"]),
    )
    with Session() as session:
        session.add(new_user)
        session.commit()

    return {"message": "User created!"}, HTTPStatus.CREATED


@users.patch("/<int:id>")
@jwt_required()
def update_user(id):
    """Update a user."""
    with Session() as session:
        user = session.scalars(select(User).where(User.id == id)).one_or_none()

        if not user:
            return {"message": f"User {id} not found!"}, HTTPStatus.NOT_FOUND

        data = request.get_json()
        try:
            UserPatchSchema().load(data)
        except ValidationError:
            return {"message": "Invalid data in request."}, HTTPStatus.BAD_REQUEST
        if data == {}:
            return {"message": "No data provided in request."}, HTTPStatus.BAD_REQUEST

        if get_jwt_identity() != user.email:
            return {"message": "Unauthorized access."}, HTTPStatus.UNAUTHORIZED

        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password = data["password"]
        session.commit()

    return {"message": f"User {id} updated!"}, HTTPStatus.OK


@users.delete("/<int:id>")
@jwt_required()
def delete_user(id):
    """Delete a user."""
    with Session() as session:
        user = session.scalars(select(User).where(User.id == id)).one_or_none()

        if not user:
            return {"message": f"User {id} not found!"}, HTTPStatus.NOT_FOUND

        print(get_jwt_identity())
        if get_jwt_identity() != user.email:
            return {"message": "Unauthorized access."}, HTTPStatus.UNAUTHORIZED
        session.delete(user)
        session.commit()

    return {"message": f"User {id} deleted!"}, HTTPStatus.OK
