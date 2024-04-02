from flask import Blueprint, jsonify, request
from flask_project_demo.models import User
import flask_project_demo.models.user as user_table
from flask_project_demo.db import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

users = Blueprint("users", __name__)


@users.get("/")
def get_users():
    with Session(engine) as session:
        result = session.scalars(select(User)).all()

    return jsonify(result), 200


@users.get("/<int:id>")
def get_user(id: int):
    with Session(engine) as session:
        result = session.scalars(select(User).where(User.id == id)).one_or_none()

    return jsonify(result), 200


@users.post("/")
def create_user():
    data = request.form
    if not user_table.is_valid(data):
        return {"message": "Invalid data in request."}, 400

    new_user = User(name=data["name"], email=data["email"])  # type: ignore
    with Session(engine) as session:
        session.add(new_user)
        session.commit()

    return {"message": "User created!"}, 201


@users.put("/<int:id>")
def update_user(id):
    return {"message": f"User {id} updated!"}, 200


@users.delete("/<int:id>")
def delete_user(id):
    return {"message": f"User {id} deleted!"}, 204
