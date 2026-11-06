"""Run one document through the real Phase E local pipeline."""

from __future__ import annotations

import argparse
from pathlib import Path

from document_converter.intelligence.model_manager import LocalModelManager
from document_converter.intelligence.pipeline import (
    build_local_intelligence_batch_converter,
)


MODEL_ID = "hybrid-document-intelligence"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    parser.add_argument("output", type=Path)
    arguments = parser.parse_args()

    service = build_local_intelligence_batch_converter(
        LocalModelManager(), MODEL_ID
    )
    batch = service.convert((arguments.document.resolve(),))
    outcome = batch.outcomes[0]
    if not outcome.succeeded or outcome.result is None:
        raise SystemExit(outcome.error or "conversion failed")
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(outcome.result.markdown, encoding="utf-8")
    print(arguments.output.resolve())
    print(f"characters: {len(outcome.result.markdown)}")
    print(f"contains_local_analysis: {'# Local document intelligence' in outcome.result.markdown}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
