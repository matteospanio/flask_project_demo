from sqlalchemy import inspect
from flask_project_demo.db import create_database, delete_database, Session, engine


def test_create_database():
    create_database()
    # list all tables in the database

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert len(tables) == 1
    assert "users" in tables


def test_delete_database():
    create_database()
    delete_database()

    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert len(tables) == 0
