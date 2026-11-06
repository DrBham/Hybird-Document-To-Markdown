"""Persistent, integrity-checked model storage for offline inference."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path, PurePosixPath
from typing import Any


class ModelState(StrEnum):
    NOT_INSTALLED = "not-installed"
    INCOMPLETE = "incomplete"
    CORRUPT = "corrupt"
    READY = "ready"


@dataclass(frozen=True, slots=True)
class ModelInspection:
    state: ModelState
    model_id: str
    version: str = ""
    detail: str = ""


class LocalModelManager:
    """Inspect versioned models without downloading or executing them."""

    MANIFEST_NAME = "model-manifest.json"

    def __init__(self, root: Path | None = None):
        self.root = (root or self.default_root()).expanduser().resolve()

    @staticmethod
    def default_root() -> Path:
        base = os.environ.get("LOCALAPPDATA")
        if base:
            return Path(base) / "HybridDocumentToMarkdown" / "models"
        return Path.home() / ".hybrid-document-to-markdown" / "models"

    def inspect(self, model_id: str) -> ModelInspection:
        model_directory = self.model_directory(model_id)
        manifest_path = model_directory / self.MANIFEST_NAME
        if not manifest_path.is_file():
            return ModelInspection(ModelState.NOT_INSTALLED, model_id)

        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            version = self._required_text(manifest, "version")
            artifacts = manifest["artifacts"]
            if not isinstance(artifacts, list) or not artifacts:
                raise ValueError("artifacts must be a non-empty list")
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            return ModelInspection(ModelState.CORRUPT, model_id, detail=str(exc))

        for artifact in artifacts:
            try:
                relative_path = self._safe_relative_path(
                    self._required_text(artifact, "path")
                )
                expected_hash = self._required_text(artifact, "sha256").lower()
                expected_size = int(artifact["size"])
            except (KeyError, TypeError, ValueError) as exc:
                return ModelInspection(
                    ModelState.CORRUPT,
                    model_id,
                    version,
                    f"invalid artifact entry: {exc}",
                )

            artifact_path = model_directory / relative_path
            if not artifact_path.is_file():
                return ModelInspection(
                    ModelState.INCOMPLETE,
                    model_id,
                    version,
                    f"missing artifact: {relative_path.as_posix()}",
                )
            if artifact_path.stat().st_size != expected_size:
                return ModelInspection(
                    ModelState.CORRUPT,
                    model_id,
                    version,
                    f"size mismatch: {relative_path.as_posix()}",
                )
            if self._sha256(artifact_path) != expected_hash:
                return ModelInspection(
                    ModelState.CORRUPT,
                    model_id,
                    version,
                    f"checksum mismatch: {relative_path.as_posix()}",
                )

        return ModelInspection(ModelState.READY, model_id, version)

    def model_directory(self, model_id: str) -> Path:
        """Return the validated persistent directory for one model pack."""
        return self.root / self._safe_model_id(model_id)

    def read_manifest(self, model_id: str) -> dict[str, Any]:
        """Read a verified pack manifest for runtime configuration."""
        inspection = self.inspect(model_id)
        if inspection.state != ModelState.READY:
            raise ValueError(
                f"local model pack is not ready: {inspection.state.value}"
            )
        manifest_path = self.model_directory(model_id) / self.MANIFEST_NAME
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError("model manifest must contain an object")
        return manifest

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def _required_text(mapping: dict[str, Any], key: str) -> str:
        value = mapping[key]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be non-empty text")
        return value.strip()

    @staticmethod
    def _safe_model_id(model_id: str) -> str:
        allowed = "abcdefghijklmnopqrstuvwxyz0123456789-_"
        if not model_id or any(character not in allowed for character in model_id):
            raise ValueError("model_id may contain lowercase letters, digits, '-' and '_'")
        return model_id

    @staticmethod
    def _safe_relative_path(value: str) -> Path:
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or not path.parts:
            raise ValueError("artifact paths must stay inside the model directory")
        return Path(*path.parts)
