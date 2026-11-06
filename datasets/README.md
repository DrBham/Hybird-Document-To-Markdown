# Phase E Dataset Workspace

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
