"""Stable result schema shared by OCR and diagram-understanding backends."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


def _validate_confidence(value: float | None) -> None:
    if value is not None and not 0.0 <= value <= 1.0:
        raise ValueError("confidence must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class BoundingBox:
    """Axis-aligned image coordinates in pixels."""

    left: float
    top: float
    right: float
    bottom: float

    def __post_init__(self) -> None:
        if min(self.left, self.top, self.right, self.bottom) < 0:
            raise ValueError("bounding-box coordinates cannot be negative")
        if self.right < self.left or self.bottom < self.top:
            raise ValueError("bounding-box edges are out of order")


@dataclass(frozen=True, slots=True)
class TextRegion:
    """Text recognized in one bounded image region."""

    text: str
    bounds: BoundingBox
    confidence: float | None = None

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("text regions cannot be blank")
        _validate_confidence(self.confidence)


@dataclass(frozen=True, slots=True)
class VisualElement:
    """A meaningful diagram, chart, or document element."""

    identifier: str
    kind: str
    label: str
    bounds: BoundingBox | None = None
    confidence: float | None = None

    def __post_init__(self) -> None:
        if not self.identifier.strip() or not self.kind.strip():
            raise ValueError("visual elements need an identifier and kind")
        _validate_confidence(self.confidence)


@dataclass(frozen=True, slots=True)
class VisualRelationship:
    """A directional or semantic connection between visual elements."""

    source_id: str
    target_id: str
    kind: str
    label: str = ""
    confidence: float | None = None

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.target_id.strip():
            raise ValueError("relationships need source and target identifiers")
        if not self.kind.strip():
            raise ValueError("relationships need a kind")
        _validate_confidence(self.confidence)


@dataclass(frozen=True, slots=True)
class DocumentIntelligenceResult:
    """Framework-independent analysis result ready for Markdown rendering."""

    source_path: Path
    backend_name: str
    model_version: str
    summary: str = ""
    text_regions: tuple[TextRegion, ...] = ()
    elements: tuple[VisualElement, ...] = ()
    relationships: tuple[VisualRelationship, ...] = ()
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.backend_name.strip() or not self.model_version.strip():
            raise ValueError("backend name and model version are required")
