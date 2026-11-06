"""Backend contract for replaceable, fully local vision engines."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from .models import DocumentIntelligenceResult


@runtime_checkable
class DocumentIntelligenceBackend(Protocol):
    """Analyze one image without assuming a particular ML framework."""

    @property
    def name(self) -> str:
        """Return a human-readable backend name."""

    def analyze(self, image_path: Path) -> DocumentIntelligenceResult:
        """Return structured text and visual relationships for an image."""
