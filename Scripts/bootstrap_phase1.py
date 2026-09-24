"""
TAZV Comprehension Machine - Phase 1 Bootstrap (PyQt6 UI)
=========================================================
Run this from the SAME directory as the Phase 0 bootstrap.
It adds the UI files to the existing comprehension_machine/ folder.

After it runs:
    pip install PyQt6
    cd comprehension_machine
    python main.py
"""

import sys
from pathlib import Path

ROOT = Path("comprehension_machine")

FILES = {}

FILES["main.py"] = (
    'import sys\n'
    'from PyQt6.QtWidgets import QApplication\n'
    'from comprehension.ui.main_window import MainWindow\n\n\n'
    'def main():\n'
    '    app = QApplication(sys.argv)\n'
    '    window = MainWindow()\n'
    '    window.show()\n'
    '    sys.exit(app.exec())\n\n\n'
    'if __name__ == "__main__":\n'
    '    main()\n'
)

FILES["comprehension/ui/r7_progress.py"] = (
    'from PyQt6.QtWidgets import QWidget\n'
    'from PyQt6.QtGui import QPainter, QColor, QFont\n'
    'from PyQt6.QtCore import Qt\n\n\n'
    'class R7ProgressWidget(QWidget):\n'
    '    def __init__(self, parent=None):\n'
    '        super().__init__(parent)\n'
    '        self.phases = ["\\u2205", "\\u00ac", "\\u2206", "1", "\\u29d6", "\\u222e", "\\u27e1"]\n'
    '        self.names = ["BIOS", "STATE", "UAF", "JEWIK", "APD", "MICRO", "VIS"]\n'
    '        self.current = -1\n'
    '        self.setFixedHeight(36)\n'
    '        self.setMinimumWidth(300)\n\n'
    '    def set_phase(self, idx):\n'
    '        self.current = idx\n'
    '        self.update()\n\n'
    '    def reset(self):\n'
    '        self.current = -1\n'
    '        self.update()\n\n'
    '    def paintEvent(self, event):\n'
    '        p = QPainter(self)\n'
    '        p.setRenderHint(QPainter.RenderHint.Antialiasing)\n'
    '        sw = self.width() / 7\n'
    '        h = self.height()\n'
    '        p.setFont(QFont("Segoe UI", 9))\n'
    '        for i in range(7):\n'
    '            x = int(i * sw)\n'
    '            w = int(sw) - 4\n'
    '            if i == self.current:\n'
    '                c = QColor(64, 200, 64)\n'
    '                t = QColor(20, 20, 20)\n'
    '            elif i < self.current:\n'
    '                c = QColor(40, 100, 40)\n'
    '                t = QColor(180, 180, 180)\n'
    '            else:\n'
    '                c = QColor(30, 30, 30)\n'
    '                t = QColor(80, 80, 80)\n'
    '            p.fillRect(x + 2, 2, w, h - 4, c)\n'
    '            p.setPen(t)\n'
    '            p.drawText(x + 2, 2, w, h - 4, Qt.AlignmentFlag.AlignCenter, self.phases[i])\n'
)

FILES["comprehension/ui/module_window.py"] = (
    'import json\n'
    'from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit\n'
    'from PyQt6.QtGui import QFont\n\n\n'
    'class ModuleWindow(QWidget):\n'
    '    def __init__(self, phase, module_name, parent=None):\n'
    '        super().__init__(parent)\n'
    '        self.phase = phase\n'
    '        self.module_name = module_name\n'
    '        layout = QVBoxLayout(self)\n'
    '        title = QLabel(f"{phase} \\u2014 {module_name}")\n'
    '        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #c0ffc0;")\n'
    '        layout.addWidget(title)\n'
    '        self.results = QTextEdit()\n'
    '        self.results.setReadOnly(True)\n'
    '        self.results.setFont(QFont("Consolas", 10))\n'
    '        layout.addWidget(self.results)\n\n'
    '    def display(self, data):\n'
    '        text = json.dumps(data, indent=2, ensure_ascii=False)\n'
    '        self.results.setPlainText(text)\n\n'
    '    def clear(self):\n'
    '        self.results.clear()\n'
)

