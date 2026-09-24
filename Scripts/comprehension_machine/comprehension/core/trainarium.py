"""
TRAINARIUM — Prevod Sikanja
===========================

"Sikanje ni primitivnost. Je zgodnji jezik meje.
Otrok sikne, ker še nima pojmov, a že ima zaznavo kršitve." — topic_19, Obs1

"Pedagoška napaka ni sikanje. Napaka je zadušiti sikanje brez prevoda."

"Naloga rasti: sik → beseda → stavek → dejanje"

TRAINARIUM JE prevod sikanja:
  NEUSPEH (sikanje) → DOCTRINARIUM (ker) → TRAINARIUM (kako ne ponavljati) → DEJANJE

Drill prevaja:
  - beseda: novo pravilo za modul (Hebb učenje)
  - stavek: nov SOP za sistem
  - dejanje: nova mikro-akcija za uporabnika

"Sikanje je začetek govora. Odraslost je zmožnost transformacije sile v smer."

RESILIARIUM: ko nekaj poči, sistem zmanjša funkcijo brez kolapsa,
preusmeri tok in se povrne močnejši.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
from datetime import datetime
import numpy as np
from enum import Enum


# ── Stanja drilla (iz cikla) ──

class DrillStatus(Enum):
    ACTIVE = "ACTIVE"      # Drill je aktiven, se izvajajo ukrepi
    COMPLETED = "COMPLETED"  # Drill uspešen, prevod končan
    STALLED = "STALLED"    # Drill ne deluje, potrebuje intervencijo


# ── Vrste prevoda (sik → beseda → stavek → dejanje) ──

class PrevodType(Enum):
    SIK = "sik"            # Izvorno sikanje (neuspeh)
    BESEDA = "beseda"       # Novo pravilo modula
    STAVEK = "stavek"       # Nov SOP sistema
    DEJANJE = "dejanje"     # Nova mikro-akcija uporabnika


# ── Hebb učenje + pozaba formula ──
# A_ij(t+1) = clip(A_ij(t) + η·x_j·x_i - λ·A_ij, 0, 1)

@dataclass
class HebbConfig:
    """Konfiguracija Hebb učenja."""
    eta: float = 0.1       # učna hitrost
    lambda_: float = 0.01  # pozaba
    clip_min: float = 0.0
    clip_max: float = 1.0


class HebbLearner:
    """
    Učenje po Hebbovi formuli s pozabo.
    
    Korpus: "modul se nauči ne ponavljati poti neuspeha"
    """
    
    def __init__(self, config: Optional[HebbConfig] = None):
        self.config = config or HebbConfig()
        self.weights: Dict[str, np.ndarray] = {}  # modul -> uteži
    
    def init_module(self, modul_name: str, input_size: int, output_size: int):
        """Inicializiraj uteži za modul."""
        self.weights[modul_name] = np.random.rand(input_size, output_size)
    
    def update(self, modul_name: str, x_j: np.ndarray, x_i: np.ndarray) -> np.ndarray:
        """
        Posodobi uteži po Hebbovi formuli.
        
        Args:
            modul_name: ime modula
            x_j: aktivacija vhodne nevrone
            x_i: aktivacija izhodne nevrone
            
        VRNE: posodobljene uteži
        """
        if modul_name not in self.weights:
            raise ValueError(f"Modul {modul_name} ni inicializiran")
        
        A = self.weights[modul_name]
        eta = self.config.eta
        lambda_ = self.config.lambda_
        
        # Hebb: A_ij += eta * x_j * x_i
        update = eta * np.outer(x_j, x_i)
        
        # Pozaba: - lambda * A_ij
        decay = -lambda_ * A
        
        # Posodobi
        A_new = A + update + decay
        
        # Clip
        A_new = np.clip(A_new, self.config.clip_min, self.config.clip_max)
        
        self.weights[modul_name] = A_new
        
        return A_new
    
    def get_weights(self, modul_name: str) -> Optional[np.ndarray]:
        """VRNE: uteži modula."""
        return self.weights.get(modul_name)


# ── Drill: Prevod sikanja v besedo/stavek/dejanje ──

@dataclass
class TrainariumDrill:
    """
    En drill = en prevod sikanja.
    
    Drill prevaja NEUSPEH (sikanje) v:
      1. BESEDA: novo pravilo za modul
      2. STAVEK: nov SOP za sistem
      3. DEJANJE: nova mikro-akcija za uporabnika
    
    Korpus: "Drill je en akt prevoda, ne dve ločeni operaciji"
    """
    
    # Identifikacija
    drill_id: str
    test_id: str  # referenca na originalni test
    modul: str
    trditev: str
    
    # Izvor (sikanje)
    sikanje: str  # opis neuspeha
    fail_reason: str  # razlog za FAIL (iz DOCTRINARIUM)
    fail_type: str  # kateri preizkus je padel (čas, drugi, tretji, nujno, ego, soma)
    
    # Prevod
    beseda: str  # novo pravilo modula
    stavek: str  # nov SOP sistema
    dejanje: str  # nova mikro-akcija uporabnika
    
    # Stanje
    status: DrillStatus = DrillStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    applied_count: int = 0
    success_count: int = 0
    
    # Uteži (Hebb)
    hebb_config: Optional[HebbConfig] = None
    weight_update: Optional[np.ndarray] = None
    
    # Meta
    ring: int = 1  # R-7 ring
    priority: str = "S2"  # Razred tveganja
    
    def to_dict(self) -> Dict:
        """VRNE: drill kot dictionary (za shranjevanje v DB)."""
        return {
            "drill_id": self.drill_id,
            "test_id": self.test_id,
            "modul": self.modul,
            "trditev": self.trditev,
            "sikanje": self.sikanje,
            "fail_reason": self.fail_reason,
            "fail_type": self.fail_type,
            "beseda": self.beseda,
            "stavek": self.stavek,
            "dejanje": self.dejanje,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "applied_count": self.applied_count,
            "success_count": self.success_count,
            "ring": self.ring,
            "priority": self.priority,
        }
    
    @classmethod
    def from_fail(cls, test_id: str, modul: str, trditev: str, 
                  fail_type: str, fail_reason: str, 
                  hebb_config: Optional[HebbConfig] = None,
                  ring: int = 1) -> "TrainariumDrill":
        """
        Ustvari drill iz FAIL rezultata.
        
        Korpus: NEUSPEH → DOCTRINARIUM (ker) → TRAINARIUM (kako ne ponavljati)
        """
        drill_id = f"DRILL_{test_id}_{modul}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Prevedi sikanje v besedo/stavek/dejanje
        beseda, stavek, dejanje = cls._prevedi_sikanje(fail_type, fail_reason, modul, trditev)
        
        return cls(
            drill_id=drill_id,
            test_id=test_id,
            modul=modul,
            trditev=trditev,
            sikanje=f"Test {test_id} padel: {fail_reason}",
            fail_reason=fail_reason,
            fail_type=fail_type,
            beseda=beseda,
            stavek=stavek,
            dejanje=dejanje,
            hebb_config=hebb_config,
            ring=ring,
            priority="S3" if fail_type == "ego" else "S2",
        )
    
    @staticmethod
    def _prevedi_sikanje(fail_type: str, fail_reason: str, 
                        modul: str, trditev: str) -> Tuple[str, str, str]:
        """
        Prevedi sikanje (fail) v besedo/stavek/dejanje.
        
        Korpus:
          "Drill prevaja: sik → beseda (pravilo modula) → stavek (SOP sistema) → dejanje (akcija uporabnika)"
        """
        
        # Osnovni prevodi glede na fail_type
        prevodi = {
            "ego": (
                # BESEDA: pravilo modula
                f"Modul {modul}: prepovedano izvajati pravilnost. "
                f"Vse izbire morajo ostati odprte kot vprašanja.",
                # STAVEK: SOP sistema
                f"SOP: Preden potrdiš trditev v modulu {modul}, preveri: "
                f"Ali je to 'prav' (konec vprašanja) ali 'trenutno najbolj nosilna mera'?",
                # DEJANJE: mikro-akcija uporabnika
                f"Preden pritisneš PREVERI: preveri čeljust — je stisnjena? "
                f"Če da, je preslikava vsiljena, ne prepoznana.",
            ),
            "soma": (
                f"Modul {modul}: vsaka preslikava mora prejeti somatsko potrditev.",
                f"SOP: Pred vsako preverbo odpelji SOMA_CHECK. "
                f"Če telo pravi NE, je FAIL ne glede na logiko.",
                f"Preden pritisneš PREVERI: spraši telo 'Ali čutiš, da drži?' "
                f"Če telo pravi NE, ne nadaljuj.",
            ),
            "čas": (
                f"Modul {modul}: preslikave morajo preživeti časovni test. "
                f"Če 3× padejo, grejo v MEGLA.",
                f"SOP: Vsakih 7 dni ponovno testiraj vse KANDIDAT preslikave.",
                f"Ob vsakem ponovnem testu: preveri, ali trditev še drži v novem kontekstu.",
            ),
            "drugi": (
                f"Modul {modul}: preslikava ne sme varuje drugih na račun sebe. "
                f"Preveri, ali ustvari novo odprtje (⟡) ali lažno mejo (⊘).",
                f"SOP: Pred potrditvijo preveri, ali preslikava zmanjšuje drugega. "
                f"Če ustvari lažno hierarhijo → FAIL.",
                f"Preden shraniš: vprašaj 'Ali to varuje drugega ali ga veže?'",
            ),
            "tretji": (
                f"Modul {modul}: preslikava mora imeti konkreten okvir v praksi. "
                f"Abstrakcije brez uporabe so LENI (§51).",
                f"SOP: Vsakih 7 dni preveri, ali ima preslikava realno uporabo. "
                f"Če ni uporabe → FAIL.",
                f"Ob vsaki preslikavi: vprašaj 'Kaj je okvir v praksi?'",
            ),
            "nujno": (
                f"Modul {modul}: preslikava mora služiti realni nujnosti. "
                f"Akumulacija brez odpiranja dimenzije je prepovedana (§58 prop VII).",
                f"SOP: Pred dodajanjem vsebine preveri, ali odpira novo dimenzijo. "
                f"Če le dodaja brez odpiranja → FAIL.",
                f"Preden dodaj: vprašaj 'Kaj dejansko potrebujem?'",
            ),
        }
        
        # Če fail_type ni v slovarju, uporabi generični
        if fail_type not in prevodi:
            return (
                f"Modul {modul}: ne ponavljaj poti, ki je povzročila neuspeh: {fail_reason}",
                f"SOP: Ob neuspehu modula {modul}: preveri kontekst in poskusi alternativno pot.",
                f"Ko se spomniš neuspeha: vprašaj 'Kako ne ponoviti iste napake?'",
            )
        
        return prevodi[fail_type]
    
    def apply(self, hebb_learner: Optional[HebbLearner] = None) -> bool:
        """
        Izvede drill (prevod sikanja).
        
        1. Posodobi uteži modula (Hebb)
        2. Shrani SOP v sistem
        3. Vrni mikro-akcijo uporabniku
        
        VRNE: True, če je drill uspešen
        """
        self.applied_count += 1
        
        # 1. Posodobi uteži (beseda: novo pravilo modula)
        if hebb_learner and self.hebb_config:
            # Simuliraj aktivacijo (v resnici iz modula)
            x_j = np.random.rand(10)  # primer vhod
            x_i = np.random.rand(10)  # primer izhod
            
            old_weights = hebb_learner.get_weights(self.modul)
            new_weights = hebb_learner.update(self.modul, x_j, x_i)
            self.weight_update = new_weights - old_weights
        
        # 2. Shrani SOP (stavek)
        # TODO: Integracija s sistemom SOP
        
        # 3. Vrni dejanje uporabniku
        # TODO: Integracija z UI
        
        self.success_count += 1
        return True
    
    def mark_completed(self):
        """Označi drill kot končan."""
        self.status = DrillStatus.COMPLETED
        self.completed_at = datetime.now()


# ── Glavni Trainarium razred ──

class Trainarium:
    """
    Glavni razred za upravljanje TRAINARIUM drillov.
    
    Korpus:
      "TRAINARIUM = mikro-drill — kako NE ponoviti napake."
      "Drill, ki sistem trenira, da se izogne poti neuspeha naslednjič."
      
    Integracija:
      - Prejme FAIL od Preverba
      - Ustvari Drill
      - Izvede Drill (prevod sikanja)
      - Shrani v proof_log
    """
    
    def __init__(self, db_path: Optional[str] = None, 
                 hebb_config: Optional[HebbConfig] = None):
        self.db_path = db_path
        self.drills: Dict[str, TrainariumDrill] = {}
        self.hebb_learner = HebbLearner(hebb_config)
        self.history: List[str] = []
    
    def create_drill(self, test_id: str, modul: str, trditev: str,
                     fail_type: str, fail_reason: str,
                     ring: int = 1) -> TrainariumDrill:
        """
        Ustvari nov drill iz FAIL rezultata.
        
        Korpus: DOCTRINARIUM → TRAINARIUM
        """
        drill = TrainariumDrill.from_fail(
            test_id=test_id,
            modul=modul,
            trditev=trditev,
            fail_type=fail_type,
            fail_reason=fail_reason,
            hebb_config=self.hebb_learner.config,
            ring=ring,
        )
        
        self.drills[drill.drill_id] = drill
        self.history.append(drill.drill_id)
        
        return drill
    
    def get_drill(self, drill_id: str) -> Optional[TrainariumDrill]:
        """VRNE: drill po ID."""
        return self.drills.get(drill_id)
    
    def run_drill(self, drill_id: str) -> bool:
        """
        Izvede drill.
        
        VRNE: True, če uspešen
        """
        drill = self.get_drill(drill_id)
        if not drill:
            return False
        
        success = drill.apply(self.hebb_learner)
        
        if success:
            # Preveri, ali je drill končan
            if drill.applied_count >= 3:  # Po 3x izvajanju
                drill.mark_completed()
        
        return success
    
    def get_active_drills(self, modul: Optional[str] = None) -> List[TrainariumDrill]:
        """VRNE: vse aktivne drille (filter po modulu)."""
        drills = [d for d in self.drills.values() if d.status == DrillStatus.ACTIVE]
        if modul:
            drills = [d for d in drills if d.modul == modul]
        return drills
    
    def get_trainarium_report(self, modul: Optional[str] = None) -> Dict:
        """
        VRNE: poročilo o drillih (za UI prikaz).
        
        Korpus: "Drill piše tako v uteži modula KOT v poziv uporabniku"
        """
        drills = self.get_active_drills(modul)
        
        report = {
            "active_drills": len(drills),
            "drills": [d.to_dict() for d in drills],
            "hebb_weights": {}
        }
        
        # Dodaj uteži modulov
        for modul_name in self.hebb_learner.weights:
            report["hebb_weights"][modul_name] = {
                "shape": self.hebb_learner.weights[modul_name].shape,
                "mean": float(np.mean(self.hebb_learner.weights[modul_name])),
            }
        
        return report
    
    def apply_all_active(self) -> Dict[str, bool]:
        """
        Izvede vse aktivne drille.
        
        VRNE: slovar {drill_id: success}
        """
        results = {}
        for drill_id, drill in self.drills.items():
            if drill.status == DrillStatus.ACTIVE:
                results[drill_id] = self.run_drill(drill_id)
        return results
    
    def get_dejanje_for_user(self, modul: str) -> List[str]:
        """
        VRNE: seznam mikro-akcij za uporabnika (iz aktivnih drillov).
        
        Korpus: "nova mikro-akcija: 'preden pritisneš PREVERI, preveri čeljust'"
        """
        drills = self.get_active_drills(modul)
        return [d.dejanje for d in drills]
    
    def get_sop_for_system(self, modul: str) -> List[str]:
        """
        VRNE: seznam SOP-ov za sistem (iz aktivnih drillov).
        
        Korpus: "nov SOP: 'ko preslikavaš tradicijo... preveri SOMO NAJPREJ'"
        """
        drills = self.get_active_drills(modul)
        return [d.stavek for d in drills]


# ── Integracija z Preverba (proof_log) ──

class TrainariumLogger:
    """
    Pomožni razred za logiranje drillov v proof_log.
    
    Korpus: "MEMORI — shramba dokaza"
    """
    
    @staticmethod
    def log_drill_to_proof(drill: TrainariumDrill, proof_log_path: str):
        """
        Zapiše drill v proof_log (sqlite).
        
        TODO: Integracija s Preverba.log_proof
        """
        import sqlite3
        import os
        
        os.makedirs(os.path.dirname(proof_log_path), exist_ok=True)
        
        with sqlite3.connect(proof_log_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO proof_log 
                (test_id, modul, statement, phase, result, soma, dokaz, doctrinarium, trainarium, kanon_status, ring)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                drill.drill_id,
                drill.modul,
                f"TRAINARIUM: {drill.trditev}",
                "∆",  # TRAINARIUM = ∆ (razlika)
                "TRAINARIUM_DRILL",
                None,  # soma
                f"beseda: {drill.beseda}",
                drill.fail_reason,
                f"stavek: {drill.stavek}|dejanje: {drill.dejanje}",
                "TRAINARIUM",
                drill.ring,
            ))
            conn.commit()
        
        return cursor.lastrowid


# ── Self-test ──

if __name__ == "__main__":
    print("=" * 60)
    print("TRAINARIUM — Prevod Sikanja")
    print("=" * 60)
    
    # Inicializiraj
    trainarium = Trainarium()
    
    # Ustvari drill iz FAIL
    drill = trainarium.create_drill(
        test_id="TEST_20260912_002",
        modul="APD",
        trditev="différance = ∂, ki nikoli ne prispe do 1",
        fail_type="ego",
        fail_reason="preslikava zapre vprašanje namesto da bi ga odprla — kršitev §52",
        ring=1
    )
    
    print(f"\n✓ Ustvarjen drill: {drill.drill_id}")
    print(f"  Modul: {drill.modul}")
    print(f"  Fail type: {drill.fail_type}")
    print(f"  Sikanje: {drill.sikanje}")
    print(f"\n  BESEDA (novo pravilo):")
    print(f"    {drill.beseda}")
    print(f"\n  STAVEK (nov SOP):")
    print(f"    {drill.stavek}")
    print(f"\n  DEJANJE (mikro-akcija):")
    print(f"    {drill.dejanje}")
    
    # Izvede drill
    success = trainarium.run_drill(drill.drill_id)
    print(f"\n✓ Drill izveden: {'SUCCESS' if success else 'FAILED'}")
    
    # Poročilo
    report = trainarium.get_trainarium_report()
    print(f"\nPoročilo: {report['active_drills']} aktivnih drillov")
    
    # Mikro-akcije za uporabnika
    actions = trainarium.get_dejanje_for_user("APD")
    print(f"\nMikro-akcije za uporabnika:")
    for action in actions:
        print(f"  • {action}")
    
    print("\n✓ Trainarium module OK")
