
from pathlib import Path


SUPPORTED_FORMATS = {".txt", ".docx", ".pdf"}


def validate_file(file_path: Path) -> None:
    """Validate the source file before conversion."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not file_path.is_file():
        raise ValueError(
            f"Path is not a file: {file_path}"
        )

    if file_path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported file format: {file_path.suffix}"
        )
