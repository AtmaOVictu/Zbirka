"""
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
