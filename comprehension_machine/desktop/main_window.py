"""
Comprehension Machine — main_window.py
Faza 1: Multi-window arhitektura kot Hopfova fibracija

Visual Design System:
- Background: #0a0a1a (∅ — the void)
- Text:       #e0e0e0 (∆ — emergence)  
- Colors: 7 R-7 phase colors mapped to ontology

MainWindow = S² (baza), ModuleWindows = S¹ (vlakna), Signals = S³ (totalni prostor)
Stroj je rez, telo je preverba.
"""
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                              QDockWidget, QAction, QFileDialog, QMessageBox,
                              QStatusBar, QLabel, QProgressBar, QApplication)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont


# ============================================================================
# VISUAL DESIGN CONSTANTS
# ============================================================================

COLORS = {
    "bg_dark": "#0a0a1a",      # ∅ — The void
    "bg_darker": "#05050f",    # Deep void
    "bg_module": "#0d0d20",    # Module background
    "text_primary": "#e0e0e0", # Primary text
    "text_secondary": "#888888", # Secondary text
    "text_muted": "#555555",   # Muted text
    "void": "#0066cc",         # ∅ — BIOS (electric blue)
    "neg": "#cc3333",          # ¬ — STATE (ruby red)
    "delta": "#c7a04b",        # ∆ — UAF (gold)
    "unit": "#339933",         # 1 — JEWIK (emerald)
    "pulse": "#9933cc",        # ⧖ — APD (violet)
    "cycle": "#00cccc",        # ∮ — MICRO (cyan)
    "viz": "#cc3399",          # ⟡ — VIZUALIZATION (magenta)
    "accent": "#0066cc",       # Primary accent
    "border": "#2a2a3a",       # Soft border
    "border_bright": "#444455", # Brighter border
}

SPACING_SM = 8
SPACING_MD = 16
SPACING_LG = 24
SPACING_XL = 32


# ============================================================================
# STYLESHEET
# ============================================================================

