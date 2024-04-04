"""Script per eseguire il server."""

# !/usr/bin/env python3

from dotenv import load_dotenv
from flask_project_demo import create_app

# leggo le variabili d'ambiente definite nel file .env
load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run()
