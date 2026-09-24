#!/usr/bin/env python3
"""
TAZV Preverba Bootstrap — Faza 5
================================
Generira komplet Preverba sistema za R-7 pipeline:
  - preverba.py       : 5 preizkusov + 10 preizkusov A-J
  - soma.py           : SOMA_CHECK (telo kot bitje)
  - doctrinarium.py   : ∴→∆→⊢→∮ cikel
  - cadence.py        : mikro/makro kadenco
  - kanon_flow.py     : KANDIDAT→PREVERJEN→KANON, MEGLA→ARHIV
  - seriousness.py    : S1-S4 klasifikacija
  - schema_patch.sql  : proof_log + kanon_entry + doctrinarium_log
  - main_window_v5.py : 5-gumbni pipeline + SOMA + KANON

Run: python tazv_phase5_preverba_bootstrap.py
CWD:  D:\\OntoProjekt\\CanvasMinstral\\Scripts\\
"""

import os
import sys
from pathlib import Path

BASE = Path("comprehension_machine")
CORE = BASE / "comprehension" / "core"
UI   = BASE / "comprehension" / "ui"
DATA = BASE / "comprehension" / "data"

for d in (CORE, UI, DATA):
    d.mkdir(parents=True, exist_ok=True)


def write_file(path, content):
    """Write a file, creating parent directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {path}")


# ============================================================
# 1. comprehension/core/preverba.py
# ============================================================

write_file(CORE / "preverba.py", r'''"""
Preverba — 5 preizkusov + 10 preizkusov A-J
============================================
Korpus: Obs11 "Preverba" dokument.

5 PREIZKUSOV (osnovni):
  1. Cas(⧖)     — Ali trditev prezivi cas? (casovna stabilnost)
  2. Drugi(⟡)   — Ali lahko drugi pride do iste trditve? (intersubjektivnost)
  3. Tretji(∴)  — Ali obstaja tretja pot? (neodvisna potrditev)
  4. Nujno(∅)   — Ali je nujno? (ni izbirno, ni pogojeno)
  5. Ego(⊘)     — Ali ego posreduje? (ali volja moti?)

10 PREIZKUSOV A-J (razsirjeni, vsak mapiran na R-7 modul):
  A. KERNEL        -> ∅  (ali trditev ima jedro?)
  B. OPERATOR      -> ¬  (kateri operater je aktiven?)
  C. AGENT         -> ∆  (kdo/kaj je agent?)
  D. MICRO-AKCIJA  -> 1  (kakna mikro-akcija sledi?)
  E. SOMA          -> ⧖ (ali telo potrjuje brez krsitve?)
  F. CAS/POT       -> ⧖ (ali cas in pot sovpadata?)
  G. DOKAZ         -> ∮ (ali obstaja dokaz?)
  H. UI            -> ⟡ (ali je vmensik jasno povezan?)
  I. SKUPNOST/SUM  -> ⟡ (ali skupnost zazna ali sum prevladuje?)
  J. KANON/ARHIV   -> ∮ (ali je vreden kanona ali arhiva?)

3 KRITERIJI: Stvarna, Ponovljiva, Ne-zlorabljiva
HIERARHIJA DOKAZA:
  ⊢ brez ∮ = blisk (lokalna resnica)
  ⊢ + ∮    = stabilna resnica
  ∮        = integrirana resnica (zivljena)