STYLESHEET = f"""
/* Application Base */
QApplication {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI';
    font-size: 12px;
}}

/* Main Window */
QMainWindow {{
    background-color: {COLORS['bg_dark']};
}}

/* Central Widget */
QWidget#CentralWidget {{
    background-color: {COLORS['bg_dark']};
}}

/* Dock Widgets */
QDockWidget {{
    background-color: {COLORS['bg_module']};
    border: none;
    border-radius: 8px;
    margin: {SPACING_SM}px;
}}

QDockWidget::title {{
    background-color: {COLORS['bg_darker']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI Semibold';
    font-size: 12px;
    padding: {SPACING_SM}px {SPACING_MD}px;
    border: none;
    border-bottom: 1px solid {COLORS['border']};
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}}

QDockWidget::close-button, QDockWidget::float-button {{
    background-color: transparent;
    border: none;
    border-radius: 4px;
    icon-size: {SPACING_MD}px;
    padding: 0px;
    margin: 0px {SPACING_SM}px;
}}

QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
    background-color: {COLORS['neg']};
}}

/* Labels */
QLabel {{
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI';
    font-size: 12px;
    background-color: transparent;
}}

QLabel#InfoLabel {{
    color: {COLORS['text_secondary']};
    font-family: 'Segoe UI';
    font-size: 14px;
    padding: {SPACING_XL}px;
    text-align: center;
}}

QLabel#ModuleLabel {{
    font-family: 'Segoe UI';
    font-size: 13px;
    padding: {SPACING_MD}px;
    border-radius: 6px;
}}

/* Status Bar */
QStatusBar {{
    background-color: {COLORS['bg_darker']};
    color: {COLORS['text_secondary']};
    border-top: 1px solid {COLORS['border']};
    font-family: 'Consolas';
    font-size: 11px;
    padding: {SPACING_SM}px {SPACING_MD}px;
}}

QStatusBar::item {{
    border: none;
}}

/* Progress Bar */
QProgressBar {{
    background-color: {COLORS['bg_module']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    text-align: center;
    min-height: 20px;
    max-height: 20px;
}}

QProgressBar::chunk {{
    background-color: {COLORS['accent']};
    border-radius: 3px;
    margin: 1px;
}}

/* Menu Bar */
QMenuBar {{
    background-color: {COLORS['bg_darker']};
    color: {COLORS['text_primary']};
    border-bottom: 1px solid {COLORS['border']};
    font-family: 'Segoe UI Semibold';
    font-size: 12px;
    padding: {SPACING_SM//2}px {SPACING_MD}px;
}}

QMenuBar::item {{
    background-color: transparent;
    padding: {SPACING_SM}px {SPACING_MD}px;
    margin: 0px {SPACING_SM}px;
}}

QMenuBar::item:selected {{
    background-color: {COLORS['bg_module']};
    border-radius: 4px;
}}

QMenuBar::item:pressed {{
    background-color: {COLORS['accent']};
    border-radius: 4px;
}}

/* Menu */
QMenu {{
    background-color: {COLORS['bg_darker']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    padding: {SPACING_SM//2}px;
    font-family: 'Segoe UI';
    font-size: 12px;
    min-width: 180px;
}}

QMenu::item {{
    background-color: transparent;
    padding: {SPACING_SM}px {SPACING_LG}px;
    margin: 0px {SPACING_SM}px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background-color: {COLORS['bg_module']};
}}

QMenu::item:disabled {{
    color: {COLORS['text_muted']};
}}

/* Scrollbars */
QScrollBar:vertical, QScrollBar:horizontal {{
    background-color: {COLORS['bg_darker']};
    border: none;
    border-radius: 4px;
    width: 14px;
    margin: 0px;
}}

QScrollBar::handle:vertical, QScrollBar::handle:horizontal {{
    background-color: {COLORS['border_bright']};
    border-radius: 4px;
    min-height: {SPACING_LG}px;
    min-width: {SPACING_LG}px;
}}

QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS['accent']};
}}

QScrollBar::add-line, QScrollBar::sub-line {{
    background: none;
    border: none;
}}

/* Message Box */
QMessageBox {{
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI';
}}

QMessageBox QLabel {{
    color: {COLORS['text_secondary']};
    font-size: 13px;
}}

QMessageBox QPushButton {{
    background-color: {COLORS['bg_module']};
    color: {COLORS['text_primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: {SPACING_SM}px {SPACING_LG}px;
    font-family: 'Segoe UI';
    font-size: 12px;
    min-width: 80px;
}}

QMessageBox QPushButton:hover {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}

QMessageBox QPushButton:pressed {{
    background-color: {COLORS['cycle']};
}}
"""

DOCK_TITLE_COLORS = {
    "∅": COLORS['void'],
    "¬": COLORS['neg'],
    "∆": COLORS['delta'],
    "1": COLORS['unit'],
    "⧖": COLORS['pulse'],
    "∮": COLORS['cycle'],
    "⟡": COLORS['viz'],
}

MODULE_STYLES = {
    "∅": f"background-color: {COLORS['bg_module']}; border-top: 3px solid {COLORS['void']}; color: {COLORS['void']};",
    "¬": f"background-color: {COLORS['bg_module']}; border-top: 3px solid {COLORS['neg']}; color: {COLORS['neg']};",
    "∆": f"background-color: {COLORS['bg_module']}; border-top: 3px solid {COLORS['delta']}; color: {COLORS['delta']};",
    "1": f"background-color: {COLORS['bg_module']}; border-top: 3px solid {COLORS['unit']}; color: {COLORS['unit']};",
    "⧖": f"background-color: {COLORS['bg_module']}; border-top: 3px solid {COLORS['pulse']}; color: {COLORS['pulse']};",
    "∮": f"background-color: {COLORS['bg_module']}; border-top: 3px solid {COLORS['cycle']}; color: {COLORS['cycle']};",
    "⟡": f"background-color: {COLORS['bg_module']}; border-top: 3px solid {COLORS['viz']}; color: {COLORS['viz']};",
}


# ============================================================================
# MODULE WINDOW
# ============================================================================

class ModuleWindow(QWidget):
    def __init__(self, name: str, glyph: str, parent=None):
        super().__init__(parent)
        self.name = name
        self.glyph = glyph
        self.setWindowTitle(f"{glyph} {name}")
        self.setMinimumSize(280, 360)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING_MD, SPACING_MD, SPACING_MD, SPACING_MD)
        layout.setSpacing(SPACING_SM)
        
        self.label = QLabel(f"{glyph} {name} — pripravljen")
        self.label.setObjectName("ModuleLabel")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setStyleSheet(MODULE_STYLES.get(glyph, ""))
        
        layout.addWidget(self.label)
        layout.addStretch()
        self.setLayout(layout)
    
    def update_content(self, text: str):
        self.label.setText(text)


