from flask_project_demo.db import Session
from flask_project_demo.models import User
from sqlalchemy import select
import pytest

API_URL = "/api/v1/users/"


class TestGetUsers:
    def test_requires_authentication(self, client):
        response = client.get(API_URL)

        assert response.status_code == 401

    def test_standard_usage(self, auth_client):
        response = auth_client.get(API_URL)

        assert response.status_code == 200

    def test_filtered_result(self, auth_client):
        response = auth_client.get(API_URL + "?name=Tester")

        assert len(response.json) == 1
        assert response.json[0]["name"] == "Tester"
        assert response.json[0]["email"] == "test@test.com"

    @pytest.mark.parametrize(
        "filter,expected",
        [
            ("limit=-1", 400),
            ("offset=-1", 400),
            ("order=invalid", 400),
            ("name=Tester", 200),
            ("email=test", 200),
            ("order=asc", 200),
            ("order=desc", 200),
            ("", 200),
        ],
    )
    def test_query_parameters(self, auth_client, filter, expected):
        response = auth_client.get(f"{API_URL}?{filter}")

        assert response.status_code == expected


class TestGetSingleUser:
    def test_requires_authentication(self, client):
        response = client.get(API_URL + "1")

        assert response.status_code == 401

    def test_get_user(self, auth_client):
        response = auth_client.get(API_URL + "1")

        assert response.status_code == 200


class TestPostUsers:
    @pytest.mark.parametrize(
        "payload, expected",
        [
            (
                {
                    "name": "John Doe",
                    "email": "john@doe.com",
                    "password": "password",
                },
                201,
            ),
            (
                {
                    "name": "John Doe",
                    "email": "invalid_email",
                    "password": "password",
                },
                400,
            ),
            (
                {
                    "email": "invalid_email",
                    "password": "password",
                },
                400,
            ),
            ({}, 400),
        ],
    )
    def test_new_user(self, client, payload, expected):
        response = client.post(
            API_URL,
            json=payload,
        )

        assert response.status_code == expected


class TestPatchUser:

    def test_requires_authentication(self, client):
        response = client.patch(API_URL + "1", json={"name": "New Name"})

        assert response.status_code == 401

    @pytest.mark.parametrize(
        "payload, expected",
        [
            ({"name": "New Name"}, 200),
            ({"email": "new_email"}, 400),
            ({"email": "new@email.com"}, 200),
            ({"password": "new_password"}, 200),
            ({}, 400),
        ],
    )
    def test_change_record(self, auth_client, payload, expected):
        with Session() as session:
            query = select(User).where(User.name == "Tester")
            tester = session.scalars(query).one()

            response = auth_client.patch(
                f"{API_URL}{tester.id}",
                json=payload,
            )

            assert response.status_code == expected

            if response.status_code == 200:
                tester.name = "Tester"
                tester.email = "test@test.com"
                tester.password = "pwd"
                session.commit()