"""

from dataclasses import dataclass, field
from enum import Enum


class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLISK = "BLISK"


class KanonStatus(Enum):
    KANDIDAT = "KANDIDAT"
    PREVERJEN = "PREVERJEN"
    KANON = "KANON"
    MEGLA = "MEGLA"
    ARHIV = "ARHIV"


# --- 5 OSNOVNIH PREIZKUSOV ---

class CasTest:
    glyph = "⧖"
    ime = "Cas"

    def run(self, modul, trditev, kontekst=None):
        kontekst = kontekst or {}
        zgodovina = kontekst.get("zgodovina", [])
        if zgodovina:
            jedro_sedaj = trditev.strip().lower().rstrip(".!?")
            jedro_prej = zgodovina[-1].strip().lower().rstrip(".!?")
            if jedro_sedaj == jedro_prej:
                return TestResult.PASS.value
            return TestResult.FAIL.value
        return TestResult.PASS.value


class DrugiTest:
    glyph = "⟡"
    ime = "Drugi"

    def run(self, modul, trditev, kontekst=None):
        kontekst = kontekst or {}
        potrditve = kontekst.get("drugi_potrditve", 0)
        samostojen = kontekst.get("samostojen", False)
        if potrditve >= 1 or samostojen:
            return TestResult.PASS.value
        return TestResult.FAIL.value


class TretjiTest:
    glyph = "∴"
    ime = "Tretji"

    def run(self, modul, trditev, kontekst=None):
        kontekst = kontekst or {}
        poti = kontekst.get("tretje_poti", [])
        if len(poti) >= 1:
            return TestResult.PASS.value
        return TestResult.BLISK.value


class NujnoTest:
    glyph = "∅"
    ime = "Nujno"

    def run(self, modul, trditev, kontekst=None):
        kontekst = kontekst or {}
        if kontekst.get("izbirno", False) or kontekst.get("pogojeno", False):
            return TestResult.FAIL.value
        return TestResult.PASS.value


class EgoTest:
    glyph = "⊘"
    ime = "Ego"

    def run(self, modul, trditev, kontekst=None):
        kontekst = kontekst or {}
        if kontekst.get("zelja", False) or kontekst.get("identifikacija", False):
            return TestResult.FAIL.value
        if len(kontekst.get("ego_markerji", [])) > 0:
            return TestResult.FAIL.value
        return TestResult.PASS.value


# --- 10 PREIZKUSOV A-J ---

class _AJ:
    def run(self, modul, trditev, kontekst=None):
        raise NotImplementedError

class KernelPreizkus(_AJ):
    oznaka, modul_glyph, ime = "A", "∅", "KERNEL"
    def run(self, m, t, k=None):
        k = k or {}
        if k.get("jedro") or (t and len(t.strip()) > 10):
            return TestResult.PASS.value
        return TestResult.FAIL.value

class OperatorPreizkus(_AJ):
    oznaka, modul_glyph, ime = "B", "¬", "OPERATOR"
    def run(self, m, t, k=None):
        k = k or {}
        op = k.get("operator", m)
        if op in ("∅", "¬", "∆", "1", "⧖", "∮", "⟡"):
            return TestResult.PASS.value
        return TestResult.FAIL.value

class AgentPreizkus(_AJ):
    oznaka, modul_glyph, ime = "C", "∆", "AGENT"
    def run(self, m, t, k=None):
        k = k or {}
        if k.get("agent", ""):
            return TestResult.PASS.value
        return TestResult.FAIL.value

class MikroAkcijaPreizkus(_AJ):
    oznaka, modul_glyph, ime = "D", "1", "MICRO-AKCIJA"
    def run(self, m, t, k=None):
        k = k or {}
        if k.get("mikro_akcija", ""):
            return TestResult.PASS.value
        return TestResult.FAIL.value

class SomaPreizkus(_AJ):
    oznaka, modul_glyph, ime = "E", "⧖", "SOMA"
    def run(self, m, t, k=None):
        k = k or {}
        s = k.get("soma_ok")
        if s is True: return TestResult.PASS.value
        if s is False: return TestResult.FAIL.value
        return TestResult.BLISK.value

class CasPotPreizkus(_AJ):
    oznaka, modul_glyph, ime = "F", "⧖", "CAS/POT"
    def run(self, m, t, k=None):
        k = k or {}
        if k.get("cas_usklajen") and k.get("pot_usklajena"):
            return TestResult.PASS.value
        if k.get("cas_usklajen") or k.get("pot_usklajena"):
            return TestResult.BLISK.value
        return TestResult.FAIL.value

class DokazPreizkus(_AJ):
    oznaka, modul_glyph, ime = "G", "∮", "DOKAZ"
    def run(self, m, t, k=None):
        k = k or {}
        if len(k.get("dokazi", [])) >= 1:
            return TestResult.PASS.value
        return TestResult.BLISK.value

class UIPreizkus(_AJ):
    oznaka, modul_glyph, ime = "H", "⟡", "UI"
    def run(self, m, t, k=None):
        k = k or {}
        if k.get("ui_povezan", True):
            return TestResult.PASS.value
        return TestResult.FAIL.value

class SkupnostSumPreizkus(_AJ):
    oznaka, modul_glyph, ime = "I", "⟡", "SKUPNOST/SUM"
    def run(self, m, t, k=None):
        k = k or {}
        s = k.get("skupnost_soglasje", 0)
        u = k.get("sum", 0)
        if s > u: return TestResult.PASS.value
        if s == u and s > 0: return TestResult.BLISK.value
        return TestResult.FAIL.value

class KanonArhivPreizkus(_AJ):
    oznaka, modul_glyph, ime = "J", "∮", "KANON/ARHIV"
    def run(self, m, t, k=None):
        k = k or {}
        if k.get("preverba_passed") and k.get("soma_passed"):
            return TestResult.PASS.value
        if k.get("preverba_passed"):
            return TestResult.BLISK.value
        return TestResult.FAIL.value


# --- PREVERBA ---

@dataclass
class PreverbaResult:
    skupni_rezultat: str = "PASS"
    ego_flag: bool = False
    rezultati_5: dict = field(default_factory=dict)
    rezultati_aj: dict = field(default_factory=dict)
    kanon_status: str = KanonStatus.KANDIDAT.value
    dokaz_nivo: str = ""
    suma_opis: str = ""


class Preverba:
    """5 + 10 preizkusov."""

    def __init__(self):
        self.pet = {
            "cas": CasTest(),
            "drugi": DrugiTest(),
            "tretji": TretjiTest(),
            "nujno": NujnoTest(),
            "ego": EgoTest(),
        }
        self.aj = {
            "A_KERNEL": KernelPreizkus(),
            "B_OPERATOR": OperatorPreizkus(),
            "C_AGENT": AgentPreizkus(),
            "D_MICRO_AKCIJA": MikroAkcijaPreizkus(),
            "E_SOMA": SomaPreizkus(),
            "F_CAS_POT": CasPotPreizkus(),
            "G_DOKAZ": DokazPreizkus(),
            "H_UI": UIPreizkus(),
            "I_SKUPNOST_SUM": SkupnostSumPreizkus(),
            "J_KANON_ARHIV": KanonArhivPreizkus(),
        }

    def run_5(self, modul, trditev, kontekst=None):
        kontekst = kontekst or {}
        results = {}
        ego_flag = False
        for name, test in self.pet.items():
            r = test.run(modul, trditev, kontekst)
            results[name] = r
            if r == TestResult.FAIL.value and name == "ego":
                ego_flag = True
        skupni = TestResult.PASS.value
        if any(r == TestResult.FAIL.value for r in results.values()):
            skupni = TestResult.FAIL.value
        elif any(r == TestResult.BLISK.value for r in results.values()):
            skupni = TestResult.BLISK.value
        return skupni, ego_flag, results

    def run_10(self, modul, trditev, kontekst=None):
        kontekst = kontekst or {}
        return {name: test.run(modul, trditev, kontekst)
                for name, test in self.aj.items()}

    def run_all(self, modul, trditev, kontekst=None):
        kontekst = kontekst or {}
        skupni_5, ego_flag, rez_5 = self.run_5(modul, trditev, kontekst)
        rez_aj = self.run_10(modul, trditev, kontekst)

        if skupni_5 == TestResult.PASS.value:
            kanon = KanonStatus.PREVERJEN.value
        elif skupni_5 == TestResult.BLISK.value:
            kanon = KanonStatus.KANDIDAT.value
        else:
            kanon = KanonStatus.MEGLA.value

        dokaz_nivo = ""
        if skupni_5 == TestResult.PASS.value:
            if kontekst.get("soma_passed") and kontekst.get("preverba_passed"):
                dokaz_nivo = "integrirana"
            elif kontekst.get("preverba_passed"):
                dokaz_nivo = "stabilna"
            else:
                dokaz_nivo = "blisk"
        elif skupni_5 == TestResult.BLISK.value:
            dokaz_nivo = "blisk"

        p5 = sum(1 for r in rez_5.values() if r == TestResult.PASS.value)
        paj = sum(1 for r in rez_aj.values() if r == TestResult.PASS.value)
        suma = f"5: {p5}/5 PASS | A-J: {paj}/10 PASS"
        if ego_flag:
            suma += " | EGO FLAG"

        return PreverbaResult(
            skupni_rezultat=skupni_5, ego_flag=ego_flag,
            rezultati_5=rez_5, rezultati_aj=rez_aj,
            kanon_status=kanon, dokaz_nivo=dokaz_nivo, suma_opis=suma,
        )

    def preveri_kriterije(self, trditev, kontekst=None):
        kontekst = kontekst or {}
        return {
            "stvarna": kontekst.get("stvarna", True),
            "ponovljiva": kontekst.get("ponovljiva", True),
            "ne_zlorabljiva": kontekst.get("ne_zlorabljiva", True),
        }
''')


# ============================================================
# 2. comprehension/core/soma.py
# ============================================================

write_file(CORE / "soma.py", r'''"""
SOMA_CHECK — telo kot bitje, ne kot preverjevalec
=================================================
"Telo ni preverjevalec trditve — telo je bitje, ki ga test ne sme krsiti."

