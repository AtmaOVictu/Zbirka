#!/usr/bin/env python3
"""
TAZV Faza 5 — IGRALNA PLAST
============================
Korpus: "IGRA = NUJA, NE IZBIRA." (Obs1, Yggdrasil doc)
Korpus: "Razum ig-entitete = raz-um giba.
         Razum brez giba je smrt. Gib brez razuma je slepa sila.
         Samo v razpoki ('IG-RA') nastane nekaj, kar ni 'le' ponovitev."

Aplikacija JE ZE IGRA. 5-gumbni pipeline (ZAJEMI-REZI-POKAZI-PREVERI-SHRANI)
JE igralni loop. Fraktalna kadenca JE return mechanic. TRAINARIUM drills
SO progression. Hebb utezi SO skill tree. Zep JE achievement.

Kaj manjka: plast, ki naredi te strukture VIDNE kot igralne mehanike.

6 mehanik iz korpusa:
  1. DNEVNA VRATA — vsak dan drugace vprasanje (R-7 faza dneva)
  2. ZEP — trenutek hkratnosti, ko preverba + soma + kadenca uskladijo
  3. RUNA KOT BRAZGOTINA — fail pusti sled, ki zna govoriti
  4. HEBB SKILL TREE — utezi kot ziv graf (ne staticno drevo)
  5. ETAZE — 7 R-7 faz kot 7 nadstropij (app odpre na etazi dneva)
  6. MITHOS — globlje ko razumes korpus, globlje app pokaze

Korpus o motivaciji (Obs1, topic_30):
  "Motivacija = razpoka + pot + smisel"
  "Motivacija je ziva, ker je ziva tvoja razpoka."
  "Ti si motiviran, ko si v resnici, ne v vlogi."
  Mo-Ti-Va: Mo = tlak/temelj, Ti = smer, Va = val/razsirjanje

Generira:
  1. comprehension/core/game_layer.py — dnevna vrata, zep, runa, etaze, mithos
  2. comprehension/ui/game_overlay.py — QWidget overlay za igralno plast

Run: python tazv_phase5_game_layer_bootstrap.py
CWD:  D:\\OntoProjekt\\CanvasMinstral\\Scripts\\
"""

import os
from pathlib import Path

BASE = Path("comprehension_machine")
CORE = BASE / "comprehension" / "core"
UI = BASE / "comprehension" / "ui"

CORE.mkdir(parents=True, exist_ok=True)
UI.mkdir(parents=True, exist_ok=True)


