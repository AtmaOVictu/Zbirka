#!/usr/bin/env python3
"""
TAZV Comprehension Machine - Color Patch
Updates QSS colors and module semantics to match corpus-validated R-7 mapping.

Run from D:\OntoProjekt\CanvasMinstral\Scripts:
  python patch_colors.py

Then:
  cd comprehension_machine
  python main.py
"""
import os

# ─── Corpus-validated color system ───
COLORS = {
    'desher_red':    '#B43A2E',  # STATE (¬) — cut, separation, RANA
    'khenet_yellow': '#D6A83A',  # UAF (∆) — antinomy, bridge-not-yet-bridge
    'deep_blue':     '#1B2838',  # BIOS (∅) — praznina, mir, refleksija
    'jewik_orange':  '#C77800',  # JEWIK (1) — dejanje, activation
    'gold_seal':     '#D6A83A',  # APD (⧖) — imperishable definitional force
    'kem_black':     '#080705',  # MICRO (∮) — void for rebirth, NEGATIV_888
    'hedj_white':    '#F3E9D2',  # VISUALIZATION (⟡) — new beginning, fullness
    'bg':            '#0A0A0A',  # App background
    'text':          '#E0E0E0',  # Default text
    'accent':        '#40A040',  # Green accent
}

# ─── Module → color mapping ───
MODULE_COLORS = {
    'bios':          COLORS['deep_blue'],
    'state':         COLORS['desher_red'],
    'uaf':           COLORS['khenet_yellow'],
    'jewik':         COLORS['jewik_orange'],
    'apd':           COLORS['gold_seal'],
    'micro':         COLORS['kem_black'],
    'visualization': COLORS['hedj_white'],
}

QSS = f"""
/* TAZV Comprehension Machine — Corpus-validated QSS */

QWidget {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
}}

QMainWindow {{
    background-color: {COLORS['bg']};
}}

/* Module tab colors — each phase carries its ontological color */
QTabWidget::pane {{
    border: 1px solid #333;
    background-color: #111;
}}

QTabBar::tab {{
    background-color: #1a1a1a;
    color: {COLORS['text']};
    padding: 8px 16px;
    border: 1px solid #333;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}}

QTabBar::tab:selected {{
    background-color: #222;
    font-weight: bold;
}}

/* BIOS tab — deep blue (praznina) */
QTabBar::tab:nth-child(1) {{
    color: {COLORS['deep_blue']};
    border-top: 2px solid {COLORS['deep_blue']};
}}

/* STATE tab — desher red (cut) */
QTabBar::tab:nth-child(2) {{
    color: {COLORS['desher_red']};
    border-top: 2px solid {COLORS['desher_red']};
}}

/* UAF tab — khenet yellow (antinomy) */
QTabBar::tab:nth-child(3) {{
    color: {COLORS['khenet_yellow']};
    border-top: 2px solid {COLORS['khenet_yellow']};
}}

/* JEWIK tab — orange (dejanje) */
QTabBar::tab:nth-child(4) {{
    color: {COLORS['jewik_orange']};
    border-top: 2px solid {COLORS['jewik_orange']};
}}

/* APD tab — gold (seal) */
QTabBar::tab:nth-child(5) {{
    color: {COLORS['gold_seal']};
    border-top: 2px solid {COLORS['gold_seal']};
    font-weight: bold;
}}

/* MICRO tab — kem black (return) */
QTabBar::tab:nth-child(6) {{
    color: #555;
    border-top: 2px solid {COLORS['kem_black']};
}}

/* VISUALIZATION tab — hedj white (new possibility) */
QTabBar::tab:nth-child(7) {{
    color: {COLORS['hedj_white']};
    border-top: 2px solid {COLORS['hedj_white']};
}}

/* R-7 progress bar */
QProgressBar {{
    border: 1px solid #333;
    border-radius: 3px;
    background-color: #111;
    text-align: center;
    height: 20px;
}}

QProgressBar::chunk {{
    background-color: {COLORS['accent']};
    border-radius: 2px;
}}

/* Input */
QTextEdit, QLineEdit {{
    background-color: #111;
    color: {COLORS['text']};
    border: 1px solid #333;
    border-radius: 3px;
    padding: 4px;
}}

QPushButton {{
    background-color: #1a1a1a;
    color: {COLORS['text']};
    border: 1px solid #333;
    padding: 6px 16px;
    border-radius: 3px;
}}

QPushButton:hover {{
    background-color: #222;
    border-color: {COLORS['accent']};
}}

QPushButton:pressed {{
    background-color: #0a0a0a;
}}

/* Menu bar — ∂ (depth-control) replaces "Indent" */
QMenuBar {{
    background-color: #0a0a0a;
    color: {COLORS['text']};
    border-bottom: 1px solid #333;
}}

QMenuBar::item:selected {{
    background-color: #1a1a1a;
}}

QMenu {{
    background-color: #111;
    border: 1px solid #333;
}}

QMenu::item:selected {{
    background-color: #222;
}}

/* Status bar */
QStatusBar {{
    background-color: #0a0a0a;
    color: #888;
    border-top: 1px solid #333;
}}

/* Scrollbar */
QScrollBar:vertical {{
    border: none;
    background: #0a0a0a;
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: #333;
    min-height: 20px;
    border-radius: 4px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}
"""

