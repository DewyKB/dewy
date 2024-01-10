from typing import List

from fastapi import HTTPException, status
from llama_index import Document
from loguru import logger

from .pdf import load_pdf
from .source import ExtractSource


async def extract(source: ExtractSource) -> List[Document]:
    """Extract documents from a local or remote URL."""
    import httpx

    async with httpx.AsyncClient() as client:
        # Determine the extension by requesting the headers.
        response = await client.head(source.url)
        response.raise_for_status()
        content_type = response.headers["content-type"]
        logger.debug("Content type of {} is {}", source.url, content_type)

        # Load the content.
        if content_type == "application/pdf":
            from tempfile import NamedTemporaryFile

            with NamedTemporaryFile(suffix=".pdf") as temp_file:
                logger.debug("Downloading {} to {}", source.url, temp_file.name)
                response = await client.get(source.url)
                response.raise_for_status()
                temp_file.write(response.content)

                return load_pdf(temp_file.name, source)
        else:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Cannot add document from content-type '{content_type}'",
            )
