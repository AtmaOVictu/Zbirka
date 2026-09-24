"""
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
