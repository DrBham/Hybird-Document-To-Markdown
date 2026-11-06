"""Evaluate OCR predictions stored in newline-delimited JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from document_converter.intelligence.evaluation import evaluate_ocr_samples


def load_samples(path: Path) -> list[tuple[str, str]]:
    samples: list[tuple[str, str]] = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            try:
                samples.append((record["reference_text"], record["predicted_text"]))
            except KeyError as exc:
                raise ValueError(
                    f"line {line_number} is missing {exc.args[0]}"
                ) from exc
    return samples


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calculate exact-match rate and OCR character error rate."
    )
    parser.add_argument("dataset", type=Path, help="UTF-8 JSONL evaluation file")
    arguments = parser.parse_args()
    result = evaluate_ocr_samples(load_samples(arguments.dataset))
    print(f"samples: {result.sample_count}")
    print(f"exact_match_rate: {result.exact_match_rate:.4f}")
    print(f"character_error_rate: {result.character_error_rate:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
