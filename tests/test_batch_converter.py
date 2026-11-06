from pathlib import Path

import pytest

from document_converter.core.base_converter import BaseConverter
from document_converter.core.models import ConversionResult
from document_converter.core.router import ConverterRouter
from document_converter.services.batch_converter import BatchConverter


class SelectiveConverter(BaseConverter):
    """Return Markdown unless the filename is configured to fail."""

    def __init__(self, failing_name: str | None = None):
        self.failing_name = failing_name
        self.converted_paths: list[Path] = []

    def convert(self, file_path: Path) -> ConversionResult:
        self.converted_paths.append(file_path)

        if file_path.name == self.failing_name:
            raise RuntimeError("simulated conversion failure")

        return ConversionResult(
            source_path=file_path,
            source_format=file_path.suffix.lower().lstrip("."),
            markdown=f"# {file_path.stem}",
        )


def create_files(tmp_path: Path, *names: str) -> list[Path]:
    paths: list[Path] = []

    for name in names:
        path = tmp_path / name
        path.write_text("content", encoding="utf-8")
        paths.append(path)

    return paths


def test_batch_converts_same_extension_case_insensitively(tmp_path):
    paths = create_files(tmp_path, "one.PDF", "two.pdf")
    converter = SelectiveConverter()
    service = BatchConverter(ConverterRouter({".pdf": converter}))

    result = service.convert(paths)

    assert result.extension == ".pdf"
    assert len(result.successful) == 2
    assert not result.failed
    assert converter.converted_paths == paths


def test_batch_rejects_mixed_extensions_before_conversion(tmp_path):
    paths = create_files(tmp_path, "one.pdf", "two.docx")
    converter = SelectiveConverter()
    service = BatchConverter(ConverterRouter({
        ".pdf": converter,
        ".docx": converter,
    }))

    with pytest.raises(ValueError, match="same extension"):
        service.convert(paths)

    assert converter.converted_paths == []


def test_batch_preserves_successes_when_one_file_fails(tmp_path):
    paths = create_files(tmp_path, "one.pdf", "broken.pdf", "three.pdf")
    converter = SelectiveConverter(failing_name="broken.pdf")
    service = BatchConverter(ConverterRouter({".pdf": converter}))

    result = service.convert(paths)

    assert len(result.successful) == 2
    assert len(result.failed) == 1
    assert result.failed[0].source_path.name == "broken.pdf"
    assert result.failed[0].error is not None
    assert "RuntimeError" in result.failed[0].error


def test_batch_rejects_empty_input():
    with pytest.raises(ValueError, match="at least one file"):
        BatchConverter().convert([])
