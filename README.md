# Knowledge Base Service

# Execute Locally

You'll need a running Redis, as well as models in the `/models/embedding` and `/models/llm` directories for this.

TODO: Improve the local execution.

```
poetry run -- uvicorn app.main:app --reload
```

Runs on `http://localhost:8000/docs`

# Execute using Docker Compose

```
docker compose up -d --build
```

Runs on `http://localhost:8000/docs`.

# Practices

Some skeleton code based on best practices from https://github.com/zhanymkanov/fastapi-best-practices.

In `poetry shell` or using `poetry run ${command}`:

* Linting (and formatting): `ruff check --fix`
* Formatting: `ruff format`
* Type Checking: `mypy app`