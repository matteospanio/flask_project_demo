"""Questo modulo contiene la blueprint API.

La blueprint API "registra" tutte le sub-blueprint, infatti, alla fine,
tutti gli endpoint api saranno raggiungibili tramite il percorso
/api/v1/specific-path.
"""

from flask import Blueprint

from flask_project_demo.api.auth import auth
from flask_project_demo.api.users import users

api = Blueprint("api", __name__)
api.register_blueprint(auth, url_prefix="/auth")
api.register_blueprint(users, url_prefix="/users")
