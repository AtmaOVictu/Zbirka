#!/usr/bin/env python3
"""
TAZV Faza 5 — IGRALNA PLAST (napredovanje, grajenje, optimizirane akcije)
=========================================================================
Korpus: "IGRA = NUJA, NE IZBIRA." (Obs1, Yggdrasil)
Korpus: "Loki se aktivira, ko igralec postane preveucinkovit."
Korpus: "Nidhoggr deluje kot timer globine."
Korpus: "Odin dobi rune samo, ce nekaj pusti viseti za seboj."
Korpus: "Progress naj bo vezan na prehode in receipts, ne na score."

PREJSNJI NAPAVEK: app "ze je igra" — ne, je konstrukt.
Igra potrebuje:
  1. NAPREDOVANJE — igralec napreduje skozi etaze, odklepa sposobnosti
  2. GRAJENJE — igralec gradi persistentno strukturo (kanon = Yggdrasil)
  3. OPTIMIZIRANE AKCIJE — vec poti, izbire, trade-offs, vir sprotno

3 sistemi igre:
  A. PROGRESSION — register transitions (candidate->approved->canon) = napredek
     Hebb utezi rastejo = modul postaja "tvoj"
     Etaze se odklepajo z globino
     Mithos plasti se odklepajo z razumevanjem

  B. CANON BUILDER — igralec gradi osebni Yggdrasil
     Vsaka preverba PASS = vozlisce v drevesu
     Vozlisca se povezujejo z robovi (odnosi med resnicami)
     Hebb utezi med vozlisci = moc povezave
     Runa = brazgotina, ki se zaceli in postane modrost
     Odin: zrtvuj kanon vnos za globlje znanje (rune)

  C. ACTION ECONOMY — vir "preverba energija" na sejo
     Vsaka preverba stane energijo
     Izbira: kateri modul testirati (7 modulov = 7 poti)
     Izbira: katero etazo obdelati (globlje = drainscno a bolj vredno)
     Izbira: resiti kontradikcijo ali karanteno ali ignorirati (Nidhoggr)
     Loki: ce ponavljas isto resitev, spremeni pravila
     Nidhoggr: ce delas samo povrsinsko, korenine gnijejo

Korpus o napredku (Obs1, 2fca2330):
  "3 contradictions resolved today."
  "2 candidate definitions approved."
  "1 canon conflict quarantined."
  "5 orphan nodes linked."
  Ne score kot avtoriteta — receipts in prehodi.

Generira:
  1. comprehension/core/game_engine.py — progression, canon builder, action economy
  2. comprehension/ui/game_panel.py — igralni panel (drevo, vir, etaze, cilji)

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
# 1. comprehension/core/game_engine.py
#    Igralni engine — progression, canon builder, action economy
# ============================================================

write_file(CORE / "game_engine.py", r'''"""
Igralni engine — napredovanje, grajenje, optimizirane akcije
=============================================================
Trije sistemi:

A. PROGRESSION
   - Register transitions (candidate->approved->canon) = napreduk
   - Hebb utezi rastejo z rabo = modul postaja "tvoj"
   - Etaze se odklepajo z globino (1-7)
   - Mithos plasti se odklepajo z razumevanjem

B. CANON BUILDER
   - Igralec gradi osebni Yggdrasil iz preverjenih resnic
   - Vsaka preverba PASS = vozlisce v drevesu
   - Vozlisca se povezujejo z robovi (odnosi)
   - Runa = brazgotina iz FAIL, ki se zaceli ob kasnejsi PASS
   - Odin: zrtvuj kanon vnos za rune (globlje znanje)

C. ACTION ECONOMY
   - Vir "preverba energija" na sejo (pocasi se obnovi)
   - Izbira modula (7 poti)
   - Izbira etaze (globina = tveganje/nagrada)
   - Loki: preprecuje repetitivno optimizacijo
   - Nidhoggr: timer globine — povrsinsko delo = razpad

Korpus:
  "Progress naj bo vezan na prehode in receipts, ne na score."
  "Loki se aktivira, ko igralec postane preveucinkovit."
  "Nidhoggr deluje kot timer globine."
  "Odin dobi rune samo, ce nekaj pusti viseti za seboj."
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from enum import Enum
from collections import defaultdict, deque
import json
import math
import hashlib


# ============================================================
# A. PROGRESSION SYSTEM
# ============================================================

class RegisterStatus(Enum):
    RAW = "raw"
    CANDIDAT = "candidate"
    APPROVED = "approved"
    CANON = "canon"
    MEGLA = "megla"
    ARHIV = "arhiv"


@dataclass
class CanonNode:
    """Vozlisce v osebnem Yggdrasil-u — preverjena resnica."""
    node_id: str = ""
    modul: str = ""
    trditev: str = ""
    status: str = "candidate"
    dokaz_nivo: str = ""
    timestamp: str = ""
    etaza: int = 1
    hebb_utez: float = 0.5
    povezave: list = field(default_factory=list)
    runa_id: Optional[str] = None
    zrtvovana: bool = False


@dataclass
class Runa:
    """Runa = brazgotina, ki zn govoriti. Nastane iz FAIL."""
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
    cena: str = ""
    znanje: str = ""


@dataclass
class EtazaInfo:
    """7 etaz Yggdrasil-a."""
    stevilka: int
    ime: str
    glyph: str
    tema: str
    vprasanje: str
    odklenjena: bool = False
    zahteva_kanon: int = 0


