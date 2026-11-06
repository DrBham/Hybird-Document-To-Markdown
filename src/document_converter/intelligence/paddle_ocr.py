"""Lazy PaddleOCR adapter for the optional local Phase E runtime."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from typing import Any

from .models import BoundingBox, DocumentIntelligenceResult, TextRegion


class PaddleOCRBackendError(RuntimeError):
    """Explain an unavailable or incompatible local OCR runtime."""


class PaddleOCRBackend:
    """Extract bounded text using locally stored PaddleOCR models."""

    name = "PaddleOCR local text engine"

    def __init__(
        self,
        model_directory: Path,
        *,
        model_version: str,
        language: str = "en",
        orientation_model_name: str | None = None,
        detection_model_name: str | None = None,
        recognition_model_name: str | None = None,
        engine_factory: Callable[..., Any] | None = None,
    ):
        self._model_directory = model_directory.expanduser().resolve()
        self._model_version = model_version
        self._language = language
        self._orientation_model_name = orientation_model_name
        self._detection_model_name = detection_model_name
        self._recognition_model_name = recognition_model_name
        self._engine_factory = engine_factory
        self._engine: Any | None = None

    def analyze(self, image_path: Path) -> DocumentIntelligenceResult:
        source = image_path.expanduser().resolve()
        try:
            pages = self._engine_instance().predict(input=str(source))
            regions = tuple(self._read_regions(pages))
        except PaddleOCRBackendError:
            raise
        except Exception as exc:
            raise PaddleOCRBackendError(
                f"Local OCR could not analyze {source.name}: {exc}"
            ) from exc

        warnings: tuple[str, ...] = ()
        if not regions:
            warnings = (
                "No readable text was detected. Diagram understanding may still "
                "require a later Phase E model.",
            )
        return DocumentIntelligenceResult(
            source_path=source,
            backend_name=self.name,
            model_version=self._model_version,
            summary=f"Detected {len(regions)} text region(s) locally.",
            text_regions=regions,
            warnings=warnings,
        )

    def _engine_instance(self) -> Any:
        if self._engine is not None:
            return self._engine

        factory = self._engine_factory
        if factory is None:
            try:
                from paddleocr import PaddleOCR
            except ImportError as exc:
                raise PaddleOCRBackendError(
                    "PaddleOCR is not installed. Install the optional local "
                    "intelligence dependencies first."
                ) from exc
            factory = PaddleOCR

        detection = self._model_directory / "detection"
        recognition = self._model_directory / "recognition"
        if not detection.is_dir() or not recognition.is_dir():
            raise PaddleOCRBackendError(
                "The local OCR model pack is incomplete: detection and "
                "recognition directories are required."
            )

        options: dict[str, Any] = {
            "text_detection_model_dir": str(detection),
            "text_recognition_model_dir": str(recognition),
            "use_doc_orientation_classify": False,
            "use_doc_unwarping": False,
            "use_textline_orientation": False,
            "enable_mkldnn": False,
        }
        if self._orientation_model_name:
            orientation = self._model_directory / "orientation"
            if not orientation.is_dir():
                raise PaddleOCRBackendError(
                    "The local OCR model pack names an orientation model but "
                    "contains no orientation directory."
                )
            options["doc_orientation_classify_model_name"] = (
                self._orientation_model_name
            )
            options["doc_orientation_classify_model_dir"] = str(orientation)
            options["use_doc_orientation_classify"] = True
        if self._detection_model_name:
            options["text_detection_model_name"] = self._detection_model_name
        if self._recognition_model_name:
            options["text_recognition_model_name"] = self._recognition_model_name
        if not self._detection_model_name and not self._recognition_model_name:
            options["lang"] = self._language
        self._engine = factory(**options)
        return self._engine

    @classmethod
    def _read_regions(cls, pages: Iterable[Any]) -> Iterable[TextRegion]:
        for page in pages:
            payload = cls._payload(page)
            texts = list(payload.get("rec_texts", ()))
            scores = list(payload.get("rec_scores", ()))
            boxes = list(payload.get("rec_boxes", ()))
            for index, text in enumerate(texts):
                value = str(text).strip()
                if not value or index >= len(boxes):
                    continue
                score = float(scores[index]) if index < len(scores) else None
                yield TextRegion(
                    text=value,
                    bounds=cls._box(boxes[index]),
                    confidence=score,
                )

    @staticmethod
    def _payload(page: Any) -> Mapping[str, Any]:
        payload = getattr(page, "json", page)
        if callable(payload):
            payload = payload()
        if not isinstance(payload, Mapping):
            raise PaddleOCRBackendError("PaddleOCR returned an unknown result type")
        nested = payload.get("res", payload)
        if not isinstance(nested, Mapping):
            raise PaddleOCRBackendError("PaddleOCR result has no readable payload")
        return nested

    @staticmethod
    def _box(value: Any) -> BoundingBox:
        coordinates = list(value)
        if len(coordinates) != 4:
            raise PaddleOCRBackendError("PaddleOCR returned an invalid text box")
        return BoundingBox(*(float(coordinate) for coordinate in coordinates))
