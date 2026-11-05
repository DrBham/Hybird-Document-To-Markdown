# Third-Party Notices

## Scope

This independent project currently uses third-party libraries for its desktop interface, source-document parsing, and testing. The document-to-Markdown conversion algorithms are intended to be implemented in this repository.

| Package | Purpose | Upstream |
|---|---|---|
| PySide6 / Qt for Python | Desktop GUI | https://doc.qt.io/qtforpython-6/ |
| python-docx | DOCX parsing | https://github.com/python-openxml/python-docx |
| pdfplumber | PDF text and layout extraction | https://github.com/jsvine/pdfplumber |
| pytest | Development testing | https://github.com/pytest-dev/pytest |

## Historical note

Microsoft MarkItDown was considered during project planning, but is **not** included in the current dependency set and is **not** part of the planned conversion pipeline.

## Licensing and release checklist

This document is an inventory, **not yet a complete set of redistribution notices**. Before distributing an executable or source bundle:

1. Check the exact versions and licenses of all distributed direct and transitive dependencies.
2. Review PySide6/Qt licensing, including relevant LGPL/GPL or commercial-license obligations and the packaging approach.
3. Include required copyright statements, license texts, and other notices for redistributed components.
4. Confirm that any custom project `LICENSE` applies only to material the project author is entitled to license.
5. Update this document to reflect the actual release contents.

No endorsement by any third-party maintainer is implied.