ETAZE = [
    EtazaInfo(1, "SEME", "\u2205", "zacetek, ki se ne ve, kaj nosi",
              "Kaj v meni raste, se preden vem, da raste?", True, 0),
    EtazaInfo(2, "KORENINA", "\u00ac", "izvor, rana, predspomin",
              "Kaj me hrani, ceprav me boli?", False, 3),
    EtazaInfo(3, "DEBLO", "\u2206", "nosilnost, pot, vztrajanje",
              "Kaj lahko nosim, ne da bi se spremenilo v oklep?", False, 7),
    EtazaInfo(4, "VEJA", "1", "razvejanje, izbira, napetost",
              "Katera pot je moja in katera je tuj posoj?", False, 12),
    EtazaInfo(5, "SADEZ", "\u29d6", "posledica, dar, breme",
              "Kaj sem ustvaril, cesar zdaj ne morem vec razglasiti za nedolzno?", False, 18),
    EtazaInfo(6, "PADEC", "\u222e", "izguba, razpustitev, nujni konec",
              "Kaj mora pasti, da se lahko kaj rodi?", False, 25),
    EtazaInfo(7, "NOVO SEME", "\u27e1", "vracanje, ponovitev kot razlika",
              "Kaj se vrne, a nikoli isto?", False, 35),
]

MITHOS_PLASTI = [
    {"id": 0, "ime": "POVRSINA", "opis": "Osnovni pipeline", "zahteva_utezi": 0.0, "zahteva_preverb": 0},
    {"id": 1, "ime": "KORENINA", "opis": "ARegister, CORPUS preslikave", "zahteva_utezi": 0.3, "zahteva_preverb": 5},
    {"id": 2, "ime": "DEBLO", "opis": "Fraktalna kadenca, R-7", "zahteva_utezi": 0.4, "zahteva_preverb": 10},
    {"id": 3, "ime": "VEJA", "opis": "TRAINARIUM, Hebb utezi", "zahteva_utezi": 0.5, "zahteva_preverb": 15},
    {"id": 4, "ime": "SADEZ", "opis": "Falsifikacija, pragovi", "zahteva_utezi": 0.6, "zahteva_preverb": 20},
    {"id": 5, "ime": "PADEC", "opis": "Mithos kot mehanika", "zahteva_utezi": 0.7, "zahteva_preverb": 30},
    {"id": 6, "ime": "SEME", "opis": "Zep kot nacin biti", "zahteva_utezi": 0.8, "zahteva_preverb": 50},
]


# ============================================================
# B. CANON BUILDER
# ============================================================

class CanonBuilder:
    """
    Igralec gradi osebni Yggdrasil iz preverjenih resnic.

    Korpus: "Vsaka etaza nastane iz prejšnje, jo nosi, jo preseze
             in se nekoc vrne k zacetku."
    """

    def __init__(self):
        self.nodes: dict = {}
        self.edges: list = []
        self.runes: list = []
        self.zrtvovane_rune: list = []

    def dodaj_kandidata(self, modul: str, trditev: str, etaza: int = 1) -> CanonNode:
        """Dodaj nov kandidat v kanon (po ZAJEMI)."""
        nid = hashlib.md5(
            f"{modul}:{trditev[:50]}:{datetime.now().isoformat()}"
            .encode()).hexdigest()[:10]
        node = CanonNode(
            node_id=nid, modul=modul, trditev=trditev[:200],
            status="candidate", timestamp=datetime.now().isoformat(),
            etaza=etaza,
        )
        self.nodes[nid] = node
        return node

    def promoviraj(self, node_id: str, nov_status: str, dokaz: str = ""):
        """Promoviraj node: candidate -> approved -> canon."""
        node = self.nodes.get(node_id)
        if not node:
            return
        node.status = nov_status
        node.dokaz_nivo = dokaz

        if nov_status == "canon":
            for other in self.nodes.values():
                if (other.node_id != node_id and other.status == "canon"
                        and other.modul == node.modul):
                    self.dodaj_povezavo(node_id, other.node_id, 0.5)

    def dodaj_povezavo(self, from_id: str, to_id: str, utez: float = 0.5):
        """Dodaj povezavo med vozlisci (odnos med resnicami)."""
        for e in self.edges:
            if (e["from"] == from_id and e["to"] == to_id) or \
               (e["from"] == to_id and e["to"] == from_id):
                e["utez"] = max(e["utez"], utez)
                return
        self.edges.append({"from": from_id, "to": to_id, "utez": utez})
        n1 = self.nodes.get(from_id)
        n2 = self.nodes.get(to_id)
        if n1 and to_id not in n1.povezave:
            n1.povezave.append(to_id)
        if n2 and from_id not in n2.povezave:
            n2.povezave.append(from_id)

    def stevilo_kanon(self) -> int:
        return sum(1 for n in self.nodes.values() if n.status == "canon")

    def stevilo_kandidat(self) -> int:
        return sum(1 for n in self.nodes.values() if n.status == "candidate")

    def stevilo_approved(self) -> int:
        return sum(1 for n in self.nodes.values() if n.status == "approved")

    def ustvari_runo(self, modul: str, test: str, trditev: str,
                     beseda: str, stavek: str, dejanje: str, etaza: int = 1) -> Runa:
        """Ustvari runo iz neuspeha."""
        runa = Runa(
            runa_id=f"RUN-{len(self.runes)+1:04d}",
            timestamp=datetime.now().isoformat(),
            modul=modul, test_ki_padla=test, trditev=trditev[:200],
            beseda=beseda, stavek=stavek, dejanje=dejanje, etaza=etaza,
            cena=test, znanje=beseda,
        )
        self.runes.append(runa)
        return runa

    def zaceli_runo(self, modul: str, test: str) -> Optional[Runa]:
        """Zaceli runo ob kasnejsi PASS."""
        for runa in reversed(self.runes):
            if runa.modul == modul and runa.test_ki_padla == test and not runa.zaceljena:
                runa.zaceljena = True
                runa.zaceljena_timestamp = datetime.now().isoformat()
                return runa
        return None

    def odin_zrtvuj(self, node_id: str) -> Optional[Runa]:
        """
        Odin: zrtvuj kanon vnos za rune (globlje znanje).

        Korpus: "Igralec dobi rune samo, ce nekaj pusti viseti za seboj."
        """
        node = self.nodes.get(node_id)
        if not node or node.status != "canon" or node.zrtvovana:
            return None

        node.zrtvovana = True
        node.status = "arhiv"

        runa = Runa(
            runa_id=f"RUN-ODIN-{len(self.zrtvovane_rune)+1:04d}",
            timestamp=datetime.now().isoformat(),
            modul=node.modul, test_ki_padla="odin_zrtvovanje",
            trditev=node.trditev,
            beseda=f"zrtvovano: {node.trditev[:60]}",
            stavek="globlje znanje zahteva ceno",
            dejanje="sprejmi izgubo kot odprtje",
            etaza=node.etaza,
            cena=node.trditev[:60],
            znanje="rune_odin",
        )
        self.zrtvovane_rune.append(runa)
        return runa

    def aktivne_rune(self) -> list:
        return [r for r in self.runes if not r.zaceljena]

    def zaceljene_rune(self) -> list:
        return [r for r in self.runes if r.zaceljena]

    def yggdrasil_graf(self) -> dict:
        """Vrne graf za vizualizacijo Yggdrasil drevesa."""
        vozlisca = []
        for n in self.nodes.values():
            if n.status == "canon" and not n.zrtvovana:
                vozlisca.append({
                    "id": n.node_id, "modul": n.modul,
                    "trditev": n.trditev[:40], "etaza": n.etaza,
                    "hebb": n.hebb_utez,
                })
        return {"vozlisca": vozlisca, "robovi": self.edges}


