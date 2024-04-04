"""Modulo di configurazione dell'applicazione.

Questo modulo contiene le configurazioni delle varie modalità in cui può
essere eseguita l'applicazione.
"""

import os
import secrets


class Config:
    """Configurazione di base."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_urlsafe(32)
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or secrets.token_urlsafe(32)


class TestConfig(Config):
    """Configurazione per il testing."""

    DEBUG = True
    TESTING = True
    DATABASE_URI = os.environ.get("TEST_DATABASE_URI") or "sqlite:////tmp/test.db"


class ProdConfig(Config):
    """Configurazione per la produzione."""

    DEBUG = False
    DATABASE_URI = os.environ.get("PROD_DATABASE_URI") or "sqlite:///data.db"


config = {
    "test": TestConfig,
    "development": ProdConfig,
    "production": ProdConfig,
    "default": TestConfig,
}