SOMA ni test resnice. SOMA je preverba, ali test spoctuje telo.
Ce test krsi telo (dih, napetost, mravljinci) -> SOMA_FAIL.
"""

from dataclasses import dataclass
from enum import Enum


class SomaResult(Enum):
    SOMA_PASS = "SOMA_PASS"
    SOMA_FAIL = "SOMA_FAIL"
    SOMA_NEZNANO = "SOMA_NEZNANO"


@dataclass
class SomaCheck:
    dih_prost: bool = True
    mravljinci: bool = False
    napetost_cejust: bool = False
    napetost_ramena: bool = False

    def evaluate(self):
        if not self.dih_prost or self.mravljinci or self.napetost_cejust or self.napetost_ramena:
            return SomaResult.SOMA_FAIL.value
        return SomaResult.SOMA_PASS.value

    def opis(self):
        deli = []
        if not self.dih_prost: deli.append("dih zadrzan")
        if self.mravljinci: deli.append("mravljinci (napetost)")
        if self.napetost_cejust: deli.append("celjust stisnjena")
        if self.napetost_ramena: deli.append("ramena dvignjena")
        return "telo prosto, dih prost" if not deli else "krsitve: " + ", ".join(deli)


SOMA_PROMPT_TEXT = """\
Preverba soma

