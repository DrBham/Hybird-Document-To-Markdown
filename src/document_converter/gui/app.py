"""Application entry point for the PySide6 desktop interface."""

import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .main_window import MainWindow
from .theme import APP_LOGO_PATH


def main() -> int:
    """Create and run the desktop application."""

    app = QApplication.instance() or QApplication(sys.argv)
    app.setApplicationName("Hybrid Document to Markdown")
    app.setOrganizationName("DrBham")
    if APP_LOGO_PATH.exists():
        app.setWindowIcon(QIcon(str(APP_LOGO_PATH)))

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
