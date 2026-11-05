from pathlib import Path

import pytest

from document_converter.core.base_converter import BaseConverter
from document_converter.core.models import ConversionResult
from document_converter.core.router import ConverterRouter


class FakeConverter(BaseConverter):
    """Simulate a converter without processing documents."""

    def convert(self, file_path: Path) -> ConversionResult:
        return ConversionResult(
            source_path=file_path,
            source_format=file_path.suffix.lower().lstrip("."),
            markdown="# Fake Markdown"
        )


def test_router_selects_txt_converter(tmp_path):
    """Verify that the router selects a registered TXT converter."""

    test_file = tmp_path / "sample.txt"
    test_file.write_text("Example document", encoding="utf-8")

    router = ConverterRouter({
        ".txt": FakeConverter()
    })

    result = router.convert(test_file)

    assert isinstance(result, ConversionResult)
    assert result.source_format == "txt"
    assert result.markdown == "# Fake Markdown"

@pytest.mark.parametrize(
    "extension, expected_markdown",
    [
        (".txt", "# TXT Converter"),
        (".docx", "# DOCX Converter"),
        (".pdf", "# PDF Converter"),
    ],
)
def test_router_selects_correct_converter(
    tmp_path, extension, expected_markdown
):
    """Verify routing for each supported document format."""

    class NamedFakeConverter(BaseConverter):
        def __init__(self, markdown: str):
            self.markdown = markdown

        def convert(self, file_path: Path) -> ConversionResult:
            return ConversionResult(
                source_path=file_path,
                source_format=file_path.suffix.lower().lstrip("."),
                markdown=self.markdown,
            )

    test_file = tmp_path / f"sample{extension}"
    test_file.write_text("Test content", encoding="utf-8")

    router = ConverterRouter({
        ".txt": NamedFakeConverter("# TXT Converter"),
        ".docx": NamedFakeConverter("# DOCX Converter"),
        ".pdf": NamedFakeConverter("# PDF Converter"),
    })

    result = router.convert(test_file)

    assert result.markdown == expected_markdown
    assert result.source_format == extension.lstrip(".")


def test_router_rejects_unregistered_converter(tmp_path):
    """Reject files without a registered converter."""

    test_file = tmp_path / "sample.pdf"
    test_file.write_text("Fake PDF content", encoding="utf-8")

    router = ConverterRouter({
        ".txt": FakeConverter()
    })

    with pytest.raises(
        ValueError,
        match=r"No converter registered for: \.pdf"
    ):
        router.convert(test_file)


def test_router_has_markitdown_defaults():
    router = ConverterRouter()

    assert set(router.converters) == {".txt", ".docx", ".pdf"}
