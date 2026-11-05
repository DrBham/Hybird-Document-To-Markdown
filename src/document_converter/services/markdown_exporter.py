
from pathlib import Path


class MarkdownExporter:
    """Export Markdown content with overwrite protection."""

    def export(
        self,
        markdown: str,
        output_path: Path,
        overwrite: bool = False,
    ) -> Path:
        if output_path.suffix.lower() != ".md":
            raise ValueError(
                "Output file must have a .md extension"
            )

        if output_path.exists() and not overwrite:
            raise FileExistsError(
                f"Output file already exists: {output_path}"
            )

        if overwrite:
            output_path.write_text(markdown, encoding="utf-8")
        else:
            with output_path.open("x", encoding="utf-8") as file:
                file.write(markdown)

        return output_path