Telo ni preverjevalec trditve — telo je bitje, ki ga test ne sme krsiti.

Ali cutis, da drzi?
1. Ali dih ostaja prost?
2. Ali cutis mravljince (napetost, kracenje)?
3. Ali je napetost v celjusti ali ramenih?

Ce karkoli od tega je DA (krsitev), test je prevec agresiven.
"""
''')


# ============================================================
# 3. comprehension/core/doctrinarium.py
# ============================================================

write_file(CORE / "doctrinarium.py", r'''"""
DOCTRINARIUM / TRAINARIUM / ASSUR-VALID / MEMORI
================================================
Cikel: ∴ -> ∆ -> ⊢ -> ∮

DOCTRINARIUM (∴) — doktrina: kaj mora drzati
TRAINARIUM  (∆) — trening: vaja, ki testira doktrino
ASSUR-VALID (⊢) — preverba: ali je slo skozi?
MEMORI      (∮) — spomin: integracija v zivljeno izkusnjo
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class DoctrinariumEntry:
    id: str = ""
    modul: str = ""
    trditev: str = ""
    princip: str = ""
    nujnost: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TrainariumEntry:
    id: str = ""
    doctrinarium_id: str = ""
    vaja: str = ""
    ponovitve: int = 0
    zadnji_rezultat: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AssurValidEntry:
    id: str = ""
    trainarium_id: str = ""
    preverba_rezultat: str = ""
    soma_rezultat: str = ""
    ego_flag: bool = False
    dokaz_nivo: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class MemoriEntry:
    id: str = ""
    assur_valid_id: str = ""
    integracija: str = ""
    zivljeno: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class DoctrinariumCikel:
    def __init__(self):
        self.doctrinarium: list = []
        self.trainarium: list = []
        self.assur_valid: list = []
        self.memori: list = []

    def dodaj_doktrino(self, modul, trditev, princip="", nujnost=""):
        entry = DoctrinariumEntry(
            id=f"DOC-{len(self.doctrinarium)+1:04d}",
            modul=modul, trditev=trditev, princip=princip, nujnost=nujnost)
        self.doctrinarium.append(entry)
        return entry

    def dodaj_vajo(self, doctrinarium_id, vaja, ponovitve=1):
        entry = TrainariumEntry(
            id=f"TRN-{len(self.trainarium)+1:04d}",
            doctrinarium_id=doctrinarium_id, vaja=vaja, ponovitve=ponovitve)
        self.trainarium.append(entry)
        return entry

    def preveri_vajo(self, trainarium_id, preverba_rezultat, soma_rezultat="",
                     ego_flag=False, dokaz_nivo="blisk"):
        entry = AssurValidEntry(
            id=f"ASV-{len(self.assur_valid)+1:04d}",
            trainarium_id=trainarium_id,
            preverba_rezultat=preverba_rezultat, soma_rezultat=soma_rezultat,
            ego_flag=ego_flag, dokaz_nivo=dokaz_nivo)
        self.assur_valid.append(entry)
        for trn in self.trainarium:
            if trn.id == trainarium_id:
                trn.zadnji_rezultat = preverba_rezultat
                break
        return entry

    def integriraj(self, assur_valid_id, integracija, zivljeno=False):
        entry = MemoriEntry(
            id=f"MEM-{len(self.memori)+1:04d}",
            assur_valid_id=assur_valid_id, integracija=integracija,
            zivljeno=zivljeno)
        self.memori.append(entry)
        return entry

    def cikel_status(self, doctrinarium_id):
        doc = next((d for d in self.doctrinarium if d.id == doctrinarium_id), None)
        if not doc:
            return {"status": "NEZNANO"}
        vaje = [t for t in self.trainarium if t.doctrinarium_id == doctrinarium_id]
        if not vaje:
            return {"status": "DOCTRINARIUM", "napredek": "∴ dodano, ∆ caka"}
        preverbe = [a for a in self.assur_valid
                    for t in vaje if a.trainarium_id == t.id]
        if not preverbe:
            return {"status": "TRAINARIUM", "napredek": "∆ vaja, ⊢ caka"}
        integracije = [m for m in self.memori
                       for a in preverbe if m.assur_valid_id == a.id]
        if not integracije:
            z = preverbe[-1]
            return {"status": "ASSUR_VALID",
                    "napredek": f"⊢ {z.preverba_rezultat}, ∮ caka",
                    "dokaz_nivo": z.dokaz_nivo}
        z = integracije[-1]
        return {"status": "MEMORI",
                "napredek": f"∮ integrirano, zivljeno={z.zivljeno}",
                "dokaz_nivo": "integrirana" if z.zivljeno else "stabilna"}

    def to_dict(self):
        return {
            "doctrinarium": [d.__dict__ for d in self.doctrinarium],
            "trainarium": [t.__dict__ for t in self.trainarium],
            "assur_valid": [a.__dict__ for a in self.assur_valid],
            "memori": [m.__dict__ for m in self.memori],
        }
