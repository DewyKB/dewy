import asyncio

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pytest_docker_fixtures.images import configure as configure_image

pytest_plugins = ["pytest_docker_fixtures"]

configure_image(
    "postgresql",
    image="ankane/pgvector",
    version="latest",
    env={
        "POSTGRES_DB": "dewydb",
        "POSTGRES_USER": "dewydbuser",
        "POSTGRES_PASSWORD": "dewdbpwd",
        "POSTGRES_HOST_AUTH_METHOD": "trust",
    },
)


@pytest.fixture(scope="session")
async def app(pg):
    # Set environment variables before the application is loaded.
    import os

    (pg_host, pg_port) = pg
    os.environ["DB"] = f"postgresql://dewydbuser:dewydbpwd@{pg_host}:{pg_port}/dewydb"

    from dewy.main import app

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest.fixture(scope="session")
async def client(app) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test"):
        yield client


# sets up a single, session-scoped async event loop.
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
