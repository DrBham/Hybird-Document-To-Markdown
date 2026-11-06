"""Orchestrate local image analysis and Markdown rendering."""

from __future__ import annotations

from pathlib import Path

from .backend import DocumentIntelligenceBackend
from .renderer import render_intelligence_markdown


SUPPORTED_IMAGE_FORMATS = frozenset(
    {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
)


class LocalDocumentIntelligence:
    """Run an injected local backend and return portable Markdown."""

    def __init__(self, backend: DocumentIntelligenceBackend):
        self._backend = backend

    def analyze_to_markdown(self, image_path: Path) -> str:
        source = image_path.expanduser().resolve()
        if source.suffix.lower() not in SUPPORTED_IMAGE_FORMATS:
            raise ValueError(f"unsupported image format: {source.suffix or '(none)'}")
        if not source.is_file():
            raise FileNotFoundError(source)
        return render_intelligence_markdown(self._backend.analyze(source))
