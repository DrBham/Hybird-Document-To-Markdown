"""MarkItDown-backed converter for local documents."""

from pathlib import Path
from typing import Protocol

from markitdown import MarkItDown

from ..core.base_converter import BaseConverter
from ..core.models import ConversionResult
from ..core.validator import validate_file


class MarkItDownResult(Protocol):
    """Describe the MarkItDown result consumed by the adapter."""

    markdown: str


class MarkItDownEngine(Protocol):
    """Describe the MarkItDown method used by the adapter."""

    def convert_local(self, path: Path) -> MarkItDownResult:
        """Convert a local file and return a MarkItDown result."""
        ...


class MarkItDownConverter(BaseConverter):
    """Convert supported local documents through Microsoft MarkItDown."""

    def __init__(self, engine: MarkItDownEngine | None = None):
        self._engine = engine if engine is not None else MarkItDown()

    def convert(self, file_path: Path) -> ConversionResult:
        """Validate and convert a local document into Markdown."""

        validate_file(file_path)
        result = self._engine.convert_local(file_path)

        return ConversionResult(
            source_path=file_path,
            source_format=file_path.suffix.lower().lstrip("."),
            markdown=result.markdown,
        )
