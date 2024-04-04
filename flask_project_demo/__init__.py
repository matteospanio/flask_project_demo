"""App Factory.

In questo modulo viene definita la funzione per creare il server
e si aggiungono blueprint. Qualora fosse necessario è anche il posto
in cui si inizializzano i plugin di Flask.
"""

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_project_demo.api import api

from flask_project_demo.config import config


jwt_manager = JWTManager()


def create_app(config_name: str = "default"):
    """Crea il server Flask.

    Questa funzione server per creare un'instanza del server Flask,
    può tornare utile in fase di testing, inoltre permette di organizzare
    meglio il codice.

    See also
    --------
    https://flask.palletsprojects.com/en/3.0.x/patterns/appfactories/
    """

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    jwt_manager.init_app(app)

    # aggiungo le blueprint
    app.register_blueprint(api, url_prefix="/api/v1")

    return app