# ============================================================
# C. ACTION ECONOMY
# ============================================================

@dataclass
class SejaCilj:
    """Sejni cilj — ne score, receipts."""
    opis: str = ""
    tip: str = ""
    cilj: int = 0
    trenutno: int = 0
    dosezen: bool = False


class ActionEconomy:
    """
    Vir preverba energije + sejni cilji.

    Korpus: "Ne bi delal 'score' kot avtoriteta.
             Progress naj bo vezan na prehode in receipts."
    """

    def __init__(self, max_energija: int = 10):
        self.max_energija = max_energija
        self.energija = max_energija
        self.st_preverb: int = 0
        self.st_fail: int = 0
        self.st_pass: int = 0
        self.cilji: list = []
        self.zadnja_resitev: str = ""
        self.st_ponovitev_resitve: int = 0
        self.loki_aktiviran: bool = False
        self.nidhogg_timer: int = 0

    def porabi_energijo(self, kolicina: int, etaza: int = 1) -> bool:
        """Porabi energijo za preverbo. Vecja etaza = vecja poraba."""
        cena = kolicina + (etaza - 1)
        if self.energija < cena:
            return False
        self.energija -= cena
        return True

    def regeneriraj(self, kolicina: int = 1):
        """Regeneriraj energijo (pocasno, s kadencom)."""
        self.energija = min(self.max_energija, self.energija + kolicina)

    def zabelezi_resitev(self, resitev: str, globina: int = 1):
        """
        Zabelezi resitev in preveri Lokija.

        Korpus: "Ko igralec predolgo uporablja isto resitev,
                 Loki pokvari njen ucinek."
        """
        if resitev == self.zadnja_resitev:
            self.st_ponovitev_resitve += 1
            if self.st_ponovitev_resitve >= 3:
                self.loki_aktiviran = True
                self.st_ponovitev_resitve = 0
                return "loki"
        else:
            self.zadnja_resitev = resitev
            self.st_ponovitev_resitve = 0
            self.loki_aktiviran = False

        if globina <= 1:
            self.nidhogg_timer += 1
        else:
            self.nidhogg_timer = max(0, self.nidhogg_timer - 2)

        return "ok"

    def nidhogg_stanje(self) -> str:
        """Stanje Nidhoggr-a (timer globine)."""
        if self.nidhogg_timer >= 7:
            return "KRITICNO — korenine gnijejo. Povrsinsko delo predolgo."
        elif self.nidhogg_timer >= 4:
            return "OPOZORILO — korenine slabijo. Poglobi se."
        elif self.nidhogg_timer >= 2:
            return "NIZJA — globina se izgublja."
        return "STABILNO"

    def postavi_cilje(self, seja_stevilo: int = 1):
        """Postavi sejne cilje (ne score, receipts)."""
        self.cilji = [
            SejaCilj("Resi 3 kontradikcije", "contradictions", 3, 0),
            SejaCilj("Odobri 2 kandidata", "approvals", 2, 0),
            SejaCilj("Povezi 5 osirotelih vozlisc", "orphans", 5, 0),
            SejaCilj("Pojdi v etazo 3+", "etaza", 3, 0),
        ]

    def posodobi_cilj(self, tip: str, kolicina: int = 1):
        """Posodobi sejni cilj."""
        for c in self.cilji:
            if c.tip == tip:
                c.trenutno += kolicina
                if c.trenutno >= c.cilj:
                    c.dosezen = True

    def povzetek_ciljev(self) -> list:
        return [
            {"opis": c.opis, "cilj": c.cilj, "trenutno": c.trenutno,
             "dosezen": c.dosezen}
            for c in self.cilji
        ]

    def regeneriraj_lokija(self):
        """Resetiraj Lokija po spremembi pravil."""
        self.loki_aktiviran = False
        self.st_ponovitev_resitve = 0
        self.zadnja_resitev = ""


# ============================================================
# GAME ENGINE — vse skupaj
# ============================================================

