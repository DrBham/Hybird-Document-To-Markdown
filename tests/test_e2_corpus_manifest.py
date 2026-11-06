import json
from pathlib import Path


MANIFEST = Path("datasets/manifests/e2-paddleocr-smoke.json")


def test_e2_corpus_manifest_has_traceable_verified_samples():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    samples = payload["samples"]
    identifiers = [sample["id"] for sample in samples]

    assert payload["license"] == "Apache-2.0"
    assert payload["redistribution_policy"].startswith("download-only")
    assert len(samples) >= 5
    assert len(identifiers) == len(set(identifiers))
    for sample in samples:
        assert sample["url"].startswith(
            "https://raw.githubusercontent.com/PaddlePaddle/PaddleOCR/"
        )
        assert len(sample["sha256"]) == 64
        assert isinstance(sample["expected_substrings"], list)
