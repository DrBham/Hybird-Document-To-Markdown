# E2 OCR Baseline Report

**Run date:** 2026-11-06  
**Status:** Completed; E2 acceptance passed 12/12 checks. Broader dataset and training work continue in E3.

## Configuration

| Item | Value |
|---|---|
| Runtime | PaddlePaddle 3.3.1, PaddleOCR 3.7.0 |
| Reproducibility | `requirements-intelligence.txt` generated with Python 3.13 |
| Orientation | `PP-LCNet_x1_0_doc_ori` |
| Detection | `PP-OCRv5_mobile_det` |
| Recognition | `latin_PP-OCRv5_mobile_rec` |
| Project model version | `paddleocr-3.7.0-ppocrv5-mobile-latin-2` |
| Model-pack size | 19.10 MiB |
| Primary optional runtime footprint | ~515 MiB installed in the development environment |
| Integrity | Per-file size and SHA-256 verification passed |
| Processing | Local Windows CPU; no document upload or API key |
| CPU | 12th Gen Intel Core i5-12450HX, 8 cores / 12 logical processors |
| System RAM | 11.71 GiB |

The model pack is stored in the per-user application data directory, not in Git. `scripts/bootstrap_ocr_model.py` can reproduce it from the official PaddleX model registry.

The runtime measurement includes approximately 380.02 MiB for `paddle`, 121.03 MiB for `cv2`, 13.03 MiB for `paddlex`, and 0.94 MiB for `paddleocr`. It excludes smaller transitive packages and is an installed development-environment measurement, not a compressed download size. The base converter does not require these packages.

## Synthetic network-diagram smoke test

The project-owned fixture contains Indonesian/English Latin labels, boxes, connectors, and arrowheads. This is a smoke test, not a representative quality benchmark.

| Metric | Result |
|---|---:|
| Detected text regions | 7 |
| Character error rate | 2.38% |
| Cold inference | 5.41 s |
| Warm inference average | 2.75 s |
| Process RSS increase | 264.82 MiB |

Reference:

```text
TOPOLOGI JARINGAN KANTOR INTERNET ROUTER UTAMA 1 GBPS SWITCH LANTAI 1 KOMPUTER ADMIN
```

Prediction:

```text
TOPOLOGI JARINGAN KANTOR INTERNET ROUTER UTAMA 1 GBPS E SWITCH LANTAI 1 KOMPUTER ADMIN
```

The extra `E` was detected near a connector/arrow region. This confirms that diagram graphics can create false text regions and must be represented in the E2/E4 evaluation corpus.

## Attributed official-fixture corpus

Five small fixtures are referenced by `datasets/manifests/e2-paddleocr-smoke.json`. They come from the official PaddleOCR repository, retain source URLs and SHA-256 values, and are downloaded into an ignored local cache. The corpus covers a real dense book scan, its 180-degree rotation, a mixed-script medal table, a noisy mixed table, and an unsupported non-Latin text line.

| Sample | Category | Regions | Expected snippets | Time |
|---|---|---:|---:|---:|
| `book-upright` | Real dense English book scan | 33 | 4/4 | 15.92 s |
| `book-rotated-180` | Rotation | 34 | 4/4 | 18.58 s |
| `medal-table` | Mixed-script table | 94 | 10/10 Latin codes | 19.53 s |
| `mixed-table` | Noisy mixed table | 10 | 6/6 | 2.41 s |
| `non-latin-textline` | Unsupported-script negative case | 0 | Not scored | 0.36 s |

Aggregate scored substring recall is **100% (24/24)**. This is a smoke-corpus metric, not proof of general OCR accuracy; it checks a deliberately small set of stable phrases and codes.

The v1 pack had no orientation model. Its rotated-book recall was 0/4 and aggregate recall was 83.33%. Adding the 7 MB orientation classifier in v2 raised rotated-book recall to 4/4 without reducing the scored upright/table results. The pack grew from 12.55 MiB to 19.10 MiB.

The Latin recognition model intentionally returned no region for the isolated non-Latin text-line fixture. Supporting additional scripts requires separately evaluated recognition coverage; fabricated Latin output would be worse than an explicit unsupported case.

## End-to-end PDF result

The synthetic fixture was also saved as an image-only PDF and passed through the real application pipeline:

1. MarkItDown document conversion;
2. local PDF-page rendering;
3. PaddleOCR detection and recognition;
4. structured result conversion;
5. Markdown composition.

The run succeeded and appended a `Local document intelligence` section containing six high-confidence text regions. This validates the application path, but only against one synthetic page.

## Compatibility decision

MKLDNN is disabled for this Windows CPU baseline. With MKLDNN enabled, PaddlePaddle 3.3.1 raised an unsupported PIR/oneDNN attribute error during detection. The non-MKLDNN path completed successfully and is the current compatibility default. Performance optimization remains separate from functional acceptance.

## License and redistribution decision

PaddleOCR and PaddlePaddle are distributed under Apache-2.0. The E2 review records the exact model names, official source, installed-package license metadata, and required release notices. This closes the E2 baseline gate. An E5 public pack must still ship the Apache-2.0 notice, provenance, hashes, and undergo a final audit against the exact release artifact. See `E2_MODEL_LICENSE_REVIEW.md`.

## E2 acceptance result

The machine-readable policy is stored at `datasets/manifests/e2-acceptance-policy.json`. The final run passed:

- model integrity and minimum version;
- model-pack size below 25 MiB;
- synthetic CER at or below 5%;
- warm CPU inference at or below 5 seconds;
- process RSS increase at or below 350 MiB;
- at least five attributed official fixtures;
- official-fixture snippet recall at or above 95%;
- GUI model availability, successful conversion, and rendered local analysis;
- E2 model-license review.

The final result was **12/12 checks passed**. The actual measurements remained inside every threshold: 19.10 MiB model pack, 2.38% synthetic CER, 2.75 s warm inference, 264.82 MiB RSS increase, and 100% smoke-corpus snippet recall.

The same pack also passed an offscreen GUI workflow using an image-only PDF: the local-analysis option became available, conversion completed, and the generated preview contained the `Local document intelligence` section.

## Work transferred to E3 and E5

- E3 owns the larger licensed Indonesian/English corpus, full held-out references, stable splits, preprocessing, and fine-tuning.
- E4 owns diagram relationships beyond OCR text extraction.
- E5 owns runtime-size optimization, final release compliance, public model packaging, and consumer-hardware acceptance.

E2 therefore establishes and closes the reproducible pretrained OCR baseline; it does not claim general OCR perfection or completed visual understanding.
