# Phase 2 — Software Architecture & Modular Design

**Status:** Completed — local tests and learning assessment passed  
**Next:** [Phase 3 — Custom TXT Conversion Engine](PHASE_03.md)

## Completed Work

| Subphase | Deliverable | Status |
|:---:|---|:---:|
| 2.1 | `document_converter` package and core/converters/gui/services boundaries | Completed |
| 2.2 | `BaseConverter` abstract interface and `ConversionResult` data model | Completed |
| 2.3 | File validator, extension-based converter router and fake-converter tests | Completed |
| 2.4 | Basic Markdown builder and UTF-8 exporter with overwrite protection | Completed |
| 2.5 | Integration test, complete local test run and learning assessment | Completed |

## Source Layout Verified During Phase 2

```text
src/document_converter/
  __init__.py
  converters/__init__.py
  core/
    __init__.py
    base_converter.py
    models.py
    validator.py
    router.py
    markdown_builder.py
  gui/__init__.py
  services/
    __init__.py
    markdown_exporter.py
tests/
  test_router.py
  test_markdown_builder.py
  test_markdown_exporter.py
  test_markdown_integration.py
```

## Verification

The most recent reported local test command was:

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests/ -v
```

**Reported result:** 14 passed (Windows, Python 3.13.0, pytest 9.2.0). The tests covered router dispatch through simulated converters, heading level validation, Markdown exporting and an integration between builder and exporter.

**Assessment:** The architecture assessment and follow-up review were passed. Git push status should be verified independently from the local test result.

## Current Limitations

- All converter routing tests used fake engines; no real TXT, DOCX or PDF conversion was implemented during Phase 2.
- `MarkdownBuilder` supports basic headings and paragraphs only; lists, tables, Markdown escaping and advanced whitespace handling remain to be implemented and tested.
- `MarkdownExporter` has UTF-8 writing and overwrite safeguards, but is not yet an atomic writer.
- The file validator checks existence, regular-file status and extension; it does not verify document signatures or parse internal file structures.
- The desktop GUI is not yet implemented.

## Design Rationale

The router selects an engine without parsing document content. `BaseConverter` defines a shared method contract. Concrete engines will return `ConversionResult` instances. The Markdown builder assembles formatted output; the exporter persists it separately to disk.

## Next Step

Begin Phase 3.1 by defining TXT input policies and representative fixtures before implementing the first real converter.
