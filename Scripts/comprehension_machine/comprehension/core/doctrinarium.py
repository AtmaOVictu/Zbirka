"""
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
