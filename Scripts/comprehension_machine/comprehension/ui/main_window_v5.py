"""
TAZV Comprehension Machine — main_window_v5
=============================================
Faza 5: Preverba sistem integriran v UI.

5-GUMBNI PIPELINE:
  1. ZAJEMI  O  (∅) — zajemi trditev
  2. REZI    ⊘  (¬) — rezi/negiraj
  3. POKAZI  ∆  (∆) — pokazi/manifest
  4. PREVERI ⊢  (⧖)— preveri (5 preizkusov + SOMA)
  5. SHRANI  ∮  (∮) — shrani v kanon
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
    QComboBox, QGroupBox, QFormLayout, QCheckBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QStatusBar, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QAction

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
from comprehension.core.preverba import Preverba, PreverbaResult, TestResult, KanonStatus
from comprehension.core.soma import SomaCheck, SomaResult, SOMA_PROMPT_TEXT
from comprehension.core.doctrinarium import DoctrinariumCikel
from comprehension.core.cadence import Cadence
from comprehension.core.kanon_flow import KanonFlow
from comprehension.core.seriousness import SeriousnessClassifier


BARVE = {
    "∅": "#1B2838", "¬": "#B43A2E", "∆": "#D6A83A", "1": "#C77800",
    "⧖": "#D4AF37", "∮": "#080705", "⟡": "#F3E9D2",
}

PIPELINE = [
    ("ZAJEMI  O",  "∅",  "#1B2838"),
    ("REZI  ⊘",   "¬",  "#B43A2E"),
    ("POKAZI  ∆", "∆",  "#D6A83A"),
    ("PREVERI  ⊢","⧖", "#D4AF37"),
    ("SHRANI  ∮", "∮",  "#080705"),
]


class TazvMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TAZV Comprehension Machine — v5 Preverba")
        self.setMinimumSize(1100, 750)

        self.preverba = Preverba()
        self.doctrinarium = DoctrinariumCikel()
        self.cadence = Cadence()
        self.kanon = KanonFlow()
        self.seriousness = SeriousnessClassifier()

        self.current_modul = "⧖"
        self.current_trditev = ""
        self.current_kanon_id = None
        self.last_result = None
        self.current_soma = None

        self.db_path = Path(__file__).resolve().parent.parent / "data" / "tazv.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self._build_ui()
        self._build_menu()
        self._apply_theme()
        self.cadence.zacetek_cikla()

    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        for p in ["schema.sql", "schema_patch_preverba.sql"]:
            f = Path(__file__).resolve().parent.parent / "data" / p
            if f.exists():
                with open(f, "r", encoding="utf-8") as fh:
                    c.executescript(fh.read())
        conn.commit()
        conn.close()

    # --- UI ---

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        lay = QVBoxLayout(central)
        lay.addWidget(self._pipeline())

        self.tabs = QTabWidget()
        self.tabs.addTab(self._tab_zajem(),    "∅ Zajem")
        self.tabs.addTab(self._tab_preverba(),  "⧖ Preverba")
        self.tabs.addTab(self._tab_soma(),      "⧖ Soma")
        self.tabs.addTab(self._tab_kanon(),      "∮ Kanon")
        self.tabs.addTab(self._tab_doctrinarium(),"∴ Doctrinarium")
        self.tabs.addTab(self._tab_cadence(),   "∮ Cadence")
        self.tabs.addTab(self._tab_zgodovina(), "⟡ Zgodovina")
        lay.addWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Pripravljen. Zajemi trditev -> ∅")

    def _pipeline(self):
        g = QGroupBox("R-7 Pipeline")
        h = QHBoxLayout()
        for besedilo, glyph, barva in PIPELINE:
            btn = QPushButton(besedilo)
            fg = "#F3E9D2" if barva in ("#1B2838", "#080705") else "#1B2838"
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
            callback = {
                "ZAJEMI": self.act_zajemi, "REZI": self.act_rezi,
                "POKAZI": self.act_pokazi, "PREVERI": self.act_preveri,
                "SHRANI": self.act_shrani,
            }[akcija]
            btn.clicked.connect(callback)
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
        self.combo_modul.addItems(["∅","¬","∆","1","⧖","∮","⟡"])
        self.combo_modul.setCurrentText("⧖")
        f.addRow("R-7 modul:", self.combo_modul)

        self.input_kontekst = QTextEdit()
        self.input_kontekst.setMaximumHeight(100)
        self.input_kontekst.setPlaceholderText(
            'Kontekst (JSON): {"jedro":"...","agent":"...","operator":"⧖"}')
        f.addRow("Kontekst:", self.input_kontekst)
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

    def _tab_soma(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>⧖ SOMA — telo kot bitje, ne kot preverjevalec</b>"))
        v.addWidget(QLabel("<i>Telo ni preverjevalec trditve — telo je bitje, "
                           "ki ga test ne sme krsiti.</i>"))
        f = QFormLayout()
        self.chk_dih = QCheckBox("Dih je prost"); self.chk_dih.setChecked(True)
        self.chk_mra = QCheckBox("Mravljinci (napetost)")
        self.chk_cel = QCheckBox("Celjust stisnjena")
        self.chk_ram = QCheckBox("Ramena dvignjena")
        for c in (self.chk_dih, self.chk_mra, self.chk_cel, self.chk_ram):
            f.addRow(c)
        v.addLayout(f)

        btn = QPushButton("SOMA CHECK")
        btn.clicked.connect(self.run_soma)
        v.addWidget(btn)

        self.lbl_soma = QLabel("")
        self.lbl_soma.setStyleSheet("font-size: 16px; font-weight: bold;")
        v.addWidget(self.lbl_soma)

        self.txt_soma = QTextEdit()
        self.txt_soma.setReadOnly(True)
        self.txt_soma.setMaximumHeight(80)
        v.addWidget(self.txt_soma)
        v.addStretch()
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
        b2 = QPushButton("Export JSON"); b2.clicked.connect(self.export_kanon)
        h.addWidget(b2)
        v.addLayout(h)
        return w

    def _tab_doctrinarium(self):
        w = QWidget()
        v = QVBoxLayout(w)
        v.addWidget(QLabel("<b>∴ DOCTRINARIUM — cikel ∴->∆->⊢->∮</b>"))
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

    # --- Menu ---

    def _build_menu(self):
        mb = self.menuBar()
        m = mb.addMenu("∂ Globina")
        for n in ["povrsinski","strukturni","ontoloski","absolutni"]:
            a = QAction(n, self)
            a.triggered.connect(lambda _,x=n: self.status.showMessage(f"∂ Globina: {x}"))
            m.addAction(a)
        m2 = mb.addMenu("Tema")
        for t in ["∅ Temno","∆ Ognjeno","∮ Tok"]:
            a = QAction(t, self)
            a.triggered.connect(lambda _,x=t: self.status.showMessage(f"Tema: {x}"))
            m2.addAction(a)

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
            QCheckBox { color: #F3E9D2; }
            QMenu { background-color: #1B2838; color: #F3E9D2; }
        """)

    # --- Pipeline akcije ---

    def _get_kontekst(self):
        t = self.input_kontekst.toPlainText().strip()
        if not t:
            return {}
        try:
            return json.loads(t)
        except json.JSONDecodeError:
            return {"_raw": t}

    def act_zajemi(self):
        self.current_trditev = self.input_trditev.toPlainText().strip()
        if not self.current_trditev:
            QMessageBox.warning(self, "∅", "Trditev je prazna.")
            return
        self.current_modul = self.combo_modul.currentText()
        kont = self._get_kontekst()
        ke = self.kanon.dodaj(self.current_modul, self.current_trditev)
        self.current_kanon_id = ke.id
        self.cadence.log_mikro(self.current_modul, "ZAJEMI", "OK")
        doc = self.doctrinarium.dodaj_doktrino(
            self.current_modul, self.current_trditev,
            princip=kont.get("princip",""), nujnost=kont.get("nujnost",""))
        self.lbl_zajem.setText(
            f"<b>✓ Zajeto:</b> modul={self.current_modul} | "
            f"kanon={ke.id} | doctrinarium={doc.id}")
        self.status.showMessage(f"∅ Zajeto: {ke.id} — pripravljen za REZI")

    def act_rezi(self):
        if not self.current_trditev:
            QMessageBox.warning(self, "¬", "Najprej zajemi (∅).")
            return
        jedro = self.current_trditev.split(".")[0].strip() or self.current_trditev[:80]
        self.cadence.log_mikro(self.current_modul, "REZI", f"jedro={len(jedro)}")
        self.status.showMessage(f"¬ Rez: jedro izlusceno — pripravljen za POKAZI")

    def act_pokazi(self):
        if not self.current_trditev:
            QMessageBox.warning(self, "∆", "Najprej zajemi (∅).")
            return
        self.txt_preverba.setText(
            f"<b>∆ MANIFEST</b><br>Modul: {self.current_modul}<br>"
            f"Trditev: {self.current_trditev}<br><br>"
            f"<i>Pripravljen za PREVERI ⊢</i>")
        self.cadence.log_mikro(self.current_modul, "POKAZI", "OK")
        self.tabs.setCurrentIndex(1)
        self.status.showMessage("∆ Pokazano — pripravljen za PREVERI ⊢")

    def act_preveri(self):
        if not self.current_trditev:
            QMessageBox.warning(self, "⧖", "Najprej zajemi (∅).")
            return
        kont = self._get_kontekst()
        r = self.preverba.run_all(self.current_modul, self.current_trditev, kont)
        self.last_result = r
        s = self.seriousness.classify(r.rezultati_5, r.ego_flag,
            self.current_soma.evaluate() if self.current_soma else "")

        self.txt_preverba.setHtml(self._fmt_result(r, s))
        sc = {"S1":"#4CAF50","S2":"#FF9800","S3":"#F44336","S4":"#8B0000"}
        self.lbl_serious.setText(
            f"<span style='color:{sc.get(s.nivo)}'>"
            f"{s.nivo} — {s.opis} | Akcija: {s.akcija}</span>")

        if self.current_kanon_id:
            akc = {"PASS":"preverba_pass","FAIL":"preverba_fail","BLISK":"preverba_blisk"}
            try:
                self.kanon.prehod(self.current_kanon_id, akc.get(r.skupni_rezultat, "preverba_fail"))
            except Exception:
                pass

        doc_id = f"DOC-{len(self.doctrinarium.doctrinarium):04d}"
        trn = self.doctrinarium.dodaj_vajo(doc_id, f"Preverba: {self.current_trditev[:60]}")
        self.doctrinarium.preveri_vajo(
            trn.id, r.skupni_rezultat, "", r.ego_flag, r.dokaz_nivo)

        self._log_proof(r, s)
        self.cadence.log_mikro(self.current_modul, "PREVERI", r.skupni_rezultat)

        if r.skupni_rezultat == "PASS":
            self.status.showMessage("⧖ Preverba PASS — SOMA caka")
            self.tabs.setCurrentIndex(2)
        else:
            self.status.showMessage(f"⧖ Preverba {r.skupni_rezultat} — {s.nivo}")

    def act_shrani(self):
        if not self.current_kanon_id:
            QMessageBox.warning(self, "∮", "Najprej zajemi in preveri.")
            return
        if not self.last_result:
            QMessageBox.warning(self, "∮", "Najprej odpelji preverbo (⊢).")
            return
        r = self.last_result
        soma_ok = self.current_soma and self.current_soma.evaluate() == "SOMA_PASS"

        if r.skupni_rezultat == "PASS" and soma_ok:
            self.kanon.prehod(self.current_kanon_id, "soma_integracija")
            asv_id = f"ASV-{len(self.doctrinarium.assur_valid):04d}"
            self.doctrinarium.integriraj(asv_id, "Integrirano v kanon", zivljeno=True)
            self.cadence.log_mikro(self.current_modul, "SHRANI", "KANON")
            self.status.showMessage(f"∮ Shranjeno v KANON: {self.current_kanon_id}")
            QMessageBox.information(self, "∮ Kanon",
                f"Trditev shranjena v KANON.\n\nID: {self.current_kanon_id}\n"
                f"Dokaz: {r.dokaz_nivo}\nSOMA: PASS")
        elif r.skupni_rezultat == "PASS" and not soma_ok:
            QMessageBox.warning(self, "∮", "SOMA ni sla skozi.\n"
                "Telo mora potrditi pred shranitvijo v KANON.")
        else:
            QMessageBox.warning(self, "∮", f"Preverba ni PASS ({r.skupni_rezultat}).\n"
                "Shranjeno kot MEGLA.")
        self.osvezi_kanon()

    # --- SOMA ---

    def run_soma(self):
        soma = SomaCheck(
            dih_prost=self.chk_dih.isChecked(),
            mravljinci=self.chk_mra.isChecked(),
            napetost_cejust=self.chk_cel.isChecked(),
            napetost_ramena=self.chk_ram.isChecked())
        self.current_soma = soma
        rez = soma.evaluate()
        if rez == "SOMA_PASS":
            self.lbl_soma.setText("<span style='color:#4CAF50'>✓ SOMA_PASS</span>")
            self.status.showMessage("SOMA PASS — pripravljen za SHRANI ∮")
        else:
            self.lbl_soma.setText("<span style='color:#F44336'>✗ SOMA_FAIL</span>")
            self.status.showMessage("SOMA FAIL — test krsi telo")
        self.txt_soma.setText(soma.opis())
        self.cadence.log_mikro(self.current_modul, "SOMA", rez)

    # --- Format / osvezevanje ---

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

    def osvezi_kanon(self):
        self.tbl_kanon.setRowCount(0)
        bmap = {"KANON":QColor("#D4AF37"),"PREVERJEN":QColor("#D6A83A"),
                "KANDIDAT":QColor("#F3E9D2"),"MEGLA":QColor("#666"),"ARHIV":QColor("#333")}
        for e in self.kanon.entries:
            r = self.tbl_kanon.rowCount()
            self.tbl_kanon.insertRow(r)
            self.tbl_kanon.setItem(r, 0, QTableWidgetItem(e.id))
            self.tbl_kanon.setItem(r, 1, QTableWidgetItem(e.modul))
            self.tbl_kanon.setItem(r, 2, QTableWidgetItem(e.trditev[:80]))
            it = QTableWidgetItem(e.status)
            it.setForeground(bmap.get(e.status, QColor("#F3E9D2")))
            self.tbl_kanon.setItem(r, 3, it)
            self.tbl_kanon.setItem(r, 4, QTableWidgetItem(e.dokaz_nivo))

    def osvezi_doc(self):
        d = self.doctrinarium
        h = "<div style='color:#F3E9D2; font-family: monospace;'>"
        h += f"<h3>∴ DOCTRINARIUM ({len(d.doctrinarium)})</h3>"
        for doc in d.doctrinarium[-10:]:
            st = d.cikel_status(doc.id)
            h += f"<p><b>{doc.id}</b> [{doc.modul}] {doc.trditev[:60]}<br>{st.get('status','?')} — {st.get('napredek','?')}</p>"
        h += f"<h3>∆ TRAINARIUM ({len(d.trainarium)})</h3>"
        for t in d.trainarium[-10:]:
            h += f"<p><b>{t.id}</b> -> {t.doctrinarium_id} | {t.vaja[:60]} | zadnji: {t.zadnji_rezultat}</p>"
        h += f"<h3>⊢ ASSUR-VALID ({len(d.assur_valid)})</h3>"
        for a in d.assur_valid[-10:]:
            h += f"<p><b>{a.id}</b> -> {a.trainarium_id} | {a.preverba_rezultat} | dokaz: {a.dokaz_nivo}</p>"
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
            r = self.tbl_zg.rowCount()
            self.tbl_zg.insertRow(r)
            for col, val in enumerate(rd):
                self.tbl_zg.setItem(r, col, QTableWidgetItem(str(val or "")))

    # --- DB ---

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

    def export_kanon(self):
        path = self.db_path.parent / "kanon_export.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.kanon.to_dict(), f, indent=2, ensure_ascii=False)
        self.status.showMessage(f"Export: {path.name}")


def main():
    app = QApplication(sys.argv)
    win = TazvMainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
