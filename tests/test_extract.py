import os

from filetype.types.document import Docx

from dewy.common.extract import extract_content, extract_url
from tests.conftest import NEARLY_EMPTY_PATH, NEARLY_EMPTY_TEXT, TEST_DATA_DIR

NEARLY_EMPTY_MD_PATH = os.path.join(TEST_DATA_DIR, "nearly_empty.md")
NEARLY_EMPTY_MD_TEXT = "This is an empty file\n\nFor testing purposes."

NEARLY_EMPTY_HTML_PATH = os.path.join(TEST_DATA_DIR, "nearly_empty.html")
NEARLY_EMPTY_HTML_TEXT = "\n\nThis is an empty file\nFor testing purposes.\n\n"

NEARLY_EMPTY_DOCX_PATH = os.path.join(TEST_DATA_DIR, "nearly_empty.docx")


async def test_extract_content_pdf():
    content = None
    with open(NEARLY_EMPTY_PATH, "rb") as input_file:
        content = input_file.read()

    result = await extract_content(content, NEARLY_EMPTY_PATH, mimetype="application/pdf")
    assert result.text == NEARLY_EMPTY_TEXT


async def test_extract_content_markdown_mimetype():
    content = None
    with open(NEARLY_EMPTY_MD_PATH, "rb") as input_file:
        content = input_file.read()

    result = await extract_content(content, NEARLY_EMPTY_MD_PATH, mimetype="text/markdown")
    assert result.text == NEARLY_EMPTY_MD_TEXT


async def test_extract_content_markdown_extension():
    content = None
    with open(NEARLY_EMPTY_MD_PATH, "rb") as input_file:
        content = input_file.read()

    result = await extract_content(content, NEARLY_EMPTY_MD_PATH)
    assert result.text == NEARLY_EMPTY_MD_TEXT


async def test_extract_content_html_mimetype():
    content = None
    with open(NEARLY_EMPTY_HTML_PATH, "rb") as input_file:
        content = input_file.read()

    result = await extract_content(content, "/root", mimetype="text/html")
    assert result.text == NEARLY_EMPTY_HTML_TEXT


async def test_extract_content_html_url():
    result = await extract_url(
        "https://python.langchain.com/docs/expression_language/cookbook/retrieval"
    )
    assert "retrieval-augmented generation" in result.text


async def test_extract_content_html_extension():
    content = None
    with open(NEARLY_EMPTY_HTML_PATH, "rb") as input_file:
        content = input_file.read()

    result = await extract_content(content, NEARLY_EMPTY_HTML_PATH)
    assert result.text == NEARLY_EMPTY_HTML_TEXT


async def test_extract_content_docx_mimetype():
    content = None
    with open(NEARLY_EMPTY_DOCX_PATH, "rb") as input_file:
        content = input_file.read()

    result = await extract_content(content, "/root", mimetype=Docx.MIME)
    # Docx extraction seems to omit the trailing "\n"
    assert result.text + "\n" == NEARLY_EMPTY_TEXT


async def test_extract_content_docx_extension():
    content = None
    with open(NEARLY_EMPTY_DOCX_PATH, "rb") as input_file:
        content = input_file.read()

    result = await extract_content(content, NEARLY_EMPTY_DOCX_PATH)
    # Docx extraction seems to omit the trailing "\n"
    assert result.text + "\n" == NEARLY_EMPTY_TEXT
