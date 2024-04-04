from flask.cli import FlaskGroup
import click
import faker

from flask_project_demo import create_app
from flask_project_demo.db import create_database, Session
from flask_project_demo.models import User
from werkzeug.security import generate_password_hash


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """CLI per gestire il server."""
    pass


@cli.command("init-db")
def init_db_command():
    """Crea il database con le tabelle"""
    create_database()
    click.echo("Initialized the database.")


@cli.command("add-data")
@click.option(
    "-n",
    "--num",
    type=int,
    help="Il numero di utenti da creare.",
)
def add_data_command(num: int):
    """Riempie il database con dati fittizzi"""
    f = faker.Faker()
    with Session() as session:
        with click.progressbar(range(num)) as prog:
            for _ in prog:
                user = User(
                    name=f.name(),
                    email=f.email(),
                    hashed_password=generate_password_hash(f.password()),
                )
                session.add(user)
        session.commit()
