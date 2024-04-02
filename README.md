# flask_project_demo
> A demo flask project for teaching purposes

## Requisiti

Per usare l'immagine con docker è necessario installare docker. Altrimenti si può installare localmente l'applicazione tramite poetry

- docker
- python 3.10 o superiore
- poetry

## Utilizzo tramite docker (consigliato)

Se si deve solamente utilizzare il server, senza svilupparlo è possibile eseguirlo tramite docker con il comando:

```bash
docker compose up
```

## Installazione

L'installazione viene gestita da poetry, si possono installare tutte le dipendenze e il server con il comando:

```bash
poetry install
```

Eseguendo questo comando poetry creerà un virtual environment in automatico con tutte le dipendenze dichiarate nel file `pyproject.toml`.

## Utilizzo
Per avviare l'applicazione si può usare lo script `runner.py` eseguendo il comando:

```bash
poetry shell
python scripts/runner.py
```

Oppure è possibile, sempre tramite la shell di poetry, eseguire il comando:

```bash
server-cli -e .env -A flask_project_demo:create_app run
```

Il file .env è il file contenente le variabili d'ambiente, cambiare il nome a seconda del proprio caso (nel caso di problemi l'opzione `-e` si può omettere). Se si vuole eseguire il server in modalità debug è necessario aggiungere la flag `--debug`.
