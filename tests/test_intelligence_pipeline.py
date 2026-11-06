import hashlib
import json

from document_converter.intelligence.model_manager import LocalModelManager
from document_converter.intelligence.pipeline import (
    build_local_intelligence_batch_converter,
)


def test_pipeline_requires_verified_model_pack(tmp_path):
    manager = LocalModelManager(tmp_path)

    try:
        build_local_intelligence_batch_converter(manager, "missing-model")
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected a missing model pack to fail")

    assert "not-installed" in message


def test_pipeline_builds_after_integrity_check(tmp_path):
    model_id = "hybrid-document-intelligence"
    model_directory = tmp_path / model_id
    (model_directory / "detection").mkdir(parents=True)
    (model_directory / "recognition").mkdir()
    artifacts = []
    for relative in ("detection/model.bin", "recognition/model.bin"):
        payload = relative.encode("utf-8")
        target = model_directory / relative
        target.write_bytes(payload)
        artifacts.append(
            {
                "path": relative,
                "size": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    (model_directory / "model-manifest.json").write_text(
        json.dumps({"version": "0.1.0", "artifacts": artifacts}),
        encoding="utf-8",
    )

    service = build_local_intelligence_batch_converter(
        LocalModelManager(tmp_path), model_id
    )

    assert service is not None
