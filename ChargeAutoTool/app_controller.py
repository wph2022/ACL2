import json

from PySide6.QtWidgets import QFileDialog

from .app_state import AppState
from .features import FeatureFacade
from .services import AdbService, LogIO, RuleManager, TaskRunner
from .ui.main_window import MainWindow


class AppController:
    def __init__(self, window: MainWindow):
        self.window = window
        self.state = AppState()
        self.adb = AdbService()
        self.io = LogIO()
        self.rules = RuleManager("ChargeAutoTool/rules/rules.json")
        self.tasks = TaskRunner()
        self.features = FeatureFacade(self.rules.rules)
        self._connect_signals()

    def _connect_signals(self) -> None:
        self.window.toolbar.open_button.clicked.connect(self.open_log_file)
        self.window.toolbar.run_button.clicked.connect(self.run_current_mode)

    def open_log_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self.window, "选择日志文件", "", "Log Files (*.log *.txt)")
        if not file_path:
            return
        self.state.selected_file = file_path
        self.state.status_message = f"Loaded: {file_path}"
        self.window.statusBar().showMessage(self.state.status_message)

    def run_current_mode(self) -> None:
        if not self.state.selected_file:
            self.window.result_view.set_result("请先选择日志文件")
            return

        text = self.io.read_file(self.state.selected_file)
        mode_index = next((i for i, b in enumerate(self.window.mode_selector.buttons) if b.isChecked()), 0)

        if mode_index == 0:
            result = self.features.search_log(text, "error")
        elif mode_index == 1:
            result = self.features.parse_healthd(text)
        elif mode_index == 2:
            result = self.features.parse_vbat(text)
        elif mode_index == 3:
            points = self.features.generate_curve_points(text)
            self.window.plot_view.show_points(points)
            result = {"curve_points": len(points)}
        elif mode_index == 4:
            result = self.features.analyze_ai_protocol(text)
        else:
            result = self.features.analyze_register_dump(text)

        self.state.parse_result = result if isinstance(result, dict) else {"lines": result[:100]}
        self.window.result_view.set_result(json.dumps(self.state.parse_result, ensure_ascii=False, indent=2))
