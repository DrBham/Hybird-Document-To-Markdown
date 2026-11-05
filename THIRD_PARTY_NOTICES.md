# Third-Party Notices

## Purpose

This document identifies third-party software used during development or planned for the application. It is **not** a substitute for the complete license texts and copyright notices that may be required when redistributing a packaged application.

**Project source license:** [MIT License](LICENSE). It covers original code and documentation owned by this project's contributors, not third-party components.

## Direct dependencies

| Package | Role | Licensing / distribution note | Official source |
|---|---|---|---|
| PySide6 / Qt for Python | Desktop GUI | Offered under open-source (LGPL/GPL) and commercial licensing options. Review the exact components and packaging obligations before shipping a Windows executable. | https://doc.qt.io/qtforpython-6/ |
| python-docx | Read DOCX content and structure | MIT; keep required notices when redistributing applicable components. | https://github.com/python-openxml/python-docx |
| pdfplumber | Extract PDF text and layout information | MIT; check the licenses of its transitive dependencies too. | https://github.com/jsvine/pdfplumber |
| pytest | Development-only automated testing | MIT; normally not part of the end-user executable. | https://github.com/pytest-dev/pytest |

Versions and actual redistributed components must be checked against the release environment (including dependencies pulled in automatically). Upstream license links are provided for verification; they are not embedded copies of license texts.

## Not used as conversion engines

[Microsoft MarkItDown](https://github.com/microsoft/markitdown) was evaluated early in planning but removed from project dependencies. [markdownify](https://github.com/matthewwithanm/python-markdownify) and `python-pptx` are likewise not part of the current conversion pipeline. Mentioning these projects does not imply their code is included or adapted.

## Release compliance checklist

1. Audit exact package versions and all redistributed direct/transitive dependencies.
2. Determine which PySide6/Qt license option applies to the Windows packaging method; satisfy the corresponding source, notice, relinking and other requirements as applicable.
3. Bundle license files, copyright statements and third-party notices required for the actual distribution.
4. Confirm that the project's MIT license applies only to material the project author or contributors can license.
5. Update this inventory before each public release and make legal/license review part of the release checklist.

This project is independent and is not affiliated with or endorsed by the listed maintainers.
