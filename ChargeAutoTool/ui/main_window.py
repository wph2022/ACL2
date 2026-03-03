from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from .widgets import PlotView, ResultView, SegmentedButton, Toolbar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChargeAutoTool")
        self.resize(1080, 720)

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        self.mode_selector = SegmentedButton([
            "日志搜索", "healthd解析", "vbat解析", "曲线生成", "AI协议分析", "寄存器分析"
        ])
        self.toolbar = Toolbar()
        self.result_view = ResultView()
        self.plot_view = PlotView()

        layout.addWidget(self.mode_selector)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.result_view)
        layout.addWidget(self.plot_view)