''')


# ============================================================
# 4. comprehension/core/cadence.py
# ============================================================

write_file(CORE / "cadence.py", r'''"""
Cadence — mikro in makro kadenco
=================================
Mikro: vsaka operacija se zabelezi (real-time)
Makro: P-7d cikel — 7-dnevni pregled (en dan na R-7 fazo)

Dan 1=∅, 2=¬, 3=∆, 4=1, 5=⧖, 6=∮, 7=⟡
P-7d = en cikel = 7 dni = en prehod skozi R-7 na makro nivoju.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


R7_DNEVI = {
    1: ("∅", "zajem"), 2: ("¬", "rez"), 3: ("∆", "manifest"),
    4: ("1", "akcija"), 5: ("⧖", "preverba"),
    6: ("∮", "integracija"), 7: ("⟡", "prikaz"),
}


@dataclass
class MikroCadence:
    id: str = ""
    modul: str = ""
    operacija: str = ""
    rezultat: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class MakroCadence:
    cikel_id: str = ""
    zacetek: str = field(default_factory=lambda: datetime.now().isoformat())
    konec: Optional[str] = None
    dan: int = 1
    faza_glyph: str = "∅"
    faza_ime: str = "zajem"
    preverbe_pass: int = 0
    preverbe_fail: int = 0
    integracije: int = 0


class Cadence:
    def __init__(self):
        self.mikro_log: list = []
        self.makro_cikli: list = []
        self._trenutni: Optional[MakroCadence] = None

    def log_mikro(self, modul, operacija, rezultat):
        entry = MikroCadence(
            id=f"MIK-{len(self.mikro_log)+1:04d}",
            modul=modul, operacija=operacija, rezultat=rezultat)
        self.mikro_log.append(entry)
        return entry

    def zacetek_cikla(self):
        c = MakroCadence(cikel_id=f"P7D-{len(self.makro_cikli)+1:03d}")
        self.makro_cikli.append(c)
        self._trenutni = c
        return c

    def dnevna_faza(self, dan=None):
        if dan is None and self._trenutni:
            zac = datetime.fromisoformat(self._trenutni.zacetek)
            dan = ((datetime.now() - zac).days % 7) + 1
        dan = max(1, min(7, dan or 1))
        g, i = R7_DNEVI[dan]
        return g, i, dan

    def posodobi_cikel(self, preverba_pass=0, preverba_fail=0, integracije=0):
        if not self._trenutni:
            self.zacetek_cikla()
        self._trenutni.preverbe_pass += preverba_pass
        self._trenutni.preverbe_fail += preverba_fail
        self._trenutni.integracije += integracije
        g, i, d = self.dnevna_faza()
        self._trenutni.faza_glyph = g
        self._trenutni.faza_ime = i
        self._trenutni.dan = d

    def to_dict(self):
        return {
            "mikro": [m.__dict__ for m in self.mikro_log],
            "makro": [m.__dict__ for m in self.makro_cikli],
        }
''')


# ============================================================
# 5. comprehension/core/kanon_flow.py
# ============================================================

write_file(CORE / "kanon_flow.py", r'''"""
Kanon Flow — statusni avtomat
==============================
KANDIDAT -> PREVERJEN -> KANON
    |          |
   MEGLA  -> ARHIV

