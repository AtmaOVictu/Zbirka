"""
TAZV Comprehension Machine — main_window_v5_integrated
=======================================================
Integrira:
  - 5-gumbni pipeline (ZAJEMI/REŽI/POKAŽI/PREVERI/SHRANI)
  - ProcessingPipeline + SymbolMapper (obstoječa arhitektura)
  - PreverbaBridge (Faza 5 most)
  - ARegister (apercepcija → operator)
  - CORPUS cevovod (∅→¬→∆→∂→⧖→∮→⟡)
  - SOMA kot QMessageBox.question (ne print!)
  - DOCTRINARIUM + KANON + CADENCE

Korpus: "SOMA_PROMPT spraša: Ali cutis, da drzi?"
         "Telo ni preverjevalec trditve — telo je bitje,
          ki ga test ne sme krsiti." (Obs11, 320d6f6a)

Razlika od main_window_v5.py:
  - Importa ProcessingPipeline + SymbolMapper
  - SOMA je QMessageBox.question, ne checkbox
  - ARegister prepozna uporabnikov vnos
  - CORPUS cevovod prikazan v posebnem tabu
  - PreverbaBridge integrira vse
"""

import sys
import json
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QPushButton, QTextEdit, QLabel, QMessageBox,
    QComboBox, QGroupBox, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QStatusBar,
    QMenu, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QAction

# Project imports — Faza 5
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from comprehension.core.preverba import Preverba, PreverbaResult, TestResult
from comprehension.core.soma import SomaCheck, SomaResult, SOMA_PROMPT_TEXT
from comprehension.core.doctrinarium import DoctrinariumCikel
from comprehension.core.cadence import Cadence
from comprehension.core.kanon_flow import KanonFlow
from comprehension.core.seriousness import SeriousnessClassifier
from comprehension.core.corpus_integrator import CorpusIntegrator, CorpusPhase
from comprehension.core.aregister_bridge import ARegisterBridge
from comprehension.core.preverba_bridge import PreverbaBridge

# Obstoječa arhitektura (Faza 3/4) — z try/except za primere ko manjkajo
try:
    from comprehension.core.processing_pipeline import ProcessingPipeline
    from comprehension.core.symbol_mapper import SymbolMapper
    HAS_PIPELINE = True
except ImportError:
    HAS_PIPELINE = False
    ProcessingPipeline = None
    SymbolMapper = None

try:
    from comprehension.core.module_semantics import MODULE_SEMANTICS, MODULE_ORDER
    HAS_SEMANTICS = True
except ImportError:
    HAS_SEMANTICS = False
    MODULE_SEMANTICS = {}
    MODULE_ORDER = ["∅","¬","∆","1","⧖","∮","⟡"]


PIPELINE_BARVE = [
    ("ZAJEMI  O",  "∅",  "#1B2838"),
    ("REZI  ⊘",   "¬",  "#B43A2E"),
    ("POKAZI  ∆", "∆",  "#D6A83A"),
    ("PREVERI  ⊢","⧖", "#D4AF37"),
    ("SHRANI  ∮", "∮",  "#080705"),
]


