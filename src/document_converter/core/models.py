
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ConversionResult:
    """Represent the result of a document conversion."""

    source_path: Path
    source_format: str
    markdown: str
