"""Combine standard document conversion with local image intelligence."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from ..core.base_converter import BaseConverter
from ..core.models import ConversionResult
from .extractor import DocumentImageExtractor
from .service import LocalDocumentIntelligence


class IntelligentDocumentConverter(BaseConverter):
    """Decorate a converter with best-effort local image analysis."""

    def __init__(
        self,
        base_converter: BaseConverter,
        intelligence: LocalDocumentIntelligence,
        extractor: DocumentImageExtractor | None = None,
    ):
        self._base_converter = base_converter
        self._intelligence = intelligence
        self._extractor = extractor or DocumentImageExtractor()

    def convert(self, file_path: Path) -> ConversionResult:
        base_result = self._base_converter.convert(file_path)
        sections: list[str] = []

        with TemporaryDirectory(prefix="hybrid-document-intelligence-") as temporary:
            images = self._extractor.extract(file_path, Path(temporary))
            for image in images:
                try:
                    analysis = self._intelligence.analyze_to_markdown(image.path)
                except Exception as exc:
                    sections.append(
                        f"### {image.context}\n\n"
                        f"> [!WARNING]\n"
                        f"> Local image analysis failed: {type(exc).__name__}: {exc}"
                    )
                else:
                    sections.append(f"### {image.context}\n\n{analysis.rstrip()}")

        markdown = base_result.markdown.rstrip()
        if sections:
            markdown += (
                "\n\n---\n\n# Local document intelligence\n\n"
                + "\n\n".join(sections)
                + "\n"
            )
        elif base_result.markdown.endswith("\n"):
            markdown += "\n"

        return ConversionResult(
            source_path=base_result.source_path,
            source_format=base_result.source_format,
            markdown=markdown,
        )
