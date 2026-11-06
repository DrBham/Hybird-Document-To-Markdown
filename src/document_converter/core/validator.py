
from pathlib import Path


SUPPORTED_FORMATS = frozenset({
    ".txt",
    ".docx",
    ".pdf",
    ".pptx",
    ".xlsx",
    ".csv",
    ".html",
    ".htm",
    ".json",
    ".xml",
})

MAX_FILE_SIZE_BYTES = 100 * 1024 * 1024


def validate_file(
    file_path: Path,
    *,
    max_size_bytes: int = MAX_FILE_SIZE_BYTES,
) -> None:
    """Validate the source file before conversion."""

    if max_size_bytes < 0:
        raise ValueError("Maximum file size cannot be negative")

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

    file_size = file_path.stat().st_size

    if file_size > max_size_bytes:
        limit_mib = max_size_bytes / (1024 * 1024)
        raise ValueError(
            f"File exceeds the {limit_mib:g} MiB size limit: {file_path}"
        )

    try:
        with file_path.open("rb") as source:
            source.read(1)
    except PermissionError as exc:
        raise PermissionError(
            f"File is not readable: {file_path}"
        ) from exc
