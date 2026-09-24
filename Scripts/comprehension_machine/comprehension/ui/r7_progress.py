from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import Qt


class R7ProgressWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.phases = ["\u2205", "\u00ac", "\u2206", "1", "\u29d6", "\u222e", "\u27e1"]
        self.names = ["BIOS", "STATE", "UAF", "JEWIK", "APD", "MICRO", "VIS"]
        self.current = -1
        self.setFixedHeight(36)
        self.setMinimumWidth(300)

    def set_phase(self, idx):
        self.current = idx
        self.update()

    def reset(self):
        self.current = -1
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        sw = self.width() / 7
        h = self.height()
        p.setFont(QFont("Segoe UI", 9))
        for i in range(7):
            x = int(i * sw)
            w = int(sw) - 4
            if i == self.current:
                c = QColor(64, 200, 64)
                t = QColor(20, 20, 20)
            elif i < self.current:
                c = QColor(40, 100, 40)
                t = QColor(180, 180, 180)
            else:
                c = QColor(30, 30, 30)
                t = QColor(80, 80, 80)
            p.fillRect(x + 2, 2, w, h - 4, c)
            p.setPen(t)
            p.drawText(x + 2, 2, w, h - 4, Qt.AlignmentFlag.AlignCenter, self.phases[i])
