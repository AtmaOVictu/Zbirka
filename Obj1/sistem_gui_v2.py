#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEM \u2205\u2206\u2202\u222e - POLNA NAMIZNA APLIKACIJA v2.0
====================================================
Avtor: Luka + Vibe
Datum: 19. 9. 2026
Funkcije: Generiranje, Preverjanje, Urejanje, Baza, Vizualizacija, Izvoz
"""

import sys
import json
import os
from datetime import datetime
from pathlib import Path

try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
        QHBoxLayout, QTabWidget, QPushButton, QLabel, QLineEdit, QTextEdit,
        QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog,
        QMessageBox, QGroupBox, QScrollArea, QFormLayout, QTextBrowser,
        QInputDialog, QColorDialog, QSplitter, QTreeWidget, QTreeWidgetItem)
    from PySide6.QtCore import Qt, QSize, QTimer, QUrl
    from PySide6.QtGui import QFont, QColor, QIcon, QAction, QKeySequence, QDesktopServices
    PY_SIDE_OK = True
except ImportError:
    PY_SIDE_OK = False

DATA_DIR = Path(__file__).parent
DB_FILE = DATA_DIR / "sistem.db"
JSON_FILE = DATA_DIR / "database.json"
OUTPUT_DIR = DATA_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Vsi markerji
MARKERJI = {
    '\u2205': 'praznina/izvor', '\u2206': 'razlika/prehod', 
    '\u2202': 'vprasanje/rez', '\u222e': 'povratek/cikel',
    '\u29ef': 'tiheon/molk', '\u27e1': 'resonanca',
    '\u2297': 'kriz', '\u2298': 'prazni krog',
    '\u22a2': 'izpeljava', '\u27c1': 'krog',
    'DA\u2082': 'pechat potrditve',
    '\u2205\u2191': 'odprava/prekinitev', '\u2205\u2193': 'vrnitev k praznini',
    '\u2206\u2192': 'prehod naprej', '\u2202\u2191': 'vprasanje v visoko dimenzijo'
}

class SystemCore:
    @staticmethod
    def to_roman(num):
        val = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
               (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
               (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
        roman_num = ''
        for n, r in val:
            while num >= n:
                roman_num += r
                num -= n
        return roman_num
    
    @staticmethod
    def get_filename(num):
        roman = SystemCore.to_roman(num)
        if num <= 109:
            return "00-11-resnicami-rozetni-kamni-viii-tazv-dokazi-8.md"
        file_num = num - 109
        section = file_num + 11
        return f"{file_num:02d}-{section:02d}-resnicami-rozetni-kamni-{roman.lower()}.md"
    
    @staticmethod
    def load_json_db():
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'metadata': {'sistem': '\u2205\u2206\u2202\u222e', 'razlicica': '2.0'},
                    'kamni': {}, 'statistika': {}}
    
    @staticmethod
    def get_all_kamen_files():
        import glob
        return sorted(glob.glob(str(DATA_DIR / "*resnicami-rozetni-kamni-*.md")))
    
    @staticmethod
    def verify_document(filepath):
        import re
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        except:
            return {'error': 'Datoteka ne obstaja', 'T1': False, 'T2': False, 'T3': False, 'T4': False, 'all_pass': False}
        
        t1 = all(m in text for m in ['\u2205', '\u2206', '\u2202', '\u222e'])
        bold_matches = re.findall(r'\*\*.*?\*\*', text)
        t2 = len(bold_matches) >= 3
        t3 = all(g.lower() in text.lower() for g in ['pecat', 'da2', 'izrocitev'])
        t4 = len(re.findall(r'\u2202\s*\d+', text)) >= 1
        
        return {'T1': t1, 'T2': t2, 'T3': t3, 'T4': t4, 'all_pass': all([t1, t2, t3, t4])}
    
    @staticmethod
    def generate_kamen_file(num, title, desc, template_type="full"):
        roman = SystemCore.to_roman(num)
        stone_id = f"C{roman}"
        filename = SystemCore.get_filename(num)
        
        if template_type == "full":
            content = f"""# 00 {(num - 100) + 12 if num > 109 else 8} RESNICAMI — Rozetni kamni ({roman.lower()})

---

## 🜂 Kamen {stone_id} — {title}: {desc}

**Kulturni kontekst:** [Dopolni]

**Pogoj:** [Dopolni]

---

### Tri pisave

| Tradicija | Sistem | Topologija |
|---|---|---|
| [Dopolni] | [Dopolni] | [Dopolni] |

