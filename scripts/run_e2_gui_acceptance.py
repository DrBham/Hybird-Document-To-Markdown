"""Exercise the real local-intelligence workflow through the desktop GUI."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from document_converter.gui.main_window import MainWindow
from document_converter.intelligence.model_manager import LocalModelManager
from document_converter.intelligence.pipeline import (
    build_local_intelligence_batch_converter,
)


MODEL_ID = "hybrid-document-intelligence"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".e2-results/gui-acceptance.json"),
    )
    parser.add_argument("--timeout", type=float, default=60.0)
    arguments = parser.parse_args()

    document = arguments.document.resolve()
    manager = LocalModelManager()
    converter = build_local_intelligence_batch_converter(manager, MODEL_ID)
    app = QApplication.instance() or QApplication([])
    window = MainWindow(
        intelligence_converter=converter,
        model_manager=manager,
    )
    report = {
        "model_option_enabled": False,
        "conversion_succeeded": False,
        "local_analysis_rendered": False,
    }
    try:
        pdf_index = window.drop_zone.format_selector.findText(
            "PDF document (.pdf)"
        )
        window.drop_zone.format_selector.setCurrentIndex(pdf_index)
        report["model_option_enabled"] = (
            window.intelligence_checkbox.isEnabled()
        )
        window.intelligence_checkbox.setChecked(True)
        window.add_files([document])
        window._start_conversion()
        deadline = time.monotonic() + arguments.timeout
        while window._thread is not None and time.monotonic() < deadline:
            app.processEvents()
            time.sleep(0.01)
        report["timed_out"] = window._thread is not None
        if window.file_tree.topLevelItemCount():
            report["row_status"] = window.file_tree.topLevelItem(0).text(3)
        preview = window.preview.toPlainText()
        report["conversion_succeeded"] = report.get("row_status") == "Converted"
        report["local_analysis_rendered"] = (
            "# Local document intelligence" in preview
        )
        report["preview_characters"] = len(preview)
    finally:
        window.close()

    passed = all(
        report[key]
        for key in (
            "model_option_enabled",
            "conversion_succeeded",
            "local_analysis_rendered",
        )
    ) and not report.get("timed_out", False)
    report["passed"] = passed
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    print(arguments.output.resolve())
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
