# Knowledge Base Service

## Execute using Docker Compose

```
docker compose up -d --build
```

Swagger docs at `http://localhost:8000/docs`.
Notebook `example_notebook.ipynb` uses the REST API directly.

## Execute Locally

Local execution can be significantly more performant, as it allows local models to better utilize your system's hardware. This is especially true for Macs with M* chips.

```
# Install Python dependencies
poetry install

# Fire up the vector store
docker compose up redis

# Configure Dewy (modify as appropriate)
export ENVIRONMENT=LOCAL 
export REDIS=redis://default:testing123@localhost:6379
export OPENAI_API_KEY=<open ai api key> 

# Run Dewy
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Practices

Some skeleton code based on best practices from https://github.com/zhanymkanov/fastapi-best-practices.

In `poetry shell` or using `poetry run ${command}`:

* Linting (and formatting): `ruff check --fix`
* Formatting: `ruff format`
* Type Checking: `mypy app`