KANDIDAT -> PREVERJEN : 5 preizkusov PASS
PREVERJEN -> KANON    : SOMA_PASS + ∮ integracija
KANDIDAT -> MEGLA     : FAIL ali BLISK
MEGLA -> ARHIV        : po P-7d ciklu brez pojasnitve
KANON -> ARHIV        : nadomescena z mocnejo trditvijo
"""

from dataclasses import dataclass, field
from datetime import datetime


VALIDNI_PREHODI = {
    ("KANDIDAT", "preverba_pass"): "PREVERJEN",
    ("KANDIDAT", "preverba_fail"): "MEGLA",
    ("KANDIDAT", "preverba_blisk"): "MEGLA",
    ("PREVERJEN", "soma_integracija"): "KANON",
    ("PREVERJEN", "oslabitev"): "MEGLA",
    ("MEGLA", "arhiviraj"): "ARHIV",
    ("MEGLA", "ponovno_preveri"): "KANDIDAT",
    ("KANON", "nadomesti"): "ARHIV",
    ("KANON", "oslabitev"): "MEGLA",
}


@dataclass
class KanonEntry:
    id: str = ""
    modul: str = ""
    trditev: str = ""
    status: str = "KANDIDAT"
    dokaz_nivo: str = ""
    soma_status: str = ""
    ring: int = 1
    zgodovina: list = field(default_factory=list)
    timestamp: str = ""

    def __post_init__(self):
        if not self.zgodovina:
            self.zgodovina = [(self.status, "")]


class KanonTransitionError(Exception):
    pass


class KanonFlow:
    def __init__(self):
        self.entries: list = []
        self._next = 1

    def dodaj(self, modul, trditev):
        e = KanonEntry(
            id=f"KAN-{self._next:04d}", modul=modul, trditev=trditev,
            timestamp=datetime.now().isoformat())
        self._next += 1
        self.entries.append(e)
        return e

    def prehod(self, kanon_id, akcija):
        e = next((x for x in self.entries if x.id == kanon_id), None)
        if not e:
            raise KanonTransitionError(f"Vnos {kanon_id} ne obstaja")
        kljuc = (e.status, akcija)
        if kljuc not in VALIDNI_PREHODI:
            raise KanonTransitionError(f"Neveljaven prehod: {e.status} + {akcija}")
        novi = VALIDNI_PREHODI[kljuc]
        e.zgodovina.append((novi, akcija))
        e.status = novi
        e.ring += 1
        return e

    def po_statusu(self, status):
        return [e for e in self.entries if e.status == status]

    def to_dict(self):
        return {"entries": [e.__dict__ for e in self.entries]}
''')


# ============================================================
# 6. comprehension/core/seriousness.py
# ============================================================

write_file(CORE / "seriousness.py", r'''"""
Seriousness — S1-S4 klasifikacija resnosti
==========================================
S1 = minimalna  — log, nadaljuj
S2 = zmerna     — flag + ponovi preverbo
S3 = visoka     — zamrzni modul + TRAINARIUM vadba
S4 = kritina    — EMERGENCY_STOP
"""

from dataclasses import dataclass
from enum import Enum


class SeriousnessLevel(Enum):
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"
    S4 = "S4"


@dataclass
class SeriousnessResult:
    nivo: str = "S1"
    opis: str = ""
    akcija: str = ""
    zamrzni_modul: bool = False
    emergency_stop: bool = False


class SeriousnessClassifier:
    def classify(self, rezultati_5, ego_flag=False, soma_rezultat=""):
        fails = [n for n, r in rezultati_5.items() if r == "FAIL"]
        nf = len(fails)
        soma_fail = soma_rezultat == "SOMA_FAIL"

        if nf >= 4 and soma_fail:
            return SeriousnessResult("S4", "Kritina odpoved — vsi fail + soma krsitev",
                                      "EMERGENCY_STOP", True, True)
        if ego_flag or nf >= 3:
            razlog = "ego posreduje" if ego_flag else f"{nf} testi fail"
            return SeriousnessResult("S3", f"Visoka resnost — {razlog}",
                                     "ZAMRZNI_MODUL + TRAINARIUM", True)
        if nf >= 2:
            return SeriousnessResult("S2", f"Zmerna — {nf} fail",
                                     "FLAG + PONOVI_PREVERBO")
        if nf == 1:
            return SeriousnessResult("S1", f"Minimalna — 1 fail ({fails[0]})",
                                     "LOG + NADALJUJ")
        return SeriousnessResult("S1", "Vsi PASS", "NADALJUJ")
''')


# ============================================================
# 7. comprehension/data/schema_patch_preverba.sql
# ============================================================

write_file(DATA / "schema_patch_preverba.sql", r'''-- TAZV Preverba — SQL patch (dodaj k schema.sql)

CREATE TABLE IF NOT EXISTS proof_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id TEXT UNIQUE,
    modul TEXT NOT NULL,
    statement TEXT NOT NULL,
    phase TEXT NOT NULL,
    result TEXT NOT NULL,
    ego_flag INTEGER DEFAULT 0,
    soma TEXT,
    dokaz TEXT,
    seriousness TEXT DEFAULT 'S1',
    kanon_status TEXT DEFAULT 'KANDIDAT',
    rezultati_5 TEXT,
    rezultati_aj TEXT,
    kriteriji TEXT,
    doctrinarium_id TEXT,
    trainarium_id TEXT,
    ring INTEGER DEFAULT 1,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS kanon_entry (
    id TEXT PRIMARY KEY,
    modul TEXT NOT NULL,
    statement TEXT NOT NULL,
    status TEXT DEFAULT 'KANDIDAT',
    dokaz_nivo TEXT,
    soma_status TEXT,
    ring INTEGER DEFAULT 1,
    zgodovina TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS doctrinarium_log (
    id TEXT PRIMARY KEY,
    tip TEXT NOT NULL,
    parent_id TEXT,
    modul TEXT,
    trditev TEXT,
    rezultat TEXT,
    podrobnosti TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cadence_log (
    id TEXT PRIMARY KEY,
    tip TEXT NOT NULL,
    modul TEXT,
    operacija TEXT,
    rezultat TEXT,
    faza_glyph TEXT,
    dan_v_ciklu INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_proof_modul ON proof_log(modul);
CREATE INDEX IF NOT EXISTS idx_proof_result ON proof_log(result);
CREATE INDEX IF NOT EXISTS idx_kanon_status ON kanon_entry(status);
CREATE INDEX IF NOT EXISTS idx_doctrinarium_tip ON doctrinarium_log(tip);
''')


# ============================================================
# 8. comprehension/ui/main_window_v5.py
# ============================================================

write_file(UI / "main_window_v5.py", r'''"""
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
''')


# ============================================================
# BOOTSTRAP RUNNER
# ============================================================

def main():
    print("=" * 60)
    print("TAZV Preverba Bootstrap — Faza 5")
    print("=" * 60)
    print()
    print("Dokoncano. Datoteke ustvarjene:")
    print("  comprehension/core/preverba.py")
    print("  comprehension/core/soma.py")
    print("  comprehension/core/doctrinarium.py")
    print("  comprehension/core/cadence.py")
    print("  comprehension/core/kanon_flow.py")
    print("  comprehension/core/seriousness.py")
    print("  comprehension/data/schema_patch_preverba.sql")
    print("  comprehension/ui/main_window_v5.py")
    print()
    print("Naslednji koraki:")
    print("  1. Backup main_window_v4.py -> main_window_v4_backup.py")
    print("  2. Posodobi main.py: from comprehension.ui.main_window_v5 import TazvMainWindow")
    print("  3. python main.py")
    print("  4. Preveri: 5 gumbi, 7 tabov, SOMA, KANON, DOCTRINARIUM")
    print("=" * 60)


if __name__ == "__main__":
    main()