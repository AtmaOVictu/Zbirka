from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QLineEdit, QPushButton, QTabWidget,
                              QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal
from comprehension.core.processing_pipeline import ProcessingPipeline
from comprehension.core.symbol_mapper import SymbolMapper
from .r7_progress import R7ProgressWidget
from .module_window import ModuleWindow
from .knowledge_renderer import KnowledgeRenderer


class PipelineWorker(QThread):
    phase_completed = pyqtSignal(str, str, dict)
    pipeline_done = pyqtSignal(object)
    pipeline_error = pyqtSignal(str)

    def __init__(self, pipeline, statement):
        super().__init__()
        self.pipeline = pipeline
        self.statement = statement

    def run(self):
        try:
            result = self.pipeline.process(self.statement)
            for phase, output in result.phases.items():
                self.phase_completed.emit(phase, output.module_name, {
                    "data": output.data,
                    "kpi": output.kpi,
                    "status": output.status,
                    "duration_ms": output.duration_ms,
                })
            self.pipeline_done.emit(result)
        except Exception as e:
            self.pipeline_error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TAZV Comprehension Machine")
        self.resize(900, 600)
        self.pipeline = ProcessingPipeline()
        self.mapper = SymbolMapper()
        self.worker = None

        ss = (
            "QMainWindow{background:#1a1a1a;color:#c0c0c0;}"
            "QWidget{background:#1a1a1a;color:#c0c0c0;}"
            "QLineEdit{background:#2a2a2a;color:#c0ffc0;border:1px solid #404040;padding:4px;}"
            "QPushButton{background:#2a4a2a;color:#c0ffc0;border:1px solid #40a040;padding:6px 16px;}"
            "QPushButton:hover{background:#3a5a3a;}"
            "QPushButton:disabled{background:#2a2a2a;color:#606060;}"
            "QTextEdit{background:#0a0a0a;color:#c0ffc0;border:1px solid #303030;}"
            "QTabWidget::pane{border:1px solid #303030;}"
            "QTabBar::tab{background:#1a1a1a;color:#808080;padding:8px 16px;border:1px solid #303030;}"
            "QTabBar::tab:selected{background:#2a4a2a;color:#c0ffc0;}"
            "QStatusBar{background:#0a0a0a;color:#808080;}"
            "QMenuBar{background:#1a1a1a;color:#c0c0c0;}"
            "QMenuBar::item:selected{background:#2a4a2a;}"
            "QLabel{color:#c0c0c0;}"
        )
        self.setStyleSheet(ss)

        central = QWidget()
        layout = QVBoxLayout(central)

        row = QHBoxLayout()
        row.addWidget(QLabel("Statement:"))
        self.input = QLineEdit()
        self.input.returnPressed.connect(self.process_statement)
        row.addWidget(self.input)
        self.btn = QPushButton("Process")
        self.btn.clicked.connect(self.process_statement)
        row.addWidget(self.btn)
        layout.addLayout(row)

        self.tabs = QTabWidget()
        self.modules = {}
        for item in self.mapper.get_r7_symbols():
            mw = ModuleWindow(item["system"], item["module"])
            self.modules[item["system"]] = mw
            label = item["system"] + " " + item["module"]
            self.tabs.addTab(mw, label)
        self.tabs.addTab(KnowledgeRenderer(), "Index")
        layout.addWidget(self.tabs)

        self.setCentralWidget(central)

        self.progress = R7ProgressWidget()
        self.statusBar().addWidget(self.progress)
        self.statusBar().showMessage("Ready")

        m = self.menuBar()
        fm = m.addMenu("File")
        fm.addAction("Clear", self.clear_all)
        fm.addAction("Exit", self.close)

    def process_statement(self):
        text = self.input.text().strip()
        if not text:
            QMessageBox.warning(self, "Empty", "Enter a statement.")
            return
        self.btn.setEnabled(False)
        self.progress.reset()
        for mw in self.modules.values():
            mw.clear()
        self.statusBar().showMessage("Processing...")
        self.worker = PipelineWorker(self.pipeline, text)
        self.worker.phase_completed.connect(self.on_phase)
        self.worker.pipeline_done.connect(self.on_done)
        self.worker.pipeline_error.connect(self.on_error)
        self.worker.start()

    def on_phase(self, phase, module, data):
        idx = self.mapper.R7_ORDER.index(phase) if phase in self.mapper.R7_ORDER else -1
        self.progress.set_phase(idx)
        if phase in self.modules:
            self.modules[phase].display(data)
        status = data.get("status", "?")
        msg = f"{phase} ({module}): {status}"
        self.statusBar().showMessage(msg)

    def on_done(self, result):
        self.btn.setEnabled(True)
        errors = len(result.all_errors)
        msg = f"Done: {result.status} | {result.total_duration_ms:.1f}ms | {errors} errors"
        self.statusBar().showMessage(msg)

    def on_error(self, msg):
        self.btn.setEnabled(True)
        self.statusBar().showMessage(f"Error: {msg}")
        QMessageBox.critical(self, "Error", msg)

    def clear_all(self):
        self.input.clear()
        for mw in self.modules.values():
            mw.clear()
        self.progress.reset()
        self.statusBar().showMessage("Ready")
