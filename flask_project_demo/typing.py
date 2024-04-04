from dataclasses import dataclass
from typing import Mapping
from flask import Request
from marshmallow import Schema, fields


class QueryError(Exception):
    def __init__(self, message):
        self.message = message


class LoginError(Exception):
    def __init__(self, message):
        self.message = message


@dataclass
class _UserQuery:
    limit: int | None
    offset: int
    order: str | None
    name: str | None
    email: str | None


class UserQuerySchema(Schema):
    name = fields.String(metadata={"description": "Username", "example": "Mario Rossi"})
    email = fields.String(
        metadata={"description": "Email", "example": "mario@example.com"}
    )
    limit = fields.Integer(
        validate=lambda x: x >= 0,
        metadata={"description": "Limit", "example": 5},
    )
    order = fields.String(
        validate=lambda x: x in ["asc", "desc"],
        metadata={"description": "Order", "example": "asc"},
    )
    offset = fields.Integer(
        validate=lambda x: x >= 0,
        metadata={"description": "Offset", "example": 100},
    )

    @classmethod
    def validate_request(cls, request: Request) -> _UserQuery:
        data: dict = cls().load(request.args)  # type: ignore
        return _UserQuery(
            limit=data.get("limit"),
            email=data.get("email"),
            name=data.get("name"),
            offset=data.get("offset") or 0,
            order=data.get("order"),
        )


class UserAuthSchema(Schema):
    name = fields.String(required=False)
    email = fields.String(required=True)
    password = fields.String(required=True)

    @classmethod
    def validate_request(cls, request: Request) -> tuple[str | None, str, str]:
        data: dict = cls().load(request.get_json())  # type: ignore
        return data.get("name"), data["email"], data["password"]


class LoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)

    @classmethod
    def validate_request(cls, request: Mapping) -> tuple[str, str]:
        data: dict = cls().load(request)  # type: ignore
        return data["email"], data["password"]
