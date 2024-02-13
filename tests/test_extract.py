from dewy.common.extract import extract_content
from tests.conftest import NEARLY_EMPTY_PATH, NEARLY_EMPTY_TEXT


async def test_extract_content():
    content = None
    with open(NEARLY_EMPTY_PATH, "rb") as input_file:
        content = input_file.read()

    result = await extract_content(content)
    print(result)
    assert result.text == NEARLY_EMPTY_TEXT
