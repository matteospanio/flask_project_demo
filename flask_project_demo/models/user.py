from typing import Mapping
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from flask_project_demo.db import Base


class User(Base):
    """Tabella "users"."""

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(32))
    email: Mapped[str] = mapped_column(String(64))

    def __repr__(self) -> str:
        return f"{self.name} - {self.email}"


def is_valid(data: Mapping) -> bool:
    """Controlla che `data` contenga sufficienti informazioni per creare un utente.

    Parameters
    ----------
    data : Mapping
        I dati della richiesta.

    Return
    ------
    bool
        True se i dati sono validi, False altrimenti

    Example
    -------
    >>> import flask_project_demo.models.user as user
    >>> req = {"name": "Mario", "email": "mario@rossi.com"}
    >>> user.is_valid(req)
    True
    """
    try:
        _ = data["name"]
        _ = data["email"]
        return True
    except KeyError:
        return False
