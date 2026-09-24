#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SISTEM ∅→∆→∂→∮ - Polna Namizna Aplikacija
===========================================
Avtor: Luka + Vibe
Datum: 18. 9. 2026

Zahtevano: pip install -r requirements.txt

Funkcije:
- Ustvarjanje novih kamnov
- Preverjanje T1-T4
- Upravljanje baze podatkov
- Vizualizacija mreze
- SQL poizvedbe
- Statistika
- Izvoz v PDF/ZIP
- Iskalnik po dokumentih
"""

import sys
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

# Preveri PySide6
try:
    from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
        QHBoxLayout, QTabWidget, QPushButton, QLabel, QLineEdit, QTextEdit,
        QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
        QFileDialog, QMessageBox, QGroupBox, QScrollArea, QFormLayout)
    from PySide6.QtCore import Qt, QSize
    from PySide6.QtGui import QFont, QColor
    PY_SIDE_OK = True
except ImportError:
    PY_SIDE_OK = False


# ============================================================================
# KONSTANTE
# ============================================================================

DATA_DIR = Path(__file__).parent
DB_FILE = DATA_DIR / "sistem.db"
JSON_FILE = DATA_DIR / "database.json"
OUTPUT_DIR = DATA_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


# ============================================================================
# POMOŽNE FUNKCIJE
# ============================================================================

class SystemCore:
    """Osrednje funkcije sistema"""
    
    @staticmethod
    def to_roman(num: int) -> str:
        val = [(100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
               (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
        roman_num = ''
        for n, r in val:
            while num >= n:
                roman_num += r
                num -= n
        return roman_num
    
    @staticmethod
    def get_filename(num: int) -> str:
        roman = SystemCore.to_roman(num)
        # Kamni 107-109 (CVII-CIX) so v dokumentu 00-11
        if num <= 109:
            return "00-11-resnicami-rozetni-kamni-viii-tazv-dokazi-8.md"
        # Za kamne >= 110: file_num = num - 109, section = file_num + 11
        file_num = num - 109
        section = file_num + 11
        return f"{file_num:02d}-{section:02d}-resnicami-rozetni-kamni-{roman.lower()}.md"
    
    @staticmethod
    def load_json_db() -> dict:
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                'metadata': {'sistem': '∅→∆→∂→∮', 'razlicica': '1.0'},
                'kamni': {}, 'aksiomi': {}, 'vprašanja': {}, 'markerji': {}, 'statistika': {}
            }
    
    @staticmethod
    def verify_document(filepath: str) -> dict:
        import re
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        except:
            return {'error': 'Datoteka ne obstaja'}
        
        t1 = all(m in text for m in ['∅', '∆', '∂', '∮'])
        t2 = len(re.findall(r'\*\*.*?\*\*', text)) >= 3
        t3 = all(g.lower() in text.lower() for g in ['pečat', 'DA₂', 'izročitev'])
        t4 = len(re.findall(r'∂\s*\d+', text)) >= 1
        
        return {'T1': t1, 'T2': t2, 'T3': t3, 'T4': t4, 'all_pass': all([t1, t2, t3, t4])}
    
    @staticmethod
    def export_dot(filename: str = "mreza.dot") -> str:
        dot = f"""// Mreža Rozetnih kamnov - ∅→∆→∂→∮
// {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

