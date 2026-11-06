"""Local document-intelligence building blocks for Phase E."""

from .backend import DocumentIntelligenceBackend
from .converter import IntelligentDocumentConverter
from .extractor import DocumentImageExtractor, ExtractedImage
from .model_manager import LocalModelManager, ModelState
from .model_pack import build_model_pack
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
from .pipeline import build_local_intelligence_batch_converter, build_local_ocr_backend

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
    "build_local_ocr_backend",
    "build_model_pack",
]
