"""Funzionalità legate alla creazione e gestione del database."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase

# leggo l'url del database dalle variabili d'ambiente
# se non è definito utilizza una stringa di default
DB_URI = os.getenv("DATABASE_URI") or "sqlite:////tmp/test.db"
engine = create_engine(DB_URI)


class Base(MappedAsDataclass, DeclarativeBase):
    """Classe base per le tabelle del db.

    Note
    ----
    Eredita dalla classe MappedAsDataclass per poter usare la
    funzione jsonify di Flask.

    See also
    --------
    serialize | deserialize
    """

    pass


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
    import flask_project_demo.models

    Base.metadata.create_all(bind=engine)
