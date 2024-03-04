import asyncio
import os

import pytest
from asgi_lifespan import LifespanManager
from dewy_client import Client
from dewy_client.api.kb import (
    get_document_status,
    upload_document_content,
)
from dewy_client.models import (
    BodyUploadDocumentContent,
    IngestState,
)
from dewy_client.types import File
from httpx import AsyncClient
from pytest_docker_fixtures.images import configure as configure_image  # noqa: E402

from dewy.config import ServeConfig

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

PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_DATA_DIR = os.path.join(PROJECT_ROOT_DIR, "test_data")
NEARLY_EMPTY_PATH = os.path.join(TEST_DATA_DIR, "nearly_empty.pdf")
assert os.path.isfile(NEARLY_EMPTY_PATH)
NEARLY_EMPTY_TEXT = "This is a nearly empty PDF to test extraction and embedding.\n"

NEARLY_EMPTY_BYTES = None
with open(NEARLY_EMPTY_PATH, "rb") as file:
    NEARLY_EMPTY_BYTES = file.read()

NEARLY_EMPTY_PATH2 = os.path.join(TEST_DATA_DIR, "nearly_empty2.pdf")
assert os.path.isfile(NEARLY_EMPTY_PATH2)
NEARLY_EMPTY_TEXT2 = " This is another nearly empty document. \n"

NEARLY_EMPTY_BYTES2 = None
with open(NEARLY_EMPTY_PATH2, "rb") as file:
    NEARLY_EMPTY_BYTES2 = file.read()


@pytest.fixture(scope="session")
async def app(pg, event_loop):
    (pg_host, pg_port) = pg
    config = ServeConfig(
        db=f"postgresql://dewydbuser:dewydbpwd@{pg_host}:{pg_port}/dewydb",
        apply_migrations=True,
    )

    from dewy.serve import create_app

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


async def upload_test_pdf(client, document_id, payload):
    document = await upload_document_content.asyncio(
        client=client,
        document_id=document_id,
        body=BodyUploadDocumentContent(
            content=File(
                payload=payload,
                file_name=f"file-${document_id}.pdf",
                mime_type="application/pdf",
            ),
        ),
    )
    assert document
    assert document.extracted_text is None
    assert document.url is None
    assert document.ingest_state == IngestState.PENDING
    assert document.ingest_error is None


async def document_ingested(client, document_id):
    status = await get_document_status.asyncio(document_id, client=client)
    while getattr(status, "ingest_state", IngestState.PENDING) == IngestState.PENDING:
        await asyncio.sleep(0.1)
        status = await get_document_status.asyncio(document_id, client=client)
    assert status
    assert status.id == document_id
    assert status.ingest_state == IngestState.INGESTED
    assert status.ingest_error is None
