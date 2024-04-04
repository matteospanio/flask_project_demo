"""Modulo per estendere le funzionalità a riga di comando del server.

Praticamente ogni funzione aggiunge un comando CLI.
"""

import click
from flask.cli import FlaskGroup

from flask_project_demo import create_app
from flask_project_demo.db import create_database


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """CLI per gestire il server."""


@cli.command("init-db")
def init_db_command():
    """Crea il database con le tabelle."""
    create_database()
    click.echo("Initialized the database.")
