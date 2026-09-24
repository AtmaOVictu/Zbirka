#!/usr/bin/env python3
"""
TAZV Faza 5 — v7 IGRA INTEGRACIJA
=================================
v7 = v6 (polna Faza 5) + igralna plast (GameEngine + GamePanelWidget)

v7 deduje od TazvMainWindowV6 in dodaja:
  1. GameEngine — napredovanje, grajenje, optimizirane akcije
  2. GamePanelWidget — igralni panel kot nov tab "IGRA ⟡"
  3. GameEngine vklopljen v act_zajemi / act_preveri / act_shrani
  4. Odin akcija — zrtvuj kanon za rune
  5. DB persistenca igralnega stanja (kanon vozlisci, rune, hebb, etaze)

Korpus:
  "IGRA = NUJA, NE IZBIRA." (Yggdrasil, Obs1)
  "Progress naj bo vezan na prehode in receipts, ne na score." (Obs1, 2fca2330)
  "Loki se aktivira, ko igralec postane prevec ucinvit." (Obs1, Yggdrasil)
  "Nidhoggr deluje kot timer globine." (Obs1, Yggdrasil)
  "Odin dobi rune samo, ce nekaj pusti viseti za seboj." (Obs1, Yggdrasil)

PREJSNJI NAPAVEK: "App je ze igra" — ne, je konstrukt.
Igra = napredovanje + grajenje + optimizirane akcije.
Konstrukt = cevovod brez izbire, napredka, grajenja.

v7 naredi iz konstrukta igro:
  - Igralec IZBIRA kateri modul, katero etazo, kako porabiti energijo
  - Igralec NAPREDUJE skozi etaze (odklep z globino)
  - Igralec GRADI osebni Yggdrasil (kanon = vozlisca v drevesu)
  - Igralec se VRACA (energija se regenerira, etaze cakajo, rune cakajo)

Generira:
  1. comprehension/ui/main_window_v7.py
     - Deduje od TazvMainWindowV6
     - Dodaja GameEngine v vse akcije
     - Nov tab: IGRA ⟡
     - Odin gumb v kanon tabu
     - DB tabela: game_state (persistenca)

Run: python tazv_phase5_v7_integration_bootstrap.py
CWD:  D:\\OntoProjekt\\CanvasMinstral\\Scripts\\
"""

import os
from pathlib import Path

BASE = Path("comprehension_machine")
UI = BASE / "comprehension" / "ui"

UI.mkdir(parents=True, exist_ok=True)