class GameEngine:
    """
    Igralni engine — napredovanje, grajenje, optimizirane akcije.

    Trije sistemi:
      A. Progression (register transitions + etaze + mithos)
      B. CanonBuilder (osebni Yggdrasil)
      C. ActionEconomy (energija + Loki + Nidhoggr + cilji)
    """

    def __init__(self):
        self.canon = CanonBuilder()
        self.economy = ActionEconomy(max_energija=10)
        self.etaze = ETAZE
        self.mithos = [dict(p, odklenjena=(p["id"] == 0)) for p in MITHOS_PLASTI]
        self.hebb_utezi: dict = {}
        self.zepi: list = []
        self.zadnji_zep = None
        self.st_preverb_skupaj: int = 0

    # --- PROGRESSION ---

    def odpri_etazo(self, stevilka: int) -> dict:
        """Preveri ali je etaza odklenjena in jo odkleni, ce je."""
        for e in self.etaze:
            if e.stevilka == stevilka:
                if not e.odklenjena:
                    if self.canon.stevilo_kanon() >= e.zahteva_kanon:
                        e.odklenjena = True
                        return {"odklenjena": True, "etaza": e.__dict__}
                    else:
                        return {"odklenjena": False,
                                "zahteva": e.zahteva_kanon,
                                "ima": self.canon.stevilo_kanon(),
                                "etaza": e.__dict__}
                return {"odklenjena": True, "etaza": e.__dict__}
        return {"odklenjena": False}

    def odklenjene_etaze(self) -> list:
        return [e for e in self.etaze if e.odklenjena]

    def preveri_mithos(self, hebb_povp: float, st_preverb: int) -> list:
        """Odklene mithos plasti z globino razumevanja."""
        novi = []
        for p in self.mithos:
            if not p["odklenjena"]:
                if hebb_povp >= p["zahteva_utezi"] and st_preverb >= p["zahteva_preverb"]:
                    p["odklenjena"] = True
                    novi.append(p)
        return novi

    def mithos_globina(self) -> int:
        return sum(1 for p in self.mithos if p["odklenjena"]) - 1

    def hebb_povprecje(self) -> float:
        if not self.hebb_utezi:
            return 0.0
        return sum(self.hebb_utezi.values()) / len(self.hebb_utezi)

    # --- AKCIJE ---

    def act_zajemi(self, modul: str, trditev: str, etaza: int = 1) -> dict:
        """ZAJEMI — dodaj kandidata. Stane 1 energijo."""
        if not self.economy.porabi_energijo(1, etaza):
            return {"napaka": "Ni dovolj energije"}

        node = self.canon.dodaj_kandidata(modul, trditev, etaza)
        self.economy.posodobi_cilj("orphans", 1)
        return {"node_id": node.node_id, "status": "candidate", "energija": self.economy.energija}

    def act_preveri(self, node_id: str, rezultat: str, modul: str,
                    test: str = "", trditev: str = "", etaza: int = 1,
                    drill: dict = None) -> dict:
        """
        PREVERI — glavna igralna akcija.

        Stane energijo (vecjo v visjih etazah).
        PASS: promoviraj node, zaceli runo, posodobi cilje.
        FAIL: ustvari runo, sprozi TRAINARIUM, posodobi Nidhoggr.
        """
        cena = 2 + (etaza - 1)
        if not self.economy.porabi_energijo(2, etaza):
            return {"napaka": "Ni dovolj energije za preverbo"}

        self.st_preverb_skupaj += 1
        self.economy.st_preverb += 1
        rezultat_detail = {"rezultat": rezultat, "energija": self.economy.energija}

        resitev_key = f"{modul}:{test}"
        loki = self.economy.zabelezi_resitev(resitev_key, etaza)
        if loki == "loki":
            rezultat_detail["loki"] = (
                "Loki aktiviran! Ponavljas isto resitev. "
                "Sprememba pravil — poisci drugo pot."
            )

        if rezultat == "PASS":
            self.economy.st_pass += 1
            if node_id:
                self.canon.promoviraj(node_id, "approved", "PASS")
            if test:
                runa = self.canon.zaceli_runo(modul, test)
                if runa:
                    rezultat_detail["runa_zaceljena"] = runa.runa_id
            self.economy.posodobi_cilj("approvals", 1)
            kljuc = (modul, test or "pass")
            self.hebb_utezi[kljuc] = min(1.0, self.hebb_utezi.get(kljuc, 0.5) + 0.1)

        elif rezultat == "FAIL":
            self.economy.st_fail += 1
            if drill:
                runa = self.canon.ustvari_runo(
                    modul, test, trditev,
                    drill.get("beseda", ""),
                    drill.get("stavek", ""),
                    drill.get("dejanje", ""),
                    etaza,
                )
                rezultat_detail["runa"] = runa.runa_id
            kljuc = (modul, test or "fail")
            self.hebb_utezi[kljuc] = max(0.0, self.hebb_utezi.get(kljuc, 0.5) - 0.15)

        etaza_rez = self.odpri_etazo(etaza + 1)
        if etaza_rez.get("odklenjena"):
            rezultat_detail["nova_etaza"] = etaza_rez["etaza"]["ime"]

        novi_mithos = self.preveri_mithos(self.hebb_povprecje(), self.st_preverb_skupaj)
        if novi_mithos:
            rezultat_detail["nova_mithos"] = [p["ime"] for p in novi_mithos]

        zep = self.preveri_zep(rezultat, etaza)
        if zep:
            rezultat_detail["zep"] = zep

        rezultat_detail["nidhogg"] = self.economy.nidhogg_stanje()

        return rezultat_detail

    def act_shrani(self, node_id: str) -> dict:
        """SHRANI — promoviraj approved v canon. Ne stane energije."""
        node = self.canon.nodes.get(node_id)
        if not node:
            return {"napaka": "node ne obstaja"}
        if node.status != "approved":
            return {"napaka": f"node ni approved (status={node.status})"}

        self.canon.promoviraj(node_id, "canon", node.dokaz_nivo)
        self.economy.posodobi_cilj("approvals", 1)

        for e in self.etaze:
            if not e.odklenjena and self.canon.stevilo_kanon() >= e.zahteva_kanon:
                e.odklenjena = True

        return {"node_id": node_id, "status": "canon",
                "kanon_stevilo": self.canon.stevilo_kanon()}

    def act_odin_zrtvuj(self, node_id: str) -> dict:
        """
        ODIN — zrtvuj kanon vnos za rune (globlje znanje).

        Korpus: "Igralec dobi rune samo, ce nekaj pusti viseti za seboj."
        """
        runa = self.canon.odin_zrtvuj(node_id)
        if not runa:
            return {"napaka": "node ni kanon ali je ze zrtvovan"}
        return {"runa": runa.runa_id, "znanje": runa.znanje, "cena": runa.cena}

    def preveri_zep(self, rezultat: str, etaza: int) -> Optional[dict]:
        """Zep = redek trenutek hkratnosti."""
        pogoji = 0
        if rezultat == "PASS": pogoji += 1
        if self.hebb_povprecje() > 0.5: pogoji += 1
        if self.st_preverb_skupaj >= 7: pogoji += 1
        if etaza >= 3: pogoji += 1
        if self.economy.energija > 3: pogoji += 1

        if pogoji >= 4:
            zep = {
                "zep_id": f"ZEP-{len(self.zepi)+1:04d}",
                "timestamp": datetime.now().isoformat(),
                "pogoji": pogoji,
                "sled": "Hkratnost ujeta — seme se vraca z brazgotino modrosti",
            }
            self.zepi.append(zep)
            self.zadnji_zep = zep
            return zep
        return None

    # --- NAPREDOVANJE ---

    def napredek(self) -> dict:
        """Vrne celoten pregled napredka."""
        return {
            "kanon": self.canon.stevilo_kanon(),
            "approved": self.canon.stevilo_approved(),
            "kandidat": self.canon.stevilo_kandidat(),
            "rune_aktivne": len(self.canon.aktivne_rune()),
            "rune_zaceljene": len(self.canon.zaceljene_rune()),
            "rune_odin": len(self.canon.zrtvovane_rune),
            "etaze_odklenjene": len(self.odklenjene_etaze()),
            "mithos_globina": self.mithos_globina(),
            "hebb_povprecje": round(self.hebb_povprecje(), 3),
            "zepi": len(self.zepi),
            "energija": self.economy.energija,
            "max_energija": self.economy.max_energija,
            "st_preverb": self.st_preverb_skupaj,
            "st_pass": self.economy.st_pass,
            "st_fail": self.economy.st_fail,
            "nidhogg": self.economy.nidhogg_stanje(),
            "loki": self.economy.loki_aktiviran,
            "cilji": self.economy.povzetek_ciljev(),
        }

    def dnevna_vrata(self) -> dict:
        """Dnevna vrata — R-7 faza dneva."""
        dan = datetime.now().weekday()
        faze = [
            ("\u2205", "Praznina", "Kaj moras odpreti?"),
            ("\u00ac", "Locitev", "Kaj moras lociti?"),
            ("\u2206", "Razlika", "Kaj moras spremeniti?"),
            ("1", "Dejanje", "Kaj moras storiti?"),
            ("\u29d6", "Izgovor", "Kaj moras izgovoriti?"),
            ("\u222e", "Povratek", "Kam se moras vrniti?"),
            ("\u27e1", "Nova moznost", "Kaj se rojeva?"),
        ]
        glyph, ime, vprasanje = faze[dan]
        etaza = self.etaze[min(dan, 6)]
        return {
            "glyph": glyph, "faza_ime": ime, "vprasanje": vprasanje,
            "etaza": etaza.stevilka, "etaza_ime": etaza.ime,
            "etaza_vprasanje": etaza.vprasanje,
        }

    def to_dict(self) -> dict:
        return {
            "canon_nodes": {k: v.__dict__ for k, v in self.canon.nodes.items()},
            "canon_edges": self.canon.edges,
            "runes": [r.__dict__ for r in self.canon.runes],
            "zrtvovane_rune": [r.__dict__ for r in self.canon.zrtvovane_rune],
            "hebb_utezi": {f"{k[0]}:{k[1]}": v for k, v in self.hebb_utezi.items()},
            "zepi": self.zepi,
            "etaze": [{"stevilka": e.stevilka, "ime": e.ime, "odklenjena": e.odklenjena}
                      for e in self.etaze],
            "mithos": self.mithos,
        }
