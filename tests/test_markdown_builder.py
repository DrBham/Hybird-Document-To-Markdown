
import pytest

from document_converter.core.markdown_builder import MarkdownBuilder


@pytest.mark.parametrize("level", [0, 7, -1])
def test_rejects_invalid_heading_levels(level):
    """Reject heading levels outside the supported range."""

    builder = MarkdownBuilder()

    with pytest.raises(
        ValueError,
        match="Heading level must be between 1 and 6"
    ):
        builder.add_heading("Invalid Heading", level)
