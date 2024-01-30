import asyncio

import pytest
from asgi_lifespan import LifespanManager
from dewy_client import Client
from httpx import AsyncClient

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
async def app(pg, event_loop):
    # Set environment variables before the application is loaded.
    import os

    (pg_host, pg_port) = pg
    os.environ["DB"] = f"postgresql://dewydbuser:dewydbpwd@{pg_host}:{pg_port}/dewydb"
    os.environ["APPLY_MIGRATIONS"] = "true"

    from dewy.main import app

    async with LifespanManager(app) as manager:
        yield manager.app


@pytest.fixture(scope="session")
async def client(app) -> Client:
    async with AsyncClient(app=app, base_url="http://test") as httpx_client:
        client = Client(base_url="http://test")
        client.set_async_httpx_client(httpx_client)
        yield client


# This approach to using a session scoped event loop doesn't seem to work
# with setting up a single, session scoped FastAPI service. Specifically,
# the service seems to capture the event loop before the event loop is
# created, and then causes problems about things being in different loops.
#
# See https://github.com/pytest-dev/pytest-asyncio/issues/705, and
# https://github.com/pytest-dev/pytest-asyncio/issues/718.
#
# def pytest_collection_modifyitems(items):
#     pytest_asyncio_tests = (item for item in items if is_async_test(item))
#     session_scope_marker = pytest.mark.asyncio(scope="session")
#     for async_test in pytest_asyncio_tests:
#         async_test.add_marker(session_scope_marker)


# sets up a single, session-scoped async event loop.
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
