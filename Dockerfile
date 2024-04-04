FROM python:3.10-alpine

ENV FLASK_RUN_HOST=0.0.0.0

ENV FLASK_RUN_PORT=8080

ENV FLASK_DEBUG=0

ENV DATABASE_URI="sqlite:////tmp/sqlite.db"

EXPOSE 8080

WORKDIR /app

COPY . /app/

RUN pip install -e . --no-cache-dir

RUN server-cli init-db

CMD ["python", "scripts/runner.py"]
