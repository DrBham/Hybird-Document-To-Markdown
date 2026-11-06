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

    backend = PaddleOCRBackend(
        manager.model_directory(model_id),
        model_version=inspection.version,
    )
    converter = IntelligentDocumentConverter(
        MarkItDownConverter(),
        LocalDocumentIntelligence(backend),
    )
    return BatchConverter(
        ConverterRouter({extension: converter for extension in INTELLIGENCE_FORMATS})
    )