class TazvMainWindowIntegrated(QMainWindow):
    """
    TAZV v5 — integrirani UI z ProcessingPipeline + Preverba + CORPUS + ARegister.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TAZV Comprehension Machine — v5 Integrirani")
        self.setMinimumSize(1100, 750)

        # Faza 5 sistemi
        self.preverba = Preverba()
        self.doctrinarium = DoctrinariumCikel()
        self.cadence = Cadence()
        self.kanon = KanonFlow()
        self.seriousness = SeriousnessClassifier()
        self.corpus = CorpusIntegrator()
        self.aregister = ARegisterBridge()
        self.bridge = PreverbaBridge()

        # Obstoječa arhitektura
        self.pipeline = ProcessingPipeline() if HAS_PIPELINE else None
        self.symbol_mapper = SymbolMapper() if HAS_PIPELINE else None

        # Stanje
        self.current_modul = "⧖"
        self.current_trditev = ""
        self.current_kanon_id = None
        self.last_preverba = None
        self.current_soma = None
        self.last_pipeline_result = None
        self.areg_entry = None

        # DB
        self.db_path = Path(__file__).resolve().parent.parent / "data" / "tazv.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

        # UI
        self._build_ui()
        self._build_menu()
        self._apply_theme()
        self.cadence.zacetek_cikla()

    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        for p in ["schema.sql", "schema_patch_preverba.sql"]:
            f = self.db_path.parent / p
            if f.exists():
                with open(f, "r", encoding="utf-8") as fh:
                    try:
                        c.executescript(fh.read())
                    except Exception:
                        pass
        conn.commit()
        conn.close()

    # --- UI ---

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)
        lay.addWidget(self._pipeline())

        self.tabs = QTabWidget()
        self.tabs.addTab(self._tab_zajem(),       "∅ Zajem")
        self.tabs.addTab(self._tab_preverba(),     "⧖ Preverba")
        self.tabs.addTab(self._tab_corpus(),      "∮ CORPUS")
        self.tabs.addTab(self._tab_kanon(),       "∮ Kanon")
        self.tabs.addTab(self._tab_doctrinarium(),"∴ Doctrinarium")
        self.tabs.addTab(self._tab_cadence(),     "∮ Cadence")
        self.tabs.addTab(self._tab_zgodovina(),   "⟡ Zgodovina")
        lay.addWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Pripravljen. Zajemi trditev → ∅")

    def _pipeline(self):
        g = QGroupBox("R-7 Pipeline")
        h = QHBoxLayout()
        for besedilo, glyph, barva in PIPELINE_BARVE:
            btn = QPushButton(besedilo)
            fg = "#F3E9D2" if barva in ("#1B2838","#080705") else "#1B2838"
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {barva}; color: {fg};
                    font-size: 14px; font-weight: bold;
                    padding: 12px 24px; border-radius: 6px;
                    border: 2px solid {barva};
                }}
                QPushButton:hover {{ border: 2px solid #F3E9D2; }}
            """)
            akcija = besedilo.split()[0]
            cb = {
                "ZAJEMI": self.act_zajemi, "REZI": self.act_rezi,
                "POKAZI": self.act_pokazi, "PREVERI": self.act_preveri,
                "SHRANI": self.act_shrani,
            }[akcija]
            btn.clicked.connect(cb)
            h.addWidget(btn)
        g.setLayout(h)
        return g

    def _tab_zajem(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∅ ZAJEM — vnesi trditev</b>"))

        self.input_trditev = QTextEdit()
        self.input_trditev.setPlaceholderText("Vnesi trditev za preverbo...")
        v.addWidget(self.input_trditev)

        f = QFormLayout()
        self.combo_modul = QComboBox()
        self.combo_modul.addItems(MODULE_ORDER)
        self.combo_modul.setCurrentText("⧖")
        f.addRow("R-7 modul:", self.combo_modul)

        # ARegister prepoznavanje
        self.lbl_areg = QLabel("ARegister: —")
        f.addRow("Apercepcija:", self.lbl_areg)

        self.input_kontekst = QTextEdit()
        self.input_kontekst.setMaximumHeight(80)
        self.input_kontekst.setPlaceholderText(
            'Kontekst (JSON): {"jedro":"...","agent":"..."}')
        f.addRow("Kontekst:", self.input_kontekst)

        # CORPUS polja (za zunanje sisteme)
        self.input_izvorno_ime = QTextEdit()
        self.input_izvorno_ime.setMaximumHeight(40)
        self.input_izvorno_ime.setPlaceholderText("Izvorno ime sistema (npr. Alkimija) — opcijsko")
        f.addRow("CORPUS ime:", self.input_izvorno_ime)

        self.input_izvorni_op = QTextEdit()
        self.input_izvorni_op.setMaximumHeight(40)
        self.input_izvorni_op.setPlaceholderText("Izvorni operator (npr. nigredo) — opcijsko")
        f.addRow("CORPUS op.:", self.input_izvorni_op)

        v.addLayout(f)

        self.lbl_zajem = QLabel("")
        v.addWidget(self.lbl_zajem)
        v.addStretch()
        return w

    def _tab_preverba(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>⧖ PREVERBA — 5 + 10 preizkusov</b>"))
        self.txt_preverba = QTextEdit()
        self.txt_preverba.setReadOnly(True)
        v.addWidget(self.txt_preverba)
        self.lbl_serious = QLabel("")
        self.lbl_serious.setStyleSheet("font-size: 16px; font-weight: bold;")
        v.addWidget(self.lbl_serious)
        return w

    def _tab_corpus(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∮ CORPUS — 7-fazni prevajalski cevovod ∅→¬→∆→∂→⧖→∮→⟡</b>"))

        # Mapping 5 gumbov → 7 faz
        mapping = self.corpus.map_5gumbov_v_corpus()
        map_html = "<table border='1' cellpadding='6'><tr><th>UI Gumb</th><th>Glyph</th><th>CORPUS faze</th></tr>"
        for gumb, glyph, faze in mapping:
            map_html += f"<tr><td>{gumb}</td><td>{glyph}</td><td>{', '.join(faze)}</td></tr>"
        map_html += "</table>"
        self.lbl_corpus_map = QLabel(map_html)
        v.addWidget(self.lbl_corpus_map)

        self.txt_corpus = QTextEdit()
        self.txt_corpus.setReadOnly(True)
        v.addWidget(self.txt_corpus)
        return w

    def _tab_kanon(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∮ KANON — statusni avtomat</b>"))
        self.tbl_kanon = QTableWidget(0, 5)
        self.tbl_kanon.setHorizontalHeaderLabels(["ID","Modul","Trditev","Status","Dokaz"])
        self.tbl_kanon.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        v.addWidget(self.tbl_kanon)
        h = QHBoxLayout()
        b1 = QPushButton("Osvezi"); b1.clicked.connect(self.osvezi_kanon)
        h.addWidget(b1)
        v.addLayout(h)
        return w

    def _tab_doctrinarium(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∴ DOCTRINARIUM — cikel ∴→∆→⊢→∮</b>"))
        self.txt_doc = QTextEdit()
        self.txt_doc.setReadOnly(True)
        v.addWidget(self.txt_doc)
        b = QPushButton("Osvezi"); b.clicked.connect(self.osvezi_doc)
        v.addWidget(b)
        return w

    def _tab_cadence(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∮ CADENCE — mikro/makro kadenco</b>"))
        self.lbl_faza = QLabel("")
        self.lbl_faza.setStyleSheet("font-size: 18px; font-weight: bold;")
        v.addWidget(self.lbl_faza)
        self.txt_cad = QTextEdit()
        self.txt_cad.setReadOnly(True)
        v.addWidget(self.txt_cad)
        b = QPushButton("Osvezi"); b.clicked.connect(self.osvezi_cad)
        v.addWidget(b)
        return w

    def _tab_zgodovina(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>⟡ ZGODOVINA — proof_log</b>"))
        self.tbl_zg = QTableWidget(0, 6)
        self.tbl_zg.setHorizontalHeaderLabels(["Cas","Modul","Trditev","Rezultat","SOMA","Kanon"])
        self.tbl_zg.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        v.addWidget(self.tbl_zg)
        b = QPushButton("Osvezi"); b.clicked.connect(self.osvezi_zg)
        v.addWidget(b)
        return w

    def _build_menu(self):
        mb = self.menuBar()
        m = mb.addMenu("∂ Globina")
        for n in ["povrsinski","strukturni","ontoloski","absolutni"]:
            a = QAction(n, self)
            a.triggered.connect(lambda _,x=n: self.status.showMessage(f"∂ Globina: {x}"))
            m.addAction(a)

    def _apply_theme(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #1B2838; }
            QGroupBox { color: #F3E9D2; border: 1px solid #D6A83A; border-radius: 4px; margin-top: 8px; padding-top: 12px; }
            QGroupBox::title { color: #D6A83A; subcontrol-origin: margin; left: 10px; }
            QLabel { color: #F3E9D2; }
            QTextEdit { background-color: #0F1A26; color: #F3E9D2; border: 1px solid #D6A83A; }
            QComboBox { background-color: #0F1A26; color: #F3E9D2; border: 1px solid #D6A83A; }
            QTableWidget { background-color: #0F1A26; color: #F3E9D2; gridline-color: #D6A83A; }
            QHeaderView::section { background-color: #1B2838; color: #D6A83A; }
            QTabWidget::pane { border: 1px solid #D6A83A; }
            QTabBar::tab { background-color: #1B2838; color: #F3E9D2; padding: 8px 16px; }
            QTabBar::tab:selected { background-color: #D6A83A; color: #1B2838; }
            QStatusBar { background-color: #080705; color: #D6A83A; }
            QMenu { background-color: #1B2838; color: #F3E9D2; }
        """)

    # --- Pipeline akcije ---

    def _get_kontekst(self):
        t = self.input_kontekst.toPlainText().strip()
        if not t: return {}
        try: return json.loads(t)
        except: return {"_raw": t}

    def act_zajemi(self):
        """∅ ZAJEMI — zajemi trditev + ARegister prepoznavanje."""
        self.current_trditev = self.input_trditev.toPlainText().strip()
        if not self.current_trditev:
            QMessageBox.warning(self, "∅", "Trditev je prazna.")
            return

        # ARegister prepoznavanje (iz korpusa)
        self.areg_entry = self.aregister.recognize(self.current_trditev)
        if self.areg_entry:
            self.lbl_areg.setText(
                f"<b>ARegister:</b> {self.areg_entry.glyph} — {self.areg_entry.perception[:60]}")
            # Ce ARegister prepozna modul, ga ponudi
            self.combo_modul.setCurrentText(self.areg_entry.glyph)
            self.current_modul = self.areg_entry.glyph
        else:
            self.lbl_areg.setText("ARegister: ni prepoznan — rocni izbor")
            self.current_modul = self.combo_modul.currentText()

        kont = self._get_kontekst()

        # ProcessingPipeline (ce obstaja)
        if self.pipeline:
            try:
                self.last_pipeline_result = self.pipeline.process(self.current_trditev)
            except Exception:
                self.last_pipeline_result = {"statement": self.current_trditev}

        # KANON dodaj kot KANDIDAT
        ke = self.kanon.dodaj(self.current_modul, self.current_trditev)
        self.current_kanon_id = ke.id
        self.cadence.log_mikro(self.current_modul, "ZAJEMI", "OK")

        # DOCTRINARIUM dodaj doktrino
        doc = self.doctrinarium.dodaj_doktrino(
            self.current_modul, self.current_trditev,
            princip=kont.get("princip",""), nujnost=kont.get("nujnost",""))

        self.lbl_zajem.setText(
            f"<b>✓ Zajeto:</b> modul={self.current_modul} | "
            f"kanon={ke.id} | doc={doc.id}")
        self.status.showMessage(f"∅ Zajeto: {ke.id} — ARegister: {self.areg_entry.glyph if self.areg_entry else 'rocno'} — pripravljen za REZI")

    def act_rezi(self):
        """¬ REZI — CORPUS PREVEDI: reže izvorni operator na korenski glif."""
        if not self.current_trditev:
            QMessageBox.warning(self, "¬", "Najprej zajemi (∅).")
            return

        # CORPUS PREVEDI: ce imamo izvorno ime + operator
        izv_ime = self.input_izvorno_ime.toPlainText().strip()
        izv_op = self.input_izvorni_op.toPlainText().strip()

        if izv_ime and izv_op:
            tabela = self.corpus.najdi_preslikavo(izv_ime, izv_op)
            if tabela:
                self.status.showMessage(
                    f"¬ REZI: {izv_op} → {tabela.korenski_glif} ({tabela.preverba} kot)")
            else:
                self.status.showMessage(f"¬ REZI: preslikava za {izv_ime}:{izv_op} ni najdena")
        else:
            # Brez CORPUS — rocni rez
            jedro = self.current_trditev.split(".")[0].strip() or self.current_trditev[:80]
            self.status.showMessage(f"¬ REZI: jedro izlusceno ({len(jedro)} znakov)")

        self.cadence.log_mikro(self.current_modul, "REZI", "OK")

    def act_pokazi(self):
        """∆ POKAZI — CORPUS PRESLIKAJ + VSTOP."""
        if not self.current_trditev:
            QMessageBox.warning(self, "∆", "Najprej zajemi (∅).")
            return

        izv_ime = self.input_izvorno_ime.toPlainText().strip()
        izv_op = self.input_izvorni_op.toPlainText().strip()

        html = "<div style='color:#F3E9D2; font-family: monospace;'>"
        html += f"<h3>∆ POKAZI / PRESLIKAJ</h3>"
        html += f"<p><b>Trditev:</b> {self.current_trditev}</p>"
        html += f"<p><b>Modul:</b> {self.current_modul}</p>"

        if self.areg_entry:
            html += f"<p><b>ARegister:</b> {self.areg_entry.glyph} — {self.areg_entry.perception}</p>"
            html += f"<p><b>Vprasanje:</b> <i>{self.areg_entry.inquiry}</i></p>"

        if izv_ime and izv_op:
            tabela = self.corpus.najdi_preslikavo(izv_ime, izv_op)
            if tabela:
                html += f"<p><b>CORPUS preslikava:</b> {izv_op} → {tabela.korenski_glif}</p>"
                html += f"<p><b>Modul:</b> {tabela.modul} | <b>Kot:</b> {tabela.preverba}</p>"
                html += f"<p><b>VSTOP ∂:</b> preslikava postane operativna v modulu {tabela.modul}</p>"
            else:
                html += f"<p style='color:#FF9800'>Preslikava ni najdena — dodaj v prevajalsko tabelo</p>"

        html += "<p><i>Pripravljen za PREVERI ⊢</i></p>"
        html += "</div>"

        self.txt_preverba.setHtml(html)
        self.cadence.log_mikro(self.current_modul, "POKAZI", "OK")
        self.tabs.setCurrentIndex(1)
        self.status.showMessage("∆ Pokazano — pripravljen za PREVERI ⊢")

    def act_preveri(self):
        """⧖ PREVERI — 5 preizkusov + 10 preizkusov A-J + SOMA (QMessageBox)."""
        if not self.current_trditev:
            QMessageBox.warning(self, "⧖", "Najprej zajemi (∅).")
            return

        kont = self._get_kontekst()

        # Odpelji preverbo
        r = self.preverba.run_all(self.current_modul, self.current_trditev, kont)
        self.last_preverba = r

        # Seriousness
        s = self.seriousness.classify(r.rezultati_5, r.ego_flag,
            self.current_soma.evaluate() if self.current_soma else "")

        # Izpisi rezultat
        self.txt_preverba.setHtml(self._fmt_result(r, s))
        sc = {"S1":"#4CAF50","S2":"#FF9800","S3":"#F44336","S4":"#8B0000"}
        self.lbl_serious.setText(
            f"<span style='color:{sc.get(s.nivo)}'>"
            f"{s.nivo} — {s.opis} | {s.akcija}</span>")

        # KANON prehod
        if self.current_kanon_id:
            akc = {"PASS":"preverba_pass","FAIL":"preverba_fail","BLISK":"preverba_blisk"}
            try:
                self.kanon.prehod(self.current_kanon_id, akc.get(r.skupni_rezultat, "preverba_fail"))
            except Exception:
                pass

        # DOCTRINARIUM
        doc_id = f"DOC-{len(self.doctrinarium.doctrinarium):04d}"
        trn = self.doctrinarium.dodaj_vajo(doc_id, f"Preverba: {self.current_trditev[:60]}")
        self.doctrinarium.preveri_vajo(trn.id, r.skupni_rezultat, "", r.ego_flag, r.dokaz_nivo)

        self._log_proof(r, s)
        self.cadence.log_mikro(self.current_modul, "PREVERI", r.skupni_rezultat)

        # SOMA preverba kot QMessageBox.question
        if r.skupni_rezultat == "PASS":
            self._soma_qmessagebox()
        else:
            self.status.showMessage(f"⧖ Preverba {r.skupni_rezultat} — {s.nivo}")

    def _soma_qmessagebox(self):
        """
        SOMA preverba kot QMessageBox.question.
        Korpus: "Telo ni preverjevalec trditve — telo je bitje,
                 ki ga test ne sme krsiti." (Obs11, 320d6f6a)
        """
        msg = QMessageBox(self)
        msg.setWindowTitle("⧖ Preverba Soma")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("Preverba soma")
        msg.setInformativeText(
            "Telo ni preverjevalec trditve — telo je bitje, ki ga test ne sme krsiti.\n\n"
            "Ali cutis, da drzi?\n\n"
            "1. Ali dih ostaja prost?\n"
            "2. Ali cutis mravljince (napetost, kracenje)?\n"
            "3. Ali je napetost v celjusti ali ramenih?\n\n"
            "Ce karkoli je DA (krsitev), test je prevec agresiven.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.button(QMessageBox.StandardButton.Yes).setText("DA — telo drzi")
        msg.button(QMessageBox.StandardButton.No).setText("NE — telo protestira")

        result = msg.exec()

        if result == QMessageBox.StandardButton.Yes:
            # SOMA_PASS
            self.current_soma = SomaCheck(dih_prost=True, mravljinci=False,
                                           napetost_cejust=False, napetost_ramena=False)
            self.status.showMessage("SOMA PASS — pripravljen za SHRANI ∮")
        else:
            # SOMA_FAIL — telo protestira
            self.current_soma = SomaCheck(dih_prost=False, mravljinci=True,
                                           napetost_cejust=True, napetost_ramena=False)
            self.status.showMessage("SOMA FAIL — test krsi telo")

        self.cadence.log_mikro(self.current_modul, "SOMA", self.current_soma.evaluate())

    def act_shrani(self):
        """∮ SHRANI — ATLAS + ODPRI (KANON integracija)."""
        if not self.current_kanon_id:
            QMessageBox.warning(self, "∮", "Najprej zajemi in preveri.")
            return
        if not self.last_preverba:
            QMessageBox.warning(self, "∮", "Najprej odpelji preverbo (⊢).")
            return

        r = self.last_preverba
        soma_ok = self.current_soma and self.current_soma.evaluate() == "SOMA_PASS"

        if r.skupni_rezultat == "PASS" and soma_ok:
            # KANON prehod
            self.kanon.prehod(self.current_kanon_id, "soma_integracija")
            asv_id = f"ASV-{len(self.doctrinarium.assur_valid):04d}"
            self.doctrinarium.integriraj(asv_id, "Integrirano v kanon", zivljeno=True)
            self.cadence.log_mikro(self.current_modul, "SHRANI", "KANON")

            # CORPUS cevovod (ce imamo zunanji sistem)
            izv_ime = self.input_izvorno_ime.toPlainText().strip()
            izv_op = self.input_izvorni_op.toPlainText().strip()
            if izv_ime and izv_op:
                corpus_rez = self.corpus.odpelji_cevovod(
                    izv_ime, izv_op,
                    soma_rezultat="SOMA_PASS",
                    preverba_rezultati=r.rezultati_5)
                self._prikazi_corpus(corpus_rez)

            self.status.showMessage(f"∮ Shranjeno v KANON: {self.current_kanon_id}")
            QMessageBox.information(self, "∮ Kanon",
                f"Trditev shranjena v KANON.\n\n"
                f"ID: {self.current_kanon_id}\n"
                f"Dokaz: {r.dokaz_nivo}\nSOMA: PASS")
        elif r.skupni_rezultat == "PASS" and not soma_ok:
            QMessageBox.warning(self, "∮", "SOMA ni sla skozi.\n"
                "Telo mora potrditi pred shranitvijo v KANON.")
        else:
            QMessageBox.warning(self, "∮", f"Preverba ni PASS ({r.skupni_rezultat}).\n"
                "Shranjeno kot MEGLA.")
        self.osvezi_kanon()

    # --- Format / prikaz ---

    def _fmt_result(self, r, s):
        h = "<div style='color:#F3E9D2; font-family: monospace;'>"
        c = {"PASS":"#4CAF50","FAIL":"#F44336","BLISK":"#FF9800"}
        h += f"<h2 style='color:{c.get(r.skupni_rezultat)}'>⧖ PREVERBA: {r.skupni_rezultat}</h2>"
        if r.dokaz_nivo:
            h += f"<p><b>Dokaz:</b> {r.dokaz_nivo}</p>"

        h += "<h3>5 PREIZKUSOV</h3><table border='1' cellpadding='6'>"
        h += "<tr><th>Preizkus</th><th>Glyph</th><th>Rezultat</th></tr>"
        gl = {"cas":"⧖","drugi":"⟡","tretji":"∴","nujno":"∅","ego":"⊘"}
        for n, v in r.rezultati_5.items():
            cc = c.get(v, "#F3E9D2")
            h += f"<tr><td>{n}</td><td>{gl.get(n,'?')}</td><td style='color:{cc}'>{v}</td></tr>"
        h += "</table>"

        h += "<h3>10 PREIZKUSOV A-J</h3><table border='1' cellpadding='6'>"
        h += "<tr><th>Ozn</th><th>Ime</th><th>R-7</th><th>Rezultat</th></tr>"
        ajm = {"A_KERNEL":("A","∅"),"B_OPERATOR":("B","¬"),"C_AGENT":("C","∆"),
               "D_MICRO_AKCIJA":("D","1"),"E_SOMA":("E","⧖"),"F_CAS_POT":("F","⧖"),
               "G_DOKAZ":("G","∮"),"H_UI":("H","⟡"),"I_SKUPNOST_SUM":("I","⟡"),
               "J_KANON_ARHIV":("J","∮")}
        for n, v in r.rezultati_aj.items():
            cc = c.get(v, "#F3E9D2")
            oz, gy = ajm.get(n, ("?","?"))
            h += f"<tr><td>{oz}</td><td>{n.split('_',1)[1] if '_' in n else n}</td><td>{gy}</td><td style='color:{cc}'>{v}</td></tr>"
        h += "</table>"

        h += f"<p><b>Suma:</b> {r.suma_opis}</p>"
        h += f"<p><b>Kanon:</b> {r.kanon_status}</p>"
        h += f"<p><b>Resnost:</b> {s.nivo} — {s.opis} | {s.akcija}</p>"
        if r.ego_flag:
            h += "<p style='color:#F44336'><b>⚠ EGO FLAG:</b> volja posreduje — zamrzni modul</p>"
        h += "</div>"
        return h

    def _prikazi_corpus(self, rezultati):
        """Prikaže CORPUS cevovod rezultate."""
        h = "<div style='color:#F3E9D2; font-family: monospace;'>"
        h += "<h3>∮ CORPUS cevovod — 7 faz</h3>"
        h += "<table border='1' cellpadding='6'>"
        h += "<tr><th>Faza</th><th>Glyph</th><th>Rezultat</th><th>Opis</th></tr>"
        for r in rezultati:
            c = "#4CAF50" if r.rezultat == "PASS" else "#F44336" if "FAIL" in r.rezultat else "#FF9800"
            h += f"<tr><td>{r.faza}</td><td>{r.glif}</td><td style='color:{c}'>{r.rezultat}</td><td>{r.opis[:80]}</td></tr>"
        h += "</table></div>"
        self.txt_corpus.setHtml(h)

    def osvezi_kanon(self):
        self.tbl_kanon.setRowCount(0)
        bmap = {"KANON":QColor("#D4AF37"),"PREVERJEN":QColor("#D6A83A"),
                "KANDIDAT":QColor("#F3E9D2"),"MEGLA":QColor("#666"),"ARHIV":QColor("#333")}
        for e in self.kanon.entries:
            row = self.tbl_kanon.rowCount()
            self.tbl_kanon.insertRow(row)
            self.tbl_kanon.setItem(row, 0, QTableWidgetItem(e.id))
            self.tbl_kanon.setItem(row, 1, QTableWidgetItem(e.modul))
            self.tbl_kanon.setItem(row, 2, QTableWidgetItem(e.trditev[:80]))
            it = QTableWidgetItem(e.status)
            it.setForeground(bmap.get(e.status, QColor("#F3E9D2")))
            self.tbl_kanon.setItem(row, 3, it)
            self.tbl_kanon.setItem(row, 4, QTableWidgetItem(e.dokaz_nivo))

    def osvezi_doc(self):
        d = self.doctrinarium
        h = "<div style='color:#F3E9D2; font-family: monospace;'>"
        h += f"<h3>∴ DOCTRINARIUM ({len(d.doctrinarium)})</h3>"
        for doc in d.doctrinarium[-10:]:
            st = d.cikel_status(doc.id)
            h += f"<p><b>{doc.id}</b> [{doc.modul}] {doc.trditev[:60]}<br>{st.get('status','?')} — {st.get('napredek','?')}</p>"
        h += f"<h3>∆ TRAINARIUM ({len(d.trainarium)})</h3>"
        for t in d.trainarium[-10:]:
            h += f"<p><b>{t.id}</b> | {t.vaja[:60]} | zadnji: {t.zadnji_rezultat}</p>"
        h += f"<h3>⊢ ASSUR-VALID ({len(d.assur_valid)})</h3>"
        for a in d.assur_valid[-10:]:
            h += f"<p><b>{a.id}</b> | {a.preverba_rezultat} | dokaz: {a.dokaz_nivo}</p>"
        h += f"<h3>∮ MEMORI ({len(d.memori)})</h3>"
        for m in d.memori[-10:]:
            h += f"<p><b>{m.id}</b> | zivljeno: {m.zivljeno} | {m.integracija[:60]}</p>"
        h += "</div>"
        self.txt_doc.setHtml(h)

    def osvezi_cad(self):
        g, i, dn = self.cadence.dnevna_faza()
        self.lbl_faza.setText(f"DAN {dn}/7 | {g} {i.upper()}")
        h = "<div style='color:#F3E9D2; font-family: monospace;'>"
        h += f"<h3>∮ MAKRO — P-7d cikel</h3>"
        if self.cadence.makro_cikli:
            c = self.cadence.makro_cikli[-1]
            h += f"<p><b>{c.cikel_id}</b> | dan {c.dan}/7 | {c.faza_glyph} {c.faza_ime}</p>"
            h += f"<p>{c.preverbe_pass} PASS / {c.preverbe_fail} FAIL | {c.integracije} integracij</p>"
        h += f"<h3>∂ MIKRO ({len(self.cadence.mikro_log)})</h3>"
        for m in self.cadence.mikro_log[-20:]:
            h += f"<p>{m.timestamp[:19]} | {m.modul} | {m.operacija} | {m.rezultat}</p>"
        h += "</div>"
        self.txt_cad.setHtml(h)

    def osvezi_zg(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        try:
            c.execute("SELECT timestamp,modul,statement,result,soma,kanon_status "
                      "FROM proof_log ORDER BY timestamp DESC LIMIT 100")
            rows = c.fetchall()
        except sqlite3.OperationalError:
            rows = []
        conn.close()
        self.tbl_zg.setRowCount(0)
        for rd in rows:
            row = self.tbl_zg.rowCount()
            self.tbl_zg.insertRow(row)
            for col, val in enumerate(rd):
                self.tbl_zg.setItem(row, col, QTableWidgetItem(str(val or "")))

    def _log_proof(self, r, s):
        tid = hashlib.md5(
            f"{self.current_modul}:{self.current_trditev}:{datetime.now().isoformat()}"
            .encode()).hexdigest()[:12]
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""INSERT OR REPLACE INTO proof_log
            (test_id,modul,statement,phase,result,ego_flag,soma,dokaz,seriousness,
             kanon_status,rezultati_5,rezultati_aj)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
            (tid, self.current_modul, self.current_trditev, self.current_modul,
             r.skupni_rezultat, int(r.ego_flag),
             self.current_soma.evaluate() if self.current_soma else "",
             r.dokaz_nivo, s.nivo, r.kanon_status,
             json.dumps(r.rezultati_5), json.dumps(r.rezultati_aj)))
        conn.commit()
        conn.close()


def main():
    app = QApplication(sys.argv)
    win = TazvMainWindowIntegrated()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