digraph RozetniKamni {{
    rankdir=LR;
    node [shape=box, style="rounded,filled", fillcolor=lightblue];
    edge [color=gray40, penwidth=1.5];
    
    // Kamni
    CVII [label="CVII\\nLungta\\n(razpad)"];
    CVIII [label="CVIII\\nPalica\\n(gibanje)"];
    CIX [label="CIX\\nGeoglifi\\n(prostor)"];
    CX [label="CX\\nPovratna zanka\\n(odziv)"];
    CXI [label="CXI\\nVečkratnost\\n(nosilci)"];
    CXII [label="CXII\\nPalimpsest\\n(plasti)"];
    
    // Povezave
    CXII -> CXI [label="večkratnost"];
    CXII -> CX [label="zanka"];
    CXII -> CIX [label="prostor"];
    CXI -> CX [label="odziv"];
    CXI -> CIX [label="∮"];
    CX -> CIX [label="hoja"];
    CX -> CVII [label="veter"];
    CIX -> CVII [label="puščava"];
    CIX -> CVIII [label="kurir"];
    
    // Markerji
    marker_∅ [label="∅", shape=ellipse, fillcolor=lightgreen];
    marker_∆ [label="∆", shape=ellipse, fillcolor=lightsalmon];
    marker_∂ [label="∂", shape=ellipse, fillcolor=lightpink];
    marker_∮ [label="∮", shape=ellipse, fillcolor=lightyellow];
    marker_⧖ [label="⧖", shape=ellipse, fillcolor=white];
    
    edge [style=dashed, color=gray];
    CVII -> marker_∅; CVII -> marker_∆; CVII -> marker_∂; CVII -> marker_∮;
    CVIII -> marker_∅; CVIII -> marker_∆; CVIII -> marker_∂;
    CIX -> marker_∅; CIX -> marker_∆; CIX -> marker_∂; CIX -> marker_∮;
    CX -> marker_∅; CX -> marker_∆; CX -> marker_∂; CX -> marker_∮; CX -> marker_⧖;
    CXI -> marker_∅; CXI -> marker_∆; CXI -> marker_∂; CXI -> marker_∮;
    CXII -> marker_∅; CXII -> marker_∆; CXII -> marker_∂; CXII -> marker_∮; CXII -> marker_⧖;
}}
"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(dot)
        return filename
    
    @staticmethod
    def execute_sql(query: str) -> list:
        import sqlite3
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            return [[f"Napaka: {str(e)}"]]
        finally:
            conn.close()
    
    @staticmethod
    def generate_kamen_file(num: int, title: str, desc: str) -> str:
        roman = SystemCore.to_roman(num)
        stone_id = f"C{roman}"
        filename = SystemCore.get_filename(num)
        section = (num - 100) + 12
        header = f"00 {section} RESNICAMI — Rozetni kamni ({roman.lower()})"
        
        content = f"""# {header}

---

## 🜂 Kamen {stone_id} — {title}: {desc}

**Kulturni kontekst:** [Dopolni]

**Pogoj:** [Dopolni]

---

### Tri pisave

| Tradicija (zgodovina) | Sistem (simbol) | Topologija (matematika) |
|---|---|---|
| [Dopolni] | [Dopolni] | [Dopolni] |
| [Dopolni] | [Dopolni] | [Dopolni] |
| [Dopolni] | [Dopolni] | [Dopolni] |

---

### Fonetično-ontološki rezi

**{title.split(':')[0].strip()}** — rez:

| Fragment | Pomen |
|---|---|
| **[]** | [] |
| **[]** | [] |

**Branje:** [Dopolni]

---

### ∴ Povezava

- [Dopolni]

---

### Zakon obogatitve

| Število | Priče | {stone_id} prispeva | Novo telo? |
|---|---|---|---|
| **X** | [Dopolni] | [Dopolni] | [Dopolni] |

**Kontrolni sklep:** [Dopolni]

---

### Mašinerija

- **PREIZKUS:** [Dopolni]

---

### Nujne napake

- **"[]"** — **ZMOTA:** [Dopolni]

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

| i | Implementacija | Evolucija | Stagnacija (meja) |
|---|---|---|---|
| 1 | [Dopolni] | [Dopolni] | [Dopolni] |

---

### Citati

→ [Dopolni]

---

## Tabela: Aksiomi (XXX-XXX)

| # | Aksiom | Onto-formula | Absolutna resnica | Znanost | Očitni znak |
|---|---|---|---|---|---|
| XXX | [Dopolni] | [Dopolni] | [Dopolni] | [Dopolni] | [Dopolni] |

---

## ∂ Vprašanja (XXX-XXX)

**XXX.** [Dopolni]

---

## Pečati

**∂ XXX — PEČAT:** [Dopolni]

---
*Naslednji kamen: [Dopolni]. Naslednja vrstica: [Dopolni]. Naslednje ∂: [Dopolni]. ∮*
"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return filename


# ============================================================================
# GLAVNO OKNO
# ============================================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SISTEM ∅→∆→∂→∮ - Rozetni Kamni v1.0")
        self.setGeometry(100, 100, 1024, 768)
        
        # Stil
        self.setStyleSheet("""
            QMainWindow { background-color: #2e3440; }
            QWidget { color: #e0e0e0; background-color: #2e3440; }
            QPushButton { background-color: #3b4252; border: 1px solid #4c566a; 
                         padding: 8px 16px; border-radius: 4px; }
            QPushButton:hover { background-color: #434c5e; }
            QPushButton[highlight="true"] { background-color: #88c0d0; }
            QLineEdit, QTextEdit, QComboBox { 
                background-color: #3b4252; border: 1px solid #4c566a; 
                color: #e0e0e0; padding: 8px; }
            QTableWidget { background-color: #2e3440; color: #e0e0e0; 
                           gridline-color: #4c566a; }
            QHeaderView::section { background-color: #3b4252; border: 1px solid #4c566a; }
            QLabel { color: #e0e0e0; }
            QTabWidget::pane { border: 1px solid #4c566a; }
        """)
        
        # Glavni layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        # Zavihe
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Inicializiraj zavihe
        self.init_generate_tab()
        self.init_verify_tab()
        self.init_database_tab()
        self.init_visualization_tab()
        self.init_query_tab()
        self.init_export_tab()
        self.init_search_tab()
        self.init_settings_tab()
        
        # Status bar
        self.status = QLabel("Pripravljen. ∅→∆→∂→∮")
        self.status.setStyleSheet("color: #88c0d0; padding: 8px;")
        main_layout.addWidget(self.status)
    
    # ========================================================================
    # INICIALIZACIJA ZAVIHOV
    # ========================================================================
    
    def init_generate_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("🜂 GENERIRANJE NOVIH KAMNOV")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        # Vnosna polja
        form = QFormLayout()
        self.num_input = QLineEdit("113")
        self.title_input = QLineEdit()
        self.desc_input = QLineEdit()
        
        form.addRow("Številka:", self.num_input)
        form.addRow("Naslov:", self.title_input)
        form.addRow("Opis:", self.desc_input)
        layout.addLayout(form)
        
        # Gumb
        btn = QPushButton("✨ GENERIRAJ KAMEN")
        btn.setProperty("highlight", "true")
        btn.clicked.connect(self.generate_kamen)
        layout.addWidget(btn)
        
        self.gen_result = QLabel("")
        layout.addWidget(self.gen_result)
        
        self.tabs.addTab(tab, "📝 Generiraj")
    
    def init_verify_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("🔍 PREVERJANJE DOKUMENTOV (T1-T4)")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        # Gumbi
        btn1 = QPushButton("🔎 PREVERI VSE")
        btn1.setProperty("highlight", "true")
        btn1.clicked.connect(self.verify_all)
        
        btn2 = QPushButton("📄 PREVERI IZBRANO")
        btn2.clicked.connect(self.verify_single)
        
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        
        # Izbor datoteke
        self.file_combo = QComboBox()
        # Avtomatsko preberi vse MD datoteke z vzorcem
        import glob
        md_files = glob.glob(str(DATA_DIR / "*resnicami-rozetni-kamni-*.md"))
        if md_files:
            self.file_combo.addItems([os.path.basename(f) for f in md_files])
        else:
            self.file_combo.addItems([
                "00-11-resnicami-rozetni-kamni-viii-tazv-dokazi-8.md",
                "01-12-resnicami-rozetni-kamni-x.md",
                "02-13-resnicami-rozetni-kamni-xi.md",
                "03-14-resnicami-rozetni-kamni-xii.md"
            ])
        layout.addWidget(self.file_combo)
        
        # Rezultati
        self.verify_table = QTableWidget()
        self.verify_table.setColumnCount(5)
        self.verify_table.setHorizontalHeaderLabels(["Datoteka", "T1", "T2", "T3", "T4"])
        self.verify_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.verify_table)
        
        self.tabs.addTab(tab, "✅ Preveri")
    
    def init_database_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("🗃️ UPRVLJANJE BAZE")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        # Gumbi
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 OSVEŽI")
        refresh_btn.clicked.connect(self.load_db_data)
        stats_btn = QPushButton("📊 STATISTIKA")
        stats_btn.clicked.connect(self.show_stats)
        btn_layout.addWidget(refresh_btn)
        btn_layout.addWidget(stats_btn)
        layout.addLayout(btn_layout)
        
        # Tabela
        self.db_table = QTableWidget()
        self.db_table.setColumnCount(5)
        self.db_table.setHorizontalHeaderLabels(["ID", "Naslov", "Status", "Datoteka", "# Aksiomi"])
        self.db_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.db_table)
        
        self.tabs.addTab(tab, "🗃️ Baza")
    
    def init_visualization_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("🖼️ VIZUALIZACIJA MREŽE")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        # Gumb
        btn = QPushButton("📊 USTVARI DOT")
        btn.setProperty("highlight", "true")
        btn.clicked.connect(self.export_dot_file)
        layout.addWidget(btn)
        
        # Prikaz
        self.dot_display = QTextEdit()
        self.dot_display.setReadOnly(True)
        self.dot_display.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        layout.addWidget(self.dot_display)
        
        info = QLabel("💡 Graphviz: dot -Tpng mreza.dot -o mreza.png")
        info.setStyleSheet("color: #88c0d0;")
        layout.addWidget(info)
        
        self.tabs.addTab(tab, "🖼️ Vizualizacija")
    
    def init_query_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("🔎 SQL POIZVEDBE")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("SELECT * FROM kamni ORDER BY stevilka")
        self.query_input.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        layout.addWidget(self.query_input)
        
        btn = QPushButton("▶ IZVEDI")
        btn.setProperty("highlight", "true")
        btn.clicked.connect(self.run_query)
        layout.addWidget(btn)
        
        self.query_table = QTableWidget()
        self.query_table.setColumnCount(1)
        self.query_table.horizontalHeader().setVisible(False)
        self.query_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.query_table)
        
        examples = QLabel("📌 Primeri: SELECT * FROM kamni | SELECT * FROM aksiomi WHERE id > 245")
        examples.setStyleSheet("color: #88c0d0;")
        layout.addWidget(examples)
        
        self.tabs.addTab(tab, "🔎 Poizvedbe")
    
    def init_export_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("📤 IZVOZ DOKUMENTOV")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        # Gumbi za izvoz
        btn_pdf = QPushButton("📄 IZVOZI V PDF")
        btn_pdf.setProperty("highlight", "true")
        btn_pdf.clicked.connect(self.export_to_pdf)
        layout.addWidget(btn_pdf)
        
        btn_md = QPushButton("📝 IZVOZI VSE MD")
        btn_md.clicked.connect(self.export_all_md)
        layout.addWidget(btn_md)
        
        btn_json = QPushButton("🗃️ IZVOZI BAZO (JSON)")
        btn_json.clicked.connect(self.export_database)
        layout.addWidget(btn_json)
        
        self.export_status = QLabel("")
        layout.addWidget(self.export_status)
        
        self.tabs.addTab(tab, "📤 Izvoz")
    
    def init_search_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("🔍 ISKALNIK")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        # Iskalno polje
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Vnesi iskalni izraz (npr. ∅, ∆, zrcalo, DA₂)...")
        layout.addWidget(self.search_input)
        
        # Gumb za iskanje
        search_btn = QPushButton("🔎 ISKI")
        search_btn.setProperty("highlight", "true")
        search_btn.clicked.connect(self.perform_search)
        layout.addWidget(search_btn)
        
        # Rezultati
        self.search_results = QTextEdit()
        self.search_results.setReadOnly(True)
        self.search_results.setStyleSheet("background-color: #1e1e1e; color: #d4d4d4;")
        layout.addWidget(self.search_results)
        
        self.tabs.addTab(tab, "🔍 Išči")
    
    def init_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        title = QLabel("⚙️  NASTAVITVE")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #88c0d0;")
        layout.addWidget(title)
        
        info = QLabel("""
        📋 SISTEM ∅→∆→∂→∮:
        • 7 kamnov (CVII-CXIII)
        • 21 aksiomov (236-256)
        • 21 vprašanj (12 odprtih)
        • 4 nosilci (MD, JSON, SQLite, PDF)
        
        🎯 FUNKCIJE:
        • Generiranje kamnov
        • Preverjanje T1-T4
        • Izvoz (PDF, ZIP, JSON)
        • Iskalnik po dokumentih
        • SQL poizvedbe
        • Mrežna vizualizacija
        
        📖 DOCUMENTACIJA:
        • STANJE-SISTEMA-18092026.md
        • Prikaz vseh funkij v zaviih
        
        🎯 NASLEDNJI KORAKI:
        1. Generiraj CXIV (114)
        2. Odgovori na ∂ vprašanja 71-76
        3. Dodaj nove vizualizacije
        
        📚 DOKUMENTACIJA:
        • Kamni: Markdown format
        • Baza: JSON + SQLite
        • Vizualizacija: DOT → PNG
        """)
        info.setStyleSheet("color: #d4d4d4;")
        layout.addWidget(info)
        
        self.tabs.addTab(tab, "⚙️  Nastavitve")
    
    # ========================================================================
    # FUNKCIJE (SLOTI)
    # ========================================================================
    
    def generate_kamen(self):
        try:
            num = int(self.num_input.text())
            title = self.title_input.text()
            desc = self.desc_input.text()
            if not title or not desc:
                QMessageBox.warning(self, "Napaka", "Vnesi naslov in opis!")
                return
            filename = SystemCore.generate_kamen_file(num, title, desc)
            self.gen_result.setText(f"✅ Ustvarjen: {filename}")
            self.status.setText(f"Generiran {SystemCore.to_roman(num)}")
            self.file_combo.addItem(filename)
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def verify_all(self):
        import glob
        self.verify_table.setRowCount(0)
        for fp in glob.glob(str(DATA_DIR / "*resnicami-rozetni-kamni-*.md")):
            r = SystemCore.verify_document(fp)
            row = self.verify_table.rowCount()
            self.verify_table.insertRow(row)
            self.verify_table.setItem(row, 0, QTableWidgetItem(os.path.basename(fp)))
            for i, test in enumerate(['T1', 'T2', 'T3', 'T4']):
                self.verify_table.setItem(row, i+1, QTableWidgetItem("✅" if r.get(test) else "❌"))
        self.status.setText("Preverjeno vseh dokumentov")
    
    def verify_single(self):
        fp = self.file_combo.currentText()
        r = SystemCore.verify_document(fp)
        self.verify_table.setRowCount(1)
        self.verify_table.setItem(0, 0, QTableWidgetItem(fp))
        for i, test in enumerate(['T1', 'T2', 'T3', 'T4']):
            self.verify_table.setItem(0, i+1, QTableWidgetItem("✅" if r.get(test) else "❌"))
        self.status.setText(f"Preverjen: {fp}")
    
    def load_db_data(self):
        data = SystemCore.load_json_db()
        kamni = data.get('kamni', {})
        self.db_table.setRowCount(len(kamni))
        for row, (k, v) in enumerate(kamni.items()):
            self.db_table.setItem(row, 0, QTableWidgetItem(k))
            self.db_table.setItem(row, 1, QTableWidgetItem(v.get('naslov', '')))
            self.db_table.setItem(row, 2, QTableWidgetItem(v.get('status', '')))
            self.db_table.setItem(row, 3, QTableWidgetItem(v.get('datoteka', '')))
            self.db_table.setItem(row, 4, QTableWidgetItem(str(len(v.get('aksiomi', [])))))
        self.status.setText(f"Naloženih: {len(kamni)} kamnov")
    
    def show_stats(self):
        data = SystemCore.load_json_db()
        s = data.get('statistika', {})
        msg = f"""📊 STATISTIKA:

Kamni: {s.get('skupaj_kamnov', 0)}
Aksiomi: {s.get('skupaj_aksiomov', 0)}
Vprašanja: {s.get('skupaj_vprasanj', 0)}
  → Odgovorjena: {s.get('odgovorjenih_vprasanj', 0)}
  → Odprta: {s.get('odprtih_vprasanj', 0)}
"""
        QMessageBox.information(self, "Statistika", msg)
    
    def export_dot_file(self):
        try:
            fp = SystemCore.export_dot()
            with open(fp, 'r', encoding='utf-8') as f:
                self.dot_display.setText(f.read())
            self.status.setText(f"Ustvarjen: {fp}")
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def run_query(self):
        query = self.query_input.toPlainText()
        if not query.strip():
            QMessageBox.warning(self, "Napaka", "Vnesi poizvedbo!")
            return
        results = SystemCore.execute_sql(query)
        self.query_table.setRowCount(len(results))
        self.query_table.setColumnCount(len(results[0]) if results else 1)
        for r, row in enumerate(results):
            for c, val in enumerate(row):
                self.query_table.setItem(r, c, QTableWidgetItem(str(val)))
        self.status.setText(f"Poizvedba: {len(results)} rezultatov")
    
    # ========================================================================
    # NOVE FUNKCIJE (Izvoz in Iskalnik)
    # ========================================================================
    
    def export_to_pdf(self):
        """Izvozi izbran dokument v PDF"""
        try:
            import glob
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Izvoz v PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options
            )
            if not file_path:
                return
            
            # Uporabi markdown → PDF (z markdown2 ali weasyprint)
            # Preprosta rešitev: uporabi browser (chromium)
            md_files = glob.glob(str(DATA_DIR / "*resnicami-rozetni-kamni-*.md"))
            if not md_files:
                QMessageBox.warning(self, "Napaka", "Ni najdenih MD datotek!")
                return
            
            # Izberi prvo datoteko
            import subprocess
            with open(md_files[0], 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # Ustvari začasno HTML
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Sistem ∅→∆→∂→∮</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    h1, h2, h3 {{ color: #2c3e50; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; }}
                    th {{ background-color: #3498db; color: white; }}
                </style>
            </head>
            <body>
            {md_content}
            </body>
            </html>
            """
            
            # Shrani začasno HTML
            temp_html = DATA_DIR / "temp.html"
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Pretvori HTML → PDF (z Chrome)
            try:
                subprocess.run([
                    'chrome', '--headless', '--disable-gpu', 
                    '--print-to-pdf=' + file_path, temp_html
                ], check=False)
                self.export_status.setText(f"✅ Izvožen: {file_path}")
                self.status.setText(f"PDF ustvarjen: {file_path}")
            except:
                # Alternativa: preprost tekst
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                self.export_status.setText(f"⚠️  Izvožen kot tekst: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka pri izvozu: {str(e)}")
    
    def export_all_md(self):
        """Izvozi vse MD datoteke v ZIP"""
        try:
            import zipfile
            import glob
            
            options = QFileDialog.Options()
            zip_path, _ = QFileDialog.getSaveFileName(
                self, "Izvoz v ZIP", "", "ZIP Files (*.zip);;All Files (*)", options=options
            )
            if not zip_path:
                return
            
            md_files = glob.glob(str(DATA_DIR / "*resnicami-rozetni-kamni-*.md"))
            if not md_files:
                QMessageBox.warning(self, "Napaka", "Ni najdenih MD datotek!")
                return
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for md_file in md_files:
                    zipf.write(md_file, os.path.basename(md_file))
            
            self.export_status.setText(f"✅ Izvožen: {zip_path}")
            self.status.setText(f"ZIP ustvarjen: {zip_path}")
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def export_database(self):
        """Izvozi bazo v JSON"""
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Izvoz baze", "database_backup.json", "JSON Files (*.json);;All Files (*)", options=options
            )
            if not file_path:
                return
            
            import shutil
            shutil.copy(JSON_FILE, file_path)
            self.export_status.setText(f"✅ Izvožen: {file_path}")
            self.status.setText(f"Baza izvožena")
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka: {str(e)}")
    
    def perform_search(self):
        """Išči po vseh MD datotekah"""
        try:
            import glob
            search_term = self.search_input.text()
            if not search_term.strip():
                QMessageBox.warning(self, "Napaka", "Vnesi iskalni izraz!")
                return
            
            md_files = glob.glob(str(DATA_DIR / "*resnicami-rozetni-kamni-*.md"))
            results = []
            
            for md_file in md_files:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if search_term.lower() in line.lower():
                            results.append(f"{os.path.basename(md_file)} (vrstica {i}): {line.strip()}")
            
            if results:
                self.search_results.setText("\n".join(results))
                self.status.setText(f"Najdenih: {len(results)} ujemanj")
            else:
                self.search_results.setText("Ni najdenih ujemanj.")
                self.status.setText("Ni ujemanj")
        except Exception as e:
            QMessageBox.critical(self, "Napaka", f"Napaka pri iskanju: {str(e)}")


# ============================================================================
# ZAGON
# ============================================================================

if __name__ == '__main__':
    if not PY_SIDE_OK:
        print("NAPAKA: PySide6 ni nameščeno!")
        print("Namestitev:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
