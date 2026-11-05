
import pytest

from document_converter.services.markdown_exporter import MarkdownExporter


def test_export_markdown_file(tmp_path):
    """Verify Markdown content can be exported."""

    output_path = tmp_path / "report.md"
    markdown = "# Report\n\nHello, Markdown!"

    exporter = MarkdownExporter()
    result = exporter.export(markdown, output_path)

    assert result == output_path
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == markdown


def test_export_preserves_unicode(tmp_path):
    """Verify Unicode characters are preserved."""

    output_path = tmp_path / "unicode.md"
    markdown = "# Laporan\n\n日本語 — α β γ 😊"

    exporter = MarkdownExporter()
    exporter.export(markdown, output_path)

    assert output_path.read_text(encoding="utf-8") == markdown


def test_export_rejects_invalid_extension(tmp_path):
    """Reject output paths without a Markdown extension."""

    output_path = tmp_path / "report.txt"

    exporter = MarkdownExporter()

    with pytest.raises(
        ValueError,
        match=r"Output file must have a \.md extension"
    ):
        exporter.export("# Report", output_path)

    assert not output_path.exists()


def test_export_prevents_overwrite(tmp_path):
    """Prevent overwriting existing Markdown files by default."""

    output_path = tmp_path / "report.md"
    output_path.write_text("Original content", encoding="utf-8")

    exporter = MarkdownExporter()

    with pytest.raises(FileExistsError):
        exporter.export("New content", output_path)

    assert output_path.read_text(encoding="utf-8") == "Original content"


def test_export_allows_explicit_overwrite(tmp_path):
    """Allow overwriting when explicitly requested."""

    output_path = tmp_path / "report.md"
    output_path.write_text("Original content", encoding="utf-8")

    exporter = MarkdownExporter()

    exporter.export(
        "Updated content",
        output_path,
        overwrite=True
    )

    assert output_path.read_text(encoding="utf-8") == "Updated content"
