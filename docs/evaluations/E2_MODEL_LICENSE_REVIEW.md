# E2 Model License Review

**Review date:** 2026-11-06  
**Scope:** `PP-LCNet_x1_0_doc_ori`, `PP-OCRv5_mobile_det`, and `latin_PP-OCRv5_mobile_rec` obtained through the official PaddleX model registry.

## Decision

The E2 baseline may use, reproduce, and prepare these official PaddleOCR artifacts for redistribution under **Apache License 2.0**, provided the distributed model pack preserves the applicable license and attribution notices. This decision closes the E2 license gate; it is not a substitute for the final E5 release audit.

The repository does not currently commit the model binaries. `scripts/bootstrap_ocr_model.py` downloads them from the selected official model host and records their hashes, model names, source repository, upstream license, and notice requirement in the local manifest.

## Evidence reviewed

- The [official PaddleOCR repository](https://github.com/PaddlePaddle/PaddleOCR) declares Apache License 2.0 for the project.
- The installed PaddleOCR 3.7.0 distribution declares `Apache License 2.0` and includes its `LICENSE` file.
- [Official text-detection documentation](https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/module_usage/text_detection.html) identifies `PP-OCRv5_mobile_det` as an inference/training model.
- [Official text-recognition documentation](https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/module_usage/text_recognition.html) identifies `latin_PP-OCRv5_mobile_rec` as a pretrained Latin-script recognition model.
- Every binary in the local pack is identified by a relative path, byte size, and SHA-256 digest.

## Distribution requirements

When an E5 public model pack is produced:

1. include the PaddleOCR Apache-2.0 license text;
2. identify PaddlePaddle/PaddleOCR and the exact model names;
3. preserve model provenance and SHA-256 values;
4. label project modifications or fine-tuning clearly;
5. repeat the audit against the exact downloaded artifacts and selected host;
6. include any additional notices required by the final inference runtime;
7. do not imply that the project MIT license replaces the model license.

## Boundary

This review covers only the current official pretrained E2 baseline. Datasets and checkpoints introduced during E3 require separate manifests and license reviews. A later model trained or fine-tuned by this project may contain obligations inherited from its source datasets and base checkpoint.

This is an engineering compliance record, not legal advice.
