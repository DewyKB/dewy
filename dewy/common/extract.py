from dataclasses import dataclass

from fastapi import HTTPException, status
from loguru import logger


@dataclass
class ExtractResult:
    text: str
    """The extracted text."""

    def is_empty(self) -> bool:
        if self.text:
            return False
        else:
            return True


def extract_from_pdf(
    local_path: str, *, extract_tables: bool = False, extract_images: bool = False
) -> ExtractResult:
    """Extract documents from a PDF."""

    logger.debug("Extracting from PDF '{}'", local_path)

    texts = []
    tables = []
    import fitz

    doc = fitz.open(local_path)
    for page in doc.pages():
        texts.append(page.get_text(sort=True))

        # TODO: Make the table analysis work using PyMuPDF or look at using
        # Table Transformer
        # (https://docs.llamaindex.ai/en/stable/examples/multi_modal/multi_modal_pdf_tables.html)
        if extract_tables:
            for table in page.find_tables():
                # TODO: join tables spanning multiple pages?
                # https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/table-analysis/join_tables.ipynb
                df = table.to_pandas()
                table = df.to_csv(index=False)
                tables.extend(table)

        # TODO: Make image extraction work.
        if extract_images:
            for image in page.get_image_info(hashes=True, xrefs=True):
                print(f"Image: {image}")

    # TODO: Create image nodes for the tables and text.
    # TODO: Test that the document store is populated.
    # TODO: Test that the URL is included in the metadata.

    text = "".join(texts)
    return ExtractResult(text=text)


async def extract(
    url: str, *, extract_tables: bool = False, extract_images: bool = False
) -> ExtractResult:
    """Extract documents from a local or remote URL."""
    import httpx

    async with httpx.AsyncClient(follow_redirects=True) as client:
        # Determine the extension by requesting the headers.
        response = await client.head(url)
        response.raise_for_status()
        content_type = response.headers["content-type"]
        logger.debug("Content type of {} is {}", url, content_type)

        # Load the content.
        if content_type.startswith("application/pdf"):
            from tempfile import NamedTemporaryFile

            with NamedTemporaryFile(suffix=".pdf") as temp_file:
                logger.debug("Downloading {} to {}", url, temp_file.name)
                response = await client.get(url)
                response.raise_for_status()
                temp_file.write(response.content)

                return extract_from_pdf(
                    temp_file.name,
                    extract_tables=extract_tables,
                    extract_images=extract_images,
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"Cannot add document from content-type '{content_type}'",
            )