def write_file(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {path}")


# ============================================================
# 1. comprehension/ui/main_window_v7.py
#    v7 = v6 + igralna plast
# ============================================================

write_file(UI / "main_window_v7.py", r'''"""
TAZV Comprehension Machine — main_window_v7
==========================================
v7 = v6 (polna Faza 5 integracija) + IGRA (napredovanje, grajenje, akcije)

Deduje od TazvMainWindowV6 in dodaja igralne sisteme:
  - GameEngine: progression, canon builder, action economy
  - GamePanelWidget: igralni panel (energija, etaze, cilji, drevo)
  - GameEngine vklopljen v ZAJEMI, PREVERI, SHRANI
  - Odin: zrtvuj kanon vnos za rune (globlje znanje)
  - Loki: 3x ista resitev = sprememba pravil
  - Nidhoggr: povrsinsko delo = korenine gnijejo
  - Zep: trenutek hkratnosti — več etaz se ujamejo
  - DB persistenca igralnega stanja

Razlika od v6:
  - ZAJEMI: tudi doda kandidata v GameEngine.canon (osebni Yggdrasil)
  - PREVERI: tudi porabi energijo, preveri Lokija, ustvari runo ob FAIL
  - SHRANI: tudi promovira v GameEngine.canon, preveri odklep etaze, zazna zep
  - Nov tab: IGRA ⟡ (igralni panel)
  - Odin gumb v kanon tabu
  - Energija se regenerira (timer)
  - Etaze se odklepajo s stevilom kanon vnosov
  - Mithos plasti se odklepajo z Hebb povprecjem + preverbami
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
    QMenu, QAction, QSplitter, QFrame, QProgressBar, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QAction

# --- v6 dedovanje ---
from comprehension.ui.main_window_v6 import TazvMainWindowV6

# --- Igralni sistemi ---
from comprehension.core.game_engine import (
    GameEngine, CanonBuilder, CanonNode, Runa, ActionEconomy,
    EtazaInfo, ETAZE, MITHOS_PLASTI, RegisterStatus,
)
from comprehension.ui.game_panel import GamePanelWidget


# ============================================================
# TazvMainWindowV7 — v6 + igralna plast
# ============================================================

class TazvMainWindowV7(TazvMainWindowV6):
    """
    TAZV v7 — v6 + IGRA (napredovanje, grajenje, optimizirane akcije).

    Korpus: "IGRA = NUJA, NE IZBIRA."
    Prejsnji napavek: "App je ze igra" — ne, je konstrukt.
    Igra potrebuje napredovanje, grajenje, optimizirane akcije.
    """

    def __init__(self):
        # Najprej v6 init (vsi Faza 5 sistemi)
        super().__init__()
        self.setWindowTitle("TAZV Comprehension Machine — v7 IGRA")

        # --- Igralni engine ---
        self.game_engine = GameEngine()
        self.game_engine.economy.postavi_cilje()
        self.current_game_node_id = None
        self.current_etaza = 1

        # --- DB za igro ---
        self._init_game_db()
        self._load_game_state()

        # --- Igralni panel ---
        self.game_panel = GamePanelWidget(self.game_engine)
        self.tabs.addTab(self.game_panel, "IGRA ⟡")

        # --- Odin gumb v kanon tab ---
        self._dodaj_odin_gumb()

        # --- Energija regeneracija timer ---
        self.energija_timer = QTimer(self)
        self.energija_timer.timeout.connect(self._regeneriraj_energijo)
        self.energija_timer.start(30000)  # +1 energija na 30s

        # --- Osvezi igralni panel ---
        self.game_panel.osvezi_vse()

    # ============================================================
    # DB — igralno stanje
    # ============================================================

    def _init_game_db(self):
        """Ustvari tabele za persistenco igralnega stanja."""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        try:
            c.execute("""CREATE TABLE IF NOT EXISTS game_canon_nodes (
                node_id TEXT PRIMARY KEY,
                modul TEXT,
                trditev TEXT,
                status TEXT,
                dokaz_nivo TEXT,
                timestamp TEXT,
                etaza INTEGER,
                hebb_utez REAL,
                runa_id TEXT,
                zrtvovana INTEGER DEFAULT 0
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS game_edges (
                from_id TEXT,
                to_id TEXT,
                utez REAL,
                PRIMARY KEY (from_id, to_id)
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS game_runes (
                runa_id TEXT PRIMARY KEY,
                timestamp TEXT,
                modul TEXT,
                test_ki_padla TEXT,
                trditev TEXT,
                beseda TEXT,
                stavek TEXT,
                dejanje TEXT,
                zaceljena INTEGER DEFAULT 0,
                zaceljena_timestamp TEXT,
                etaza INTEGER,
                cena TEXT,
                znanje TEXT,
                zrtvovana INTEGER DEFAULT 0
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS game_etaze (
                stevilka INTEGER PRIMARY KEY,
                odklenjena INTEGER DEFAULT 0
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS game_mithos (
                plast_id INTEGER PRIMARY KEY,
                odklenjena INTEGER DEFAULT 0
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS game_zepi (
                zep_id TEXT PRIMARY KEY,
                timestamp TEXT,
                etaze TEXT,
                opis TEXT
            )""")
            c.execute("""CREATE TABLE IF NOT EXISTS game_energija (
                id INTEGER PRIMARY KEY DEFAULT 1,
                energija INTEGER,
                max_energija INTEGER,
                st_preverb_skupaj INTEGER,
                UNIQUE(id)
            )""")
            conn.commit()
        except Exception as e:
            print(f"[game_db] napaka: {e}")
        conn.close()

    def _save_game_state(self):
        """Shrani igralno stanje v DB."""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()

        # Canon nodes
        for n in self.game_engine.canon.nodes.values():
            c.execute("""INSERT OR REPLACE INTO game_canon_nodes
                (node_id, modul, trditev, status, dokaz_nivo, timestamp,
                 etaza, hebb_utez, runa_id, zrtvovana)
                VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (n.node_id, n.modul, n.trditev, n.status, n.dokaz_nivo,
                 n.timestamp, n.etaza, n.hebb_utez, n.runa_id or "",
                 int(n.zrtvovana)))

        # Edges
        for e in self.game_engine.canon.edges:
            c.execute("""INSERT OR REPLACE INTO game_edges
                (from_id, to_id, utez) VALUES(?,?,?)""",
                (e["from"], e["to"], e["utez"]))

        # Runes
        for r in self.game_engine.canon.runes + self.game_engine.canon.zrtvovane_rune:
            is_zrtv = r in self.game_engine.canon.zrtvovane_rune
            c.execute("""INSERT OR REPLACE INTO game_runes
                (runa_id, timestamp, modul, test_ki_padla, trditev,
                 beseda, stavek, dejanje, zaceljena, zaceljena_timestamp,
                 etaza, cena, znanje, zrtvovana)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (r.runa_id, r.timestamp, r.modul, r.test_ki_padla,
                 r.trditev, r.beseda, r.stavek, r.dejanje,
                 int(r.zaceljena), r.zaceljena_timestamp or "",
                 r.etaza, r.cena, r.znanje, int(is_zrtv)))

        # Etaze
        for e in self.game_engine.etaze:
            c.execute("""INSERT OR REPLACE INTO game_etaze
                (stevilka, odklenjena) VALUES(?,?)""",
                (e.stevilka, int(e.odklenjena)))

        # Mithos
        for p in self.game_engine.mithos:
            c.execute("""INSERT OR REPLACE INTO game_mithos
                (plast_id, odklenjena) VALUES(?,?)""",
                (p["id"], int(p["odklenjena"])))

        # Energija
        ec = self.game_engine.economy
        c.execute("""INSERT OR REPLACE INTO game_energija
            (id, energija, max_energija, st_preverb_skupaj)
            VALUES(1,?,?,?)""",
            (ec.energija, ec.max_energija, self.game_engine.st_preverb_skupaj))

        conn.commit()
        conn.close()

    def _load_game_state(self):
        """Nalozi igralno stanje iz DB (ce obstaja)."""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()

        # Canon nodes
        try:
            c.execute("SELECT node_id, modul, trditev, status, dokaz_nivo, "
                       "timestamp, etaza, hebb_utez, runa_id, zrtvovana "
                       "FROM game_canon_nodes")
            for row in c.fetchall():
                nid, modul, trditev, status, dokaz, ts, etaza, hebb, runa_id, zrtv = row
                node = CanonNode(
                    node_id=nid, modul=modul, trditev=trditev,
                    status=status, dokaz_nivo=dokaz or "",
                    timestamp=ts or "", etaza=etaza,
                    hebb_utez=hebb, runa_id=runa_id or None,
                    zrtvovana=bool(zrtv),
                )
                self.game_engine.canon.nodes[nid] = node
        except Exception:
            pass

        # Edges
        try:
            c.execute("SELECT from_id, to_id, utez FROM game_edges")
            for row in c.fetchall():
                self.game_engine.canon.edges.append(
                    {"from": row[0], "to": row[1], "utez": row[2]})
        except Exception:
            pass

        # Runes
        try:
            c.execute("SELECT runa_id, timestamp, modul, test_ki_padla, trditev, "
                       "beseda, stavek, dejanje, zaceljena, zaceljena_timestamp, "
                       "etaza, cena, znanje, zrtvovana FROM game_runes")
            for row in c.fetchall():
                runa = Runa(
                    runa_id=row[0], timestamp=row[1] or "", modul=row[2],
                    test_ki_padla=row[3], trditev=row[4], beseda=row[5],
                    stavek=row[6], dejanje=row[7],
                    zaceljena=bool(row[8]),
                    zaceljena_timestamp=row[9] or "",
                    etaza=row[10], cena=row[11] or "", znanje=row[12] or "",
                )
                if row[13]:
                    self.game_engine.canon.zrtvovane_rune.append(runa)
                else:
                    self.game_engine.canon.runes.append(runa)
        except Exception:
            pass

        # Etaze
        try:
            c.execute("SELECT stevilka, odklenjena FROM game_etaze")
            for row in c.fetchall():
                for e in self.game_engine.etaze:
                    if e.stevilka == row[0]:
                        e.odklenjena = bool(row[1])
        except Exception:
            pass

        # Mithos
        try:
            c.execute("SELECT plast_id, odklenjena FROM game_mithos")
            for row in c.fetchall():
                for p in self.game_engine.mithos:
                    if p["id"] == row[0]:
                        p["odklenjena"] = bool(row[1])
        except Exception:
            pass

        # Energija
        try:
            c.execute("SELECT energija, max_energija, st_preverb_skupaj FROM game_energija WHERE id=1")
            row = c.fetchone()
            if row:
                self.game_engine.economy.energija = row[0]
                self.game_engine.economy.max_energija = row[1]
                self.game_engine.st_preverb_skupaj = row[2]
        except Exception:
            pass

        conn.close()

    # ============================================================
    # Odin gumb v kanon tab
    # ============================================================

    def _dodaj_odin_gumb(self):
        """Dodaj Odin gumb za zrtvovanje kanon vnosa."""
        # Najdi kanon tab (ZGODOVINA ali KANON tab)
        # Dodaj gumb v kanon layout
        for i in range(self.tabs.count()):
            if "KANON" in self.tabs.tabText(i).upper() or "ZGODOVINA" in self.tabs.tabText(i).upper():
                tab_widget = self.tabs.widget(i)
                layout = tab_widget.layout()
                if layout:
                    odin_btn = QPushButton("🜂 ODIN — žrtvuj kanon za runo")
                    odin_btn.setStyleSheet(
                        "QPushButton { background-color: #B43A2E; color: #F3E9D2; "
                        "font-weight: bold; padding: 8px; border-radius: 4px; }"
                        "QPushButton:hover { background-color: #D6A83A; }"
                    )
                    odin_btn.clicked.connect(self._act_odin)
                    layout.addWidget(odin_btn)
                break

    def _act_odin(self):
        """
        Odin: zrtvuj kanon vnos za rune (globlje znanje).

        Korpus: "Igralec dobi rune samo, ce nekaj pusti viseti za seboj."
        """
        # Poisci izbrani kanon vnos
        izbrani_id = None
        for i in range(self.tabs.count()):
            if "KANON" in self.tabs.tabText(i).upper():
                tab_widget = self.tabs.widget(i)
                # Poisci tabelo
                for child in tab_widget.findChildren(QTableWidget):
                    row = child.currentRow()
                    if row >= 0:
                        item = child.item(row, 0)
                        if item:
                            izbrani_id = item.text()
                    break
                break

        if not izbrani_id:
            # Poskusi z game canon node
            if self.current_game_node_id:
                izbrani_id = self.current_game_node_id

        if not izbrani_id:
            QMessageBox.warning(self, "🜂 ODIN",
                "Izberi kanon vnos za zrtvovanje.\n"
                "Klikni na vrstico v kanon tabeli.")
            return

        # Preveri, da je v GameEngine canon
        node = self.game_engine.canon.nodes.get(izbrani_id)
        if not node:
            QMessageBox.warning(self, "🜂 ODIN",
                f"Kanon vnos {izbrani_id} ni v igralnem drevesu.\n"
                "Sam kanon (v6) in igralni canon (v7) sta locena.")
            return

        if node.status != "canon":
            QMessageBox.warning(self, "🜂 ODIN",
                "Sam KANON status lahko zrtvujes. "
                f"Trenutni status: {node.status}")
            return

        if node.zrtvovana:
            QMessageBox.warning(self, "🜂 ODIN",
                "Ta vnos je ze zrtvovan.")
            return

        # Potrdi z uporabnikom
        msg = QMessageBox(self)
        msg.setWindowTitle("🜂 ODIN — žrtvovanje")
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setText("Odin zahteva ceno.")
        msg.setInformativeText(
            f"Zrtvujes kanon vnos:\n\n"
            f"  {node.trditev[:80]}\n\n"
            f"Modul: {node.modul} | Etaza: {node.etaza}\n\n"
            f"V zameno dobis RUNO — globlje znanje.\n"
            f"Vnos bo arhiviran. Ne moreš ga povrniti.\n\n"
            f"Korpus: 'Igralec dobi rune samo, ce nekaj pusti viseti za seboj.'"
        )
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.button(QMessageBox.StandardButton.Yes).setText("🜂 Žrtvuj")
        msg.button(QMessageBox.StandardButton.No).setText("Ne")

        if msg.exec() != QMessageBox.StandardButton.Yes:
            return

        runa = self.game_engine.canon.odin_zrtvuj(izbrani_id)
        if runa:
            self._save_game_state()
            self.game_panel.osvezi_vse()
            QMessageBox.information(self, "🜂 RUNA",
                f"Runa {runa.runa_id} je nastala iz zrtvovanja.\n\n"
                f"Znanje: {runa.znanje}\n"
                f"Cena: {runa.cena}\n\n"
                f"Korpus: 'Runa = brazgotina, ki zn govoriti.'")
        else:
            QMessageBox.warning(self, "🜂 ODIN", "Zrtvovanje ni uspelo.")

    # ============================================================
    # Energija regeneracija
    # ============================================================

    def _regeneriraj_energijo(self):
        """Regeneriraj +1 energijo na 30s (timer callback)."""
        self.game_engine.economy.regeneriraj(1)
        self.game_panel.osvezi_vse()

    # ============================================================
    # AKCIJE — override v6 metod z igralno plastjo
    # ============================================================

    def act_zajemi(self):
        """
        ∅ ZAJEMI — v6 zajem + igralni dodatek.

        Igralni dodatek:
        - Doda kandidata v GameEngine.canon (osebni Yggdrasil)
        - Preveri, ali je dovolj energije
        - Zabelezi v sejne cilje
        """
        # Najprej v6 zajem (osnovni cevovod)
        # Poklici parent act_zajemi
        super().act_zajemi()

        # --- Igralni dodatek ---

        # Dobi trenutni modul in trditev
        modul = self.current_modul
        trditev = self.current_trditev
        etaza = self.current_etaza

        if not trditev:
            return

        # Preveri energijo
        if not self.game_engine.economy.porabi_energijo(1, etaza):
            QMessageBox.warning(self, "∅ ZAJEMI",
                "Ni dovolj preverba energije.\n"
                f"Trenutna energija: {self.game_engine.economy.energija}/{self.game_engine.economy.max_energija}\n"
                "Energija se regenerira +1 na 30 sekund.")
            return

        # Doda kandidata v igralni canon
        node = self.game_engine.canon.dodaj_kandidata(modul, trditev, etaza)
        self.current_game_node_id = node.node_id

        # Zabelezi v sejne cilje
        self.game_engine.economy.posodobi_cilj("approvals", 0)  # se ne steje kot approval

        self.game_panel.osvezi_vse()
        self.status.showMessage(
            f"∅ ZAJEMI | Energija: {self.game_engine.economy.energija} | "
            f"Kandidat: {node.node_id[:8]}")

    def act_preveri(self):
        """
        ⧖ PREVERI — v6 preverba + igralni dodatek.

        Igralni dodatek:
        - Porabi energijo (globje etaze = vecja poraba)
        - Ob FAIL: ustvari runo v igralnem drevesu
        - Preveri Lokija (3x ista resitev = sprememba pravil)
        - Preveri Nidhoggr (povrsinsko delo = korenine gnijejo)
        - Ob PASS: zaceli runo (ce obstaja nezaceljena iz istega modula)
        - Preveri odklep etaze
        - Preveri odklep mithos plasti
        - Zazna zep (trenutek hkratnosti)
        """
        # Najprej v6 preverba (osnovni 5+10 preizkusi + SOMA + trainarium + falsifikacija)
        super().act_preveri()

        if not self.current_game_node_id:
            return

        r = self.last_preverba
        if not r:
            return

        modul = self.current_modul
        etaza = self.current_etaza
        node_id = self.current_game_node_id

        # --- Porabi energijo za preverbo ---
        cena_ok = self.game_engine.economy.porabi_energijo(2, etaza)

        # --- Zabelezi resitev + preveri Lokija ---
        test_ime = list(r.rezultati_5.keys())[0] if r.rezultati_5 else "neznan"
        loki_rez = self.game_engine.economy.zabelezi_resitev(
            f"{modul}:{test_ime}", globina=etaza)

        if loki_rez == "loki":
            # Loki aktiviran — spremeni pravila
            QMessageBox.warning(self, "🜂 LOKI",
                "Loki je aktiviran!\n\n"
                "3x si uporabil(a) isto resitev.\n"
                "Loki pokvari njen ucinek — ne kot kazen, "
                "ampak kot sila, ki te sili v novo etazo.\n\n"
                "Korpus: 'Ko igralec predolgo uporablja isto resitev, "
                "Loki pokvari njen ucinek.'")
            self.game_engine.economy.regeneriraj_lokija()

        # --- Nidhoggr preverba ---
        nidhogg = self.game_engine.economy.nidhogg_stanje()
        if "KRITICNO" in nidhogg:
            self.status.showMessage(f"🐉 NIDHÖGGGR: {nidhogg}")
        elif "OPOZORILO" in nidhogg:
            self.status.showMessage(f"🐉 NIDHÖGGGR: {nidhogg}")

        # --- Ob FAIL: ustvari runo ---
        if r.skupni_rezultat in ("FAIL", "MEGLA"):
            # Ustvari runo (brazgotina)
            # Sik → beseda → stavek → dejanje (ce imamo drill iz v6)
            beseda_txt = ""
            stavek_txt = ""
            dejanje_txt = ""

            if self.last_drill:
                if self.last_drill.beseda:
                    beseda_txt = self.last_drill.beseda.beseda
                if self.last_drill.stavek:
                    stavek_txt = self.last_drill.stavek.stavek
                if self.last_drill.dejanje:
                    dejanje_txt = self.last_drill.dejanje.dejanje
            else:
                beseda_txt = f"FAIL v {modul}"
                stavek_txt = f"Test {test_ime} je padel"
                dejanje_txt = "Ponovi z drugacnim pristopom"

            runa = self.game_engine.canon.ustvari_runo(
                modul=modul, test=test_ime, trditev=self.current_trditev,
                beseda=beseda_txt, stavek=stavek_txt, dejanje=dejanje_txt,
                etaza=etaza,
            )

            self.game_engine.economy.st_fail += 1
            self.status.showMessage(
                f"⧖ FAIL → RUNA {runa.runa_id} | "
                f"Energija: {self.game_engine.economy.energija}")

        # --- Ob PASS: zaceli runo + promoviraj v igralnem canon ---
        elif r.skupni_rezultat == "PASS":
            # Zaceli runo (ce obstaja nezaceljena iz istega modula)
            zaceljena = self.game_engine.canon.zaceli_runo(modul, test_ime)
            if zaceljena:
                self.status.showMessage(
                    f"⧖ PASS → RUNA {zaceljena.runa_id} zaceljena! | "
                    f"Energija: {self.game_engine.economy.energija}")

            # Promoviraj v igralnem canon (candidate → approved)
            self.game_engine.canon.promoviraj(node_id, "approved", r.dokaz_nivo)

            self.game_engine.economy.st_pass += 1
            self.game_engine.economy.posodobi_cilj("contradictions", 1)

        # --- Preveri odklep etaze ---
        for e in self.game_engine.etaze:
            if not e.odklenjena:
                rez = self.game_engine.odpri_etazo(e.stevilka)
                if rez.get("odklenjena"):
                    QMessageBox.information(self, f"∅ ETAZA {e.stevilka}",
                        f"ETAZA {e.stevilka} ODKLEPNJENA!\n\n"
                        f"  {e.ime} ({e.glyph})\n"
                        f"  Tema: {e.tema}\n\n"
                        f"  Vprasanje: {e.vprasanje}\n\n"
                        f"Korpus: 'Vsaka etaza nastane iz prejsnje, "
                        f"jo nosi, jo preseze in se nekoc vrne k zacetku.'")
                    self.game_panel.osvezi_vse()

        # --- Preveri odklep mithos plasti ---
        hebb_povp = self.game_engine.hebb_povprecje()
        novi_mithos = self.game_engine.preveri_mithos(
            hebb_povp, self.game_engine.st_preverb_skupaj)
        if novi_mithos:
            for p in novi_mithos:
                QMessageBox.information(self, f"∂ MITHOS",
                    f"Mithos plast odklenjena!\n\n"
                    f"  {p['ime']} (plast {p['id']})\n"
                    f"  {p['opis']}")

        # --- Zazna zep (trenutek hkratnosti) ---
        # Zep se odpri, ko igralec dela v globji etazi hkrati z razumevanjem mithos
        if etaza >= 3 and self.game_engine.mithos_globina() >= 2:
            # Rocno zazna zep (trenutek hkratnosti)
            zep_id = hashlib.md5(
                f"zep:{etaza}:{datetime.now().isoformat()}".encode()
            ).hexdigest()[:8]
            zep_opis = (
                f"Zep pri etazi {etaza} + mithos globina {self.game_engine.mithos_globina()}. "
                f"Vec etaz se ujamejo."
            )
            self.game_engine.zepi.append({
                "zep_id": zep_id,
                "timestamp": datetime.now().isoformat(),
                "etaze": f"etaza_{etaza}_mithos_{self.game_engine.mithos_globina()}",
                "opis": zep_opis,
            })
            self.status.showMessage(f"⟡ ZEP {zep_id} — trenutek hkratnosti!")

        # --- Posodobi sejne cilje ---
        self.game_engine.economy.posodobi_cilj("etaza", etaza)

        # --- Shrani stanje + osvezi panel ---
        self._save_game_state()
        self.game_panel.osvezi_vse()

    def act_shrani(self):
        """
        ∮ SHRANI — v6 shranitev + igralni dodatek.

        Igralni dodatek:
        - Promoviraj v igralnem canon: approved → canon
        - Preveri odklep etaze (nova kanon = napredek)
        - Posodobi Hebb utezi v igralnem drevesu
        - Zabelezi sejni cilj: approvals
        - Preveri zep (ce se shrani v globji etazi)
        """
        # Najprej v6 shranitev
        super().act_shrani()

        if not self.current_game_node_id:
            return

        r = self.last_preverba
        if not r:
            return

        node_id = self.current_game_node_id
        modul = self.current_modul
        etaza = self.current_etaza

        # Sam ce je PASS + SOMA
        soma_ok = self.current_soma and self.current_soma.evaluate() == "SOMA_PASS"
        if r.skupni_rezultat == "PASS" and soma_ok:
            # Promoviraj v igralnem canon: approved → canon
            self.game_engine.canon.promoviraj(node_id, "canon", r.dokaz_nivo)

            # Posodobi Hebb utez vozlisca (raste z rabo)
            node = self.game_engine.canon.nodes.get(node_id)
            if node:
                node.hebb_utez = min(1.0, node.hebb_utez + 0.1)

            # Zabelezi sejni cilj
            self.game_engine.economy.posodobi_cilj("approvals", 1)

            # Preveri odklep etaze
            for e in self.game_engine.etaze:
                if not e.odklenjena:
                    rez = self.game_engine.odpri_etazo(e.stevilka)
                    if rez.get("odklenjena"):
                        QMessageBox.information(self, f"∅ ETAZA {e.stevilka}",
                            f"ETAZA {e.stevilka} ODKLEPNJENA!\n\n"
                            f"  {e.ime} ({e.glyph})\n"
                            f"  Tema: {e.tema}\n"
                            f"  Vprasanje: {e.vprasanje}")

            # Preveri povezave z obstojecimi canon vozlisci
            for other in self.game_engine.canon.nodes.values():
                if (other.node_id != node_id and other.status == "canon"
                        and other.modul == modul and not other.zrtvovana):
                    self.game_engine.canon.dodaj_povezavo(
                        node_id, other.node_id, 0.5)

            # Stej preverbe
            self.game_engine.st_preverb_skupaj += 1

            self.status.showMessage(
                f"∮ KANON | Canon vozlisc: {self.game_engine.canon.stevilo_kanon()} | "
                f"Energija: {self.game_engine.economy.energija}")

        # Posodobi cilj: osirotela vozlisc
        # (ce smo povezali vozlisc, stevilo povezav > 0)
        if self.game_engine.canon.edges:
            self.game_engine.economy.posodobi_cilj("orphans", 1)

        # --- Shrani stanje + osvezi panel ---
        self._save_game_state()
        self.game_panel.osvezi_vse()

    # ============================================================
    # Etaza izbira (igralna akcija)
    # ============================================================

    def _spremeni_etazo(self, etaza: int):
        """
        Igralec izbere etazo (1-7).
        Vecja etaza = vecja poraba energije, a vecja nagrada.
        """
        for e in self.game_engine.etaze:
            if e.stevilka == etaza:
                if e.odklenjena:
                    self.current_etaza = etaza
                    self.status.showMessage(
                        f"∅ Etaza {etaza}: {e.ime} ({e.glyph}) | {e.tema}")
                else:
                    QMessageBox.warning(self, "∅ ETAZA",
                        f"Etaza {etaza} ({e.ime}) ni odklenjena.\n"
                        f"Zahteva {e.zahteva_kanon} kanon vnosov.\n"
                        f"Trenutno: {self.game_engine.canon.stevilo_kanon()}")
                return

    # ============================================================
    # Nova seja (reset igralnih ciljev)
    # ============================================================

    def nova_seja(self):
        """Nova seja — ponastavi igralne cilje, regeneriraj energijo."""
        self.game_engine.economy.energija = self.game_engine.economy.max_energija
        self.game_engine.economy.st_preverb = 0
        self.game_engine.economy.st_fail = 0
        self.game_engine.economy.st_pass = 0
        self.game_engine.economy.postavi_cilje()
        self.game_engine.economy.regeneriraj_lokija()
        self.game_engine.economy.nidhogg_timer = 0

        if hasattr(self.game_panel, 'init_sejo'):
            self.game_panel.init_sejo()

        self._save_game_state()
        self.game_panel.osvezi_vse()
        self.status.showMessage("∅ Nova seja | Energija polna | Cilji ponastavljeni")

    # ============================================================
    # Menu — dodaj igralne akcije
    # ============================================================

    def _build_menu(self):
        """Override: dodaj igralne akcije v menu."""
        super()._build_menu()

        # Dodaj igralni menu
        menubar = self.menuBar()
        igra_menu = menubar.addMenu("🎮 IGRA")

        nova_seja = QAction("Nova seja", self)
        nova_seja.triggered.connect(self.nova_seja)
        igra_menu.addAction(nova_seja)

        igra_menu.addSeparator()

        # Etaze submenu
        etaze_menu = igra_menu.addMenu("Etaze")
        for e in ETAZE:
            act = QAction(f"{e.stevilka}. {e.ime} ({e.glyph})", self)
            act.triggered.connect(lambda checked, n=e.stevilka: self._spremeni_etazo(n))
            etaze_menu.addAction(act)

        igra_menu.addSeparator()

        odin_act = QAction("🜂 Odin — žrtvuj kanon", self)
        odin_act.triggered.connect(self._act_odin)
        igra_menu.addAction(odin_act)

    # ============================================================
    # Override _apply_theme — dodaj igralne barve
    # ============================================================

    def _apply_theme(self):
        """Override: v6 tema + igralni dodatki."""
        super()._apply_theme()
        # Igralni panel dobi svoj styling iz GamePanelWidget
        # Tukaj ne dodajamo — game_panel.py ima svoj styling


# ============================================================
# MAIN
# ============================================================

def main():
    app = QApplication(sys.argv)
    win = TazvMainWindowV7()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
''')


# ============================================================
# BOOTSTRAP RUNNER
# ============================================================

def main():
    print("=" * 60)
    print("TAZV Faza 5 — v7 IGRA INTEGRACIJA")
    print("=" * 60)
    print()
    print("v7 = v6 (polna Faza 5) + IGRA (napredovanje, grajenje, akcije)")
    print()
    print("Generira:")
    print()
    print("  comprehension/ui/main_window_v7.py")
    print("  Deduje od TazvMainWindowV6, dodaja igralne sisteme.")
    print()
    print("KAJ V7 NAREDI IZ KONSTRUKTA IGRO:")
    print()
    print("  1. NAPREDOVANJE")
    print("     - 7 etaz Yggdrasil-a odklepajo s kanon vnosi")
    print("       Etaza 1 (SEME) = odprta")
    print("       Etaza 2 (KORENINA) = 3 kanon")
    print("       Etaza 3 (DEBLO) = 7 | 4 (VEJA) = 12 | ...")
    print("     - 7 mithos plasti odklepajo z Hebb povprecjem")
    print("     - Hebb utezi rastejo z rabo (modul postaja 'tvoj')")
    print()
    print("  2. GRAJENJE")
    print("     - Igralec gradi osebni Yggdrasil iz preverjenih resnic")
    print("     - Vsaka PASS = vozlisce v drevesu")
    print("     - Vozlisca se povezujejo z robovi (odnosi med resnicami)")
    print("     - Runa = brazgotina iz FAIL, ki se zaceli ob PASS")
    print("     - ODIN: zrtvuj kanon vnos za rune (globlje znanje)")
    print()
    print("  3. OPTIMIZIRANE AKCIJE")
    print("     - Vir 'preverba energija' (10 na sejo, regenerira se)")
    print("     - Izbira modula (7 poti)")
    print("     - Izbira etaze (globje = drainscno a bolj vredno)")
    print("     - Loki: 3x ista resitev = sprememba pravil")
    print("     - Nidhoggr: povrsinsko delo = korenine gnijejo")
    print("     - Zep: trenutek hkratnosti — več etaz se ujamejo")
    print("     - Sejni cilji: receipts ne score")
    print("       'Resi 3 kontradikcije' | 'Odobri 2 kandidata'")
    print("       'Povezi 5 osirotelih' | 'Pojdi v etazo 3+'")
    print()
    print("ZAKAJ SE VRACAS:")
    print("  - Energija se regenerira (+1 na 30s)")
    print("  - Etaze cakajo na odklep (3, 7, 12, 18, 25, 35 kanon)")
    print("  - Mithos plasti cakajo na globino")
    print("  - Rune cakajo, da se zacelijo")
    print("  - Cilji se ponastavijo vsako sejo")
    print()
    print("INTEGRACIJSKE TOČKE (kje se igra vklopi v cevovod):")
    print()
    print("  act_zajemi():")
    print("    - game_engine.canon.dodaj_kandidata → osebni Yggdrasil")
    print("    - economy.porabi_energijo → vir se porabi")
    print()
    print("  act_preveri():")
    print("    - economy.porabi_energijo → globje etaze = vecja poraba")
    print("    - economy.zabelezi_resitev → preveri Lokija")
    print("    - ob FAIL → canon.ustvari_runo → brazgotina")
    print("    - ob PASS → canon.zaceli_runo → brazgotina se zaceli")
    print("    - odpri_etazo → preveri odklep nove etaze")
    print("    - preveri_mithos → preveri odklep mithos plasti")
    print("    - zazna zep → trenutek hkratnosti")
    print()
    print("  act_shrani():")
    print("    - canon.promoviraj(approved → canon) → napredek")
    print("    - hebb_utez raste → modul postaja 'tvoj'")
    print("    - dodaj_povezavo → gradi drevo")
    print("    - odpri_etazo → nova kanon = odklep")
    print()
    print("  _act_odin():")
    print("    - canon.odin_zrtvuj → zrtvuj kanon za runo")
    print("    - 'Igralec dobi rune samo, ce nekaj pusti viseti.'")
    print()
    print("DB PERSISTENCA:")
    print("  - game_canon_nodes (vozlisca drevesa)")
    print("  - game_edges (povezave)")
    print("  - game_runes (brazgotine)")
    print("  - game_etaze (odklenjene etaze)")
    print("  - game_mithos (odklenjene plasti)")
    print("  - game_zepi (trenutki hkratnosti)")
    print("  - game_energija (trenutna energija)")
    print()
    print("NOVI TAB:")
    print("  IGRA ⟡ — igralni panel (energija, etaze, cilji, drevo, Loki, Nidhoggr, mithos)")
    print()
    print("NOVI MENU:")
    print("  🎮 IGRA → Nova seja | Etaze (1-7) | Odin")
    print()
    print("KORPUS CITATI:")
    print("  'IGRA = NUJA, NE IZBIRA.' (Yggdrasil)")
    print("  'Progress naj bo vezan na prehode in receipts, ne na score.'")
    print("  'Loki se aktivira, ko igralec postane prevec ucinvit.'")
    print("  'Nidhoggr deluje kot timer globine.'")
    print("  'Odin dobi rune samo, ce nekaj pusti viseti za seboj.'")
    print("  'Runa = brazgotina, ki zn govoriti.'")
    print("  'Vsaka etaza nastane iz prejsnje, jo nosi, jo preseze in se nekoc vrne.'")
    print()
    print("NASLEDNJI KORAKI:")
    print("  1. Generiraj vse Faza 5 canvas-e (ce se nisi):")
    print("     - tazv-phase5-preverba (preverba.py, soma.py, doctrinarium.py, ...)")
    print("     - tazv-phase5-integration (aregister_bridge.py, corpus_integrator.py, ...)")
    print("     - tazv-phase5-trainarium (trainarium.py, soma_proxy.py, falsifikacija.py, ...)")
    print("     - tazv-phase5-game-layer (game_engine.py, game_panel.py)")
    print("     - tazv-phase5-v6-integration (main_window_v6.py)")
    print("  2. python tazv_phase5_v7_integration_bootstrap.py")
    print("  3. Posodobi main.py:")
    print("     from comprehension.ui.main_window_v7 import TazvMainWindowV7")
    print("  4. python main.py")
    print("  5. Preveri:")
    print("     - IGRA ⟡ tab prikazuje energijo, etaze, cilje, drevo")
    print("     - ZAJEMI doda kandidata v igralni canon + porabi energijo")
    print("     - PREVERI porabi energijo + ob FAIL ustvari runo")
    print("     - PREVERI ob PASS zaceli runo + promovira v canon")
    print("     - SHRANI promovira v canon + preveri odklep etaze")
    print("     - Loki opozori pri 3x isti resitvi")
    print("     - Nidhoggr opozori pri povrsinskem delu")
    print("     - Odin gumb deluje (zrtvuj kanon za runo)")
    print("     - Energija se regenerira (+1 na 30s)")
    print("     - Etaze se odklepajo s kanon vnosi")
    print("     - Mithos plasti se odklepajo z globino")
    print("     - Stanje persistira v DB med sejami")
    print("=" * 60)


if __name__ == "__main__":
    main()