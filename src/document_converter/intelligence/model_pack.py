"""Build reproducible, integrity-checked local model packs."""

from __future__ import annotations

import hashlib
import json
import shutil
from collections.abc import Mapping
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from .model_manager import LocalModelManager


IGNORED_MODEL_FILES = frozenset({".cache", ".git", ".gitattributes"})


def _ignore_model_cache(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name in IGNORED_MODEL_FILES}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_model_pack(
    manager: LocalModelManager,
    model_id: str,
    version: str,
    components: Mapping[str, Path],
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Path:
    """Copy model components and write a verifiable manifest.

    Component names become top-level directories in the model pack. Existing
    packs are never overwritten, so a version must be reviewed before replacement.
    """

    if not version.strip():
        raise ValueError("model pack version is required")
    if not components:
        raise ValueError("at least one model component is required")

    target = manager.model_directory(model_id)
    if target.exists():
        raise FileExistsError(f"model pack already exists: {target}")

    manager.root.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=f".{model_id}-", dir=manager.root) as temporary:
        staging = Path(temporary) / model_id
        staging.mkdir()
        for name, source in components.items():
            if not name or any(character not in "abcdefghijklmnopqrstuvwxyz-_" for character in name):
                raise ValueError(f"invalid component name: {name}")
            resolved_source = source.expanduser().resolve()
            if not resolved_source.is_dir():
                raise FileNotFoundError(resolved_source)
            shutil.copytree(
                resolved_source,
                staging / name,
                ignore=_ignore_model_cache,
            )

        artifacts = []
        for artifact in sorted(path for path in staging.rglob("*") if path.is_file()):
            artifacts.append(
                {
                    "path": artifact.relative_to(staging).as_posix(),
                    "size": artifact.stat().st_size,
                    "sha256": _sha256(artifact),
                }
            )
        if not artifacts:
            raise ValueError("model components contain no files")

        manifest: dict[str, Any] = {
            "schema_version": 1,
            "model_id": model_id,
            "version": version.strip(),
            "artifacts": artifacts,
        }
        if metadata:
            manifest["metadata"] = dict(metadata)
        (staging / manager.MANIFEST_NAME).write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        shutil.move(str(staging), str(target))

    return target
