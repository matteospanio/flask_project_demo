import pytest


class TestLogin:
    URL = "/api/v1/auth/login"

    @pytest.mark.parametrize(
        "payload, expected",
        [
            ({"email": "test@test.com", "password": "pwd"}, 200),
            ({"email": "test@test.com", "password": "password"}, 401),
            ({"email": "tst@test.com", "password": "pwd"}, 401),
            ({}, 400),
        ],
    )
    def test_login(self, client, payload, expected):
        response = client.post(
            self.URL,
            json=payload,
        )

        assert response.status_code == expected
