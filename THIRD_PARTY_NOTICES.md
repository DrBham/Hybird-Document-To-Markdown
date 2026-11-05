# Third-Party Notices

## Purpose and status definitions

This document tracks external software currently used during development and components planned for the project's MarkItDown-based conversion architecture. Listing a planned component **does not mean it has been installed, integrated, packaged, or redistributed**.

This inventory is not a substitute for complete license texts, attribution records, or a release-specific audit of direct and transitive dependencies.

**Project source license:** [MIT License](LICENSE). It applies to original content that contributors are authorized to license; third-party components retain their respective licenses.

## Core and planned architecture components

| Component | Intended role | License / distribution considerations | Upstream source | Status |
|---|---|---|---|---|
| Microsoft MarkItDown 0.1.9 | Primary document-to-Markdown conversion engine | MIT; retain the applicable license and copyright notices when distributing | [Microsoft MarkItDown](https://github.com/microsoft/markitdown) | Installed and integrated with DOCX/PDF extras |
| PySide6 / Qt for Python | Desktop GUI | Open-source and commercial licensing options; verify the applicable Qt modules and LGPL/GPL obligations for Windows packaging | [Qt for Python](https://doc.qt.io/qtforpython-6/) | Development dependency; full GUI pending |
| `markitdown-ocr` | Optional image/OCR enhancement through a compatible Vision model | MIT; review plugin and dependency notices; API access may involve separate provider terms, data processing, and usage fees | [MarkItDown OCR plugin](https://github.com/microsoft/markitdown/tree/main/packages/markitdown-ocr) | Planned; not yet integrated |
| Compatible cloud Vision API / client | Optional image understanding and OCR | Provider/model not selected; verify SDK license, data-handling terms, authentication, and fees before use | To be determined | Planned; undecided |

The `markitdown-ocr` plugin is designed around an LLM/Vision client. It should **not** be described as a guaranteed offline OCR engine. The application's ordinary local conversion path is intended to remain usable without online enhancement.

## Development and migration dependencies

| Component | Existing development role | License / distribution consideration | Upstream source | Migration decision |
|---|---|---|---|---|
| `python-docx` | Previously used for the custom-converter design and local test-fixture creation | MIT; preserve applicable notices if redistributed | [python-docx](https://github.com/python-openxml/python-docx) | Removed from the project's direct dependency list; not required by the production adapter |
| `pdfplumber` | PDF extraction used by MarkItDown's PDF extra | MIT; audit transitive packages if redistributed | [pdfplumber](https://github.com/jsvine/pdfplumber) | Retained as a transitive MarkItDown dependency |
| `pytest` | Development and automated tests | MIT; generally a development dependency, not required in the released application | [pytest](https://github.com/pytest-dev/pytest) | Retain for project testing |

Other libraries may be installed transitively by MarkItDown, the GUI framework, or optional plugins. Their presence and distribution obligations must be audited against the **actual release environment** rather than assumed from this preliminary list.

## Licensing and attribution notes

- **MarkItDown and `markitdown-ocr`:** Both are identified upstream as MIT-licensed. The exact distributed versions and their license/copyright notices must be checked and retained as required.
- **PySide6 / Qt:** The framework offers open-source LGPL/GPL and commercial licensing options. Obligations depend on the actual modules and deployment approach; requirements may include appropriate notices, license texts, and compliance with users' rights concerning covered libraries. Verify before packaging.
- **Optional cloud API:** Using a service does not automatically mean its server software is included in the application's distribution. Review the separately applicable API/provider terms, privacy disclosures, and any client SDK shipped with the app.
- **Original code:** The repository's MIT license is not a relicensing of third-party code.

## Release compliance checklist

1. Record the exact package versions and the final direct/transitive dependency tree.
2. Confirm which packages and native binaries actually ship inside the Windows executable or installer.
3. Review the precise licenses and copyright notices of all redistributed items, including MarkItDown, OCR/plugin dependencies, PySide6, and Qt components.
4. Determine the relevant Qt LGPL/GPL/commercial licensing path and satisfy its obligations for the chosen Windows packaging method.
5. Include required complete license texts, copyright statements, and notices with the distribution.
6. Verify selected cloud API/SDK terms and document consent, privacy, credential handling, and potential processing costs.
7. Recheck this notice document against the actual release build before publishing a GitHub release.

## Independence statement

This is an independent portfolio project. It is not affiliated with, sponsored by, or endorsed by Microsoft, The Qt Company, or other upstream software maintainers.
