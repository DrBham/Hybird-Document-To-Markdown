from pathlib import Path

import pytest

from document_converter.core.validator import (
    MAX_FILE_SIZE_BYTES,
    SUPPORTED_FORMATS,
    validate_file,
)


EXPECTED_FORMATS = {
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
}


def test_supported_formats_match_mvp_scope():
    assert SUPPORTED_FORMATS == EXPECTED_FORMATS


def test_validator_accepts_uppercase_extension(tmp_path):
    source = tmp_path / "REPORT.PDF"
    source.write_bytes(b"pdf")

    validate_file(source)


def test_validator_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        validate_file(tmp_path / "missing.txt")


def test_validator_rejects_directory(tmp_path):
    directory = tmp_path / "document.pdf"
    directory.mkdir()

    with pytest.raises(ValueError, match="Path is not a file"):
        validate_file(directory)


def test_validator_rejects_unsupported_extension(tmp_path):
    source = tmp_path / "archive.zip"
    source.write_bytes(b"zip")

    with pytest.raises(ValueError, match="Unsupported file format"):
        validate_file(source)


def test_validator_rejects_file_over_size_limit(tmp_path):
    source = tmp_path / "large.txt"
    source.write_bytes(b"too large")

    with pytest.raises(ValueError, match="size limit"):
        validate_file(source, max_size_bytes=1)


def test_validator_rejects_unreadable_file(tmp_path, monkeypatch):
    source = tmp_path / "locked.txt"
    source.write_text("content", encoding="utf-8")
    original_open = Path.open

    def deny_source_file(path, *args, **kwargs):
        if path == source:
            raise PermissionError("access denied")

        return original_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, "open", deny_source_file)

    with pytest.raises(PermissionError, match="File is not readable"):
        validate_file(source)


def test_default_size_limit_is_100_mib():
    assert MAX_FILE_SIZE_BYTES == 100 * 1024 * 1024


def test_validator_rejects_negative_size_limit(tmp_path):
    source = tmp_path / "sample.txt"
    source.write_text("sample", encoding="utf-8")

    with pytest.raises(ValueError, match="cannot be negative"):
        validate_file(source, max_size_bytes=-1)