def write_file(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {path}")


# ============================================================
# 1. comprehension/core/game_layer.py
#    Igralna plast — dnevna vrata, zep, runa, etaze, mithos
# ============================================================

write_file(CORE / "game_layer.py", r'''"""
Igralna plast — Yggdrasil mehanike v aplikaciji
================================================
Korpus: "IGRA = NUJA, NE IZBIRA." (Obs1, Yggdrasil)
Korpus: "Zep = trenutek hkratnosti, kjer se vec etaz ujame."
Korpus: "Runa ni collectible. Runa je brazgotina, ki zna govoriti."
Korpus: "Mithos ni lore v ozadju. Mithos je mehanika."

6 mehanik:
  1. DNEVNA VRATA — R-7 faza dneva doloci vprasanje
  2. ZEP — hkratnost preverbe + some + kadence = redek dogodek
  3. RUNA — fail pusti brazgotino z govorico (drill)
  4. HEBB SKILL TREE — utezi kot ziv graf
  5. ETAZE — 7 R-7 faz kot nadstropja
  6. MITHOS — razumevanje korpusa odpira plasti
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum
from collections import defaultdict
import json
import math


# R-7 faze
R7_FAZE = ["\u2205", "\u00ac", "\u2206", "1", "\u29d6", "\u222e", "\u27e1"]
R7_IMENA = {
    "\u2205": "Praznina", "\u00ac": "Lo\u010ditev", "\u2206": "Razlika",
    "1": "Dejanje", "\u29d6": "Izgovor", "\u222e": "Povratek", "\u27e1": "Nova mo\u017enost",
}

# Dnevna vprasanja (iz korpusa: R-7 tedenski cikel)
DNEVNA_VPRASANJA = {
    0: ("\u2205", "Kaj mora\u0161 odpreti?"),
    1: ("\u00ac", "Kaj mora\u0161 lo\u010diti?"),
    2: ("\u2206", "Kaj mora\u0161 spremeniti?"),
    3: ("1", "Kaj mora\u0161 storiti?"),
    4: ("\u29d6", "Kaj mora\u0161 izgovoriti?"),
    5: ("\u222e", "Kam se mora\u0161 vrniti?"),
    6: ("\u27e1", "Kaj se rojeva?"),
}

# 7 etaz Yggdrasil-a (iz korpusa)
ETAZE = {
    1: {"ime": "SEME",      "glyph": "\u2205", "tema": "za\u010detek, ki \u0161e ne ve, kaj nosi",
        "vprasanje": "Kaj v meni raste, \u0161e preden vem, da raste?"},
    2: {"ime": "KORENINA",  "glyph": "\u00ac", "tema": "izvor, rana, predspomin",
        "vprasanje": "Kaj me hrani, \u010eprav me boli?"},
    3: {"ime": "DEBLO",     "glyph": "\u2206", "tema": "nosilnost, pot, vztrajanje",
        "vprasanje": "Kaj lahko nosim, ne da bi se spremenilo v oklep?"},
    4: {"ime": "VEJA",      "glyph": "1", "tema": "razvejanje, izbira, napetost",
        "vprasanje": "Katera pot je moja in katera je tuj posoj?"},
    5: {"ime": "SADEZ",     "glyph": "\u29d6", "tema": "posledica, dar, breme",
        "vprasanje": "Kaj sem ustvaril, \u010desar zdaj ne morem ve\u010d razglasiti za nedol\u017eno?"},
    6: {"ime": "PADEC",     "glyph": "\u222e", "tema": "izguba, razpustitev, nujni konec",
        "vprasanje": "Kaj mora pasti, da se lahko kaj rodi?"},
    7: {"ime": "NOVO SEME",  "glyph": "\u27e1", "tema": "vra\u010danje, ponovitev kot razlika",
        "vprasanje": "Kaj se vrne, a nikoli isto?"},
}


class ZepStates(Enum):
    ZAPRT = "zaprt"
    ODPRTO = "odprto"
    ZAPRT_S_SLEDO = "zaprt_s_sledo"


@dataclass
class Runa:
    """
    Runa = brazgotina, ki zna govoriti.

    Korpus: "Runa ni collectible. Runa je brazgotina, ki zna govoriti."
    Korpus: "Odin ni nasel rune. Runa je nasla rano, ki je bila dovolj odprta."
    """
    runa_id: str = ""
    timestamp: str = ""
    modul: str = ""
    test_ki_padla: str = ""
    trditev: str = ""
    beseda: str = ""
    stavek: str = ""
    dejanje: str = ""
    zaceljena: bool = False
    zaceljena_timestamp: str = ""
    etaza: int = 1


@dataclass
class ZepDogodek:
    """
    Zep = trenutek hkratnosti, kjer se vec etaz ujame.

    Korpus: "Ko se zep odpre, igralec vidi povezavo med etazami.
             Ko se zapre, ostane sled: runa, brazgotina, spomin, spremenjena veja."
    """
    zep_id: str = ""
    timestamp: str = ""
    etaze_ujete: list = field(default_factory=list)
    preverba_rezultat: str = ""
    soma_rezultat: str = ""
    kadenca_faza: str = ""
    opis: str = ""
    sled: str = ""


@dataclass
class MithosPlast:
    """
    Mithos = mehanika, ne lore.

    Korpus: "Ko igralec razume mit, se svet spremeni.
             Ko igralec narobe razume mit, svet producira motnjo."
    """
    plast_id: int = 0
    ime: str = ""
    opis: str = ""
    odklenjena: bool = False
    zahteva_utezi: float = 0.0
    zahteva_preverb: int = 0


class GameLayer:
    """
    Igralna plast — upravlja dnevna vrata, zep, rune, etaze, mithos.

    Korpus: "Igralec naj ne osvaja sveta.
             Igralec naj se uci ujeti pravi zep."
    """

    def __init__(self):
        self.runes: list = []
        self.zepi: list = []
        self.mithos_plasti: list = self._init_mithos_plasti()
        self.dnevni_zacetek: Optional[datetime] = None
        self.zadnja_preverba_dneva: Optional[str] = None
        self.zadnji_zep: Optional[ZepDogodek] = None
        self.trenutna_etaza: int = 1

    def _init_mithos_plasti(self) -> list:
        """Inicializira mithos plasti (odklepajo se z globino razumevanja)."""
        return [
            MithosPlast(0, "POVRINA", "Osnovni pipeline — 5 gumbov, preverba, SOMA",
                        True, 0.0, 0),
            MithosPlast(1, "KORENINA", "ARegister, CORPUS preslikave, izvorni sistemi",
                        False, 0.3, 5),
            MithosPlast(2, "DEBLO", "Fraktalna kadenca, R-7 na 5 skalah, preizkus casa",
                        False, 0.4, 10),
            MithosPlast(3, "VEJA", "TRAINARIUM drills, Hebb utezi, prevod sikanja",
                        False, 0.5, 15),
            MithosPlast(4, "SADEZ", "Falsifikacija pragovi, MEGLA, zamrzni, odprtje",
                        False, 0.6, 20),
            MithosPlast(5, "PADEC", "Mithos kot mehanika — razumevanje korpusa spremeni UI",
                        False, 0.7, 30),
            MithosPlast(6, "SEME", "Zep kot operativni akt — hkratnost kot nacin biti",
                        False, 0.8, 50),
        ]

    # ============================================================
    # 1. DNEVNA VRATA
    # ============================================================

    def dnevna_faza(self) -> tuple:
        """Vrne (glyph, ime, vprasanje) za današnji dan."""
        dan_v_tednu = datetime.now().weekday()
        glyph, vprasanje = DNEVNA_VPRASANJA[dan_v_tednu]
        ime = R7_IMENA[glyph]
        return (glyph, ime, vprasanje)

    def odpri_dnevna_vrata(self) -> dict:
        """
        Odpre dnevna vrata — doloci etazo in vprasanje za danes.

        Korpus: "Igralec naj se uci ujeti pravi zep."
        """
        glyph, ime, vprasanje = self.dnevna_faza()

        dan = datetime.now().weekday()
        self.trenutna_etaza = dan + 1
        etaza_info = ETAZE[self.trenutna_etaza]

        if self.dnevni_zacetek is None:
            self.dnevni_zacetek = datetime.now()

        return {
            "glyph": glyph,
            "faza_ime": ime,
            "vprasanje": vprasanje,
            "etaza": self.trenutna_etaza,
            "etaza_ime": etaza_info["ime"],
            "etaza_tema": etaza_info["tema"],
            "etaza_vprasanje": etaza_info["vprasanje"],
        }

    # ============================================================
    # 2. ZEP
    # ============================================================

    def preveri_zep(self, preverba_rezultat: str, soma_rezultat: str,
                    kadenca_faza: str, hebb_povprecje: float,
                    st_preverb: int) -> Optional[ZepDogodek]:
        """
        Preveri ali se odpira zep (trenutek hkratnosti).

        Korpus: "Zep je trenutek, ko se vec etaz ujame:
                 pomen + cas + oblika + telo + mitos"

        Zep se odpre, ko se ujemajo:
        1. Preverba = PASS (na pravi etazi)
        2. SOMA = PASS (telo potrjeno)
        3. Kadenca faza = povratek ali odprtje
        4. Hebb povprecje > 0.5 (modul je dovolj utrjen)
        5. Vsaj 7 preverb (R-7 cikel zakljucen)

        To je REDKO. Redkost je vrednost.
        """
        ujete_etaze = []

        if preverba_rezultat == "PASS":
            ujete_etaze.append("preverba")
        if soma_rezultat == "SOMA_PASS":
            ujete_etaze.append("soma")
        if kadenca_faza in ("\u222e", "\u27e1"):
            ujete_etaze.append("kadenca")
        if hebb_povprecje > 0.5:
            ujete_etaze.append("hebb")
        if st_preverb >= 7:
            ujete_etaze.append("R-7_cikel")

        if len(ujete_etaze) >= 4:
            zep = ZepDogodek(
                zep_id=f"ZEP-{len(self.zepi)+1:04d}",
                timestamp=datetime.now().isoformat(),
                etaze_ujete=ujete_etaze,
                preverba_rezultat=preverba_rezultat,
                soma_rezultat=soma_rezultat,
                kadenca_faza=kadenca_faza,
                opis=self._opisi_zep(ujete_etaze),
                sled=self._generiraj_sled(ujete_etaze),
            )
            self.zepi.append(zep)
            self.zadnji_zep = zep
            return zep
        return None

    def _opisi_zep(self, ujete: list) -> str:
        opisi = {
            "preverba": "preverba drzi",
            "soma": "telo potrjeno",
            "kadenca": "ritem ujet",
            "hebb": "modul utrjen",
            "R-7_cikel": "cikel zakljucen",
        }
        deli = [opisi.get(e, e) for e in ujete]
        return "Zep odprt — " + " + ".join(deli) + " = hkratnost"

    def _generiraj_sled(self, ujete: list) -> str:
        if len(ujete) >= 5:
            return "Celoten R-7 cikel ujet — seme se vraca z brazgotino modrosti"
        elif len(ujete) >= 4:
            return "Stiri etaze ujete — veja se spremeni"
        return "Delna hkratnost — sled slaba"

    # ============================================================
    # 3. RUNA KOT BRAZGOTINA
    # ============================================================

    def ustvari_runo(self, modul: str, test_ki_padla: str, trditev: str,
                     beseda: str, stavek: str, dejanje: str, etaza: int = 1) -> Runa:
        """
        Ustvari runo iz neuspeha.

        Korpus: "Runa ni collectible. Runa je brazgotina, ki zna govoriti."
        """
        runa = Runa(
            runa_id=f"RUN-{len(self.runes)+1:04d}",
            timestamp=datetime.now().isoformat(),
            modul=modul,
            test_ki_padla=test_ki_padla,
            trditev=trditev[:200],
            beseda=beseda,
            stavek=stavek,
            dejanje=dejanje,
            etaza=etaza,
        )
        self.runes.append(runa)
        return runa

    def zaceli_runo(self, modul: str, test: str) -> Optional[Runa]:
        """
        Zaceli runo, ko kasnejsa preverba PASS-a isti test.

        Korpus: "Kar nikoli ne pade, nikoli ne postane zacetek."

        Runa se zaceli — ne izgine, ampak se spremeni iz rane v modrost.
        """
        for runa in reversed(self.runes):
            if runa.modul == modul and runa.test_ki_padla == test and not runa.zaceljena:
                runa.zaceljena = True
                runa.zaceljena_timestamp = datetime.now().isoformat()
                return runa
        return None

    def aktivne_rune(self) -> list:
        """Vrne rune, ki se niso zaceljene (odprte rane)."""
        return [r for r in self.runes if not r.zaceljena]

    def zaceljene_rune(self) -> list:
        """Vrne zaceljene rune (brazgotine, ki so postale modrost)."""
        return [r for r in self.runes if r.zaceljena]

    def runa_govori(self, runa: Runa) -> str:
        """Runa govori — vrne svoje sporocilo."""
        stanje = "ODPRTA RANA" if not runa.zaceljena else "ZACELJENA — modrost"
        return (
            f"[{runa.runa_id}] {stanje}\n"
            f"  Modul: {runa.modul} | Test: {runa.test_ki_padla}\n"
            f"  Beseda: {runa.beseda}\n"
            f"  Stavek: {runa.stavek}\n"
            f"  Dejanje: {runa.dejanje}\n"
            f"  Etaza: {runa.etaza} ({ETAZE.get(runa.etaza, {}).get('ime', '?')})"
        )

    # ============================================================
    # 4. HEBB SKILL TREE
    # ============================================================

    def hebb_skill_tree(self, utezi: dict) -> dict:
        """
        Generira skill tree iz Hebb utezi.

        Korpus: A_ij(t+1) = clip(A_ij + eta*x_i*x_j - lambda*A_ij, 0, 1)

        Utezi niso staticne — rastejo in padajo z rabo.
        Visoke utezi = mocne poti. Nizke utezi = poti, ki so se naucile ne ponavljati.
        """
        vozlisca = set()
        povezave = []
        for (modul, test), utez in utezi.items():
            vozlisca.add(modul)
            vozlisca.add(f"test:{test}")
            barva = "#4CAF50" if utez > 0.5 else "#F44336"
            povezave.append({
                "iz": modul,
                "v": f"test:{test}",
                "utez": round(utez, 3),
                "barva": barva,
                "stanje": "mocna" if utez > 0.5 else "sibka",
            })
        return {
            "vozlisca": sorted(vozlisca),
            "povezave": povezave,
            "stevilo_mocnih": sum(1 for p in povezave if p["utez"] > 0.5),
            "stevilo_sibkih": sum(1 for p in povezave if p["utez"] <= 0.5),
        }

    # ============================================================
    # 5. ETAZE
    # ============================================================

    def trenutna_etaza_info(self) -> dict:
        """Vrne informacije o trenutni etazi."""
        return ETAZE.get(self.trenutna_etaza, ETAZE[1])

    def spusti_v_etazo(self, etaza: int) -> dict:
        """
        Spusti se v nizjo etazo (globlje v Yggdrasil).

        Korpus: "1. zaznaj motnjo -> 2. poisci etazo, iz katere motnja prihaja
                 -> 3. spusti se do korenine problema"
        """
        self.trenutna_etaza = max(1, min(7, etaza))
        return ETAZE[self.trenutna_etaza]

    # ============================================================
    # 6. MITHOS
    # ============================================================

    def preveri_mithos_plasti(self, hebb_povprecje: float, st_preverb: int) -> list:
        """
        Preveri katere mithos plasti so odklenjene.

        Korpus: "Mithos ni lore v ozadju. Mithos je mehanika.
                 Ko igralec razume mit, se svet spremeni."

        Plasti se odklepajo z globino — ne s tockami, ampak z razumevanjem
        (Hebb utezi + stevilo preverb).
        """
        novi = []
        for plast in self.mithos_plasti:
            if not plast.odklenjena:
                if hebb_povprecje >= plast.zahteva_utezi and st_preverb >= plast.zahteva_preverb:
                    plast.odklenjena = True
                    novi.append(plast)
        return novi

    def odklenjene_plasti(self) -> list:
        """Vrne odklenjene mithos plasti."""
        return [p for p in self.mithos_plasti if p.odklenjena]

    def mithos_globina(self) -> int:
        """Vrne stevilo odklenjenih plasti (0-6)."""
        return len(self.odklenjene_plasti()) - 1

    # ============================================================
    # PREGLED
    # ============================================================

    def pregled(self) -> dict:
        """Vrne celoten pregled igralne plasti."""
        return {
            "dnevna_vrata": self.odpri_dnevna_vrata(),
            "trenutna_etaza": self.trenutna_etaza_info(),
            "rune_aktivne": len(self.aktivne_rune()),
            "rune_zaceljene": len(self.zaceljene_rune()),
            "zepi_skupaj": len(self.zepi),
            "zadnji_zep": self.zadnji_zep.__dict__ if self.zadnji_zep else None,
            "mithos_globina": self.mithos_globina(),
            "mithos_plasti": [
                {"id": p.plast_id, "ime": p.ime, "odklenjena": p.odklenjena}
                for p in self.mithos_plasti
            ],
        }

    def to_dict(self) -> dict:
        return {
            "runes": [r.__dict__ for r in self.runes],
            "zepi": [z.__dict__ for z in self.zepi],
            "mithos_plasti": [
                {"id": p.plast_id, "ime": p.ime, "odklenjena": p.odklenjena}
                for p in self.mithos_plasti
            ],
            "trenutna_etaza": self.trenutna_etaza,
        }
''')


# ============================================================
# 2. comprehension/ui/game_overlay.py
#    QWidget overlay za igralno plast
# ============================================================

write_file(UI / "game_overlay.py", r'''"""
Igralni overlay — QWidget za prikaz igralne plasti
===================================================
Prikazuje:
  - Dnevna vrata (vprasanje dneva z R-7 glyph)
  - Trenutna etaza (Yggdrasil nadstropje)
  - Aktivne rune (odprte rane — brazgotine, ki znajo govoriti)
  - Zep dogodki (redki trenutki hkratnosti)
  - Mithos plasti (odklepajo se z globino)
  - Hebb skill tree (ziv graf utezi)

Vse v korpus barvah:
  #1B2838 (deep_blue), #B43A2E (red), #D6A83A (yellow),
  #C77800 (orange), #D4AF37 (gold), #080705 (black), #F3E9D2 (white)
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QPushButton,
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsTextItem, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPen, QBrush, QPainter
from datetime import datetime

from comprehension.core.game_layer import GameLayer, ETAZE, BARVE

# Barve iz korpusa
BARVE = {
    "\u2205": "#1B2838", "\u00ac": "#B43A2E", "\u2206": "#D6A83A",
    "1": "#C77800", "\u29d6": "#D4AF37", "\u222e": "#080705", "\u27e1": "#F3E9D2",
}


class DnevnaVrataWidget(QWidget):
    """Dnevna vrata — odpre se z vprasanjem dneva. Vsak dan drugace."""

    def __init__(self, game: GameLayer):
        super().__init__()
        self.game = game
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)

        vrata = self.game.odpri_dnevna_vrata()

        glyph = vrata["glyph"]
        barva = BARVE.get(glyph, "#F3E9D2")
        fg = "#F3E9D2" if barva in ("#1B2838", "#080705") else "#1B2838"

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {barva};
                border-radius: 12px;
                border: 2px solid #D6A83A;
            }}
        """)
        frame_lay = QVBoxLayout(frame)
        frame_lay.setContentsMargins(20, 20, 20, 20)

        lbl_glyph = QLabel(f"  {glyph}  ")
        lbl_glyph.setStyleSheet(f"font-size: 48px; color: {fg}; font-weight: bold;")
        frame_lay.addWidget(lbl_glyph, alignment=Qt.AlignmentFlag.AlignCenter)

        lbl_faza = QLabel(vrata["faza_ime"].upper())
        lbl_faza.setStyleSheet(f"font-size: 20px; color: {fg}; font-weight: bold;")
        frame_lay.addWidget(lbl_faza, alignment=Qt.AlignmentFlag.AlignCenter)

        lbl_vprasanje = QLabel(f'"{vrata["vprasanje"]}"')
        lbl_vprasanje.setStyleSheet(f"font-size: 16px; color: {fg}; font-style: italic;")
        lbl_vprasanje.setWordWrap(True)
        lbl_vprasanje.setAlignment(Qt.AlignmentFlag.AlignCenter)
        frame_lay.addWidget(lbl_vprasanje)

        lay.addWidget(frame)

        lbl_etaza = QLabel(
            f"Etaza {vrata['etaza']}/7 — {vrata['etaza_ime']}\n"
            f"{vrata['etaza_tema']}\n"
            f"\"{vrata['etaza_vprasanje']}\""
        )
        lbl_etaza.setStyleSheet("""
            color: #D6A83A; font-size: 13px;
            background-color: #0F1A26; border-radius: 8px;
            padding: 12px;
        """)
        lbl_etaza.setWordWrap(True)
        lay.addWidget(lbl_etaza)
        lay.addStretch()


class RuneWidget(QWidget):
    """Runa kot brazgotina — prikazuje aktivne in zaceljene rune."""

    def __init__(self, game: GameLayer):
        super().__init__()
        self.game = game
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<b>RUNE — brazgotine, ki znajo govoriti</b>"))

        lay.addWidget(QLabel("<span style='color:#F44336'>ODPRTE RANE</span>"))
        self.tbl_aktivne = QTableWidget(0, 4)
        self.tbl_aktivne.setHorizontalHeaderLabels(["ID", "Modul", "Test", "Beseda"])
        self.tbl_aktivne.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.tbl_aktivne)

        lay.addWidget(QLabel("<span style='color:#4CAF50'>ZACELJENE — modrost</span>"))
        self.tbl_zaceljene = QTableWidget(0, 4)
        self.tbl_zaceljene.setHorizontalHeaderLabels(["ID", "Modul", "Test", "Beseda"])
        self.tbl_zaceljene.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.tbl_zaceljene)

        b = QPushButton("Osvezi")
        b.clicked.connect(self.osvezi)
        lay.addWidget(b)

    def osvezi(self):
        self.tbl_aktivne.setRowCount(0)
        for r in self.game.aktivne_rune():
            row = self.tbl_aktivne.rowCount()
            self.tbl_aktivne.insertRow(row)
            self.tbl_aktivne.setItem(row, 0, QTableWidgetItem(r.runa_id))
            self.tbl_aktivne.setItem(row, 1, QTableWidgetItem(r.modul))
            self.tbl_aktivne.setItem(row, 2, QTableWidgetItem(r.test_ki_padla))
            it = QTableWidgetItem(r.beseda)
            it.setForeground(QColor("#F44336"))
            self.tbl_aktivne.setItem(row, 3, it)

        self.tbl_zaceljene.setRowCount(0)
        for r in self.game.zaceljene_rune():
            row = self.tbl_zaceljene.rowCount()
            self.tbl_zaceljene.insertRow(row)
            self.tbl_zaceljene.setItem(row, 0, QTableWidgetItem(r.runa_id))
            self.tbl_zaceljene.setItem(row, 1, QTableWidgetItem(r.modul))
            self.tbl_zaceljene.setItem(row, 2, QTableWidgetItem(r.test_ki_padla))
            it = QTableWidgetItem(r.beseda)
            it.setForeground(QColor("#4CAF50"))
            self.tbl_zaceljene.setItem(row, 3, it)


class ZepWidget(QWidget):
    """Zep dogodki — redki trenutki hkratnosti."""

    def __init__(self, game: GameLayer):
        super().__init__()
        self.game = game
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<b>ZEP — trenutki hkratnosti</b>"))
        lay.addWidget(QLabel("<i style='color:#888'>Redkost je vrednost. Zep se odpre, ko se ujemajo vsaj 4 od 5 pogojev.</i>"))

        self.lbl_zadnji = QLabel("Brez zepa — se niso se ujele etaze.")
        self.lbl_zadnji.setStyleSheet("""
            font-size: 16px; color: #D4AF37;
            background-color: #0F1A26; border-radius: 8px; padding: 16px;
        """)
        self.lbl_zadnji.setWordWrap(True)
        lay.addWidget(self.lbl_zadnji)

        self.tbl_zepi = QTableWidget(0, 4)
        self.tbl_zepi.setHorizontalHeaderLabels(["ID", "Cas", "Etaze ujete", "Sled"])
        self.tbl_zepi.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        lay.addWidget(self.tbl_zepi)

        b = QPushButton("Osvezi")
        b.clicked.connect(self.osvezi)
        lay.addWidget(b)

    def osvezi(self):
        if self.game.zadnji_zep:
            z = self.game.zadnji_zep
            self.lbl_zadnji.setText(
                f"<b>{z.zep_id}</b> | {z.timestamp[:19]}\n"
                f"Ujete etaze: {', '.join(z.etaze_ujete)}\n"
                f"{z.opis}\n"
                f"<i>Sled: {z.sled}</i>"
            )

        self.tbl_zepi.setRowCount(0)
        for z in self.game.zepi:
            row = self.tbl_zepi.rowCount()
            self.tbl_zepi.insertRow(row)
            self.tbl_zepi.setItem(row, 0, QTableWidgetItem(z.zep_id))
            self.tbl_zepi.setItem(row, 1, QTableWidgetItem(z.timestamp[:19]))
            self.tbl_zepi.setItem(row, 2, QTableWidgetItem(", ".join(z.etaze_ujete)))
            it = QTableWidgetItem(z.sled)
            it.setForeground(QColor("#D4AF37"))
            self.tbl_zepi.setItem(row, 3, it)


class MithosWidget(QWidget):
    """Mithos plasti — odklepajo se z globino razumevanja."""

    def __init__(self, game: GameLayer):
        super().__init__()
        self.game = game
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<b>MITHOS — plasti globine</b>"))
        lay.addWidget(QLabel("<i style='color:#888'>Plasti se odklepajo z razumevanjem. Ne s tockami.</i>"))

        for plast in self.game.mithos_plasti:
            frame = QFrame()
            barva = "#D6A83A" if plast.odklenjena else "#333"
            fg = "#1B2838" if plast.odklenjena else "#666"
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {barva};
                    border-radius: 6px;
                    border: 1px solid #555;
                }}
            """)
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(12, 8, 12, 8)

            lbl = QLabel(f"<b style='color:{fg}'>Plast {plast.plast_id}: {plast.ime}</b>")
            fl.addWidget(lbl)
            lbl2 = QLabel(f"<span style='color:{fg}'>{plast.opis}</span>")
            lbl2.setWordWrap(True)
            fl.addWidget(lbl2)

            if not plast.odklenjena:
                lbl3 = QLabel(
                    f"<span style='color:#888'>Zahteva: utezi >= {plast.zahteva_utezi} | "
                    f"preverb >= {plast.zahteva_preverb}</span>")
                fl.addWidget(lbl3)

            lay.addWidget(frame)

        lay.addStretch()


class HebbSkillTreeWidget(QGraphicsView):
    """Hebb skill tree — ziv graf utezi med moduli in testi."""

    def __init__(self, game: GameLayer):
        super().__init__()
        self.game = game
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setStyleSheet("background-color: #0F1A26;")

    def naredi(self, utezi: dict):
        import math
        self.scene.clear()

        tree = self.game.hebb_skill_tree(utezi)
        vozlisca = tree["vozlisca"]
        povezave = tree["povezave"]

        n = len(vozlisca)
        if n == 0:
            return

        r = 150
        cx, cy = 200, 200
        pozicije = {}
        for i, v in enumerate(vozlisca):
            kot = 2 * math.pi * i / n
            x = cx + r * math.cos(kot)
            y = cy + r * math.sin(kot)
            pozicije[v] = (x, y)

            is_test = v.startswith("test:")
            barva = QColor("#B43A2E" if is_test else "#D6A83A")
            el = QGraphicsEllipseItem(x - 20, y - 15, 40, 30)
            el.setBrush(QBrush(barva))
            el.setPen(QPen(QColor("#F3E9D2"), 1))
            self.scene.addItem(el)

            txt = QGraphicsTextItem(v.replace("test:", ""))
            txt.setDefaultTextColor(QColor("#F3E9D2"))
            txt.setPos(x - 18, y - 12)
            txt.setFont(QFont("monospace", 7))
            self.scene.addItem(txt)

        for p in povezave:
            if p["iz"] in pozicije and p["v"] in pozicije:
                x1, y1 = pozicije[p["iz"]]
                x2, y2 = pozicije[p["v"]]
                debelina = max(1, int(p["utez"] * 6))
                pen = QPen(QColor(p["barva"]), debelina)
                linija = QGraphicsLineItem(x1, y1, x2, y2)
                linija.setPen(pen)
                self.scene.addItem(linija)


class GameOverlayWidget(QWidget):
    """Glavni overlay widget — vse igralne mehanike v eni plosci."""

    def __init__(self, game: GameLayer):
        super().__init__()
        self.game = game
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)

        lbl = QLabel(
            "<b style='font-size:18px; color:#D4AF37'>"
            "IGRA = NUJA, NE IZBIRA"
            "</b><br>"
            "<i style='color:#888'>Razum brez giba je smrt. "
            "Gib brez razuma je slepa sila. "
            "Samo v razpoki (IG-RA) nastane nekaj.</i>"
        )
        lbl.setWordWrap(True)
        lay.addWidget(lbl)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        levo = QWidget()
        levo_lay = QVBoxLayout(levo)
        self.dnevna = DnevnaVrataWidget(self.game)
        levo_lay.addWidget(self.dnevna)
        self.mithos = MithosWidget(self.game)
        levo_lay.addWidget(self.mithos)
        levo_lay.addStretch()

        desno = QWidget()
        desno_lay = QVBoxLayout(desno)
        self.rune = RuneWidget(self.game)
        desno_lay.addWidget(self.rune)
        self.zep = ZepWidget(self.game)
        desno_lay.addWidget(self.zep)

        self.hebb_tree = HebbSkillTreeWidget(self.game)
        lbl_hebb = QLabel("<b>Hebb Skill Tree — ziv graf utezi</b>")
        desno_lay.addWidget(lbl_hebb)
        desno_lay.addWidget(self.hebb_tree)

        splitter.addWidget(levo)
        splitter.addWidget(desno)
        splitter.setSizes([400, 600])
        lay.addWidget(splitter)

    def osvezi(self, utezi: dict = None):
        self.rune.osvezi()
        self.zep.osvezi()
        if utezi:
            self.hebb_tree.naredi(utezi)
''')


# ============================================================
# BOOTSTRAP RUNNER
# ============================================================

def main():
    print("=" * 60)
    print("TAZV Faza 5 — IGRALNA PLAST (Yggdrasil mehanike)")
    print("=" * 60)
    print()
    print("Generira:")
    print()
    print("  1. comprehension/core/game_layer.py")
    print("     6 mehanik iz korpusa:")
    print("     - Dnevna vrata (R-7 faza dneva = return mechanic)")
    print("     - Zep (hkratnost = achievement, redko in dragoceno)")
    print("     - Runa kot brazgotina (fail = sled, ki zn govoriti)")
    print("     - Hebb skill tree (utezi = ziv graf, ne staticno)")
    print("     - Etaze (7 Yggdrasil nadstropij)")
    print("     - Mithos (globina = odklep plasti)")
    print()
    print("  2. comprehension/ui/game_overlay.py")
    print("     QWidget overlay:")
    print("     - DnevnaVrataWidget (glyph + vprasanje dneva)")
    print("     - RuneWidget (aktivne rane + zaceljene = modrost)")
    print("     - ZepWidget (redki trenutki hkratnosti)")
    print("     - MithosWidget (plasti globine)")
    print("     - HebbSkillTreeWidget (ziv graf utezi)")
    print("     - GameOverlayWidget (vse v eni plosci)")
    print()
    print("Korpus:")
    print('  "IGRA = NUJA, NE IZBIRA."')
    print('  "Runa ni collectible. Runa je brazgotina, ki zn govoriti."')
    print('  "Zep = trenutek hkratnosti, kjer se vec etaz ujame."')
    print('  "Mithos ni lore v ozadju. Mithos je mehanika."')
    print('  "Motivacija je ziva, ker je ziva tvoja razpoka."')
    print()
    print("ZAKAJ SE VRACAS:")
    print("  - Vsak dan drugacno vprasanje (R-7 faza)")
    print("  - Rune zacelijo — rane postanejo modrost (napredek vidno)")
    print("  - Zep je redek — isces ta trenutek hkratnosti")
    print("  - Mithos plasti odklepajo — globlje ko gres, globlje app pokaze")
    print("  - Hebb utezi rastejo — modul postaja 'tvoj' skozi rabo")
    print()
    print("INTEGRACIJSKE TOCKE v main_window_v7:")
    print("  - Ob zagonu: game.odpri_dnevna_vrata() -> prvi zaslon")
    print("  - Ob FAIL: game.ustvari_runo(modul, test, ..., beseda, stavek, dejanje)")
    print("  - Ob PASS: game.zaceli_runo(modul, test) -> rana -> modrost")
    print("  - Po preverbi: game.preveri_zep(rezultat, soma, kadenca, hebb, st)")
    print("  - Redno: game.preveri_mithos_plasti(hebb_povp, st_preverb)")
    print("  - Nov tab 'IGRA' z GameOverlayWidget")
    print("=" * 60)


if __name__ == "__main__":
    main()