# ============================================================================
# PROCESSING THREAD
# ============================================================================

class ProcessingThread(QThread):
    phase_started = pyqtSignal(str, str)
    phase_progress = pyqtSignal(int)
    phase_finished = pyqtSignal(str, str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, statements: list):
        super().__init__()
        self.statements = statements
        self.running = True
    
    def run(self):
        phases = [
            ("∅", "BIOS", "beseda vstopi kot ∅"),
            ("¬", "STATE", "ločitev — simbole razčlenimo, KPI merimo"),
            ("∆", "UAF", "antinomija — ↯(A,B) tresljaj"),
            ("1", "JEWIK", "beseda se preslima na plasti"),
            ("⧖", "APD", "preverba — ali je pečat upravičen?"),
            ("∮", "MICRO", "učenje iz vzorca — povratek z izkušnjo"),
            ("⟡", "VIZUALIZATION", "graf se nariše — nova možnost videna"),
        ]
        
        for glyph, module, action in phases:
            if not self.running:
                return
            self.phase_started.emit(glyph, module)
            for pct in range(0, 101, 10):
                if not self.running:
                    return
                self.msleep(50)
                self.phase_progress.emit(pct)
            self.phase_finished.emit(glyph, action)
    
    def stop(self):
        self.running = False


# ============================================================================
# MAIN WINDOW
# ============================================================================