''')


# ============================================================
# 2. comprehension/ui/game_panel.py
#    Igralni panel — drevo, energija, etaze, cilji, Loki, Nidhoggr
# ============================================================

write_file(UI / "game_panel.py", r'''"""
Igralni panel — prikazuje napredovanje, grajenje, akcije
========================================================
Prikazuje:
  - Energija (vir preverbe) s trenutnim stanjem
  - Sejni cilji (receipts, ne score)
  - Etaze Yggdrasil-a (odklepajo se z napredkom)
  - Canon builder (stevilo kanon/approved/candidate)
  - Rune (aktivne rane + zaceljene = modrost)
  - Loki status (ce je aktiviran)
  - Nidhoggr timer (stanje korenin)
  - Mithos plasti (odklepajo se z razumevanjem)
  - Dnevna vrata (R-7 faza dneva)
  - Zep (redki trenutki hkratnosti)
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QProgressBar, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QSplitter, QGraphicsView,
    QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem,
    QGraphicsTextItem, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPen, QBrush, QPainter
from datetime import datetime
import math

from comprehension.core.game_engine import GameEngine, ETAZE, MITHOS_PLASTI


class EnergijaWidget(QWidget):
    """Prikaz preverba energije — vir, ki omejuje akcije."""

    def __init__(self, engine: GameEngine):
        super().__init__()
        self.engine = engine
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<b>PREVERBA ENERGIJA</b>"))
        self.bar = QProgressBar()
        self.bar.setRange(0, 10)
        self.bar.setFormat("%v / %m")
        self.bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #D6A83A; border-radius: 6px;
                background-color: #0F1A26; text-align: center;
                color: #F3E9D2; font-size: 14px; font-weight: bold;
            }
            QProgressBar::chunk { background-color: #D6A83A; border-radius: 4px; }
        """)
        lay.addWidget(self.bar)
        self.lbl_status = QLabel("")
        lay.addWidget(self.lbl_status)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._regeneriraj)
        self.timer.start(30000)

    def _regeneriraj(self):
        self.engine.economy.regeneriraj(1)
        self.osvezi()

    def osvezi(self):
        e = self.engine.economy
        self.bar.setValue(e.energija)
        self.bar.setMaximum(e.max_energija)
        if e.energija <= 2:
            self.lbl_status.setText("<span style='color:#F44336'>NIZKA — pocakaj ali pojdi plitveje</span>")
        elif e.energija <= 5:
            self.lbl_status.setText("<span style='color:#FF9800'>SREDNJA</span>")
        else:
            self.lbl_status.setText("<span style='color:#4CAF50'>DOVOLJ za globoko preverbo</span>")


