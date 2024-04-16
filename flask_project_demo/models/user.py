"""Classi relative agli utenti."""

from dataclasses import dataclass
from datetime import datetime

from flask import Request
from marshmallow import Schema, fields
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from flask_project_demo.models import Base


class UserPostSchema(Schema):
    """Schema for User POST request."""

    name = fields.String(
        metadata={"description": "Username", "example": "Mario Rossi"},
        required=True,
    )
    email = fields.Email(
        metadata={
            "description": "Email",
            "example": "mario@example.com",
        },
        required=True,
    )
    password = fields.String(metadata={"description": "Password"}, required=True)


class UserPatchSchema(Schema):
    """Schema for User PATCH request."""

    name = fields.String(
        metadata={"description": "Username", "example": "Mario Rossi"},
        required=False,
    )
    email = fields.Email(
        metadata={"description": "Email", "example": "mario@example.com"},
        required=False,
    )
    password = fields.String(metadata={"description": "Password"}, required=False)


class UserSchema(Schema):
    """Schema for User."""

    id = fields.Integer(metadata={"description": "User ID", "example": 42})
    name = fields.String(metadata={"description": "Username", "example": "Mario Rossi"})
    email = fields.Email(
        metadata={"description": "Email", "example": "mario@example.com"},
    )
    created_at = fields.DateTime(
        metadata={
            "description": "Creation date",
            "example": "Wed, 03 Apr 2024 09:41:37 GMT",
        },
    )
    updated_at = fields.DateTime(
        metadata={
            "description": "Last update",
            "example": "Wed, 03 Apr 2024 09:41:37 GMT",
        },
    )
    hashed_password = fields.String(metadata={"description": "Hashed password"})


@dataclass
class _UserQuery:
    limit: int | None
    offset: int
    order: str | None
    name: str | None
    email: str | None


class UserQuerySchema(Schema):
    """Schema per validare la query string di filtraggio lista utenti."""

    name = fields.String(metadata={"description": "Username", "example": "Mario Rossi"})
    email = fields.Email(
        metadata={"description": "Email", "example": "mario@example.com"},
    )
    limit = fields.Integer(
        validate=lambda x: x >= 0,
        metadata={"description": "Limit", "example": 5},
    )
    order = fields.String(
        validate=lambda x: x in set({"asc", "desc"}),
        metadata={"description": "Order", "example": "asc"},
    )
    offset = fields.Integer(
        validate=lambda x: x >= 0,
        metadata={"description": "Offset", "example": 100},
    )

    @classmethod
    def validate_request(cls, request: Request) -> _UserQuery:
        """Validate the query string.

        Parameters
        ----------
        request : Request
            The URL request

        Returns
        -------
        _UserQuery
            The parsed query string.

        Raises
        ------
        ValidationError
            if the query string is invalid.
        """
        data: dict = cls().load(request.args)  # type: ignore
        return _UserQuery(
            limit=data.get("limit"),
            email=data.get("email"),
            name=data.get("name"),
            offset=data.get("offset") or 0,
            order=data.get("order"),
        )


class User(Base):
    """Tabella "user"."""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(64), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(256))
    created_at: Mapped[datetime] = mapped_column(DateTime, default_factory=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default_factory=datetime.now,
        onupdate=datetime.now(),
    )

    @property
    def password(self) -> str:
        """Il campo password non è readable, usare solo il setter."""
        msg = "Password is not a readable attribute."
        raise AttributeError(msg)

    @password.setter
    def password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Verifica che la password corrisponda all'hash memorizzato."""
        return check_password_hash(self.hashed_password, password)

    def __repr__(self) -> str:
        """Produce una rappresentazione testuale di un utente."""
        return f"{self.name} - {self.email}"
