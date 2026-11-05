
from abc import ABC, abstractmethod
from pathlib import Path

from .models import ConversionResult

class BaseConverter(ABC):
    """Define the common interface for document converters."""

    @abstractmethod
    def convert(self, file_path: Path) -> ConversionResult:
        """Convert a source document into Markdown text."""
        pass
