from fastapi import status


class DewyError(Exception):
    def __init__(self, message):
        super().__init__(message)

    def status(self):
        return status.HTTP_500_INTERNAL_SERVER_ERROR


class NoSuchCollection(DewyError):
    def __init__(self, name: str):
        super().__init__(f"No collection named '{name}'")
        self.name = name

    def status(self):
        return status.HTTP_404_NOT_FOUND


class NoSuchDocument(DewyError):
    def __init__(self, document_id: int):
        super().__init__(f"No document with ID {document_id}")
        self.document_id = document_id

    def status(self):
        return status.HTTP_404_NOT_FOUND


class NoSuchChunk(DewyError):
    def __init__(self, chunk_id: int):
        super().__init__(f"No chunk with ID {chunk_id}")
        self.chunk_id = chunk_id

    def status(self):
        return status.HTTP_404_NOT_FOUND
