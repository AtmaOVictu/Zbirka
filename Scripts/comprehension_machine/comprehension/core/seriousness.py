"""
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