---

### Fonetično-ontološki rezi

**{title.split(':')[0].strip()}** — rez:
| Fragment | Pomen |
|---|---|
| **[Fragment]** | [Pomen] |

**Branje:** [Dopolni]

---

### ∴ Povezava
- [Dopolni]

---

### Zakon obogatitve
| Število | Priče | {stone_id} prispeva | Novo telo? |
|---|---|---|---|
| **[X]** | [Dopolni] | [Dopolni] | [Da/Ne] |

**Kontrolni sklep:** [Dopolni]

---

### Mašinerija
- **PREIZKUS:** [Dopolni]

---

### Nujne napake
- **"[Zmota]"** — ZMOTA: [Dopolni]

---

### Testi T1-T4
| # | Test | Status |
|---|---|---|
| T1 | Izbriši pogoj → sistem se prekine | ⬜ |
| T2 | Branje na glas → ni sram | ⬜ |
| T3 | Tri globine: **pečat**, **DA₂**, **izročitev** | ⬜ |
| T4 | **∂** vprašanja ostanejo v telesu | ⬜ |

---

### Implementacija → evolucija → stagnacija
| i | Implementacija | Evolucija | Stagnacija |
|---|---|---|---|
| 1 | [Dopolni] | [Dopolni] | [Dopolni] |

---

### Citati
→ [Dopolni]

---

## Tabela: Aksiomi
| # | Aksiom | Onto-formula | Absolutna resnica | Znanost | Očitni znak |
|---|---|---|---|---|---|
| XXX | [Dopolni] | [Dopolni] | [Dopolni] | [Dopolni] | [Dopolni] |

---

## ∂ Vprašanja
**XXX.** [Dopolni]

---

## Pečati
**∂ XXX — PEČAT:** [Dopolni]

