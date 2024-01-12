"""Extraction of text, tables, and images from PDFs."""

from typing import List

from llama_index import Document
from loguru import logger

from .source import ExtractSource


def load_pdf(local_path: str, source: ExtractSource) -> List[Document]:
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
        if source.extract_tables:
            for table in page.find_tables():
                # TODO: join tables spanning multiple pages?
                # https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/table-analysis/join_tables.ipynb
                df = table.to_pandas()
                table = df.to_csv(index=False)
                tables.extend(table)

        # TODO: Make image extraction work.
        if source.extract_images:
            for image in page.get_image_info(hashes=True, xrefs=True):
                print(f"Image: {image}")

    # TODO: Configure sentence splitting for the text.
    # TODO: Create image nodes for the tables and text.
    # TODO: Test that the document store is populated.
    # TODO: Test that the URL is included in the metadata.

    text = "".join(texts)
    document = Document(text=text, extra_info=source.extra_info)
    return [document]
