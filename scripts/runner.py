#!/usr/bin/env python3

import os
from flask_project_demo import create_app
from dotenv import load_dotenv

# leggo le variabili d'ambiente definite nel file .env
# se non le trovo uso i valori di default
load_dotenv()
HOST = os.getenv("FLASK_RUN_HOST") or "127.0.0.1"
PORT = int(os.getenv("FLASK_RUN_PORT") or 5000)
DEBUG = True if os.getenv("FLASK_DEBUG") == "1" else False

app = create_app()

if __name__ == "__main__":
    app.run(host=HOST, debug=DEBUG, port=PORT)
