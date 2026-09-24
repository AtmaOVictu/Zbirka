"""
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
from enum import Enum


class R7Phase(Enum):
    PRAZNINA = "∅"
    LOCITVE = "¬"
    RAZLIKA = "∆"
    DEJANJE = "1"
    TEST = "⧖"
    POVRATEK = "∮"
    ODPRTJE = "⟡"


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


class KadencaPreverba:
    """
    Integracija kadence z Preverba sistemom.
    """
    def __init__(self, preverba=None, soma_check=None, trainarium=None):
        self.preverba = preverba
        self.soma_check = soma_check
        self.trainarium = trainarium
    
    def register_preverba_callbacks(self, kadenca):
        """Registriraj callbacke za avtomatsko odpeljevanje preverbe."""
        pass


# Alias for Kadenca (compatibility with existing code)
Kadenca = Cadence
