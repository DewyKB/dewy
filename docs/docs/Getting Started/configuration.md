---
title: Configuration
sidebar_position: 2
--- 

# Configuration

Dewy will read env vars from an `.env` file if provided. You can also set these directly in the environment, for example when configuring an instance running in docker / kubernetes.

```sh
# ~/.env
ENVIRONMENT=LOCAL
DB=postgresql://...
OPENAI_API_KEY=...
```

The following config keys are available (see [config.py](https://github.com/DewyKB/dewy/blob/main/dewy/config.py) for additional details)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `SERVE_ADMIN_UI` | bool | `True` | If true, serve the admin UI.
| `DB` | PostgresDsn | `None | The Postgres database to connect to. |
| `APPLY_MIGRATIONS` | bool | `True` | Whether migrations should be applied to the database. |
| `ENVIRONMENT` | [Environment](https://github.com/DewyKB/dewy/blob/main/dewy/constants.py) | `PRODUCTION` | The environment the application is running in. |
| `OPENAI_API_KEY` | str | `None` | The OpenAI API Key to use for OpenAI models (if using OpenAI models). |
| `LLAMA_INDEX_CACHE_DIR` | str | `None` | The path for caching artifacts used by LlamaIndex. |
| `HF_HOME` | str | `None` | The path for caching  artifacts used by HuggingFace. |