FILES["comprehension/ui/main_window.py"] = (
    'from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,\n'
    '                              QLabel, QLineEdit, QPushButton, QTabWidget,\n'
    '                              QMessageBox)\n'
    'from PyQt6.QtCore import QThread, pyqtSignal\n'
    'from comprehension.core.processing_pipeline import ProcessingPipeline\n'
    'from comprehension.core.symbol_mapper import SymbolMapper\n'
    'from .r7_progress import R7ProgressWidget\n'
    'from .module_window import ModuleWindow\n\n\n'
    'class PipelineWorker(QThread):\n'
    '    phase_completed = pyqtSignal(str, str, dict)\n'
    '    pipeline_done = pyqtSignal(object)\n'
    '    pipeline_error = pyqtSignal(str)\n\n'
    '    def __init__(self, pipeline, statement):\n'
    '        super().__init__()\n'
    '        self.pipeline = pipeline\n'
    '        self.statement = statement\n\n'
    '    def run(self):\n'
    '        try:\n'
    '            result = self.pipeline.process(self.statement)\n'
    '            for phase, output in result.phases.items():\n'
    '                self.phase_completed.emit(phase, output.module_name, {\n'
    '                    "data": output.data,\n'
    '                    "kpi": output.kpi,\n'
    '                    "status": output.status,\n'
    '                    "duration_ms": output.duration_ms,\n'
    '                })\n'
    '            self.pipeline_done.emit(result)\n'
    '        except Exception as e:\n'
    '            self.pipeline_error.emit(str(e))\n\n\n'
    'class MainWindow(QMainWindow):\n'
    '    def __init__(self):\n'
    '        super().__init__()\n'
    '        self.setWindowTitle("TAZV Comprehension Machine")\n'
    '        self.resize(900, 600)\n'
    '        self.pipeline = ProcessingPipeline()\n'
    '        self.mapper = SymbolMapper()\n'
    '        self.worker = None\n\n'
    '        ss = (\n'
    '            "QMainWindow{background:#1a1a1a;color:#c0c0c0;}"\n'
    '            "QWidget{background:#1a1a1a;color:#c0c0c0;}"\n'
    '            "QLineEdit{background:#2a2a2a;color:#c0ffc0;border:1px solid #404040;padding:4px;}"\n'
    '            "QPushButton{background:#2a4a2a;color:#c0ffc0;border:1px solid #40a040;padding:6px 16px;}"\n'
    '            "QPushButton:hover{background:#3a5a3a;}"\n'
    '            "QPushButton:disabled{background:#2a2a2a;color:#606060;}"\n'
    '            "QTextEdit{background:#0a0a0a;color:#c0ffc0;border:1px solid #303030;}"\n'
    '            "QTabWidget::pane{border:1px solid #303030;}"\n'
    '            "QTabBar::tab{background:#1a1a1a;color:#808080;padding:8px 16px;border:1px solid #303030;}"\n'
    '            "QTabBar::tab:selected{background:#2a4a2a;color:#c0ffc0;}"\n'
    '            "QStatusBar{background:#0a0a0a;color:#808080;}"\n'
    '            "QMenuBar{background:#1a1a1a;color:#c0c0c0;}"\n'
    '            "QMenuBar::item:selected{background:#2a4a2a;}"\n'
    '            "QLabel{color:#c0c0c0;}"\n'
    '        )\n'
    '        self.setStyleSheet(ss)\n\n'
    '        central = QWidget()\n'
    '        layout = QVBoxLayout(central)\n\n'
    '        row = QHBoxLayout()\n'
    '        row.addWidget(QLabel("Statement:"))\n'
    '        self.input = QLineEdit()\n'
    '        self.input.returnPressed.connect(self.process_statement)\n'
    '        row.addWidget(self.input)\n'
    '        self.btn = QPushButton("Process")\n'
    '        self.btn.clicked.connect(self.process_statement)\n'
    '        row.addWidget(self.btn)\n'
    '        layout.addLayout(row)\n\n'
    '        self.tabs = QTabWidget()\n'
    '        self.modules = {}\n'
    '        for item in self.mapper.get_r7_symbols():\n'
    '            mw = ModuleWindow(item["system"], item["module"])\n'
    '            self.modules[item["system"]] = mw\n'
    '            label = item["system"] + " " + item["module"]\n'
    '            self.tabs.addTab(mw, label)\n'
    '        layout.addWidget(self.tabs)\n\n'
    '        self.setCentralWidget(central)\n\n'
    '        self.progress = R7ProgressWidget()\n'
    '        self.statusBar().addWidget(self.progress)\n'
    '        self.statusBar().showMessage("Ready")\n\n'
    '        m = self.menuBar()\n'
    '        fm = m.addMenu("File")\n'
    '        fm.addAction("Clear", self.clear_all)\n'
    '        fm.addAction("Exit", self.close)\n\n'
    '    def process_statement(self):\n'
    '        text = self.input.text().strip()\n'
    '        if not text:\n'
    '            QMessageBox.warning(self, "Empty", "Enter a statement.")\n'
    '            return\n'
    '        self.btn.setEnabled(False)\n'
    '        self.progress.reset()\n'
    '        for mw in self.modules.values():\n'
    '            mw.clear()\n'
    '        self.statusBar().showMessage("Processing...")\n'
    '        self.worker = PipelineWorker(self.pipeline, text)\n'
    '        self.worker.phase_completed.connect(self.on_phase)\n'
    '        self.worker.pipeline_done.connect(self.on_done)\n'
    '        self.worker.pipeline_error.connect(self.on_error)\n'
    '        self.worker.start()\n\n'
    '    def on_phase(self, phase, module, data):\n'
    '        idx = self.mapper.R7_ORDER.index(phase) if phase in self.mapper.R7_ORDER else -1\n'
    '        self.progress.set_phase(idx)\n'
    '        if phase in self.modules:\n'
    '            self.modules[phase].display(data)\n'
    '        status = data.get("status", "?")\n'
    '        msg = f"{phase} ({module}): {status}"\n'
    '        self.statusBar().showMessage(msg)\n\n'
    '    def on_done(self, result):\n'
    '        self.btn.setEnabled(True)\n'
    '        errors = len(result.all_errors)\n'
    '        msg = f"Done: {result.status} | {result.total_duration_ms:.1f}ms | {errors} errors"\n'
    '        self.statusBar().showMessage(msg)\n\n'
    '    def on_error(self, msg):\n'
    '        self.btn.setEnabled(True)\n'
    '        self.statusBar().showMessage(f"Error: {msg}")\n'
    '        QMessageBox.critical(self, "Error", msg)\n\n'
    '    def clear_all(self):\n'
    '        self.input.clear()\n'
    '        for mw in self.modules.values():\n'
    '            mw.clear()\n'
    '        self.progress.reset()\n'
    '        self.statusBar().showMessage("Ready")\n'
)


def main():
    if not (ROOT / "comprehension" / "core" / "processing_pipeline.py").exists():
        print("ERROR: Phase 0 not found. Run bootstrap_tazv.py first.")
        sys.exit(1)

    print("TAZV Comprehension Machine - Phase 1 Bootstrap (PyQt6 UI)")
    print("=" * 55)

    for relpath, content in FILES.items():
        path = ROOT / relpath
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"  file {relpath}  ({len(content)} bytes)")

    print(f"\nDONE: {len(FILES)} files added to {ROOT}/")
    print("\nNext:")
    print("  pip install PyQt6")
    print("  cd comprehension_machine")
    print("  python main.py")


if __name__ == "__main__":
    main()