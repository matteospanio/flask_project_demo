from flask import Blueprint
from flask_project_demo.api.users import users

api = Blueprint("api", __name__)
api.register_blueprint(users, url_prefix="/users")


@api.get("/")
def index():
    return {"message": "Hello, API!"}