# ─── Updated module semantics (corpus-validated descriptions) ───
MODULE_SEMANTICS = '''MODULE_SEMANTICS = {
    'bios': {
        'symbol': '\u2205', 'phase': 0, 'historical': 'Nun',
        'color': '#1B2838', 'color_name': 'deep_blue',
        'meaning': 'Praznina, potencial, odprtost \u2014 modra PRAZNINA, mir, refleksija',
    },
    'state': {
        'symbol': '\u00ac', 'phase': 1, 'historical': "Ma'at",
        'color': '#B43A2E', 'color_name': 'desher_red',
        'meaning': 'Lo\u010ditev, struktura, meritev \u2014 RANA, rez, za\u010detek impulza',
    },
    'uaf': {
        'symbol': '\u2206', 'phase': 2, 'historical': 'Khepri',
        'color': '#D6A83A', 'color_name': 'khenet_yellow',
        'meaning': 'Razlika, gibanje, antinomija \u2014 UPANJE, vez ki \u0161e ni most; '
                   '\u03b1UAF=mean(\u03b14,\u03b16), M=1\u2212\u03b1UAF, GUARD: EX/RE/OBST',
    },
    'jewik': {
        'symbol': '1', 'phase': 3, 'historical': 'Ptah',
        'color': '#C77800', 'color_name': 'jewik_orange',
        'meaning': 'Dejanje, emanacija, pe\u010dat \u2014 aktivacija, izrek kot akt',
    },
    'apd': {
        'symbol': '\u2316', 'phase': 4, 'historical': 'Tiheon',
        'color': '#D6A83A', 'color_name': 'gold_seal',
        'meaning': 'Ti\u0161ina, preverba, izgovor \u2014 zlato kot \u017eiva sila; '
                   'absolutni poskus definicije, ne dokon\u010dna resnica; '
                   'SEAL spro\u017ei povratek (\u222e)',
    },
    'micro': {
        'symbol': '\u222e', 'phase': 5, 'historical': '\u262f',
        'color': '#080705', 'color_name': 'kem_black',
        'meaning': 'Povratek, u\u010denje, dva cikla \u2014 NEGATIV_888, '
                   'ni\u010dnost kot prostor za ponovno rojstvo; 8~\u221e=povratek',
    },
    'visualization': {
        'symbol': '\u27e1', 'phase': 6, 'historical': '\u27e1',
        'color': '#F3E9D2', 'color_name': 'hedj_white',
        'meaning': 'Nova mo\u017enost, manifestacija, graf \u2014 '
                   'ABSOLUTNI ZA\u010cETEK, polnost; baza novega cikla',
    },
}
'''

