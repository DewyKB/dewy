# Knowledge Base Service

## Execute using Docker Compose

```
docker compose up -d --build
```

Swagger docs at `http://localhost:8000/docs`.
Notebook `example_notebook.ipynb` uses the REST API directly.

## Practices

Some skeleton code based on best practices from https://github.com/zhanymkanov/fastapi-best-practices.

In `poetry shell` or using `poetry run ${command}`:

* Linting (and formatting): `ruff check --fix`
* Formatting: `ruff format`
* Type Checking: `mypy app`
