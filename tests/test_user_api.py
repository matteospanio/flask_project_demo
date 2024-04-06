from http import HTTPStatus

import pytest
from flask_project_demo.db import Session
from flask_project_demo.models import User
from sqlalchemy import select

API_URL = "/api/v1/users/"


class TestGetUsers:
    def test_requires_authentication(self, client):
        response = client.get(API_URL)

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_standard_usage(self, auth_client):
        response = auth_client.get(API_URL)

        assert response.status_code == HTTPStatus.OK

    def test_filtered_result(self, auth_client):
        response = auth_client.get(API_URL + "?name=Tester")

        assert len(response.json) == 1
        assert response.json[0]["name"] == "Tester"
        assert response.json[0]["email"] == "test@test.com"

    @pytest.mark.parametrize(
        "query",
        [
            "limit=-3",
            "offset=-2",
            "order=invalid",
            "limit=-10&email=test",
            "name=Tester&limit=-5",
        ],
    )
    def test_invalid_query(self, auth_client, query):
        response = auth_client.get(API_URL + "?" + query)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize(
        ("filter", "expected"),
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

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_get_user(self, auth_client):
        response = auth_client.get(API_URL + "1")

        assert response.status_code == HTTPStatus.OK


class TestPostUsers:
    @pytest.mark.parametrize(
        ("payload", "expected"),
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
            (
                {
                    "name": "prova",
                    "email": "test@test.com",
                    "password": "pwd",
                },
                409,
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

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_unauthorized(self, auth_client):
        response = auth_client.patch(API_URL + "2", json={"name": "New Name"})

        assert response.status_code == HTTPStatus.UNAUTHORIZED

    @pytest.mark.parametrize(
        "payload",
        [{"email": "new_email"}, {"password": 1}, {}],
    )
    def test_bad_request_payload(self, auth_client, payload):
        with Session() as session:
            query = select(User).where(User.email == "test@test.com")
            tester = session.scalars(query).one()

        response = auth_client.patch(
            f"{API_URL}{tester.id}",
            json=payload,
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST

    def test_failing_email_update(self, auth_client):
        new_user = User(name="New User", email="ciao@ciao.com", hashed_password="pwd")
        with Session() as session:
            session.add(new_user)
            session.commit()

            query = select(User).where(User.email == "test@test.com")
            tester = session.scalars(query).one()

        response = auth_client.patch(
            f"{API_URL}{tester.id}",
            json={"email": "ciao@ciao.com"},
        )

        assert response.status_code == HTTPStatus.CONFLICT

    @pytest.mark.parametrize(
        "payload",
        [
            {"name": "New Name"},
            {"email": "new@email.com"},
            {"password": "new_password"},
        ],
    )
    def test_ok_request(self, auth_client, payload):
        with Session() as session:
            query = select(User).where(User.email == "test@test.com")
            tester = session.scalars(query).one()

            response = auth_client.patch(
                f"{API_URL}{tester.id}",
                json=payload,
            )

            assert response.status_code == HTTPStatus.OK

            tester.name = "Tester"
            tester.email = "test@test.com"
            tester.password = "pwd"
            session.commit()