class CiljiWidget(QWidget):
    """Sejni cilji — receipts, ne score."""

    def __init__(self, engine: GameEngine):
        super().__init__()
        self.engine = engine
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<b>SEJNI CILJI</b>"))
        lay.addWidget(QLabel("<i style='color:#888'>Receipts, ne score</i>"))
        self.lbl_cilji = QLabel("")
        self.lbl_cilji.setStyleSheet("font-size: 13px;")
        lay.addWidget(self.lbl_cilji)

    def osvezi(self):
        h = ""
        for c in self.engine.economy.cilji:
            barva = "#4CAF50" if c.dosezen else "#F3E9D2"
            check = "\u2713" if c.dosezen else "\u25cb"
            h += f"<span style='color:{barva}'>{check} {c.opis}: {c.trenutno}/{c.cilj}</span><br>"
        self.lbl_cilji.setText(h)


class EtazeWidget(QWidget):
    """7 etaz Yggdrasil-a — odklepajo se z napredkom."""

    def __init__(self, engine: GameEngine):
        super().__init__()
        self.engine = engine
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<b>ETAZE YGGDRASIL-A</b>"))
        self.frame_etaze = []
        for e in ETAZE:
            frame = QFrame()
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(8, 6, 8, 6)
            lbl = QLabel(f"{e.glyph} {e.stevilka}. {e.ime}")
            fl.addWidget(lbl)
            lbl2 = QLabel(f"<span style='font-size:10px; color:#888'>{e.tema}</span>")
            lbl2.setWordWrap(True)
            fl.addWidget(lbl2)
            self.frame_etaze.append(frame)
            lay.addWidget(frame)
        lay.addStretch()

    def osvezi(self):
        for i, e in enumerate(ETAZE):
            frame = self.frame_etaze[i]
            if e.odklenjena:
                frame.setStyleSheet("""
                    QFrame { background-color: #D6A83A; border-radius: 6px;
                             border: 1px solid #D4AF37; }
                """)
                for child in frame.children():
                    if isinstance(child, QLabel):
                        child.setStyleSheet("color: #1B2838; font-weight: bold;")
            else:
                frame.setStyleSheet("""
                    QFrame { background-color: #1a1a1a; border-radius: 6px;
                             border: 1px solid #333; }
                """)
                for child in frame.children():
                    if isinstance(child, QLabel):
                        child.setStyleSheet("color: #666;")
                razlika = e.zahteva_kanon - self.engine.canon.stevilo_kanon()
                if razlika > 0:
                    labels = [c for c in frame.children() if isinstance(c, QLabel)]
                    if len(labels) >= 2:
                        labels[1].setText(
                            f"<span style='font-size:10px; color:#666'>"
                            f"Zahteva {e.zahteva_kanon} kanon (imas {self.engine.canon.stevilo_kanon()})</span>")


class CanonBuilderWidget(QWidget):
    """Prikaz grajenja kanona — stevilo vnosov po statusu."""

    def __init__(self, engine: GameEngine):
        super().__init__()
        self.engine = engine
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<b>GRADNJA KANONA</b>"))
        lay.addWidget(QLabel("<i style='color:#888'>Vsaka preverba PASS = vozlisce v Yggdrasilu</i>"))

        self.lbl_kanon = QLabel("")
        self.lbl_kanon.setStyleSheet("font-size: 16px; font-weight: bold;")
        lay.addWidget(self.lbl_kanon)

        self.lbl_rune = QLabel("")
        lay.addWidget(self.lbl_rune)

        self.lbl_odin = QLabel("")
        lay.addWidget(self.lbl_odin)

        lay.addStretch()

    def osvezi(self):
        c = self.engine.canon
        self.lbl_kanon.setText(
            f"<span style='color:#D4AF37'>KANON: {c.stevilo_kanon()}</span> | "
            f"<span style='color:#D6A83A'>APPROVED: {c.stevilo_approved()}</span> | "
            f"<span style='color:#F3E9D2'>KANDIDAT: {c.stevilo_kandidat()}</span>"
        )
        aktivne = len(c.aktivne_rune())
        zaceljene = len(c.zaceljene_rune())
        self.lbl_rune.setText(
            f"<span style='color:#F44336'>RUNE (odprte rane): {aktivne}</span> | "
            f"<span style='color:#4CAF50'>ZACELJENE (modrost): {zaceljene}</span>"
        )
        self.lbl_odin.setText(
            f"<span style='color:#C77800'>ODIN zrtvovane: {len(c.zrtvovane_rune)}</span>"
        )


