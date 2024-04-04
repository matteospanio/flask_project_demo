#!/usr/bin/env python3

from flask_project_demo import create_app
from dotenv import load_dotenv

# leggo le variabili d'ambiente definite nel file .env
load_dotenv()

app = create_app()

if __name__ == "__main__":
    app.run()
