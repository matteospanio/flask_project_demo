"""App Factory.

In questo modulo viene definita la funzione per creare il server
e si aggiungono blueprint. Qualora fosse necessario è anche il posto
in cui si inizializzano i plugin di Flask.
"""

from flask import Flask

from flask_project_demo.api import api
from flask_project_demo.api.auth import refresh_expiring_token
from flask_project_demo.config import config
from flask_project_demo.plugins import jwt_manager


def create_app(config_name: str = "default"):
    """Crea il server Flask.

    Questa funzione server per creare un'instanza del server Flask,
    può tornare utile in fase di testing, inoltre permette di organizzare
    meglio il codice.

    See Also
    --------
    https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    jwt_manager.init_app(app)
    app.after_request(refresh_expiring_token)

    # aggiungo le blueprint
    app.register_blueprint(api, url_prefix="/api/v1")

    return app
