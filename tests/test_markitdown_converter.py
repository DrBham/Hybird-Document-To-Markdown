from pathlib import Path
from types import SimpleNamespace

import pytest

from document_converter.converters.markitdown_converter import (
    MarkItDownConverter,
)


class FakeMarkItDown:
    def __init__(self, markdown: str = "# Converted"):
        self.markdown = markdown
        self.converted_path: Path | None = None

    def convert_local(self, path: Path):
        self.converted_path = path
        return SimpleNamespace(markdown=self.markdown)


@pytest.mark.parametrize("extension", [".txt", ".docx", ".pdf"])
def test_converter_returns_application_result(tmp_path, extension):
    source = tmp_path / f"sample{extension}"
    source.write_bytes(b"test document")
    engine = FakeMarkItDown()

    result = MarkItDownConverter(engine=engine).convert(source)

    assert engine.converted_path == source
    assert result.source_path == source
    assert result.source_format == extension.lstrip(".")
    assert result.markdown == "# Converted"


def test_converter_rejects_missing_file(tmp_path):
    converter = MarkItDownConverter(engine=FakeMarkItDown())

    with pytest.raises(FileNotFoundError):
        converter.convert(tmp_path / "missing.txt")
