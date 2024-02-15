import asyncio
import os

import pytest
from asgi_lifespan import LifespanManager
from dewy_client import Client
from httpx import AsyncClient

from dewy.config import Config

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

TEST_DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_data"
)
NEARLY_EMPTY_PATH = os.path.join(TEST_DATA_DIR, "nearly_empty.pdf")
assert os.path.isfile(NEARLY_EMPTY_PATH)
NEARLY_EMPTY_TEXT = "This is a nearly empty PDF to test extraction and embedding.\n"

NEARLY_EMPTY_PATH2 = os.path.join(TEST_DATA_DIR, "nearly_empty2.pdf")
assert os.path.isfile(NEARLY_EMPTY_PATH2)
NEARLY_EMPTY_TEXT2 = " This is another nearly empty document. \n" 

NEARLY_EMPTY_BYTES = None
with open(NEARLY_EMPTY_PATH, "rb") as file:
    NEARLY_EMPTY_BYTES = file.read()


@pytest.fixture(scope="session")
async def app(pg, event_loop):
    (pg_host, pg_port) = pg
    config = Config(
        DB=f"postgresql://dewydbuser:dewydbpwd@{pg_host}:{pg_port}/dewydb",
        APPLY_MIGRATIONS=True,
    )

    from dewy.main import create_app

    app = create_app(config)

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
