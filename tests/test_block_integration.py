
"""Integration tests for TXT block analysis."""


from document_converter.converters.txt_converter import (
    BlockSplitter,
    BlockClassifier,
)

def test_splitter_and_classifier_integration() -> None:
    """Verify block splitting and basic code classification."""

    source = (
        "This is a normal paragraph.\n"
        "It contains another sentence.\n"
        "\n"
        "def hello():\n"
        "    print('Hello World')"
    )

    blocks = BlockSplitter.split(source)

    assert len(blocks) == 2

    assert BlockClassifier.is_code_block(blocks[0]) is False
    assert BlockClassifier.is_code_block(blocks[1]) is True

    assert "    print('Hello World')" in blocks[1]
