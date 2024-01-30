from enum import Enum


class IngestState(str, Enum):
    FAILED = "failed"
    INGESTED = "ingested"
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
