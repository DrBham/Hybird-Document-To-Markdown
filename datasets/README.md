# Phase E Dataset Workspace

**Current checkpoint: E3 — Dataset & Training (WIP).** E2 established the frozen pretrained baseline and its acceptance thresholds. E3 now owns corpus expansion, stable data splits, preprocessing, training, and checkpoint comparison.

Keep evaluation and training data outside Git unless its license explicitly allows redistribution. Record every dataset in a local manifest with:

- source URL and retrieval date;
- upstream license and permitted uses;
- document/image categories and languages;
- preprocessing steps;
- train, validation, and test split rules;
- known bias, privacy, and quality limitations.

The OCR evaluator accepts UTF-8 JSONL records:

```json
{"reference_text":"Router A connects to Switch B","predicted_text":"Router A connects to Switch B"}
```

Run it from the repository root:

```powershell
$env:PYTHONPATH = "src"
python scripts/evaluate_ocr.py path\to\evaluation.jsonl
```

Do not train on the held-out test split. Keep it stable so model versions remain comparable.

## E3 entry checklist

- Register each candidate dataset before downloading or processing it.
- Reject sources whose license, consent, privacy, or redistribution terms are unclear.
- Deduplicate documents before creating splits to prevent evaluation leakage.
- Keep train, validation, and held-out test identifiers stable and versioned.
- Store generated data and model outputs outside Git unless redistribution is explicitly allowed.
- Compare every checkpoint with the frozen E2 policy before promoting it.

The first E3 deliverable will define the dataset-manifest schema and validation command. Training must not start until those controls are tested.