class LokiNidhoggWidget(QWidget):
    """Loki in Nidhoggr status — anti-optimizacija in timer globine."""

    def __init__(self, engine: GameEngine):
        super().__init__()
        self.engine = engine
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)

        self.lbl_loki = QLabel("")
        self.lbl_loki.setWordWrap(True)
        self.lbl_loki.setStyleSheet("""
            font-size: 13px; background-color: #0F1A26;
            border-radius: 6px; padding: 10px;
        """)
        lay.addWidget(self.lbl_loki)

        self.lbl_nidhogg = QLabel("")
        self.lbl_nidhogg.setWordWrap(True)
        self.lbl_nidhogg.setStyleSheet("""
            font-size: 13px; background-color: #0F1A26;
            border-radius: 6px; padding: 10px;
        """)
        lay.addWidget(self.lbl_nidhogg)

    def osvezi(self):
        e = self.engine.economy
        if e.loki_aktiviran:
            self.lbl_loki.setText(
                "<span style='color:#F44336; font-weight:bold'>"
                "LOKI AKTIVIRAN</span><br>"
                "<span style='color:#F3E9D2'>"
                "Ponavljas isto resitev. Loki spremeni pravila. "
                "Poisci drugo pot ali drugo etazo.</span>"
            )
        else:
            pon = e.st_ponovitev_resitve
            self.lbl_loki.setText(
                f"<span style='color:#888'>LOKI: miren</span> "
                f"<span style='color:#666'>(ponovitve: {pon}/3)</span>"
            )

        stanje = e.nidhogg_stanje()
        barva = "#F44336" if "KRITICNO" in stanje else "#FF9800" if "OPOZORILO" in stanje else "#4CAF50"
        self.lbl_nidhogg.setText(
            f"<span style='color:{barva}; font-weight:bold'>NIDHOGGR</span><br>"
            f"<span style='color:#F3E9D2'>{stanje}</span><br>"
            f"<span style='color:#888'>Povrsinske preverbe brez globine: {e.nidhogg_timer}</span>"
        )


class MithosWidget(QWidget):
    """Mithos plasti — odklepajo se z globino razumevanja."""

    def __init__(self, engine: GameEngine):
        super().__init__()
        self.engine = engine
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("<b>MITHOS — plasti globine</b>"))
        self.frame_plasti = []
        for p in MITHOS_PLASTI:
            frame = QFrame()
            fl = QVBoxLayout(frame)
            fl.setContentsMargins(8, 4, 8, 4)
            lbl = QLabel(f"Plast {p['id']}: {p['ime']}")
            fl.addWidget(lbl)
            lbl2 = QLabel(f"<span style='font-size:10px'>{p['opis']}</span>")
            lbl2.setWordWrap(True)
            fl.addWidget(lbl2)
            self.frame_plasti.append(frame)
            lay.addWidget(frame)
        lay.addStretch()

    def osvezi(self):
        for i, p in enumerate(self.engine.mithos):
            frame = self.frame_plasti[i]
            if p["odklenjena"]:
                frame.setStyleSheet("""
                    QFrame { background-color: #D6A83A; border-radius: 4px;
                             border: 1px solid #D4AF37; }
                """)
                for c in frame.children():
                    if isinstance(c, QLabel):
                        c.setStyleSheet("color: #1B2838;")
            else:
                frame.setStyleSheet("""
                    QFrame { background-color: #1a1a1a; border-radius: 4px;
                             border: 1px solid #333; }
                """)
                for c in frame.children():
                    if isinstance(c, QLabel):
                        c.setStyleSheet("color: #666;")