# ─── Patched main_window.py with QSS loading ───
MAIN_WINDOW_PATCH = '''#!/usr/bin/env python3
"""Patched main_window.py — loads QSS from ta3v_colors.qss"""
import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QPushButton, QLabel, QStatusBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from comprehension.core.processing_pipeline import ProcessingPipeline
from comprehension.core.symbol_mapper import SymbolMapper
from comprehension.ui.r7_progress import R7ProgressWidget
from comprehension.ui.module_window import ModuleWindow


class PipelineWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, statement, config=None):
        super().__init__()
        self.statement = statement
        self.config = config or {}

    def run(self):
        try:
            pipeline = ProcessingPipeline()
            result = pipeline.process(self.statement, self.config)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TAZV Comprehension Machine")
        self.setGeometry(100, 100, 1200, 800)

        # Load QSS
        qss_path = os.path.join(os.path.dirname(__file__), '..', 'ta3v_colors.qss')
        if os.path.exists(qss_path):
            with open(qss_path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())

        self.pipeline = ProcessingPipeline()
        self.mapper = SymbolMapper()
        self.module_windows = {}

        self._init_ui()
        self._init_menu()
        self._init_status()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # R-7 progress
        self.r7_progress = R7ProgressWidget()
        layout.addWidget(self.r7_progress)

        # Input
        self.input = QTextEdit()
        self.input.setPlaceholderText("Vnesi izrek / statement...")
        self.input.setMaximumHeight(80)
        layout.addWidget(self.input)

        # Process button
        self.btn_process = QPushButton("Izvedi R-7 cikel")
        self.btn_process.clicked.connect(self.on_process)
        layout.addWidget(self.btn_process)

        # Tabs for each module
        self.tabs = QTabWidget()
        modules = ['bios', 'state', 'uaf', 'jewik', 'apd', 'micro', 'visualization']
        labels = [
            '\u2205 BIOS',
            '\u00ac STATE',
            '\u2206 UAF',
            '1 JEWIK',
            '\u2316 APD',
            '\u222e MICRO',
            '\u27e1 VIS',
        ]
        for mod, label in zip(modules, labels):
            w = ModuleWindow(mod)
            self.module_windows[mod] = w
            self.tabs.addTab(w, label)
        layout.addWidget(self.tabs)

    def _init_menu(self):
        menubar = self.menuBar()
        # File menu
        file_menu = menubar.addMenu("Datoteka")
        file_menu.addAction("Izhod", self.close)

        # ∂ Depth menu (replaces "Indent")
        depth_menu = menubar.addMenu("\u2202 Globina")
        depth_menu.addAction("Nivo 1 \u2014 povr\u0161inski rez")
        depth_menu.addAction("Nivo 2 \u2014 strukturni rez")
        depth_menu.addAction("Nivo 3 \u2014 ontolo\u0161ki rez")
        depth_menu.addAction("Nivo 4 \u2014 absolutni rez")

        # Theme menu
        theme_menu = menubar.addMenu("Tema")
        theme_menu.addAction("\u2205 Temno", lambda: self._apply_theme('praznina'))
        theme_menu.addAction("\u2206 Ognjeno", lambda: self._apply_theme('ognjeno'))
        theme_menu.addAction("\u222e Tok", lambda: self._apply_theme('tok'))

        # Help
        help_menu = menubar.addMenu("Pomo\u010d")
        help_menu.addAction("R-7 protokol")
        help_menu.addAction("TAZV ontologija")

    def _init_status(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Pripravljen. \u2205 \u2192 \u00ac \u2192 \u2206 \u2192 1 \u2192 \u2316 \u2192 \u222e \u2192 \u27e1")

    def _apply_theme(self, name):
        themes = {
            'praznina': '#0A0A0A',
            'ognjeno': '#1a0500',
            'tok': '#001020',
        }
        # Simple bg change — full theme swap can be added later
        pass

    def on_process(self):
        statement = self.input.toPlainText().strip()
        if not statement:
            self.status.showMessage("Vnesi izrek.")
            return

        self.status.showMessage("Obdelujem...")
        self.btn_process.setEnabled(False)

        self.worker = PipelineWorker(statement)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, result):
        self.btn_process.setEnabled(True)
        phases = result.get('phases', {})

        for i, mod in enumerate(['bios', 'state', 'uaf', 'jewik', 'apd', 'micro', 'visualization']):
            if mod in phases:
                self.module_windows[mod].update_result(phases[mod])
                self.r7_progress.set_phase(i)

        errors = result.get('errors', [])
        status = result.get('status', 'unknown')
        self.status.showMessage(
            f"Status: {status} | Faze: {len(phases)}/7 | Napake: {len(errors)}"
        )

    def on_error(self, msg):
        self.btn_process.setEnabled(True)
        self.status.showMessage(f"Napaka: {msg}")
'''

# ─── Write files ───
base = 'comprehension_machine'
files = {
    'ta3v_colors.qss': QSS,
    'comprehension/core/module_semantics.py': MODULE_SEMANTICS,
    'comprehension/ui/main_window.py': MAIN_WINDOW_PATCH,
}

print('TAZV Color Patch — Corpus-validated R-7 mapping')
print('=' * 55)

for path, content in files.items():
    full = os.path.join(base, path)
    dirpath = os.path.dirname(full)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    size = os.path.getsize(full)
    print(f'  file {path}  ({size} bytes)')

print()
print('Color assignments applied:')
for mod, color in MODULE_COLORS.items():
    print(f'  {mod:15s} -> {color}')
print()
print('Menu bar: "Indent" replaced with "\u2202 Globina" (depth-control)')
print()
print('Next:')
print('  cd comprehension_machine')
print('  python main.py  # launch with updated colors + QSS')
print()
print('Answers to your 4 questions:')
print('  1. UAF = Univerzalno Antinomijsko Polje (∆) — khenet/yellow HOLDS')
print('  2. APD->gold, MICRO->black, VIS->white — ALL CONFIRMED')
print('  3. "Indent" -> ∂ Globina (depth-control, not formatting)')
print('  4. Gold = APD, no 8th position; 7 is the whole')