"""Run a real local OCR benchmark and report quality/resource metrics."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import psutil

from document_converter.intelligence.evaluation import (
    character_error_rate,
    normalize_ocr_text,
)
from document_converter.intelligence.model_manager import LocalModelManager, ModelState
from document_converter.intelligence.pipeline import build_local_ocr_backend


MODEL_ID = "hybrid-document-intelligence"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--reference", required=True)
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--runs", type=int, default=3)
    arguments = parser.parse_args()
    if arguments.runs < 1:
        raise SystemExit("--runs must be at least 1")

    manager = LocalModelManager()
    inspection = manager.inspect(MODEL_ID)
    if inspection.state != ModelState.READY:
        raise SystemExit(f"model pack is not ready: {inspection.state.value}")

    process = psutil.Process()
    memory_before = process.memory_info().rss
    backend = build_local_ocr_backend(manager, MODEL_ID)
    elapsed_runs = []
    result = None
    for _ in range(arguments.runs):
        started = time.perf_counter()
        result = backend.analyze(arguments.image)
        elapsed_runs.append(time.perf_counter() - started)
    if result is None:
        raise AssertionError("benchmark produced no result")
    memory_after = process.memory_info().rss
    prediction = " ".join(region.text for region in result.text_regions)
    metrics = {
        "model_version": inspection.version,
        "image": str(arguments.image.resolve()),
        "recognized_regions": len(result.text_regions),
        "reference_text": normalize_ocr_text(arguments.reference),
        "predicted_text": normalize_ocr_text(prediction),
        "character_error_rate": character_error_rate(
            arguments.reference, prediction
        ),
        "elapsed_seconds": elapsed_runs,
        "elapsed_seconds_cold": elapsed_runs[0],
        "elapsed_seconds_warm_average": (
            sum(elapsed_runs[1:]) / len(elapsed_runs[1:])
            if len(elapsed_runs) > 1
            else None
        ),
        "rss_before_mib": memory_before / (1024 * 1024),
        "rss_after_mib": memory_after / (1024 * 1024),
        "rss_delta_mib": (memory_after - memory_before) / (1024 * 1024),
    }
    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    if arguments.json_output:
        arguments.json_output.parent.mkdir(parents=True, exist_ok=True)
        arguments.json_output.write_text(
            json.dumps(metrics, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
