import hashlib
import json

from document_converter.intelligence.model_manager import (
    LocalModelManager,
    ModelState,
)


MODEL_ID = "hybrid-document-intelligence"


def write_model(tmp_path, payload=b"local model weights"):
    model_directory = tmp_path / MODEL_ID
    model_directory.mkdir()
    artifact = model_directory / "weights.bin"
    artifact.write_bytes(payload)
    manifest = {
        "version": "0.1.0",
        "artifacts": [
            {
                "path": "weights.bin",
                "size": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        ],
    }
    (model_directory / "model-manifest.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    return artifact


def test_model_manager_reports_not_installed(tmp_path):
    inspection = LocalModelManager(tmp_path).inspect(MODEL_ID)

    assert inspection.state == ModelState.NOT_INSTALLED


def test_model_manager_verifies_persistent_artifacts(tmp_path):
    write_model(tmp_path)

    inspection = LocalModelManager(tmp_path).inspect(MODEL_ID)

    assert inspection.state == ModelState.READY
    assert inspection.version == "0.1.0"


def test_model_manager_detects_modified_weights(tmp_path):
    artifact = write_model(tmp_path)
    artifact.write_bytes(b"tampered")

    inspection = LocalModelManager(tmp_path).inspect(MODEL_ID)

    assert inspection.state == ModelState.CORRUPT
    assert "mismatch" in inspection.detail


def test_model_manager_rejects_path_traversal(tmp_path):
    model_directory = tmp_path / MODEL_ID
    model_directory.mkdir()
    (model_directory / "model-manifest.json").write_text(
        json.dumps(
            {
                "version": "0.1.0",
                "artifacts": [
                    {"path": "../outside.bin", "size": 0, "sha256": "0"}
                ],
            }
        ),
        encoding="utf-8",
    )

    inspection = LocalModelManager(tmp_path).inspect(MODEL_ID)

    assert inspection.state == ModelState.CORRUPT
    assert "inside the model directory" in inspection.detail
