import os
import secrets


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_urlsafe(32)
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or secrets.token_urlsafe(32)
    SESSION_TYPE = "filesystem"


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE_URI = os.environ.get("TEST_DATABASE_URI") or "sqlite:////tmp/test.db"


class ProdConfig(Config):
    DEBUG = False
    DATABASE_URI = os.environ.get("PROD_DATABASE_URI") or "sqlite:///data.db"


config = {
    "test": TestConfig,
    "development": ProdConfig,
    "production": ProdConfig,
    "default": TestConfig,
}
