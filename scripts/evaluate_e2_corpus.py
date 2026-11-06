"""Evaluate the local OCR model against the attributed E2 smoke corpus."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from document_converter.intelligence.evaluation import normalize_ocr_text
from document_converter.intelligence.model_manager import LocalModelManager
from document_converter.intelligence.pipeline import build_local_ocr_backend


MODEL_ID = "hybrid-document-intelligence"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("datasets/manifests/e2-paddleocr-smoke.json"),
    )
    parser.add_argument("--corpus", type=Path, default=Path(".e2-corpus"))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".e2-results/corpus-baseline.json"),
    )
    arguments = parser.parse_args()

    manifest = json.loads(arguments.manifest.read_text(encoding="utf-8"))
    manager = LocalModelManager()
    inspection = manager.inspect(MODEL_ID)
    backend = build_local_ocr_backend(manager, MODEL_ID)
    results = []
    total_expected = 0
    total_matched = 0

    for sample in manifest["samples"]:
        image = arguments.corpus / sample["filename"]
        started = time.perf_counter()
        analysis = backend.analyze(image)
        elapsed = time.perf_counter() - started
        prediction = " ".join(region.text for region in analysis.text_regions)
        normalized = normalize_ocr_text(prediction)
        expected = sample.get("expected_substrings", [])
        matches = [
            substring
            for substring in expected
            if normalize_ocr_text(substring) in normalized
        ]
        total_expected += len(expected)
        total_matched += len(matches)
        results.append(
            {
                "id": sample["id"],
                "category": sample["category"],
                "recognized_regions": len(analysis.text_regions),
                "elapsed_seconds": elapsed,
                "expected_substrings": expected,
                "matched_substrings": matches,
                "substring_recall": (
                    len(matches) / len(expected) if expected else None
                ),
                "predicted_text": prediction,
            }
        )
        print(
            f"{sample['id']}: {len(analysis.text_regions)} regions, "
            f"{len(matches)}/{len(expected)} expected snippets, {elapsed:.2f}s"
        )

    report = {
        "model_version": inspection.version,
        "manifest": str(arguments.manifest),
        "sample_count": len(results),
        "scored_substring_recall": (
            total_matched / total_expected if total_expected else None
        ),
        "results": results,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"scored substring recall: {report['scored_substring_recall']:.2%}")
    print(arguments.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
