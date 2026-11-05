
class MarkdownBuilder:
    """Build Markdown content from structured elements."""

    def __init__(self):
        self._blocks = []

    def add_heading(self, text: str, level: int) -> None:
        if not 1 <= level <= 6:
            raise ValueError("Heading level must be between 1 and 6")

        heading = f"{'#' * level} {text}"
        self._blocks.append(heading)

    def add_paragraph(self, text: str) -> None:
        self._blocks.append(text)

    def build(self) -> str:
        return "\n\n".join(self._blocks)
