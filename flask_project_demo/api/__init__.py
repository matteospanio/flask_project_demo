from flask import Blueprint, redirect
from flask_project_demo.api.users import users
from flask_project_demo.api.auth import auth

api = Blueprint("api", __name__)
api.register_blueprint(auth, url_prefix="/auth")
api.register_blueprint(users, url_prefix="/users")


@api.get("/")
def index():
    return redirect("/api/v1/docs/swagger_ui")
