
import pytest

from document_converter.converters.txt_converter import BlockClassifier


@pytest.mark.parametrize(
    "block, expected",
    [
        ("def hello():\n    print(123)", True),
        ("class Student:\n    pass", True),
        ("This is a paragraph.\nAnother sentence.", False),
        ("Shopping List\n    Milk\n    Bread", False),
    ],
)
def test_code_block_classification(block: str, expected: bool) -> None:
    """Verify conservative Python code detection."""

    result = BlockClassifier.is_code_block(block)

    assert result is expected
