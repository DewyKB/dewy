from __future__ import annotations

from typing import Any, Coroutine
from urllib.parse import urlparse

import asyncpg
import taskiq
from taskiq.serializers import CBORSerializer

from dewy.config import ServeConfig

from ._ingest import ingest_task


class _KeywordMiddleware(taskiq.TaskiqMiddleware):
    """Midleware to make sure all calls use keyword arguments.

    This avoids a lot of issues with changing task signatures."""

    def pre_send(
        self, message: taskiq.TaskiqMessage
    ) -> taskiq.TaskiqMessage | Coroutine[Any, Any, taskiq.TaskiqMessage]:
        assert (
            len(message.args) == 0
        ), f"All arguments should be passed by keyword, got: {message.args}"
        return super().pre_send(message)


def _create_broker(config: ServeConfig) -> taskiq.AsyncBroker:
    if config.broker is None:
        return taskiq.InMemoryBroker()
    else:
        broker_url = urlparse(config.broker)
        if broker_url.scheme == "amqp":
            from taskiq_aio_pika import AioPikaBroker

            return AioPikaBroker(url=config.broker)
        else:
            raise ValueError(
                f"Unsupported scheme '{broker_url.scheme}' in broker URL: '{config.broker}'"
            )


class DewyTasks:
    """
    The main class providing the dewy worker.
    """

    def __init__(self, pg_pool: asyncpg.Pool, config: ServeConfig) -> None:
        broker = (
            _create_broker(config)
            .with_middlewares(_KeywordMiddleware())
            # Use the CBORSerializer. Some messages (currently `IngestContent`)
            # contain `bytes` which are not JSON serialiazable. We could use a
            # different mechanism for passing the content (S3 or `bytes` in the DB)
            # which would allow us to use JSON or ORJSONSerializer. These would
            # have benefits in debugging the messages in the queue.
            .with_serializer(CBORSerializer())
        )
        self.broker = broker

        # Add dependencies that can be injected directly.
        broker.add_dependency_context(
            {
                asyncpg.Pool: pg_pool,
                # TODO: split out worker configuration?
                ServeConfig: config,
            }
        )

        self.ingest = broker.register_task(ingest_task)