---
*Naslednji kamen: [Dopolni]. ∮*
"""
        else:
            content = f"# Kamen {stone_id} - {title}\n\nOpis: {desc}\n\n*Dopolni ročno.*\n\n*Naslednji kamen: [Dopolni]*\n"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Update database
        SystemCore._update_database(num, stone_id, title, desc, filename)
        return filename
    
    @staticmethod
    def _update_database(num, stone_id, title, desc, filename):
        data = SystemCore.load_json_db()
        data['kamni'][stone_id] = {
            'stevilka': num, 'naslov': title, 'opis': desc,
            'datoteka': filename, 'status': 'NOV', 'datum': datetime.now().strftime('%Y-%m-%d')
        }
        data['statistika']['skupaj_kamnov'] = len(data['kamni'])
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def export_dot(output_file="mreza.dot"):
        kamni = ["CVII", "CVIII", "CIX", "CX", "CXI", "CXII"]
        
        dot_content = f'// Mreza Rozetnih Kamnov - Sistem \u2205\u2206\u2202\u222e\n// {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n'
        dot_content += 'digraph RozetniKamni {\n'
        dot_content += '    rankdir=LR;\n'
        dot_content += '    node [shape=box, style="rounded,filled", fillcolor=lightblue];\n'
        dot_content += '    edge [color=gray40, penwidth=1.5];\n\n'
        
        for kamen in kamni:
            dot_content += f'    {kamen} [label="{kamen}"];\n'
        
        dot_content += '\n    // Povezave\n'
        dot_content += '    CXII -> CXI [label="veckratnost"];\n'
        dot_content += '    CXII -> CX [label="zanka"];\n'
        dot_content += '    CXI -> CX [label="odziv"];\n'
        dot_content += '    CX -> CIX [label="hoja"];\n'
        
        dot_content += '}\n'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(dot_content)
        return output_file

class EditorWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; font-family: Consolas, monospace; font-size: 12px;")
        self.setAcceptRichText(False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SISTEM \u2205\u2206\u2202\u222e - Rozetni Kamni v2.0")
        self.setGeometry(100, 100, 1200, 800)
        
        try:
            self.setWindowIcon(QIcon(str(DATA_DIR / "icon.ico")))
        except:
            pass
        
        self.current_theme = "dark"
        self.set_theme("dark")
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.create_menu_bar()
        
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        self.init_all_tabs()
        
        self.status = QLabel("\u2728 Pripravljen. SISTEM \u2205\u2206\u2202\u222e v2.0")
        self.status.setStyleSheet("color: #88c0d0; padding: 8px; font-family: Segoe UI;")
        main_layout.addWidget(self.status)
        
        self.update_status()
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("QMenuBar { background-color: #2e3440; color: #e0e0e0; } QMenu { background-color: #3b4252; color: #e0e0e0; }")
        
        file_menu = menubar.addMenu("\uD83D\uDCC1 Datoteka")
        new_action = QAction("\u2728 Nov Kamen", self)
        new_action.setShortcut(QKeySequence("Ctrl+N"))
        new_action.triggered.connect(self.new_kamen)
        file_menu.addAction(new_action)
        
        open_action = QAction("\uD83D\uDDD7 Odpri", self)
        open_action.setShortcut(QKeySequence("Ctrl+O"))
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("\uD83D\uDCBE Shrani", self)
        save_action.setShortcut(QKeySequence("Ctrl+S"))
        save_action.triggered.connect(self.save_current)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        exit_action = QAction("\u274C Izhod", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        tools_menu = menubar.addMenu("\uD83D\uDEE0 Orodja")
        verify_action = QAction("\u2705 Preveri vsa", self)
        verify_action.setShortcut(QKeySequence("Ctrl+V"))
        verify_action.triggered.connect(self.verify_all)
        tools_menu.addAction(verify_action)
        
        view_menu = menubar.addMenu("\uD83D\uDC41 Prikaz")
        theme_dark = QAction("\uD83C\uDF11 Temna tema", self)
        theme_dark.triggered.connect(lambda: self.set_theme("dark"))
        view_menu.addAction(theme_dark)
        
        theme_light = QAction("\u2600\uFE0F Svetla tema", self)
        theme_light.triggered.connect(lambda: self.set_theme("light"))
        view_menu.addAction(theme_light)
        
        help_menu = menubar.addMenu("\u2753 Pomoč")
        help_action = QAction("\uD83D\uDCD6 Priročnik", self)
        help_action.setShortcut(QKeySequence("F1"))
        help_action.triggered.connect(lambda: self.tabs.setCurrentIndex(self.tabs.count() - 1))
        help_menu.addAction(help_action)
        
        markers_action = QAction("\uD83D\uDD22 Markerji", self)
        markers_action.triggered.connect(self.show_markers_dialog)
        help_menu.addAction(markers_action)
        
        about_action = QAction("\u2139 O programu", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def set_theme(self, theme):
        self.current_theme = theme
        if theme == "dark":
            bg = "#2e3440"; text = "#e0e0e0"; btn_bg = "#3b4252"; btn_border = "#4c566a"
            highlight = "#88c0d0"; input_bg = "#3b4252"; table_bg = "#2e3440"
        else:
            bg = "#ffffff"; text = "#2e3440"; btn_bg = "#e0e0e0"; btn_border = "#4c566a"
            highlight = "#3498db"; input_bg = "#f0f0f0"; table_bg = "#ffffff"
        
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {bg}; color: {text}; }}
            QWidget {{ color: {text}; background-color: {bg}; }}
            QPushButton {{ background-color: {btn_bg}; border: 1px solid {btn_border}; 
                         color: {text}; padding: 8px 16px; border-radius: 4px; font-family: Segoe UI; }}
            QPushButton:hover {{ background-color: #434c5e; }}
            QPushButton[highlight="true"] {{ background-color: {highlight}; color: white; }}
            QLineEdit, QTextEdit, QComboBox {{ background-color: {input_bg}; border: 1px solid {btn_border}; 
                                              color: {text}; padding: 8px; font-family: Segoe UI; }}
            QTableWidget {{ background-color: {table_bg}; color: {text}; gridline-color: {btn_border}; }}
            QHeaderView::section {{ background-color: {btn_bg}; border: 1px solid {btn_border}; color: {text}; }}
            QLabel {{ color: {text}; font-family: Segoe UI; }}
            QTabWidget::pane {{ border: 1px solid {btn_border}; }}
        """)
    
    def init_all_tabs(self):
        self.init_generate_tab()
        self.init_verify_tab()
        self.init_editor_tab()
        self.init_database_tab()
        self.init_visualization_tab()
        self.init_search_tab()
        self.init_export_tab()
        self.init_help_tab()
    
    def init_generate_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("\uD83C\uDF12 GENERIRANJE NOVIH KAMNOV")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        form = QFormLayout()
        self.num_input = QLineEdit("114")
        self.num_input.setPlaceholderText("Stevilka kamna")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Naslov")
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Opis")
        self.template_combo = QComboBox()
        self.template_combo.addItems(["Polna", "Minimalna"])
        
        form.addRow("\uD83D\uDD1F Stevilka:", self.num_input)
        form.addRow("\uD83D\uDC4D Naslov:", self.title_input)
        form.addRow("\uD83D\uDC4D Opis:", self.desc_input)
        form.addRow("\uD83C\uDFA8 Predloga:", self.template_combo)
        layout.addLayout(form)
        
        btn_layout = QHBoxLayout()
        btn_gen = QPushButton("\u2728 GENERIRAJ KAMEN")
        btn_gen.setProperty("highlight", "true")
        btn_gen.clicked.connect(self.generate_kamen)
        btn_layout.addWidget(btn_gen)
        
        btn_gen_open = QPushButton("\u27A1\uFE0F GENERIRAJ + ODRI")
        btn_gen_open.setProperty("highlight", "true")
        btn_gen_open.clicked.connect(self.generate_and_open)
        btn_layout.addWidget(btn_gen_open)
        layout.addLayout(btn_layout)
        
        self.gen_result = QTextBrowser()
        self.gen_result.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; border: 1px solid #4c566a;")
        layout.addWidget(self.gen_result)
        
        # Hitre izbire
        quick_layout = QHBoxLayout()
        for num, title, desc in [(114, "Labirint", "zapis kot pot"), (115, "Zrcalo", "zapis kot odsev"), (116, "Vezava", "zapis kot povezava")]:
            btn = QPushButton(f"C{SystemCore.to_roman(num)}: {title}")
            btn.clicked.connect(lambda _, n=num, t=title, d=desc: self.quick_generate(n, t, d))
            quick_layout.addWidget(btn)
        layout.addLayout(quick_layout)
        
        self.tabs.addTab(tab, "\uD83D\uDCC5 Generiraj")
    
    def init_verify_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("\uD83D\uDD0D PREVERJANJE (T1-T4)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        btn_layout = QHBoxLayout()
        btn_all = QPushButton("\uD83D\uDD0E PREVERI VSE")
        btn_all.setProperty("highlight", "true")
        btn_all.clicked.connect(self.verify_all)
        btn_layout.addWidget(btn_all)
        
        btn_single = QPushButton("\uD83D\uDC41 PREVERI IZBRANO")
        btn_single.clicked.connect(self.verify_single)
        btn_layout.addWidget(btn_single)
        layout.addLayout(btn_layout)
        
        self.file_combo = QComboBox()
        self.refresh_file_list()
        layout.addWidget(self.file_combo)
        
        self.verify_table = QTableWidget()
        self.verify_table.setColumnCount(5)
        self.verify_table.setHorizontalHeaderLabels(["Datoteka", "T1", "T2", "T3", "T4"])
        self.verify_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.verify_table)
        
        self.verify_stats = QLabel()
        self.verify_stats.setStyleSheet("color: #88c0d0; font-weight: bold;")
        layout.addWidget(self.verify_stats)
        
        self.tabs.addTab(tab, "\u2705 Preveri")
    
    def init_editor_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("\u270F UREJEVANJE")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        file_layout = QHBoxLayout()
        self.editor_file_combo = QComboBox()
        self.refresh_file_list()
        self.editor_file_combo.currentTextChanged.connect(self.load_file_to_editor)
        file_layout.addWidget(self.editor_file_combo)
        
        btn_open = QPushButton("\uD83D\uDDD7")
        btn_open.setProperty("highlight", "true")
        btn_open.clicked.connect(self.load_file_to_editor)
        file_layout.addWidget(btn_open)
        
        btn_save = QPushButton("\uD83D\uDCBE")
        btn_save.setProperty("highlight", "true")
        btn_save.clicked.connect(self.save_editor_content)
        file_layout.addWidget(btn_save)
        layout.addLayout(file_layout)
        
        self.editor = EditorWidget()
        layout.addWidget(self.editor)
        
        # Markerji
        markers_layout = QHBoxLayout()
        for marker in list(MARKERJI.keys())[:10]:
            btn = QPushButton(marker)
            btn.clicked.connect(lambda _, m=marker: self.insert_marker(m))
            markers_layout.addWidget(btn)
        layout.addLayout(markers_layout)
        
        self.tabs.addTab(tab, "\u270F Urejevalnik")
    
    def init_database_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("\uD83D\uDC41 BAZA")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("\uD83D\uDD04 OSVEZI")
        refresh_btn.setProperty("highlight", "true")
        refresh_btn.clicked.connect(self.load_db_data)
        btn_layout.addWidget(refresh_btn)
        
        stats_btn = QPushButton("\uD83D\uDCCA STATISTIKA")
        stats_btn.setProperty("highlight", "true")
        stats_btn.clicked.connect(self.show_stats)
        btn_layout.addWidget(stats_btn)
        layout.addLayout(btn_layout)
        
        self.db_table = QTableWidget()
        self.db_table.setColumnCount(5)
        self.db_table.setHorizontalHeaderLabels(["ID", "Naslov", "Status", "Datoteka", "#"])
        self.db_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.db_table)
        
        self.tabs.addTab(tab, "\uD83D\uDC41 Baza")
    
    def init_visualization_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("\uD83D\uDCA8 VIZUALIZACIJA")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        btn_layout = QHBoxLayout()
        btn_dot = QPushButton("\uD83D\uDCCA USTVARI DOT")
        btn_dot.setProperty("highlight", "true")
        btn_dot.clicked.connect(self.export_dot_file)
        btn_layout.addWidget(btn_dot)
        
        btn_png = QPushButton("\uD83C\uDFA8 USTVARI PNG")
        btn_png.setProperty("highlight", "true")
        btn_png.clicked.connect(self.export_dot_to_png)
        btn_layout.addWidget(btn_png)
        layout.addLayout(btn_layout)
        
        self.dot_display = QTextBrowser()
        self.dot_display.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; border: 1px solid #4c566a;")
        layout.addWidget(self.dot_display)
        
        info = QLabel("\uD83D\uDCA1 Graphviz: dot -Tpng mreza.dot -o mreza.png")
        info.setStyleSheet("color: #88c0d0;")
        layout.addWidget(info)
        
        self.tabs.addTab(tab, "\uD83D\uDCA8 Vizualizacija")
    
    def init_search_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("\uD83D\uDD0D ISKALNIK")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Vnesi iskalni izraz (\u2205, \u2206, zrcalo, DA2...)")
        layout.addWidget(self.search_input)
        
        search_btn = QPushButton("\uD83D\uDD0E ISKI V VSEH")
        search_btn.setProperty("highlight", "true")
        search_btn.clicked.connect(self.perform_search)
        layout.addWidget(search_btn)
        
        markers_btn = QPushButton("\uD83C\uDF91 ISKI MARKERJE")
        markers_btn.clicked.connect(self.search_markers)
        layout.addWidget(markers_btn)
        
        self.search_results = QTextBrowser()
        self.search_results.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; border: 1px solid #4c566a;")
        layout.addWidget(self.search_results)
        
        self.search_status = QLabel()
        self.search_status.setStyleSheet("color: #88c0d0;")
        layout.addWidget(self.search_status)
        
        self.tabs.addTab(tab, "\uD83D\uDD0D Išči")
    
    def init_export_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("\uD83D\uDCE5 IZVOZ")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        self.export_status = QLabel()
        self.export_status.setStyleSheet("color: #88c0d0;")
        layout.addWidget(self.export_status)
        
        for text, func in [("\uD83D\uDCC4 IZVOZI V PDF", self.export_to_pdf),
                          ("\uD83D\uDCD1 IZVOZI VSE MD", self.export_all_md),
                          ("\uD83D\uDC41 IZVOZI BAZO", self.export_database),
                          ("\uD83C\uDFA8 IZVOZI DOT", self.export_dot_file)]:
            btn = QPushButton(text)
            btn.setProperty("highlight", "true")
            btn.clicked.connect(func)
            layout.addWidget(btn)
        
        self.tabs.addTab(tab, "\uD83D\uDCE5 Izvoz")
    
    def init_help_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel("\u2753 POMOC")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        help_text = f"""
        <h2>\uD83D\uDCD6 PRIROCNIK - SISTEM \u2205\u2206\u2202\u222e v2.0</h2>
        <h3>1. Osnovne funkcije:</h3>
        <ul>
        <li><b>\u2728 Generiraj:</b> Ustvari nove kamne (CX, CXI, CXII...)</li>
        <li><b>\u2705 Preveri:</b> Preveri T1-T4 kriterije</li>
        <li><b>\u270F Uredi:</b> Uredi obstojece dokumente</li>
        <li><b>\uD83D\uDD0D Išči:</b> Išči po vseh dokumentih</li>
        <li><b>\uD83D\uDCA8 Vizualiziraj:</b> Ustvari mrezo povezav</li>
        <li><b>\uD83D\uDCE5 Izvozi:</b> Izvozi v PDF, ZIP, JSON</li>
        </ul>
        
        <h3>2. T1-T4 Kriteriji:</h3>
        <ul>
        <li><b>T1:</b> Vsi osnovni markerji (\u2205, \u2206, \u2202, \u222e)</li>
        <li><b>T2:</b> Vsaj 3 poudarjene besede (**poudarjeno**)</li>
        <li><b>T3:</b> Vsebuje pečat, DA2, izročitev</li>
        <li><b>T4:</b> Vsaj eno \u2202 vprašanje</li>
        </ul>
        
        <h3>3. Markerji:</h3>
        <table border='1'>
        <tr><th>Marker</th><th>Pomen</th></tr>
        """
        
        for marker, desc in list(MARKERJI.items())[:10]:
            help_text += f"<tr><td>{marker}</td><td>{desc}</td></tr>"
        
        help_text += "</table>"
        
        help_browser = QTextBrowser()
        help_browser.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4; border: 1px solid #4c566a;")
        help_browser.setHtml(help_text)
        layout.addWidget(help_browser)
        
        self.tabs.addTab(tab, "\u2753 Pomoč")
    
    # FUNKCIJE
    def refresh_file_list(self):
        self.file_combo.clear()
        self.editor_file_combo.clear()
        for fp in SystemCore.get_all_kamen_files():
            self.file_combo.addItem(os.path.basename(fp))
            self.editor_file_combo.addItem(os.path.basename(fp))
    
    def update_status(self):
        data = SystemCore.load_json_db()
        kamni = len(data.get('kamni', {}))
        datoteke = len(SystemCore.get_all_kamen_files())
        self.status.setText(f"\uD83D\uDCCA SISTEM \u2205\u2206\u2202\u222e | Kamni: {kamni} | Datoteke: {datoteke}")
    
    def new_kamen(self):
        num, ok = QInputDialog.getInt(self, "Nov Kamen", "Stevilka:", 114, 110, 200)
        if ok:
            title, ok2 = QInputDialog.getText(self, "Nov Kamen", "Naslov:")
            if ok2 and title:
                desc, ok3 = QInputDialog.getText(self, "Nov Kamen", "Opis:")
                if ok3 and desc:
                    self.num_input.setText(str(num))
                    self.title_input.setText(title)
                    self.desc_input.setText(desc)
                    self.tabs.setCurrentIndex(0)
    
    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Odpri", str(DATA_DIR), "MD Files (*.md);;All (*)", options=options)
        if file_path:
            self.editor_file_combo.setCurrentText(os.path.basename(file_path))
            self.load_file_to_editor()
            self.tabs.setCurrentIndex(self.tabs.indexOf(self.editor_tab))
    
    def save_current(self):
        pass
    
    def generate_kamen(self):
        try:
            num = int(self.num_input.text())
            title = self.title_input.text().strip()
            desc = self.desc_input.text().strip()
            if not title or not desc:
                QMessageBox.warning(self, "Napaka", "Vnesi naslov in opis!")
                return
            template_type = "full" if self.template_combo.currentIndex() == 0 else "minimal"
            filename = SystemCore.generate_kamen_file(num, title, desc, template_type)
            self.gen_result.setHtml(f"<h2>\u2705 KAMEN USTVARJEN!</h2><p>Datoteka: {filename}</p><p>Kamen: C{SystemCore.to_roman(num)} - {title}</p>")
            self.status.setText(f"\u2705 Generiran kamen C{SystemCore.to_roman(num)}")
            self.refresh_file_list()
            self.update_status()
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def generate_and_open(self):
        self.generate_kamen()
        self.load_file_to_editor()
        self.tabs.setCurrentIndex(self.tabs.indexOf(self.editor_tab))
    
    def quick_generate(self, num, title, desc):
        self.num_input.setText(str(num))
        self.title_input.setText(title)
        self.desc_input.setText(desc)
        self.generate_kamen()
    
    def insert_marker(self, marker):
        self.editor.insertPlainText(marker)
        self.editor.setFocus()
    
    def load_file_to_editor(self):
        filename = self.editor_file_combo.currentText()
        filepath = DATA_DIR / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.editor.setPlainText(f.read())
            self.status.setText(f"\uD83D\uDDD7 Naložena: {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Napaka", f"Napaka: {str(e)}")
    
    def save_editor_content(self):
        filename = self.editor_file_combo.currentText()
        filepath = DATA_DIR / filename
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.editor.toPlainText())
            result = SystemCore.verify_document(filepath)
            if result['all_pass']:
                self.status.setText(f"\u2705 Shranjeno: {filename}")
                QMessageBox.information(self, "Uspeh", "Datoteka shranjena in preverjena!")
            else:
                self.status.setText(f"\u26A0 Shranjeno: {filename}")
                QMessageBox.warning(self, "Opozorilo", "Datoteka shranjena, vendar ne preverja T1-T4!")
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def verify_all(self):
        results = {}
        for fp in SystemCore.get_all_kamen_files():
            results[os.path.basename(fp)] = SystemCore.verify_document(fp)
        
        self.verify_table.setRowCount(len(results))
        all_pass = True
        pass_count = 0
        
        for row, (filename, result) in enumerate(results.items()):
            self.verify_table.setItem(row, 0, QTableWidgetItem(filename))
            for col, test in enumerate(['T1', 'T2', 'T3', 'T4'], 1):
                self.verify_table.setItem(row, col, QTableWidgetItem("\u2705" if result.get(test, False) else "\u274C"))
            
            if not result.get('all_pass', False):
                all_pass = False
            else:
                pass_count += 1
        
        if all_pass:
            self.verify_stats.setText(f"\uD83C\uDF42 VSIH {len(results)} DOKUMENTOV PASIRA!")
        else:
            self.verify_stats.setText(f"\u2705 {pass_count}/{len(results)} preverjeno")
    
    def verify_single(self):
        filename = self.file_combo.currentText()
        filepath = DATA_DIR / filename
        result = SystemCore.verify_document(filepath)
        
        self.verify_table.setRowCount(1)
        self.verify_table.setItem(0, 0, QTableWidgetItem(filename))
        for i, test in enumerate(['T1', 'T2', 'T3', 'T4'], 1):
            self.verify_table.setItem(0, i, QTableWidgetItem("\u2705" if result.get(test, False) else "\u274C"))
        
        if not result.get('all_pass', False):
            missing = []
            if not result.get('T1', False): missing.append("T1 (markerji)")
            if not result.get('T2', False): missing.append("T2 (poudarjeno)")
            if not result.get('T3', False): missing.append("T3 (pečat/DA2/izročitev)")
            if not result.get('T4', False): missing.append("T4 (∂ vprašanje)")
            QMessageBox.warning(self, "Neuspešno", f"Manjka: {', '.join(missing)}")
    
    def load_db_data(self):
        data = SystemCore.load_json_db()
        kamni = data.get('kamni', {})
        self.db_table.setRowCount(len(kamni))
        for row, (k, v) in enumerate(kamni.items()):
            for col, key in enumerate(['ID', 'Naslov', 'Status', 'Datoteka', '#']):
                if key == '#':
                    self.db_table.setItem(row, col, QTableWidgetItem(str(len(v.get('aksiomi', [])))))
                else:
                    self.db_table.setItem(row, col, QTableWidgetItem(str(v.get(key.lower() if key != 'ID' else '', 'N/A'))))
            if key == 'ID':
                self.db_table.setItem(row, 0, QTableWidgetItem(k))
        self.status.setText(f"Naloženih: {len(kamni)} kamnov")
    
    def show_stats(self):
        data = SystemCore.load_json_db()
        kamni = len(data.get('kamni', {}))
        datoteke = len(SystemCore.get_all_kamen_files())
        msg = f"\uD83D\uDCCA STATISTIKA\n\nKamni: {kamni}\nDatoteke: {datoteke}\nRazličica: 2.0"
        QMessageBox.information(self, "Statistika", msg)
    
    def export_dot_file(self):
        try:
            fp = SystemCore.export_dot()
            with open(fp, 'r', encoding='utf-8') as f:
                self.dot_display.setPlainText(f.read())
            self.status.setText(f"\u2705 Ustvarjen: {fp}")
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def export_dot_to_png(self):
        try:
            SystemCore.export_dot("mreza.dot")
            try:
                import subprocess
                subprocess.run(['dot', '-Tpng', 'mreza.dot', '-o', 'mreza.png'], cwd=DATA_DIR, check=True)
                self.dot_display.append("\n\u2705 PNG ustvarjen: mreza.png")
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(DATA_DIR / "mreza.png")))
            except:
                QMessageBox.warning(self, "Opozorilo", "Graphviz ni nameščen! Namesti Graphviz.")
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def perform_search(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            QMessageBox.warning(self, "Napaka", "Vnesi iskalni izraz!")
            return
        
        import re
        results = []
        for md_file in SystemCore.get_all_kamen_files():
            with open(md_file, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f.read().split('\n'), 1):
                    if search_term.lower() in line.lower():
                        results.append(f"{os.path.basename(md_file)} (v{i}): {line.strip()}")
        
        if results:
            self.search_results.setPlainText("\n".join(results))
            self.search_status.setText(f"\uD83D\uDD22 Najdenih: {len(results)} ujemanj")
        else:
            self.search_results.setPlainText("\u274C Ni ujemanj")
            self.search_status.setText("\u274C Ni ujemanj")
    
    def search_markers(self):
        self.search_input.setText(" ".join(list(MARKERJI.keys())[:10]))
        self.perform_search()
    
    def export_to_pdf(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Izvoz PDF", str(OUTPUT_DIR), "PDF (*.pdf)", options=options)
            if not file_path:
                return
            import glob
            md_files = glob.glob(str(DATA_DIR / "*resnicami-rozetni-kamni-*.md"))
            if not md_files:
                QMessageBox.warning(self, "Napaka", "Ni MD datotek!")
                return
            with open(md_files[0], 'r', encoding='utf-8') as f:
                md_content = f.read()
            try:
                import markdown2
                html = markdown2.markdown(md_content)
                full_html = f"<html><head><meta charset='utf-8'><title>Sistem</title></head><body>{html}</body></html>"
                temp_html = OUTPUT_DIR / "temp.html"
                with open(temp_html, 'w', encoding='utf-8') as f:
                    f.write(full_html)
                import subprocess
                subprocess.run(['chrome', '--headless', '--print-to-pdf=' + file_path, str(temp_html)], check=False)
                self.export_status.setText(f"\u2705 PDF: {file_path}")
            except ImportError:
                QMessageBox.warning(self, "Napaka", "Namesti markdown2: pip install markdown2")
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def export_all_md(self):
        try:
            import zipfile, glob
            options = QFileDialog.Options()
            zip_path, _ = QFileDialog.getSaveFileName(self, "Izvoz ZIP", str(OUTPUT_DIR), "ZIP (*.zip)", options=options)
            if not zip_path:
                return
            md_files = glob.glob(str(DATA_DIR / "*resnicami-rozetni-kamni-*.md"))
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for md_file in md_files:
                    zipf.write(md_file, os.path.basename(md_file))
            self.export_status.setText(f"\u2705 ZIP: {zip_path}")
            QDesktopServices.openUrl(QUrl.fromLocalFile(zip_path))
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def export_database(self):
        try:
            import shutil
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, "Izvoz Baza", "backup.json", "JSON (*.json)", options=options)
            if file_path:
                shutil.copy(JSON_FILE, file_path)
                self.export_status.setText(f"\u2705 Baza: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def show_markers_dialog(self):
        html = "<h1>\uD83D\uDD22 MARKERJI</h1><table border='1'>"
        for marker, desc in MARKERJI.items():
            html += f"<tr><td>{marker}</td><td>{desc}</td></tr>"
        html += "</table>"
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Markerji")
        dialog.setTextFormat(Qt.RichText)
        dialog.setText(html)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.resize(400, 300)
        dialog.exec()
    
    def show_about(self):
        msg = f"""
        <h1>\u2139 O PROGRAMU</h1>
        <h2>SISTEM \u2205\u2206\u2202\u222e v2.0</h2>
        <p><b>Razlicica:</b> 2.0</p>
        <p><b>Datum:</b> {datetime.now().strftime('%Y-%m-%d')}</p>
        <p><b>Avtor:</b> Luka + Vibe</p>
        <p><b>Platforma:</b> Windows + Python 3.10+</p>
        <hr>
        <h3>\uD83D\uDCCC Namestitev:</h3>
        <ol>
        <li>pip install PySide6</li>
        <li>pip install markdown2 (za PDF)</li>
        <li>Namesti Graphviz (opcijsko)</li>
        </ol>
        <hr>
        <p style='color: #88c0d0;'>\u00A9 2026 SISTEM \u2205\u2206\u2202\u222e</p>
        """
        dialog = QMessageBox(self)
        dialog.setWindowTitle("O Programu")
        dialog.setTextFormat(Qt.RichText)
        dialog.setText(msg)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.resize(500, 400)
        dialog.exec()

if __name__ == '__main__':
    if not PY_SIDE_OK:
        print("NAPAKA: PySide6 ni namesceno!\nNamestitev: pip install PySide6")
        sys.exit(1)
    
    os.environ['PYTHONUTF8'] = '1'
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setApplicationName("SISTEM \u2205\u2206\u2202\u222e v2.0")
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