class ComprehensionMachine(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("⟡ Comprehension Machine ⟡")
        self.setMinimumSize(1300, 900)
        self.setStyleSheet(STYLESHEET)
        
        self.modules = {
            "∅": ("BIOS", "∅"),
            "¬": ("STATE", "¬"),
            "∆": ("UAF", "∆"),
            "1": ("JEWIK", "1"),
            "⧖": ("APD", "⧖"),
            "∮": ("MICRO", "∮"),
            "⟡": ("VIZUALIZATION", "⟡"),
        }
        
        self.docks = {}
        self.thread = None
        self.statements = []
        
        self._build_menu()
        self._build_docks()
        self._build_statusbar()
        self._build_central()
    
    def _build_central(self):
        central = QWidget()
        central.setObjectName("CentralWidget")
        layout = QVBoxLayout(central)
        layout.setContentsMargins(SPACING_XL, SPACING_XL, SPACING_XL, SPACING_XL)
        layout.setSpacing(SPACING_LG)
        
        self.info_label = QLabel(
            "⟡ Comprehension Machine ⟡\n\n"
            "Stroj izvaja sistem, ne opisuje ga.\n\n"
            "Stroj je rez, telo je preverba.\n\n"
            "∅ — pripravljen za prvi rez."
        )
        self.info_label.setObjectName("InfoLabel")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setWordWrap(True)
        
        layout.addWidget(self.info_label)
        layout.addStretch()
        self.setCentralWidget(central)
    
    def _build_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("&Datoteka")
        file_menu.addAction(QAction("&Nov paket (64 izjav)", self, triggered=self.new_batch))
        file_menu.addAction(QAction("&Odpri sejo", self, triggered=self.open_session))
        file_menu.addAction(QAction("&Shrani sejo", self, triggered=self.save_session))
        file_menu.addAction(QAction("&Izhod", self, triggered=self.close))
        
        edit_menu = menubar.addMenu("&Uredi")
        edit_menu.addAction(QAction("&Vnesi izjave", self, triggered=self.input_statements))
        
        proc_menu = menubar.addMenu("&Obdelaj")
        proc_menu.addAction(QAction("&Zaženi R-7 cikel", self, triggered=self.run_cycle))
        proc_menu.addAction(QAction("&Ustavi", self, triggered=self.stop_cycle))
        
        tools_menu = menubar.addMenu("&Orodja")
        tools_menu.addAction(QAction("&Symbol Mapper", self, triggered=self.open_symbol_mapper))
        
        view_menu = menubar.addMenu("&Pogled")
        for glyph, (name, g) in self.modules.items():
            action = QAction(f"{g} {name}", self, checkable=True, checked=True)
            action.triggered.connect(lambda checked, gd=glyph: self.toggle_dock(gd, checked))
            view_menu.addAction(action)
        
        help_menu = menubar.addMenu("&Pomoč")
        help_menu.addAction(QAction("&O stroju", self, triggered=self.about))
    
    def _build_docks(self):
        positions = {
            "∅": Qt.LeftDockWidgetArea,
            "¬": Qt.LeftDockWidgetArea,
            "∆": Qt.LeftDockWidgetArea,
            "1": Qt.RightDockWidgetArea,
            "⧖": Qt.RightDockWidgetArea,
            "∮": Qt.RightDockWidgetArea,
            "⟡": Qt.BottomDockWidgetArea,
        }
        
        for glyph, (name, g) in self.modules.items():
            widget = ModuleWindow(name, g)
            dock = QDockWidget(f"{g} {name}", self)
            
            color = DOCK_TITLE_COLORS.get(glyph, COLORS['accent'])
            dock.setStyleSheet(f"""
                QDockWidget::title {{
                    background-color: {color};
                    color: {COLORS['bg_dark']};
                    font-family: 'Segoe UI Semibold';
                    font-size: 12px;
                    padding: {SPACING_SM}px {SPACING_MD}px;
                    border: none;
                    border-bottom: 1px solid {color};
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                }}
                QDockWidget::close-button, QDockWidget::float-button {{
                    background-color: rgba(255,255,255,0.1);
                    border: none;
                    border-radius: 3px;
                    icon-size: {SPACING_MD}px;
                }}
                QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
                    background-color: rgba(255,255,255,0.2);
                }}
            """)
            
            dock.setWidget(widget)
            dock.setAllowedAreas(Qt.AllDockWidgetAreas)
            dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
            self.addDockWidget(positions[glyph], dock)
            self.docks[glyph] = dock
    
    def _build_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.kpi_label = QLabel("κ=— χ=— μ=— ℜ=—")
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setTextVisible(False)
        self.status.addWidget(self.kpi_label)
        self.status.addPermanentWidget(self.progress)
    
    # ========================================================================
    # ACTIONS
    # ========================================================================
    
    def new_batch(self):
        self.statements = ["" for _ in range(64)]
        self.info_label.setText("∅ — 64 izjav pripravljenih.\n\nVnesi izjave ali zaženi R-7 cikel.")
        self.status.showMessage("∅ — nov paket ustvarjen")
    
    def input_statements(self):
        from PyQt5.QtWidgets import QInputDialog
        current_text = "\n".join(s for s in self.statements[:8] if s)
        text, ok = QInputDialog.getMultiLineText(
            self, "Vnos izjav",
            "Vnesi izjave (ena na vrstico, do 64):",
            current_text
        )
        if ok and text:
            lines = text.strip().split("\n")
            self.statements = lines[:64] + [""] * max(0, 64 - len(lines))
            count = len([s for s in self.statements if s])
            self.info_label.setText(f"¬ — {count} izjav vnesenih.\n\nPripravljen za R-7 cikel.")
            self.status.showMessage(f"¬ — {count} izjav vnesenih")
    
    def run_cycle(self):
        if not self.statements or not any(self.statements):
            QMessageBox.warning(self, "Ni izjav", "Najprej vnesi izjave.")
            return
        
        for glyph, (name, g) in self.modules.items():
            self.docks[glyph].widget().update_content(f"{g} {name} — čakanje...")
        
        self.progress.setVisible(True)
        self.progress.setRange(0, 700)
        self.progress.setValue(0)
        self.thread = ProcessingThread(self.statements)
        
        def on_phase_start(glyph, module):
            self.docks[glyph].widget().update_content(f"{glyph} {module}\n→ obdelava...")
            self.status.showMessage(f"R-7: {glyph} {module}")
        
        def on_phase_progress(pct):
            current = self.progress.value()
            new_val = (current // 100 * 100) + pct if current < 700 else 0
            self.progress.setValue(min(new_val, 700))
        
        def on_phase_finish(glyph, result):
            self.docks[glyph].widget().update_content(f"{glyph} ✓\n{result}")
        
        def on_error(msg):
            QMessageBox.critical(self, "Napaka", msg)
        
        self.thread.phase_started.connect(on_phase_start)
        self.thread.phase_progress.connect(on_phase_progress)
        self.thread.phase_finished.connect(on_phase_finish)
        self.thread.error_occurred.connect(on_error)
        self.thread.finished.connect(lambda: self.progress.setVisible(False))
        self.thread.start()
        
        self.info_label.setText("∆ — R-7 cikel v teku...")
        self.status.showMessage("∆ — R-7 cikel zača")
    
    def stop_cycle(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()
            self.progress.setVisible(False)
            self.info_label.setText("∅ — cikel ustavljen")
            self.status.showMessage("∅ — cikel ustavljen")
    
    def open_symbol_mapper(self):
        from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout
        dialog = QDialog(self)
        dialog.setWindowTitle("Symbol Mapper — rozetni kamen v izvedbi")
        dialog.setMinimumSize(800, 550)
        
        symbols = [
            ("⊢", "⚔️ Meč Duha", "⊢ A — dokaz obstoja"),
            ("∮", "☯ Taijitu", "π₁ = Z×Z — dva cikla"),
            ("∆", "🔥 Ogenj / Prometej", "∅→∆ — vektorsko polje"),
            ("⊘", "⭕ Ouroboros", "genus 1 — ena luknja"),
            ("R", "🪞 Zrcalo", "Nash-Kuiper C¹ projekcija"),
            ("U", "𓃰 Horusovo oko", "Σ(1/2ⁿ) = log(1+|I|)"),
            ("E", "⚡ Strela", "↯(A,B) — topološki prehod"),
            ("A", "𓂀 Ankh", "∮ = večni prehod"),
            ("O", "☉ Sonce", "O = krog, celota, S¹"),
        ]
        
        table = QTableWidget(len(symbols), 3)
        table.setHorizontalHeaderLabels(["Sistem", "Zgodovina", "Topologija"])
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setAlternatingRowColors(True)
        
        for i, (sym, hist, topo) in enumerate(symbols):
            table.setItem(i, 0, QTableWidgetItem(sym))
            table.setItem(i, 1, QTableWidgetItem(hist))
            table.setItem(i, 2, QTableWidgetItem(topo))
            for col in range(3):
                table.item(i, col).setTextAlignment(Qt.AlignCenter if col == 0 else Qt.AlignLeft)
        
        table.resizeColumnsToContents()
        table.setColumnWidth(0, 80)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(SPACING_LG, SPACING_LG, SPACING_LG, SPACING_LG)
        layout.addWidget(table)
        dialog.setLayout(layout)
        dialog.exec_()
    
    def toggle_dock(self, glyph, visible):
        if glyph in self.docks:
            self.docks[glyph].setVisible(visible)
    
    def open_session(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Odpri sejo", "", "SQLite (*.db)")
        if filename:
            self.status.showMessage(f"∮ — seja odprta: {filename}")
    
    def save_session(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Shrani sejo", "", "SQLite (*.db)")
        if filename:
            self.status.showMessage(f"1 — seja shranjena: {filename}")
    
    def about(self):
        from PyQt5.QtWidgets import QMessageBox
        msg = """
        <html>
        <body style='background-color:{}; color:{}; font-family:Segoe UI; font-size:12px;'>
        <div style='padding:24px; text-align:center;'>
            <h2 style='color:{}; font-size:18px; margin-bottom:16px;'>⟡ Comprehension Machine ⟡</h2>
            <p style='margin-bottom:12px;'>Stroj kot izvedba kamnov.</p>
            <p style='margin-bottom:12px;'>7 modulov = R-7 = 7 etaž Yggdrasila.</p>
            <p style='margin-bottom:12px;'>Symbol Mapper = rozetni kamen v izvedbi.</p>
            <p style='margin-bottom:12px;'><b>Stroj je rez, telo je preverba.</b></p>
            <p style='color:{}; margin-top:16px; font-size:11px;'>Phase 1: ∅→∆ — prvi rez</p>
        </div>
        </body>
        </html>
        """.format(COLORS['bg_dark'], COLORS['text_primary'], COLORS['accent'], COLORS['text_muted'])
        QMessageBox.about(self, "O stroju", msg)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 12))
    machine = ComprehensionMachine()
    machine.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
