# Knowledge Base Service

# Execute Locally

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