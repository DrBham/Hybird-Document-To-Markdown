
from document_converter.core.markdown_builder import MarkdownBuilder
from document_converter.services.markdown_exporter import MarkdownExporter


def test_markdown_builder_and_exporter(tmp_path):
    """Verify Markdown generation and file export work together."""

    builder = MarkdownBuilder()

    builder.add_heading("Research Report", 1)
    builder.add_heading("Introduction", 2)
    builder.add_paragraph("This document contains research data.")

    markdown = builder.build()

    output_path = tmp_path / "report.md"

    exporter = MarkdownExporter()
    result = exporter.export(markdown, output_path)

    expected = (
        "# Research Report\n\n"
        "## Introduction\n\n"
        "This document contains research data."
    )

    assert result == output_path
    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == expected
