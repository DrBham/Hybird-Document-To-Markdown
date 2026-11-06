"""Download official PaddleOCR weights and build the first local model pack."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from document_converter.intelligence.model_manager import LocalModelManager
from document_converter.intelligence.model_pack import build_model_pack


MODEL_ID = "hybrid-document-intelligence"
MODEL_VERSION = "paddleocr-3.7.0-ppocrv5-mobile-latin-2"
ORIENTATION_MODEL = "PP-LCNet_x1_0_doc_ori"
DETECTION_MODEL = "PP-OCRv5_mobile_det"
RECOGNITION_MODEL = "latin_PP-OCRv5_mobile_rec"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build an integrity-checked local OCR model pack."
    )
    parser.add_argument(
        "--model-root",
        type=Path,
        help="Override the default per-user application model directory.",
    )
    parser.add_argument(
        "--source",
        choices=("huggingface", "bos", "modelscope", "aistudio"),
        default="huggingface",
        help="Official model host used by PaddleX.",
    )
    arguments = parser.parse_args()

    os.environ["PADDLE_PDX_MODEL_SOURCE"] = arguments.source
    from paddlex.inference.utils.official_models import official_models

    print(f"Downloading {ORIENTATION_MODEL} from {arguments.source}...")
    orientation = Path(official_models.get_model_path(ORIENTATION_MODEL))
    print(f"Downloading {DETECTION_MODEL} from {arguments.source}...")
    detection = Path(official_models.get_model_path(DETECTION_MODEL))
    print(f"Downloading {RECOGNITION_MODEL} from {arguments.source}...")
    recognition = Path(official_models.get_model_path(RECOGNITION_MODEL))

    manager = LocalModelManager(arguments.model_root)
    target = build_model_pack(
        manager,
        MODEL_ID,
        MODEL_VERSION,
        {
            "orientation": orientation,
            "detection": detection,
            "recognition": recognition,
        },
        metadata={
            "backend": "PaddleOCR",
            "paddleocr_version": "3.7.0",
            "orientation_model": ORIENTATION_MODEL,
            "detection_model": DETECTION_MODEL,
            "recognition_model": RECOGNITION_MODEL,
            "languages": ["id", "en", "latin-script"],
            "upstream_license": "Apache-2.0",
            "upstream_repository": "https://github.com/PaddlePaddle/PaddleOCR",
            "license_url": "https://github.com/PaddlePaddle/PaddleOCR/blob/main/LICENSE",
            "redistribution_status": "apache-2.0-notice-required",
            "release_compliance_checkpoint": "E5",
        },
    )
    inspection = manager.inspect(MODEL_ID)
    size = sum(path.stat().st_size for path in target.rglob("*") if path.is_file())
    print(f"Model pack: {target}")
    print(f"Version: {inspection.version}")
    print(f"Integrity: {inspection.state.value}")
    print(f"Size: {size / (1024 * 1024):.2f} MiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