class DnevnaVrataWidget(QWidget):
    """Dnevna vrata — R-7 faza dneva."""

    def __init__(self, engine: GameEngine):
        super().__init__()
        self.engine = engine
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        vrata = self.engine.dnevna_vrata()
        glyph = vrata["glyph"]
        barve = {"\u2205": "#1B2838", "\u00ac": "#B43A2E", "\u2206": "#D6A83A",
                 "1": "#C77800", "\u29d6": "#D4AF37", "\u222e": "#080705", "\u27e1": "#F3E9D2"}
        barva = barve.get(glyph, "#F3E9D2")
        fg = "#F3E9D2" if barva in ("#1B2838", "#080705") else "#1B2838"

        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{ background-color: {barva}; border-radius: 12px;
                      border: 2px solid #D6A83A; }}
        """)
        fl = QVBoxLayout(frame)
        fl.setContentsMargins(20, 16, 20, 16)
        lbl = QLabel(f"  {glyph}  ")
        lbl.setStyleSheet(f"font-size: 40px; color: {fg}; font-weight: bold;")
        fl.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        lbl2 = QLabel(vrata["faza_ime"].upper())
        lbl2.setStyleSheet(f"font-size: 18px; color: {fg}; font-weight: bold;")
        fl.addWidget(lbl2, alignment=Qt.AlignmentFlag.AlignCenter)
        lbl3 = QLabel(f'"{vrata["vprasanje"]}"')
        lbl3.setStyleSheet(f"font-size: 14px; color: {fg}; font-style: italic;")
        lbl3.setWordWrap(True)
        lbl3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fl.addWidget(lbl3)
        lay.addWidget(frame)

        lbl_e = QLabel(
            f"Etaza {vrata['etaza']}/7 — {vrata['etaza_ime']}\n"
            f"\"{vrata['etaza_vprasanje']}\""
        )
        lbl_e.setStyleSheet("""
            color: #D6A83A; font-size: 12px;
            background-color: #0F1A26; border-radius: 8px; padding: 10px;
        """)
        lbl_e.setWordWrap(True)
        lay.addWidget(lbl_e)


class GamePanelWidget(QWidget):
    """Glavni igralni panel — vse mehanike v eni plosci."""

    def __init__(self, engine: GameEngine):
        super().__init__()
        self.engine = engine
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)

        lbl = QLabel(
            "<b style='font-size:16px; color:#D4AF37'>IGRA = NUJA, NE IZBIRA</b><br>"
            "<i style='color:#888'>Napredovanje. Grajenje. Optimizirane akcije.</i>"
        )
        lbl.setWordWrap(True)
        lay.addWidget(lbl)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        levo = QWidget()
        ll = QVBoxLayout(levo)
        self.dnevna = DnevnaVrataWidget(self.engine)
        ll.addWidget(self.dnevna)
        self.etaze = EtazeWidget(self.engine)
        ll.addWidget(self.etaze)
        self.mithos = MithosWidget(self.engine)
        ll.addWidget(self.mithos)
        ll.addStretch()

        sredina = QWidget()
        sl = QVBoxLayout(sredina)
        self.energija = EnergijaWidget(self.engine)
        sl.addWidget(self.energija)
        self.cilji = CiljiWidget(self.engine)
        sl.addWidget(self.cilji)
        self.canon = CanonBuilderWidget(self.engine)
        sl.addWidget(self.canon)
        self.loki_nidhogg = LokiNidhoggWidget(self.engine)
        sl.addWidget(self.loki_nidhogg)
        sl.addStretch()

        splitter.addWidget(levo)
        splitter.addWidget(sredina)
        splitter.setSizes([350, 450])
        lay.addWidget(splitter)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.osvezi_vse)
        self.timer.start(5000)

    def osvezi_vse(self):
        self.energija.osvezi()
        self.cilji.osvezi()
        self.etaze.osvezi()
        self.canon.osvezi()
        self.loki_nidhogg.osvezi()
        self.mithos.osvezi()

    def init_sejo(self):
        """Inicializira novo sejo — postavi cilje."""
        self.engine.economy.postavi_cilje()
        self.osvezi_vse()
''')


# ============================================================
# BOOTSTRAP RUNNER
# ============================================================

def main():
    print("=" * 60)
    print("TAZV Faza 5 — IGRALNA PLAST (napredovanje, grajenje, akcije)")
    print("=" * 60)
    print()
    print("Generira:")
    print()
    print("  1. comprehension/core/game_engine.py")
    print("     Tri sistemi igre:")
    print()
    print("  A. PROGRESSION")
    print("     - Register transitions (candidate->approved->canon) = napredek")
    print("     - Hebb utezi rastejo z rabo = modul postaja 'tvoj'")
    print("     - 7 etaz Yggdrasil-a odklepajo s stevilom kanon vnosov")
    print("       Etaza 1 (SEME) = odprta | Etaza 2 (KORENINA) = 3 kanon")
    print("       Etaza 3 (DEBLO) = 7 | Etaza 4 (VEJA) = 12 | ...")
    print("     - 7 mithos plasti odklepajo z Hebb povprecjem + preverbami")
    print()
    print("  B. CANON BUILDER")
    print("     - Igralec gradi osebni Yggdrasil iz preverjenih resnic")
    print("     - Vsaka PASS = vozlisce v drevesu")
    print("     - Vozlisca se povezujejo z robovi (odnosi)")
    print("     - Runa = brazgotina iz FAIL, ki se zaceli ob PASS")
    print("     - ODIN: zrtvuj kanon vnos za rune (globlje znanje)")
    print("       'Igralec dobi rune samo, ce nekaj pusti viseti.'")
    print()
    print("  C. ACTION ECONOMY")
    print("     - Vir preverba energija (10 na sejo, regenerira se)")
    print("     - Vsaka preverba stane energijo (globje etaze = vec)")
    print("     - Loki: 3x ista resitev = sprememba pravil")
    print("     - Nidhoggr: povrsinsko delo = korenine gnijejo")
    print("     - Sejni cilji: receipts ne score")
    print("       'Resi 3 kontradikcije' | 'Odobri 2 kandidata'")
    print("       'Povezi 5 osirotelih' | 'Pojdi v etazo 3+'")
    print()
    print("  2. comprehension/ui/game_panel.py")
    print("     Igralni panel z vsemi prikazi:")
    print("     - EnergijaWidget (prograss bar + regeneracija)")
    print("     - CiljiWidget (sejni cilji z checkmarki)")
    print("     - EtazeWidget (7 etaz, odklenjene/zaklenjene)")
    print("     - CanonBuilderWidget (kanon/approved/kandidat + rune)")
    print("     - LokiNidhoggWidget (Loki + Nidhoggr status)")
    print("     - MithosWidget (7 plasti globine)")
    print("     - DnevnaVrataWidget (R-7 faza dneva)")
    print("     - GamePanelWidget (vse v eni plosci)")
    print()
    print("AKCIJSKE IZBIRE (optimizirane akcije):")
    print("  - Kateri modul testirati? (7 modulov = 7 poti)")
    print("  - Katero etazo obdelati? (globje = drainscno a bolj vredno)")
    print("  - Resiti kontradikcijo ali karanteno? (Nidhoggr)")
    print("  - Zrtvovati kanon za rune? (Odin)")
    print("  - Ponavljati resitev ali stopiti drugam? (Loki)")
    print()
    print("ZAKAJ SE VRACAS:")
    print("  - Energija se regenerira (30s = +1)")
    print("  - Dnevna vrata = drugo vprasanje vsak dan")
    print("  - Etaze cakajo na odklep (3, 7, 12, 18, 25, 35 kanon)")
    print("  - Mithos plasti cakajo na globino")
    print("  - Rune cakajo, da se zacelijo")
    print("  - Cilji se ponastavijo vsako sejo")
    print()
    print("INTEGRACIJSKE TOCKE v main_window_v7:")
    print("  engine = GameEngine()")
    print("  engine.economy.postavi_cilje()  # ob zagonu")
    print("  panel = GamePanelWidget(engine)")
    print("  tabs.addTab(panel, 'IGRA')")
    print()
    print("  # V act_zajemi:")
    print("  rez = engine.act_zajemi(modul, trditev, etaza)")
    print()
    print("  # V act_preveri:")
    print("  rez = engine.act_preveri(node_id, 'PASS'/'FAIL', modul, test, ...)")
    print("  if 'loki' in rez: # prikazi opozorilo")
    print("  if 'nova_etaza' in rez: # etaza odklenjena!")
    print("  if 'zep' in rez: # zep odprt!")
    print()
    print("  # V act_shrani:")
    print("  rez = engine.act_shrani(node_id)")
    print()
    print("  # Odin gumb (v kanon tab):")
    print("  rez = engine.act_odin_zrtvuj(node_id)")
    print()
    print("  panel.osvezi_vse()  # po vsaki akciji")
    print("=" * 60)


if __name__ == "__main__":
    main()