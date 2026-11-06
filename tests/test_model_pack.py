import json

import pytest

from document_converter.intelligence.model_manager import (
    LocalModelManager,
    ModelState,
)
from document_converter.intelligence.model_pack import build_model_pack


def test_build_model_pack_copies_components_and_hashes_artifacts(tmp_path):
    detection = tmp_path / "source-det"
    recognition = tmp_path / "source-rec"
    detection.mkdir()
    recognition.mkdir()
    (detection / "inference.json").write_text("det", encoding="utf-8")
    (recognition / "inference.json").write_text("rec", encoding="utf-8")
    (detection / ".cache").mkdir()
    (detection / ".cache" / "download.tmp").write_text(
        "cache", encoding="utf-8"
    )
    manager = LocalModelManager(tmp_path / "models")

    target = build_model_pack(
        manager,
        "hybrid-document-intelligence",
        "test-1",
        {"detection": detection, "recognition": recognition},
        metadata={"redistribution_status": "test-only"},
    )

    manifest = json.loads(
        (target / "model-manifest.json").read_text(encoding="utf-8")
    )
    assert manifest["version"] == "test-1"
    assert {item["path"] for item in manifest["artifacts"]} == {
        "detection/inference.json",
        "recognition/inference.json",
    }
    assert not (target / "detection" / ".cache").exists()
    assert manager.inspect("hybrid-document-intelligence").state == ModelState.READY


def test_build_model_pack_never_overwrites_existing_pack(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "model.bin").write_bytes(b"weights")
    manager = LocalModelManager(tmp_path / "models")
    build_model_pack(manager, "ocr-model", "1", {"detection": source})

    with pytest.raises(FileExistsError):
        build_model_pack(manager, "ocr-model", "2", {"detection": source})
