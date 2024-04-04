from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from flask_project_demo.models import Base
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields


class UserPostSchema(Schema):
    """Schema for User POST request."""

    name = fields.String(
        metadata={"description": "Username", "example": "Mario Rossi"}, required=True
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
        metadata={"description": "Username", "example": "Mario Rossi"}, required=False
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
        metadata={"description": "Email", "example": "mario@example.com"}
    )
    created_at = fields.DateTime(
        metadata={
            "description": "Creation date",
            "example": "Wed, 03 Apr 2024 09:41:37 GMT",
        }
    )
    updated_at = fields.DateTime(
        metadata={
            "description": "Last update",
            "example": "Wed, 03 Apr 2024 09:41:37 GMT",
        }
    )
    hashed_password = fields.String(metadata={"description": "Hashed password"})


class User(Base):
    """Tabella "user"."""

    __tablename__ = "user"
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
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    def __repr__(self) -> str:
        return f"{self.name} - {self.email}"
