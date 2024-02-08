import shutil
from tempfile import SpooledTemporaryFile

import pytest

from dewy.common.extract import extract_file
from tests.conftest import NEARLY_EMPTY_PATH, NEARLY_EMPTY_TEXT


async def test_extract_in_memory():
    with SpooledTemporaryFile() as temp_file:
        with open(NEARLY_EMPTY_PATH, "rb") as input_file:
            shutil.copyfileobj(input_file, temp_file)

        # This shouldn't exceed the "in-memory" size, so it shouldn't be rolled.
        assert temp_file._rolled == False
        result = await extract_file(temp_file)
        print(result)
        assert result.text == NEARLY_EMPTY_TEXT


@pytest.mark.skip(reason="currently broken -- PyMuPDF doesn't support rolled over files")
async def test_extract_rolled_over():
    with SpooledTemporaryFile() as temp_file:
        with open(NEARLY_EMPTY_PATH, "rb") as input_file:
            shutil.copyfileobj(input_file, temp_file)

        # Forcibly roll it to a file, to make sure extraction works there too.
        temp_file.rollover()
        assert temp_file._rolled
        result = await extract_file(temp_file)
        assert result.text == NEARLY_EMPTY_TEXT
