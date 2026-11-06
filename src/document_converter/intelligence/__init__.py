"""Local document-intelligence building blocks for Phase E."""

from .backend import DocumentIntelligenceBackend
from .converter import IntelligentDocumentConverter
from .extractor import DocumentImageExtractor, ExtractedImage
from .model_manager import LocalModelManager, ModelState
from .models import (
    BoundingBox,
    DocumentIntelligenceResult,
    TextRegion,
    VisualElement,
    VisualRelationship,
)
from .renderer import render_intelligence_markdown
from .service import LocalDocumentIntelligence
from .paddle_ocr import PaddleOCRBackend, PaddleOCRBackendError
from .pipeline import build_local_intelligence_batch_converter

__all__ = [
    "BoundingBox",
    "DocumentIntelligenceBackend",
    "DocumentIntelligenceResult",
    "DocumentImageExtractor",
    "ExtractedImage",
    "IntelligentDocumentConverter",
    "LocalDocumentIntelligence",
    "LocalModelManager",
    "ModelState",
    "PaddleOCRBackend",
    "PaddleOCRBackendError",
    "TextRegion",
    "VisualElement",
    "VisualRelationship",
    "render_intelligence_markdown",
    "build_local_intelligence_batch_converter",
]
