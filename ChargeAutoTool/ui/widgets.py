from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget


class Card(QFrame):
    def __init__(self, title: str, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(title))


class Toolbar(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.open_button = QPushButton("打开日志")
        self.run_button = QPushButton("执行")
        layout.addWidget(self.open_button)
        layout.addWidget(self.run_button)


class ResultView(QTextEdit):
    def set_result(self, text: str):
        self.setPlainText(text)


class PlotView(QTextEdit):
    def show_points(self, points: list[tuple[int, int]]):
        self.setPlainText("\n".join(f"{x},{y}" for x, y in points))


class SegmentedButton(QWidget):
    def __init__(self, labels: list[str], parent: QWidget | None = None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self.buttons = [QPushButton(label) for label in labels]
        for b in self.buttons:
            b.setCheckable(True)
            layout.addWidget(b)
        if self.buttons:
            self.buttons[0].setChecked(True)
