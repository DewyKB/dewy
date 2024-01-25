import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pytest_asyncio import is_async_test

pytest_plugins = ["pytest_docker_fixtures"]

from pytest_docker_fixtures.images import configure as configure_image  # noqa: E402

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
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


def pytest_collection_modifyitems(items):
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker)
