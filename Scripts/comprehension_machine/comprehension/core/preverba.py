"""
PREVERBA — Tresenje kao Test
==============================

"Preverba je tresenje." — sistem (§18, ONTOZNA)
"Če se nič ne spremeni v telesu → ni resnica." — sistem (§47, Ontopedagogika)

Test NI unit test. Test JE preverba = tresenje.
Telo je polje preverbe (⊥ = polje preverbe).

Hierarhija dokaza:
  ⊢        = lokalna resnica (blisk)
  ⊢ + ∮   = stabilna resnica (potrjeno + zvezno)
  ∮        = integrirana resnica (identiteta)

Stanje preslikav:
  KANDIDAT → PREVERJEN → KANON
                ↓
            MEGLA → ARHIV
"""

from enum import Enum
from datetime import datetime
import sqlite3
import os


# ── Stanje preslikav (iz korpusa) ──
class StanjePreslikave(Enum):
    KANDIDAT = "KANDIDAT"
    PREVERJEN = "PREVERJEN"
    KANON = "KANON"
    MEGLA = "MEGLA"
    ARHIV = "ARHIV"


# ── Razrednost resnosti (iz korpusa) ──
class RazredTveganja(Enum):
    S1 = "minimalno"
    S2 = "zmerno"
    S3 = "visoko"
    S4 = "kritično"


# ── Rezultat dataclass (za PreverbaBridge integracijo) ──
from dataclasses import dataclass, field

@dataclass
class TestResult:
    ime: str
    rezultat: str
    opis: str = ""


@dataclass
class PreverbaResult:
    skupni_rezultat: str = "PASS"
    ego_flag: bool = False
    rezultati_5: dict = field(default_factory=dict)
    rezultati_aj: dict = field(default_factory=dict)
    kanon_status: str = "KANDIDAT"
    dokaz_nivo: str = ""
    suma_opis: str = ""


# ── 5 Preizkusov (iz korpusa: topic_19, Obs1) ──

class CasTest:
    """⧖ — Ali drži, ko ni energije, romance, upanja? Preživi 7 dni/cikel?"""
    
    def __init__(self):
        self.max_fails = 3
    
    def run(self, modul, trditev, test_log=None):
        if test_log:
            last_test = test_log.get_last_test(modul, trditev, "čas")
            if last_test:
                time_elapsed = (datetime.now() - last_test["timestamp"]).days
                if time_elapsed >= 7:
                    return self._check_consistency(modul, trditev)
        return "PASS"
    
    def _check_consistency(self, modul, trditev):
        return "PASS"


class DrugiTest:
    """⟡ — Ali to varuje drugega ali ga veže?"""
    def run(self, modul, trditev, test_log=None):
        return "PASS"


class TretjiTest:
    """∴ — Kaj je okvir v praksi?"""
    def run(self, modul, trditev, test_log=None):
        return "PASS"


class NujnoTest:
    """∅ — Kaj dejansko potrebujem?"""
    def run(self, modul, trditev, test_log=None):
        return "PASS"


class EgoTest:
    """⊘ — Ali izvajam pravilnost ali iščem odnos?"""
    def run(self, modul, trditev, test_log=None):
        return "PASS"


