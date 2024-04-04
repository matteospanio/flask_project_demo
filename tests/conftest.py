from flask import Flask
from flask_project_demo.db import create_database, delete_database
import pytest
from flask_project_demo import create_app
from flask_project_demo.db import Session
from flask_project_demo.models import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app("test")

    create_database()

    test_user = User(
        "Tester",
        "test@test.com",
        generate_password_hash("pwd"),
    )

    with Session() as session:
        session.add(test_user)
        session.commit()

    yield app

    delete_database()


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@pytest.fixture
def auth_client(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@test.com",
            "password": "pwd",
        },
    )

    token = response.json["access_token"]

    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"

    return client


@pytest.fixture
def runner(app: Flask):
    return app.test_cli_runner()
