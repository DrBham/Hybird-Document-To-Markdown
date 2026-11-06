"""Factory for the optional end-to-end local intelligence converter."""

from __future__ import annotations

from ..converters.markitdown_converter import MarkItDownConverter
from ..core.router import ConverterRouter
from ..services.batch_converter import BatchConverter
from .converter import IntelligentDocumentConverter
from .model_manager import LocalModelManager, ModelState
from .paddle_ocr import PaddleOCRBackend
from .service import LocalDocumentIntelligence


INTELLIGENCE_FORMATS = frozenset({".pdf", ".docx", ".pptx", ".xlsx"})


def build_local_ocr_backend(
    manager: LocalModelManager,
    model_id: str,
) -> PaddleOCRBackend:
    """Build an OCR backend from verified model-pack metadata."""

    inspection = manager.inspect(model_id)
    if inspection.state != ModelState.READY:
        raise ValueError(
            f"local model pack is not ready: {inspection.state.value}"
        )
    manifest = manager.read_manifest(model_id)
    metadata = manifest.get("metadata", {})
    if not isinstance(metadata, dict):
        raise ValueError("model metadata must contain an object")
    detection_model = metadata.get("detection_model")
    recognition_model = metadata.get("recognition_model")
    orientation_model = metadata.get("orientation_model")
    if not isinstance(detection_model, str) or not isinstance(
        recognition_model, str
    ):
        raise ValueError("model metadata must name detection and recognition models")
    return PaddleOCRBackend(
        manager.model_directory(model_id),
        model_version=inspection.version,
        language="id",
        orientation_model_name=(
            orientation_model if isinstance(orientation_model, str) else None
        ),
        detection_model_name=detection_model,
        recognition_model_name=recognition_model,
    )


def build_local_intelligence_batch_converter(
    manager: LocalModelManager,
    model_id: str,
) -> BatchConverter:
    """Build a local converter only after its model pack passes verification."""

    inspection = manager.inspect(model_id)
    if inspection.state != ModelState.READY:
        raise ValueError(
            f"local model pack is not ready: {inspection.state.value}"
        )

    backend = build_local_ocr_backend(manager, model_id)
    converter = IntelligentDocumentConverter(
        MarkItDownConverter(),
        LocalDocumentIntelligence(backend),
    )
    return BatchConverter(
        ConverterRouter({extension: converter for extension in INTELLIGENCE_FORMATS})
    )
