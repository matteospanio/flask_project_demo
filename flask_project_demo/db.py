"""Funzionalità legate alla creazione e gestione del database."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from flask_project_demo import models

# leggo l'url del database dalle variabili d'ambiente
# se non è definito utilizza una stringa di default
DB_URI = os.getenv("DATABASE_URI") or "sqlite:////tmp/test.db"
engine = create_engine(DB_URI)

Session = scoped_session(sessionmaker(bind=engine))


def create_database(conf: str | None = None) -> None:
    """Crea il database e le tabelle.

    Al primo avvio del server, solitamente, si vuole creare il database
    dove archiviare le informazioni gestite dal server, questa funzione
    serve proprio a questo.

    Parameters
    ----------
    conf : str | None
        La configurazione del server, spesso è una stringa tipo "TEST"
        o "PRODUCTION" e può essere utile per decidere cosa fare in
        base alla situazione.
    """
    # importo tutte le classi collegate alle tabelle

    models.Base.metadata.create_all(bind=engine)


def delete_database(conf: str | None = None) -> None:
    """Svuota il database e rimuove le tabelle al suo interno."""
    models.Base.metadata.drop_all(bind=engine)
