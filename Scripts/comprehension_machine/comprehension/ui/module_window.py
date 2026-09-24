import json
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtGui import QFont


class ModuleWindow(QWidget):
    def __init__(self, phase, module_name, parent=None):
        super().__init__(parent)
        self.phase = phase
        self.module_name = module_name
        layout = QVBoxLayout(self)
        title = QLabel(f"{phase} \u2014 {module_name}")
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #c0ffc0;")
        layout.addWidget(title)
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setFont(QFont("Consolas", 10))
        layout.addWidget(self.results)

    def display(self, data):
        text = json.dumps(data, indent=2, ensure_ascii=False)
        self.results.setPlainText(text)

    def clear(self):
        self.results.clear()
