import mimetypes
import tempfile
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

from fastapi import HTTPException, status
from loguru import logger

mimetypes.add_type("text/markdown", ".md")
mimetypes.add_type("text/markdown", ".markdown")


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
    content: bytes, *, extract_tables: bool = False, extract_images: bool = False
) -> ExtractResult:
    """Extract documents from a PDF."""

    logger.debug("Extracting from PDF")

    texts = []
    tables = []
    import fitz

    doc = fitz.open(stream=content, filetype="pdf")
    logger.info("Extracting content from {} pages", doc.page_count)
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


async def extract_from_markdown(
    content: bytes, *, extract_tables: bool = False, extract_images: bool = False
) -> ExtractResult:
    """Extract documents from markdoown."""

    logger.debug("Extracting from markdown")

    # UnstructuredMarkdownLoader expects content in a file, so put it in a named
    # temporary file. This could be improved if we used unstructured more directly.
    documents = []
    with tempfile.NamedTemporaryFile(suffix=".md") as tf:
        tf.write(content)
        tf.flush()

        from langchain_community.document_loaders import UnstructuredMarkdownLoader

        loader = UnstructuredMarkdownLoader(tf.name)

        # At the time of writing, `alazy_load` is unsupported.
        documents = loader.load()

    assert len(documents) == 1, f"Expected one document, got {len(documents)}"

    return ExtractResult(text=documents[0].page_content)


async def extract_from_html(
    content: bytes,
    *,
    extract_tables: bool = False,
    extract_images: bool = False,
) -> ExtractResult:
    logger.debug("Extracting from HTML")

    # BSHTMLLoader expects content in a file, so put it in a named temporary
    # file. This could be improved if we loaded using beautiful soup directly.
    documents = []
    with tempfile.NamedTemporaryFile(suffix=".html") as tf:
        tf.write(content)
        tf.flush()

        from langchain_community.document_loaders import BSHTMLLoader

        loader = BSHTMLLoader(tf.name)

        # At the time of writing, `alazy_load` is unsupported.
        documents = loader.load()

    assert len(documents) == 1, f"Expected one document, got {len(documents)}"

    return ExtractResult(text=documents[0].page_content)


async def extract_from_docx(
    content: bytes,
    *,
    extract_tables: bool = False,
    extract_images: bool = False,
) -> ExtractResult:
    logger.debug("Extracting from docx")

    # UnstructuredWordDocumentLoader expects content in a file, so put it in a named temporary
    # file. This could be improved if we loaded using beautiful soup directly.
    documents = []
    with tempfile.NamedTemporaryFile(suffix=".docx") as tf:
        tf.write(content)
        tf.flush()

        from langchain_community.document_loaders import UnstructuredWordDocumentLoader

        loader = UnstructuredWordDocumentLoader(tf.name)

        # At the time of writing, `alazy_load` is unsupported.
        documents = loader.load()

    assert len(documents) == 1, f"Expected one document, got {len(documents)}"

    return ExtractResult(text=documents[0].page_content)


async def extract_from_doc(
    content: bytes,
    *,
    extract_tables: bool = False,
    extract_images: bool = False,
) -> ExtractResult:
    logger.debug("Extracting from doc")

    # UnstructuredWordDocumentLoader expects content in a file, so put it in a named temporary
    # file. This could be improved if we loaded using beautiful soup directly.
    documents = []
    with tempfile.NamedTemporaryFile(suffix=".doc") as tf:
        tf.write(content)
        tf.flush()

        from langchain_community.document_loaders import UnstructuredWordDocumentLoader

        loader = UnstructuredWordDocumentLoader(tf.name)

        # At the time of writing, `alazy_load` is unsupported.
        documents = loader.load()

    assert len(documents) == 1, f"Expected one document, got {len(documents)}"

    return ExtractResult(text=documents[0].page_content)


async def extract_content(
    content: bytes,
    filename: str,
    mimetype: Optional[str] = None,
    *,
    extract_tables: bool = False,
    extract_images: bool = False,
) -> ExtractResult:
    logger.info("Extracting content from {} bytes", len(content))

    if mimetype is None:
        (mimetype, encoding) = mimetypes.guess_type(filename)
        logger.debug("Inferred mime type '{}' from path '{}'", mimetype, filename)
        if encoding is not None:
            raise ValueError(f"Unsupported encoding: '{encoding}'")
    else:
        mimetype = mimetype.split(";", 2)[0]

    match mimetype:
        case "application/pdf":
            return extract_from_pdf(
                content, extract_tables=extract_tables, extract_images=extract_images
            )
        case "text/markdown":
            return await extract_from_markdown(
                content, extract_tables=extract_tables, extract_images=extract_images
            )
        case "text/html":
            return await extract_from_html(
                content, extract_tables=extract_tables, extract_images=extract_images
            )
        case "application/msword":
            return await extract_from_doc(
                content, extract_tables=extract_tables, extract_images=extract_images
            )
        case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return await extract_from_docx(
                content, extract_tables=extract_tables, extract_images=extract_images
            )
        case unrecognized:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=(
                    "Cannot add document from unrecognized mimetype "
                    f"'{unrecognized}' and file name '{filename}'"
                ),
            )


async def extract_url(
    url: str,
    *,
    extract_tables: bool = False,
    extract_images: bool = False,
) -> ExtractResult:
    """Extract documents from a local or remote URL."""
    import httpx

    async with httpx.AsyncClient(follow_redirects=True) as client:
        parsed = urlparse(url)
        if parsed.scheme != "http" and parsed.scheme != "https":
            raise ValueError(f"Unsupported scheme: '{parsed.scheme}'")

        # Determine the extension by requesting the headers.

        logger.debug("Downloading {}", url)
        response = await client.get(url)
        response.raise_for_status()
        content_type = response.headers["content-type"]
        logger.debug("Content type of {} is '{}'", url, content_type)

        return await extract_content(
            response.content,
            filename=parsed.path,
            mimetype=content_type,
            extract_tables=extract_tables,
            extract_images=extract_images,
        )
