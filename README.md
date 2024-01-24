# Knowledge Base Service

## Execute using Docker Compose

```
docker compose up -d --build
```

Swagger docs at `http://localhost:8000/docs`.
Notebook `example_notebook.ipynb` uses the REST API directly.

## Practices

Some skeleton code based on best practices from https://github.com/zhanymkanov/fastapi-best-practices.

The following commands run tests and apply linting.
If you're in a `poetry shell`, you can omit the `poetry run`:

* Running tests: `poetry run pytest`
* Linting (and formatting): `poetry run ruff check --fix`
* Formatting: `poetry run ruff format`
* Type Checking: `poetry run mypy app`
