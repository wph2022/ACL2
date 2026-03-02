import sys

from PySide6.QtWidgets import QApplication

from .app_controller import AppController
from .ui.main_window import MainWindow
from .ui.styles import APP_QSS


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyleSheet(APP_QSS)
    window = MainWindow()
    AppController(window)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
