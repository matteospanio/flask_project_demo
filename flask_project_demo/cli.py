from flask.cli import FlaskGroup
import click
import faker
from sqlalchemy.orm import Session

from flask_project_demo import create_app
from flask_project_demo.db import create_database, engine
from flask_project_demo.models import User


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
    with Session(engine) as session:
        with click.progressbar(range(num)) as prog:
            for _ in prog:
                user = User(  # type: ignore
                    name=f.name(),
                    email=f.email(),
                )
                session.add(user)
        session.commit()