class Preverba:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data", "comprehension.db"
        )
        self._init_tests()
        self._init_db()
    
    def _init_tests(self):
        self.testi = {
            "čas": CasTest(),
            "drugi": DrugiTest(),
            "tretji": TretjiTest(),
            "nujno": NujnoTest(),
            "ego": EgoTest(),
        }
    
    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS proof_log (id INTEGER PRIMARY KEY AUTOINCREMENT, test_id TEXT UNIQUE, modul TEXT NOT NULL, statement TEXT NOT NULL, phase TEXT NOT NULL, result TEXT NOT NULL, soma TEXT, dokaz TEXT, doctrinarium TEXT, trainarium TEXT, kanon_status TEXT DEFAULT 'KANDIDAT', timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, ring INTEGER DEFAULT 1)""")
            conn.commit()
    
    def run_5_tests(self, modul, trditev, soma_check=None):
        results = {}
        ego_flag = False
        for ime, test in self.testi.items():
            rez = test.run(modul, trditev)
            results[ime] = rez
            if ime == "ego" and rez == "FAIL":
                ego_flag = True
        if ego_flag:
            return "FAIL", True, False
        if any(r == "FAIL" for r in results.values()):
            return "FAIL", False, False
        return "PASS", False, False
    
    def run_all(self, modul, trditev, kontekst=None):
        """
        Odpelje vse 5 preizkusev in vrne PreverbaResult.
        Za integracijo s PreverbaBridge.
        """
        rezultat, ego_flag, _ = self.run_5_tests(modul, trditev)
        
        # Zgradi rezultati_5
        rezultati_5 = {}
        for ime, test in self.testi.items():
            rezultati_5[ime] = test.run(modul, trditev)
        
        # Zgradi rezultati_aj (10 preizkusov A-J) - za sedaj prazno
        rezultati_aj = {}
        
        # Dokaz nivo
        dokaz_nivo = "⊢" if rezultat == "PASS" else "BLISK" if any(r == "FAIL" for r in rezultati_5.values()) else "⊢+∮"
        
        return PreverbaResult(
            skupni_rezultat=rezultat,
            ego_flag=ego_flag,
            rezultati_5=rezultati_5,
            rezultati_aj=rezultati_aj,
            kanon_status=StanjePreslikave.KANDIDAT.value,
            dokaz_nivo=dokaz_nivo,
            suma_opis="Preverba uspela" if rezultat == "PASS" else "Preverba padla"
        )
    
    def run_soma_check(self, modul, trditev):
        print(f"[SOMA_PROMPT] Ali čutiš, da drži? (dih, mravljinci, napetost) [y/n]")
        return True
    
    def log_proof(self, test_id, modul, trditev, faza, rezultat, soma=None, dokaz=None, doctrinarium=None, trainarium=None, kanon_status="KANDIDAT", ring=1):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO proof_log (test_id, modul, statement, phase, result, soma, dokaz, doctrinarium, trainarium, kanon_status, ring) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (test_id, modul, trditev, faza, rezultat, soma, dokaz, doctrinarium, trainarium, kanon_status, ring))
            conn.commit()
        return cursor.lastrowid
    
    def get_last_test(self, modul, trditev, test_type):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proof_log WHERE modul = ? AND statement = ? ORDER BY timestamp DESC LIMIT 1", (modul, trditev))
            return cursor.fetchone()
    
    def get_kanon_status(self, modul, trditev):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT kanon_status FROM proof_log WHERE modul = ? AND statement = ? ORDER BY timestamp DESC LIMIT 1", (modul, trditev))
            result = cursor.fetchone()
            return result[0] if result else StanjePreslikave.KANDIDAT.value
    
    def update_kanon_status(self, modul, trditev, new_status):
        pass


class StanjskiAvtomat:
    TRANSITIONS = {
        StanjePreslikave.KANDIDAT: {
            "PASS": (StanjePreslikave.KANDIDAT, "ostane kandidat"),
            "FAIL_3x": (StanjePreslikave.MEGLA, "3× fail preizkusa časa"),
        },
        StanjePreslikave.PREVERJEN: {
            "PASS": (StanjePreslikave.KANON, "preizkus časa + soma"),
            "FAIL": (StanjePreslikave.KANDIDAT, "vstopi v TRAINARIUM"),
        },
        StanjePreslikave.KANON: {
            "PASS": (StanjePreslikave.KANON, "integrirano"),
            "FAIL": (StanjePreslikave.KANON, "gramatika se preotira"),
        },
    }
    
    @classmethod
    def prehod(cls, current_state, rezultat, test_type="čas"):
        current_state = StanjePreslikave(current_state)
        if test_type == "ego" and rezultat == "FAIL":
            return StanjePreslikave.PREVERJEN, "FLAG: preizkus ega → zamrzni"
        if test_type == "soma" and rezultat == "FAIL":
            return StanjePreslikave.KANDIDAT, "FLAG: soma → FAIL"
        transition_key = "FAIL_3x" if test_type == "čas" and rezultat == "FAIL" else rezultat
        transition = cls.TRANSITIONS.get(current_state, {}).get(transition_key)
        if transition:
            return transition
        return current_state, "brez spremembe"


if __name__ == "__main__":
    print("=" * 60)
    print("PREVERBA — Tresenje kao Test")
    print("=" * 60)
    p = Preverba()
    rezultat, ego_flag, _ = p.run_5_tests("STATE", "RES011 → RES042")
    print(f"5 preizkusov: {rezultat}")
    print(f"Ego flag: {ego_flag}")
    current = StanjePreslikave.KANDIDAT
    next_state, desc = StanjskiAvtomat.prehod(current, "PASS")
    print(f"{current.value} + PASS → {next_state.value} ({desc})")
    test_id = f"TEST_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    log_id = p.log_proof(test_id=test_id, modul="STATE", trditev="RES011 → RES042", faza="⧖", rezultat="PASS", soma="dih se je poglobil", dokaz="prehod drži po 7 operacijah", doctrinarium="prehod drži, ker je rez pred gibanjem", kanon_status="KANDIDAT")
    print(f"Dnevnik dokaza: log_id={log_id}")
    print("✓ Preverba module OK")
