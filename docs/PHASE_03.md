# Phase 3 — Custom TXT Conversion Engine

**Status:** In Progress  
**Prerequisites:** Phase 1 environment setup and Phase 2 modular architecture completed (local tests: 14/14 passed).  
**Scope:** Plain-text input (`.txt`) to Markdown (`.md`) using original Python conversion rules.

## Goal

Implement a readable, testable TXT conversion engine that conforms to `BaseConverter.convert(file_path: Path) -> ConversionResult`, cooperates with the existing router and Markdown builder, and preserves text without inventing document structure. This phase is **not yet implemented**.

> Plain text has no guaranteed semantic heading, list, or table metadata. We will only infer structure when explicit, documented rules support it; ambiguous text should be preserved rather than aggressively reformatted.

## Subphase Plan

| Subphase | Task | Deliverable | Acceptance criteria | Status |
|:---:|---|---|---|:---:|
| 3.1 | TXT input rules and test fixtures | Defined handling of UTF-8, blank lines, line endings and ambiguous syntax | Fixture decisions and examples reviewed | 🟡 In progress |
| 3.2 | Minimal TXT engine | `src/document_converter/converters/txt_converter.py` | Reads UTF-8 TXT, returns `ConversionResult`; initial tests pass | ⚪ Planned |
| 3.3 | Structure-preservation rules | Heading/list/paragraph policies with safe fallback | Source text remains readable; no unsupported structural claims | ⚪ Planned |
| 3.4 | Edge cases and error handling | Empty files, Unicode, bad encodings, whitespace and large inputs | Focused positive and negative tests pass | ⚪ Planned |
| 3.5 | Routing integration, review and assessment | Registered TXT engine and end-to-end output tests | Full test suite passes; behavior can be demonstrated | ⚪ Planned |

## Responsibilities

| Component | Responsibility |
|---|---|
| `TXTConverter` | Read and interpret plain text according to documented rules |
| `MarkdownBuilder` | Assemble supported Markdown blocks consistently |
| `ConversionResult` | Carry the source path, format and generated Markdown |
| `ConverterRouter` | Validate input and dispatch `.txt` files to the TXT engine |
| `MarkdownExporter` | Save `.md` files safely with UTF-8 encoding and overwrite protection |

## Phase 3.1 — Design Decisions to Learn First

1. Explain why plain text does not automatically contain headings or tables.
2. Compare a literal-text preservation mode with an optional rule-based formatting mode.
3. Decide how blank lines and Windows/Unix line endings should be handled.
4. Define a fixture with Unicode and text that resembles Markdown syntax.
5. Agree on what counts as success before writing `TXTConverter`.

## Early Acceptance Examples

| Input | Intended initial handling |
|---|---|
| `Hello world` | Preserve as readable text |
| `First line\nSecond line` | Preserve intentional line separation according to the documented rule |
| `# Already Markdown` | Avoid double-escaping or fabricating an extra heading |
| `日本語 — α β γ` | Preserve Unicode characters |
| Empty file | Return an empty Markdown string or a documented, tested error policy |

## Quality and Limitations

- No MarkItDown or ready-made document-to-Markdown conversion engine will be used.
- Standard Python facilities will be used for plain-text file access.
- Heuristics must be explainable and covered by tests.
- No automatic semantic reconstruction guarantee is claimed for arbitrary `.txt` files.
- DOCX/PDF conversion and the desktop GUI remain outside Phase 3.

## Assessment Questions

1. Why can a TXT converter not reliably know whether a line is a heading?
2. Why should file reading and Markdown exporting remain separate responsibilities?
3. What does `ConversionResult` add beyond a plain Markdown string?
4. How do you test that Unicode, blank lines, and line endings are not damaged?
5. Why must the router be tested again when the real TXT engine is registered?

## Phase Exit Checklist

- [ ] TXT behavior and assumptions documented in English.
- [ ] TXT engine implemented using original conversion rules.
- [ ] Positive, negative and integration tests pass.
- [ ] Full existing test suite still passes.
- [ ] Assessment completed and explained without relying on the code authoring assistant.
- [ ] README and this guide updated to Completed; next phase set to In Progress.
- [ ] Phase 3 commit pushed and verified on GitHub.
