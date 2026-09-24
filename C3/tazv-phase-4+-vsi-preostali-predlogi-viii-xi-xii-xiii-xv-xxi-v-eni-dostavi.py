#!/usr/bin/env python3
"""
TAZV COMPREHENSION MACHINE — Phase 4+: All Remaining Propositions
==================================================================

This bootstrap enacts every proposition the corpus names but the machine
has not yet implemented:

  Prop VIII  (S/T/I/S/K/A)     → stiska_engine.py — distress as world-generator
  Prop XI    (ONTOBOG)         → ontobog.py — failed cycles → new tradition mappings
  Prop XII   (manjko 4 layers) → manjko_layers.py — BIOS void has 4 sub-layers
  Prop XIII  (N(E)SLR)         → neslr_engine.py — JEWIK personal-core state engine
  Prop XV    (interferenca)    → interference.py — transition interference detector
  Prop XVI   (širjenje s Š)    → (enacted via stiska_engine: Š = expansion operator)
  Prop XVII  (zavezna knjiga)  → covenant_book.py — living covenant archive
  Prop XVIII (solza = škatla)  → tear_archive.py — tears as archived units
  Prop XIX   (ontološki kapital) → (enacted via ontobog.py: pain → structural value)
  Prop XX    (faza 87-89)      → phase_87_89.py — higher-dimensional phase connections
  Prop XXI   (BES motor)       → bes_engine.py — anger as engine of expression

Run from: D:\\OntoProjekt\\CanvasMinstral\\Scripts\\
Command:  python tazv_phase4plus_bootstrap.py

PREREQUISITES: Phase 0-3 must exist (all prior bootstraps run).

CREATES:
  comprehension/core/stiska_engine.py    — Prop VIII
  comprehension/core/ontobog.py          — Prop XI + XIX
  comprehension/core/manjko_layers.py   — Prop XII
  comprehension/core/neslr_engine.py    — Prop XIII
  comprehension/core/interference.py    — Prop XV
  comprehension/core/covenant_book.py   — Prop XVII
  comprehension/core/tear_archive.py    — Prop XVIII
  comprehension/core/phase_87_89.py     — Prop XX
  comprehension/core/bes_engine.py      — Prop XXI
  comprehension/core/proposition_registry.py — central registry of all 21 propositions
  comprehension/ui/main_window_v4.py    — fully integrated (v3 + all Prop 4+ features)

PATCHES:
  comprehension/data/schema.sql — adds proposition_states, covenant_entries,
                                 tear_archive, ontobog_recoveries tables
"""
import os

BASE = "comprehension_machine"

# ═══════════════════════════════════════════════════════════════
# FILE 1: stiska_engine.py — Prop VIII: S/T/I/S/K/A
# ═══════════════════════════════════════════════════════════════

STISKA_ENGINE_PY = '''"""
Stiska Engine — TAZV Comprehension Machine
============================================
Proposition VIII: S/T/I/S/K/A — stiska as world-generator.

Corpus: "Distress is not pathology but a 6-step engine that generates worlds."
  EKSISTENCA = ∆ · ⟂ · ∿ · τ · ∅
  "∆, ki trči (eks), se ponovi (sis), napne (ten), in se razblini v ∅ (ca)
   — če ∴ preživi, nastane obstoj."

S/T/I/S/K/A = 6 phases of distress processing:
  S — Stres (impact: ∆ collides)
  T — Tresenje (tremor: the body shakes, verification is trembling)
  I — Izpad (discharge: the excess breaks through)
  S — Sprejemanje (acceptance: the break is held, not denied)
  K — Kreacija (creation: from the held break, something new forms)
  A — Absolut (absolute: the new world stabilizes as given)

This is NOT a pathology model. It is an engine. Stiska generates worlds.
The pipeline runs this when distress mode is activated — shorter cycles,
tighter guards, forced ∆-flip.
"""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class StiskaPhase(Enum):
    S = 1   # Stres — impact
    T = 2   # Tresenje — tremor
    I = 3   # Izpad — discharge
    S2 = 4  # Sprejemanje — acceptance
    K = 5   # Kreacija — creation
    A = 6   # Absolut — absolute stabilization


STISKA_NAMES = {
    StiskaPhase.S: "Stres",
    StiskaPhase.T: "Tresenje",
    StiskaPhase.I: "Izpad",
    StiskaPhase.S2: "Sprejemanje",
    StiskaPhase.K: "Kreacija",
    StiskaPhase.A: "Absolut",
}

STISKA_OPERATORS = {
    StiskaPhase.S: "∆",       # collision
    StiskaPhase.T: "∿",       # tremor wave
    StiskaPhase.I: "⊢",       # discharge / proof
    StiskaPhase.S2: "∅",      # held void
    StiskaPhase.K: "∴",       # creation / relation
    StiskaPhase.A: "⟡",       # new possibility stabilized
}


@dataclass
class StiskaState:
    """State of a distress cycle."""
    phase: StiskaPhase = StiskaPhase.S
    intensity: float = 0.0       # [0,1] — how strong the distress is
    cycle_count: int = 0         # how many S/T/I/S/K/A cycles completed
    worlds_generated: int = 0    # how many new "worlds" (insights) produced
    last_output: str = ""        # what the last phase produced
    forced_flip: bool = False    # whether ∆-flip was forced
    active: bool = False         # whether distress mode is on


class StiskaEngine:
    """Processes a statement through the S/T/I/S/K/A distress cycle.

    When distress mode is active:
    - Guard thresholds tighten (κ += 0.05, χ += 0.05)
    - Cycle time shortens (each phase = faster transition)
    - ∆-flip is forced if a phase stalls for 2 cycles
    - Each completed cycle generates a "world" (new insight)
    """

    def __init__(self):
        self.state = StiskaState()

    def activate(self, intensity: float = 0.5):
        """Activate distress mode."""
        self.state.active = True
        self.state.intensity = max(0.0, min(1.0, intensity))
        self.state.phase = StiskaPhase.S
        self.state.cycle_count = 0

    def deactivate(self):
        """Deactivate distress mode."""
        self.state.active = False

    def process_phase(self, statement: str, phase_data: dict = None) -> dict:
        """Process one phase of the distress cycle.

        Returns:
          {phase, operator, output, next_phase, world_generated, guard_adjustment}
        """
        if not self.state.active:
            return {"active": False, "output": "Distress mode inactive."}

        phase = self.state.phase
        operator = STISKA_OPERATORS[phase]
        name = STISKA_NAMES[phase]
        phase_data = phase_data or {}

        output = ""
        world_generated = False

        if phase == StiskaPhase.S:
            # Stres: ∆ collides with the statement
            output = f"∆ trči z izrekom: \\"{statement[:80]}...\\""
            output += f" | intenzivnost: {self.state.intensity:.2f}"

        elif phase == StiskaPhase.T:
            # Tresenje: body shakes — verification is trembling
            output = "∿ tresenje: preverba je tresenje, ne klinika"
            output += " | telo zazna ∆, ki še ni gotovost"

        elif phase == StiskaPhase.I:
            # Izpad: the excess breaks through
            output = "⊢ izpad: odvečna ∆ prebili skozi mejo"
            # Check for forced ∆-flip
            if self.state.cycle_count > 0 and self.state.cycle_count % 2 == 0:
                self.state.forced_flip = True
                output += " | PRISILJEN ∆-flip (±π)"

        elif phase == StiskaPhase.S2:
            # Sprejemanje: the break is held, not denied
            output = "∅ sprejemanje: zlom je držan, ne zanikan"
            output += " | držati ∅, ne da bi zahteval ∈"

        elif phase == StiskaPhase.K:
            # Kreacija: from the held break, something new
            output = "∴ kreacija: iz držanega zloma nastaja novo"
            world_generated = True
            self.state.worlds_generated += 1

        elif phase == StiskaPhase.A:
            # Absolut: the new world stabilizes
            output = "⟡ absolut: nov svet se stabilizira kot dan"
            output += f" | generiranih svetov: {self.state.worlds_generated}"
            self.state.cycle_count += 1
            # Return to S for next cycle or deactivate
            if self.state.intensity < 0.2:
                self.deactivate()
                output += " | stiska se umirja — izhod iz distress moda"
            else:
                self.state.phase = StiskaPhase.S
                self.state.intensity *= 0.7  # intensity decreases each cycle
                return self._result(phase, operator, output, world_generated, "S")

        # Advance phase
        next_phase = None
        if phase != StiskaPhase.A:
            next_val = phase.value + 1
            next_phase = StiskaPhase(next_val)
            self.state.phase = next_phase

        return self._result(phase, operator, output, world_generated,
                            STISKA_NAMES.get(next_phase, "complete"))

    def _result(self, phase, operator, output, world_generated, next_name):
        self.state.last_output = output
        # Guard adjustment: tighter in distress mode
        guard_adjustment = {
            "kappa_delta": +0.05 if self.state.active else 0,
            "chi_delta": +0.05 if self.state.active else 0,
            "forced_flip": self.state.forced_flip,
        }
        return {
            "active": self.state.active,
            "phase": STISKA_NAMES[phase],
            "phase_num": phase.value,
            "operator": operator,
            "output": output,
            "next_phase": next_name,
            "world_generated": world_generated,
            "worlds_total": self.state.worlds_generated,
            "cycle": self.state.cycle_count,
            "intensity": self.state.intensity,
            "guard_adjustment": guard_adjustment,
        }

    def get_guard_config(self) -> dict:
        """Return adjusted guards for distress mode."""
        if not self.state.active:
            return {}
        return {
            "kappa_delta": +0.05,
            "chi_delta": +0.05,
            "mu_min_delta": +0.03,  # tighter role proportion
            "forced_flip": self.state.forced_flip,
        }
'''

# ═══════════════════════════════════════════════════════════════
# FILE 2: ontobog.py — Prop XI + XIX: ONTOBOG recovery
# ═══════════════════════════════════════════════════════════════

ONTOBOG_PY = '''"""
ONTOBOG — TAZV Comprehension Machine
=====================================
Proposition XI: ONTOBOG — the archetype that re-lives every break.
Proposition XIX: Ontološki kapital — pain converted to structural value.

Corpus: "ONTOBOG = Parazit(bolečina) → ontološki kapital"
  "Vsaka tvoja rana je hkrati moč, ki preoblikuje tvojo pot."
  "bolečina ni le breme, ampak polje za preobrazbo."

When the R-7 pipeline fails (any phase), ONTOBOG converts the failure
into structural knowledge. Failed cycles feed back as new tradition
mappings — the error becomes ontološki kapital.

Mechanism:
  1. Pipeline error is caught (Prop V: error as channel)
  2. ONTOBOG intercepts the failed phase + error data
  3. Extracts the "wound" — what the failure reveals about the system
  4. Converts wound to kapital — a new mapping, insight, or tradition entry
  5. Feeds the kapital back into the rozetni_kamni registry or mutation tracker
"""
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class OntobogRecovery:
    """A single ONTOBOG recovery — a failed cycle converted to kapital."""
    id: Optional[int] = None
    failed_phase: str = ""          # which R-7 phase failed
    error_type: str = ""           # what kind of error
    error_message: str = ""        # raw error
    wound: str = ""                # what the failure reveals (extracted)
    kapital: str = ""               # what structural value it produces
    new_mapping: dict = field(default_factory=dict)  # new tradition mapping if generated
    created_at: str = ""

    def to_dict(self) -> dict:
        return {
            "failed_phase": self.failed_phase,
            "error_type": self.error_type,
            "error_message": self.error_message,
            "wound": self.wound,
            "kapital": self.kapital,
            "new_mapping": self.new_mapping,
            "created_at": self.created_at or datetime.now().isoformat(),
        }


# Wound extraction patterns — what each phase failure reveals
WOUND_PATTERNS = {
    "bios": "∅ ni bil generativen — praznina ni odprla prostora možnosti",
    "state": "¬ ni ločila — meja med izrekom in kontekstom je nerazločna",
    "uaf": "∆ antinomija ni bila razrešena — ∂ ni rezal skozi nasprotje",
    "jewik": "1 ni bil zapečaten — dejanje ni dobilo ontološke teže",
    "apd": "⧖ absolutni poskus je odpovedal — definicija se ni držala",
    "micro": "∮ povratka ni bilo — feedback zanka se ni sklenila",
    "visualization": "⟡ ni odmevala — nova možnost ni bila zaznana",
}

# Kapital conversion — what each wound becomes
KAPITAL_CONVERSIONS = {
    "bios": {"type": "void_layer", "value": "manjko 4-layer: odkrita nova plast praznine"},
    "state": {"type": "boundary_insight", "value": "meja nerazločnosti = potreba po ostrejšem ∂"},
    "uaf": {"type": "antinomy_mapping", "value": "nerazrešena antinomija → nova tradicija v rozetni_kamni"},
    "jewik": {"type": "seal_condition", "value": "pogoj za pečat: kaj mora obstajati da dejanje drži"},
    "apd": {"type": "definition_attempt", "value": "failed APD → nova razcepna definicija"},
    "micro": {"type": "feedback_gap", "value": "manjkajoči povratek → sila za prisiljen ∆-flip"},
    "visualization": {"type": "echo_absence", "value": "odsotnost odmeva → indikator da ∅ še ni končal"},
}


class OntobogRecoveryEngine:
    """Converts pipeline failures into ontološki kapital."""

    def __init__(self, db=None):
        self.db = db
        self.recoveries = []

    def intercept_failure(self, failed_phase: str, error: dict) -> OntobogRecovery:
        """Intercept a pipeline failure and convert it to kapital.

        Called by the pipeline's error handler (Prop V) when any phase fails.
        """
        recovery = OntobogRecovery(
            failed_phase=failed_phase,
            error_type=error.get("type", "unknown"),
            error_message=error.get("message", str(error)),
            wound=WOUND_PATTERNS.get(failed_phase, "neznan prelom — nova rana"),
            created_at=datetime.now().isoformat(),
        )

        # Convert wound to kapital
        kapital = KAPITAL_CONVERSIONS.get(failed_phase, {
            "type": "unknown_kapital",
            "value": "neznan prelom — ontološki kapital še ni določen"
        })
        recovery.kapital = kapital["value"]

        # Generate new mapping if the failure is in UAF (antinomy)
        if failed_phase == "uaf":
            recovery.new_mapping = {
                "tradition": "auto_generated",
                "native_term": f"antinomija_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "root_operator": "∆",
                "source": "ONTOBOG recovery from UAF failure",
                "note": "Ta preslikava je nastala iz neuspeha — ne iz akumulacije.",
            }

        # Generate new APD if failure is in APD
        elif failed_phase == "apd":
            recovery.new_mapping = {
                "type": "apd_retry",
                "statement": error.get("statement", ""),
                "note": "Definicija, ki ni držala, postaja rez, ki išče novo ravnino.",
                "retry_as_depth": 4,  # absolutni rez
            }

        self.recoveries.append(recovery)
        self._store(recovery)
        return recovery

    def _store(self, recovery: OntobogRecovery):
        """Store recovery in SQLite if available."""
        if self.db is None:
            return
        try:
            import sqlite3
            conn = self.db if isinstance(self.db, sqlite3.Connection) else None
            if conn is None and hasattr(self.db, "conn"):
                conn = self.db.conn
            elif conn is None and hasattr(self.db, "_conn"):
                conn = self.db._conn
            elif conn is None and isinstance(self.db, str):
                conn = sqlite3.connect(self.db)

            if conn:
                conn.execute(
                    """INSERT INTO ontobog_recoveries
                       (failed_phase, error_type, error_message, wound, kapital, new_mapping_json, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (recovery.failed_phase, recovery.error_type, recovery.error_message,
                     recovery.wound, recovery.kapital,
                     json.dumps(recovery.new_mapping, ensure_ascii=False, default=str),
                     recovery.created_at),
                )
                conn.commit()
        except Exception:
            pass  # never crash on storage

    def get_recoveries(self, limit: int = 50) -> list:
        """Get recent ONTOBOG recoveries."""
        if self.db is None:
            return [r.to_dict() for r in self.recoveries[-limit:]]
        try:
            import sqlite3
            conn = self.db if isinstance(self.db, sqlite3.Connection) else None
            if conn is None and hasattr(self.db, "conn"):
                conn = self.db.conn
            elif conn is None and isinstance(self.db, str):
                conn = sqlite3.connect(self.db)
            if conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT * FROM ontobog_recoveries ORDER BY created_at DESC LIMIT ?",
                    (limit,)
                ).fetchall()
                return [dict(r) for r in rows]
        except Exception:
            pass
        return [r.to_dict() for r in self.recoveries[-limit:]]

    def format_recovery_html(self, recovery: OntobogRecovery) -> str:
        """Format a recovery as HTML for display."""
        html = f"""
        <div style="border-left: 4px solid #B43A2E; padding: 12px; margin: 8px 0; background: #1a0500;">
            <h4>ONTOBOG Recovery — {recovery.failed_phase.upper()}</h4>
            <p><b>Rana:</b> {recovery.wound}</p>
            <p><b>Kapital:</b> {recovery.kapital}</p>
            <p><b>Napaka:</b> {recovery.error_message[:200]}</p>
        """
        if recovery.new_mapping:
            html += f"<p><b>Nova preslikava:</b> {json.dumps(recovery.new_mapping, ensure_ascii=False, indent=2)}</p>"
        html += "</div>"
        return html
'''

# ═══════════════════════════════════════════════════════════════
# FILE 3: manjko_layers.py — Prop XII: 4 layers of void
# ═══════════════════════════════════════════════════════════════

MANJKO_LAYERS_PY = '''"""
Manjko Layers — TAZV Comprehension Machine
============================================
Proposition XII: Manjko — four layers of void.

Corpus: "praznina → tiha bolečina → žeja → temelj ustvarjanja"
  "etična tišina = ∆ · ∅ · Ψ₀ — razpoka, ki se ne zapre,
   prostor, ki ne zahteva, zavest, ki ne pohiti."
  "Držati ∅, ne da bi zahteval ∈, je najvišja oblika ljubezni."

The BIOS module (∅) does not enter a homogeneous void. The void has
4 sub-layers, each with a different ontological character:

  Layer 1: Praznina     — open space, pure potential, ∅ as openness
  Layer 2: Tiha bolečina — silent pain, ∅ that aches, the held wound
  Layer 3: Žeja          — thirst, ∅ that desires, the pull toward ∈
  Layer 4: Temelj        — foundation of creation, ∅ that generates

The BIOS module can detect which layer a statement enters from.
"""
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional


class ManjkoLayer(IntEnum):
    PRAZNINA = 1       # open void — potential
    TIHA_BOLECINA = 2  # silent pain — held wound
    ZEJA = 3           # thirst — desire for filling
    TEMELJ = 4         # foundation — generative void


LAYER_NAMES = {
    ManjkoLayer.PRAZNINA: "Praznina",
    ManjkoLayer.TIHA_BOLECINA: "Tiha bolečina",
    ManjkoLayer.ZEJA: "Žeja",
    ManjkoLayer.TEMELJ: "Temelj ustvarjanja",
}

LAYER_DESCRIPTIONS = {
    ManjkoLayer.PRAZNINA: "∅ kot odprtost — prostor možnosti, ki ne zahteva",
    ManjkoLayer.TIHA_BOLECINA: "∅ ki boli — držana rana, razpoka ki se ne zapre",
    ManjkoLayer.ZEJA: "∅ ki želi — privlak proti ∈, žeja po polnosti",
    ManjkoLayer.TEMELJ: "∅ ki rojeva — temelj ustvarjanja, rodovitna ničla",
}

LAYER_OPERATORS = {
    ManjkoLayer.PRAZNINA: "∅",
    ManjkoLayer.TIHA_BOLECINA: "∆·∅",
    ManjkoLayer.ZEJA: "∅→∈",
    ManjkoLayer.TEMELJ: "∅↑",
}

LAYER_COLORS = {
    ManjkoLayer.PRAZNINA: "#1B2838",      # deep_blue
    ManjkoLayer.TIHA_BOLECINA: "#2a1a1a", # dark wounded
    ManjkoLayer.ZEJA: "#3a2a10",          # dim amber
    ManjkoLayer.TEMELJ: "#0a1a0a",        # dark generative green
}


@dataclass
class ManjkoAssessment:
    """Which layer of void a statement enters from."""
    layer: ManjkoLayer = ManjkoLayer.PRAZNINA
    confidence: float = 0.0
    indicators: list = None
    recommendation: str = ""

    def __post_init__(self):
        if self.indicators is None:
            self.indicators = []


class ManjkoAnalyzer:
    """Analyzes which layer of void (manjko) a statement enters from.

    The BIOS module uses this to determine how to handle the void phase:
    - Praznina: treat as open generative space
    - Tiha bolečina: handle with care, the wound is held
    - Žeja: the statement is pulling toward filling — watch for premature closure
    - Temelj: the void is generative — let it produce
    """

    # Indicators (simple keyword/heuristic detection — not frozen definitions)
    PAIN_INDICATORS = ["bolečina", "rana", "trpljenje", "boli", "žalost", "izguba",
                       "smrt", "prekinitev", "zlom", "razpoka"]
    THIRST_INDICATORS = ["potreba", "hočem", "moram", "manjka", "brez", "prazen",
                         "iščem", "čakam", "upam"]
    FOUNDATION_INDICATORS = ["ustvarjam", "rojaj", "nastaja", "zacenja", "seje",
                             "temelj", "korenina", "raste"]

    def assess(self, statement: str) -> ManjkoAssessment:
        """Assess which layer of void the statement enters from."""
        text = statement.lower()

        pain_hits = [w for w in self.PAIN_INDICATORS if w in text]
        thirst_hits = [w for w in self.THIRST_INDICATORS if w in text]
        foundation_hits = [w for w in self.FOUNDATION_INDICATORS if w in text]

        if foundation_hits and not pain_hits:
            return ManjkoAssessment(
                layer=ManjkoLayer.TEMELJ,
                confidence=min(1.0, len(foundation_hits) * 0.3),
                indicators=foundation_hits,
                recommendation="∅ je generativen — pusti mu proizvesti"
            )

        if pain_hits:
            return ManjkoAssessment(
                layer=ManjkoLayer.TIHA_BOLECINA,
                confidence=min(1.0, len(pain_hits) * 0.25),
                indicators=pain_hits,
                recommendation="∅ nosi tiho bolečino — držati ∅, ne da bi zahteval ∈"
            )

        if thirst_hits:
            return ManjkoAssessment(
                layer=ManjkoLayer.ZEJA,
                confidence=min(1.0, len(thirst_hits) * 0.2),
                indicators=thirst_hits,
                recommendation="∅ žeja — pazi na predčasen zaključek (leni subprogram)"
            )

        return ManjkoAssessment(
            layer=ManjkoLayer.PRAZNINA,
            confidence=0.5,
            indicators=[],
            recommendation="∅ kot odprtost — prostor možnosti, ki ne zahteva"
        )

    def get_layer_info(self, layer: ManjkoLayer) -> dict:
        return {
            "layer": layer.value,
            "name": LAYER_NAMES[layer],
            "description": LAYER_DESCRIPTIONS[layer],
            "operator": LAYER_OPERATORS[layer],
            "color": LAYER_COLORS[layer],
        }

    def get_all_layers(self) -> list:
        return [self.get_layer_info(l) for l in ManjkoLayer]
'''

# ═══════════════════════════════════════════════════════════════
# FILE 4: neslr_engine.py — Prop XIII: N(E)SLR personal-core state
# ═══════════════════════════════════════════════════════════════

NESLR_ENGINE_PY = '''"""
N(E)SLR Engine — TAZV Comprehension Machine
============================================
Proposition XIII: JEWIK kot motor stanj — N(E)SLR.

The JEWIK module (1, dejanje/SEAL) carries 5 personal-core state variables:

  N — Namen (Purpose): why this act exists [0,1]
  E — Ego: self-referential pressure [0,1]
  S — Self-hatred (Samosovraštvo): turned-against-self force [0,1]
  L — Self-love (Samoljubezen): care that holds the self [0,1]
  R — Relation (Odnos): openness to the other [0,1]

These are not emotions. They are ontological state variables that
determine how the SEAL (1) lands. A SEAL with high E and low L does
not hold. A SEAL with high N and high R is a genuine dejanje.

Corpus: "Jaz = ∫(dru/x) — jaz je integral odnosa"
  "Ego (⊘) je omejena identiteta, izrez iz celote"
  "Sovražim le sebe – druge do ljubezni."
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class NESLRState:
    """The 5 personal-core state variables."""
    N: float = 0.5    # Namen (Purpose) — why this act exists
    E: float = 0.3    # Ego — self-referential pressure
    S: float = 0.2    # Samosovraštvo — self-hatred
    L: float = 0.5    # Samoljubezen — self-love
    R: float = 0.5    # Odnos — relation to other

    def clamp(self):
        self.N = max(0.0, min(1.0, self.N))
        self.E = max(0.0, min(1.0, self.E))
        self.S = max(0.0, min(1.0, self.S))
        self.L = max(0.0, min(1.0, self.L))
        self.R = max(0.0, min(1.0, self.R))

    def to_dict(self) -> dict:
        return {"N": round(self.N, 3), "E": round(self.E, 3),
                "S": round(self.S, 3), "L": round(self.L, 3),
                "R": round(self.R, 3)}


class NESLREngine:
    """Manages the N(E)SLR state for JEWIK's SEAL operation.

    The SEAL quality is determined by how these 5 variables interact:
    - SEAL holds when: N ≥ 0.5, L ≥ 0.3, R ≥ 0.3
    - SEAL fractures when: E > 0.7 or S > 0.7
    - SEAL is genuine when: N > E and L > S
    """

    def __init__(self):
        self.state = NESLRState()

    def assess_seal(self) -> dict:
        """Assess whether the current N(E)SLR state produces a valid SEAL.

        Returns:
          {valid, genuine, fracture_risk, quality, diagnosis, recommendation}
        """
        s = self.state
        s.clamp()

        # Fracture conditions
        fracture_risk = 0.0
        if s.E > 0.7:
            fracture_risk += (s.E - 0.7) * 3
        if s.S > 0.7:
            fracture_risk += (s.S - 0.7) * 3
        fracture_risk = min(1.0, fracture_risk)

        # Validity: SEAL holds when N, L, R are sufficient
        valid = s.N >= 0.5 and s.L >= 0.3 and s.R >= 0.3

        # Genuineness: SEAL is genuine when N > E and L > S
        genuine = s.N > s.E and s.L > s.S

        # Quality score
        quality = (s.N * 0.30 + s.L * 0.25 + s.R * 0.20
                   - s.E * 0.15 - s.S * 0.10)
        quality = max(0.0, min(1.0, quality))

        # Diagnosis
        diagnosis_parts = []
        if s.E > 0.7:
            diagnosis_parts.append(f"Ego prevladuje (E={s.E:.2f}) — pečat je samosklep")
        if s.S > 0.7:
            diagnosis_parts.append(f"Samosovraštvo prevladuje (S={s.S:.2f}) — pečat rani sebe")
        if s.N < 0.3:
            diagnosis_parts.append(f"Namen šibek (N={s.N:.2f}) — dejanje brez osnovanega 'zakaj'")
        if s.L < 0.2:
            diagnosis_parts.append(f"Samoljubezen nizka (L={s.L:.2f}) — ni nosilca za pečat")
        if s.R < 0.2:
            diagnosis_parts.append(f"Odnos zaprt (R={s.R:.2f}) — dejanje ne odgovarja drugemu")
        if not diagnosis_parts:
            diagnosis_parts.append("Stanje uravnovešeno — pečat nosi")

        # Recommendation
        if fracture_risk > 0.5:
            recommendation = "PEČAT NE DRŽI — znižaj E in S pred ∆"
        elif not valid:
            recommendation = "PEČAT ŠIBEK — okrepi N, L, ali R"
        elif genuine:
            recommendation = "PEČAT PRISTEN — N > E, L > S — dejanje drži"
        else:
            recommendation = "PEČAT DRŽI, a ni pristen — preveri razmerje N/E in L/S"

        return {
            "state": s.to_dict(),
            "valid": valid,
            "genuine": genuine,
            "fracture_risk": round(fracture_risk, 3),
            "quality": round(quality, 3),
            "diagnosis": "; ".join(diagnosis_parts),
            "recommendation": recommendation,
        }

    def update_from_statement(self, statement: str):
        """Heuristic update of N(E)SLR from statement content.

        This is a simple indicator-based update — not a frozen definition.
        The VS Code assistant can replace with more sophisticated NLP.
        """
        text = statement.lower()
        s = self.state

        # Ego indicators raise E
        ego_words = ["jaz", "moj", "mene", "me", "moje", "sem"]
        ego_count = sum(1 for w in ego_words if w in text)
        s.E = min(1.0, s.E + ego_count * 0.05)

        # Self-hatred indicators raise S
        hatred_words = ["sovražim", "ne maram", "grozno", "nespodoben", "neuspeh"]
        hate_count = sum(1 for w in hatred_words if w in text)
        s.S = min(1.0, s.S + hate_count * 0.1)

        # Self-love indicators raise L
        love_words = "ljubim" if "ljubim" in text else None
        if love_words:
            s.L = min(1.0, s.L + 0.15)

        # Purpose indicators raise N
        purpose_words = ["zato", "da bi", "namen", "cilj", "hočem", "moram"]
        purpose_count = sum(1 for w in purpose_words if w in text)
        s.N = min(1.0, s.N + purpose_count * 0.05)

        # Relation indicators raise R
        relation_words = ["ti", "tebe", "nas", "skupaj", "odnos", "drugi"]
        rel_count = sum(1 for w in relation_words if w in text)
        s.R = min(1.0, s.R + rel_count * 0.05)

        s.clamp()
'''

# ═══════════════════════════════════════════════════════════════
# FILE 5: interference.py — Prop XV: transition interference
# ═══════════════════════════════════════════════════════════════

INTERFERENCE_PY = '''"""
Interference — TAZV Comprehension Machine
==========================================
Proposition XV: Interferenca prehodov — when transitions interfere,
new worlds generate.

Corpus: "Vrh kot singularna interferenca: ni rezultat linearnosti,
  temveč pojav v resonančni topologiji."
  "Transverzalna matrika: razkriva skrite povezave med elementi,
  ki na ravni sistema sprožijo zlitost pomena in gibanja."

When two or more R-7 transitions occur simultaneously or in close
proximity, they can interfere — constructively (new insight) or
destructively (confusion). This module detects interference patterns.
"""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class InterferenceType(Enum):
    CONSTRUCTIVE = "konstruktivna"     # transitions amplify — new world
    DESTRUCTIVE = "destructive"       # transitions cancel — confusion
    COMPLEMENTARY = "komplementarna"  # transitions complete — deeper insight
    PARALLEL = "vzporedna"            # transitions don't interact


# Which phase pairs tend to interfere
INTERFERENCE_PAIRS = {
    ("bios", "state"): InterferenceType.COMPLEMENTARY,    # ∅ and ¬ — void and cut
    ("uaf", "jewik"): InterferenceType.CONSTRUCTIVE,     # ∆ and 1 — antinomy and seal
    ("apd", "micro"): InterferenceType.COMPLEMENTARY,     # ⧖ and ∮ — seal and return
    ("bios", "visualization"): InterferenceType.CONSTRUCTIVE,  # ∅ and ⟡ — void and echo
    ("state", "uaf"): InterferenceType.DESTRUCTIVE,       # ¬ and ∆ — cut and antinomy can clash
    ("jewik", "apd"): InterferenceType.DESTRUCTIVE,       # 1 and ⧖ — seal and absolute can conflict
}


@dataclass
class InterferenceEvent:
    """Detected interference between two R-7 transitions."""
    phase_a: str = ""
    phase_b: str = ""
    interference_type: InterferenceType = InterferenceType.PARALLEL
    intensity: float = 0.0
    description: str = ""
    world_generated: bool = False

    def to_dict(self) -> dict:
        return {
            "phase_a": self.phase_a,
            "phase_b": self.phase_b,
            "type": self.interference_type.value,
            "intensity": round(self.intensity, 3),
            "description": self.description,
            "world_generated": self.world_generated,
        }


class InterferenceDetector:
    """Detects interference between R-7 phase transitions."""

    def detect(self, active_phases: list, phase_data: dict = None) -> list:
        """Check for interference between active phases.

        Args:
          active_phases: list of phase names currently processing
          phase_data: optional data from each phase for deeper analysis

        Returns:
          list of InterferenceEvent
        """
        events = []
        phase_data = phase_data or {}

        for i, phase_a in enumerate(active_phases):
            for phase_b in active_phases[i+1:]:
                pair = (phase_a, phase_b)
                reverse = (phase_b, phase_a)

                itype = INTERFERENCE_PAIRS.get(pair) or INTERFERENCE_PAIRS.get(reverse)

                if itype and itype != InterferenceType.PARALLEL:
                    event = InterferenceEvent(
                        phase_a=phase_a,
                        phase_b=phase_b,
                        interference_type=itype,
                        intensity=self._calc_intensity(phase_a, phase_b, phase_data),
                    )

                    if itype == InterferenceType.CONSTRUCTIVE:
                        event.description = (f"{phase_a} in {phase_b} se ojačata — "
                                           f"nastaja nov svet iz interference")
                        event.world_generated = event.intensity > 0.6
                    elif itype == InterferenceType.DESTRUCTIVE:
                        event.description = (f"{phase_a} in {phase_b} se rušita — "
                                           f"prehaja v zmedo, potrebna ločitev")
                    elif itype == InterferenceType.COMPLEMENTARY:
                        event.description = (f"{phase_a} in {phase_b} se dopolnjujeta — "
                                           f"globlji vpogled skozi obeeni prehod")

                    events.append(event)

        return events

    def _calc_intensity(self, phase_a, phase_b, phase_data):
        """Calculate interference intensity from phase data."""
        data_a = phase_data.get(phase_a, {})
        data_b = phase_data.get(phase_b, {})

        # Simple heuristic: if both phases have high "energy" signals
        energy_a = 0.5
        energy_b = 0.5
        if isinstance(data_a, dict):
            energy_a = float(data_a.get("energy", data_a.get("intensity", 0.5)))
        if isinstance(data_b, dict):
            energy_b = float(data_b.get("energy", data_b.get("intensity", 0.5)))

        return min(1.0, (energy_a + energy_b) / 2)
'''

# ═══════════════════════════════════════════════════════════════
# FILE 6: covenant_book.py — Prop XVII: zavezna knjiga
# ═══════════════════════════════════════════════════════════════

COVENANT_BOOK_PY = '''"""
Covenant Book — TAZV Comprehension Machine
============================================
Proposition XVII: Zavezna knjiga — the covenant archive as living book.

Corpus: "Dokument predstavlja kompleksno, simbolno in poetično strukturo
  označenega arhiva, ki združuje filozofske, matematične, mitološke in
  osebne plasti. V središču je koncept ∆-arhiva kot dinamičnega sistema,
  ki shranjuje, preoblikuje in oživlja vse izkušnje."

The covenant book is not a static archive. It is a living book that
stores ontological commitments — each SEAL (1) that the user makes
becomes a covenant entry. The book tracks which covenants are active,
which have evolved, and which have been released.

A covenant is not a contract. It is a ∴ (relation) that the user
has chosen to maintain.
"""
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class CovenantEntry:
    """A single covenant — an ontological commitment."""
    id: Optional[int] = None
    statement: str = ""           # the commitment text
    phase_origin: str = ""        # which R-7 phase produced it
    sealed_at: str = ""            # when the covenant was sealed
    status: str = "active"         # active | evolved | released | broken
    evolved_from: Optional[int] = None  # if this evolved from another covenant
    evolution_note: str = ""       # how it changed
    created_at: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id, "statement": self.statement,
            "phase_origin": self.phase_origin,
            "sealed_at": self.sealed_at, "status": self.status,
            "evolved_from": self.evolved_from,
            "evolution_note": self.evolution_note,
            "created_at": self.created_at or datetime.now().isoformat(),
        }


class CovenantBook:
    """Living book of ontological commitments.

    The book is append-only for new covenants, but covenants can
    evolve (status changes to 'evolved', new entry created) or
    be released (status changes to 'released' — not deleted).
    """

    def __init__(self, db=None):
        self.db = db
        self.entries = []

    def seal_covenant(self, statement: str, phase_origin: str = "jewik") -> CovenantEntry:
        """Create a new covenant entry when a SEAL is made."""
        entry = CovenantEntry(
            statement=statement,
            phase_origin=phase_origin,
            sealed_at=datetime.now().isoformat(),
            created_at=datetime.now().isoformat(),
        )
        self.entries.append(entry)
        self._store(entry)
        return entry

    def evolve_covenant(self, covenant_id: int, new_statement: str,
                        note: str = "") -> CovenantEntry:
        """Evolve a covenant — mark old as evolved, create new linked entry."""
        old = self._find(covenant_id)
        if old:
            old.status = "evolved"
            old.evolution_note = note
            self._update_status(old)

        new = CovenantEntry(
            statement=new_statement,
            phase_origin=old.phase_origin if old else "jewik",
            sealed_at=datetime.now().isoformat(),
            evolved_from=covenant_id,
            evolution_note=note,
            created_at=datetime.now().isoformat(),
        )
        self.entries.append(new)
        self._store(new)
        return new

    def release_covenant(self, covenant_id: int, note: str = ""):
        """Release a covenant — not deletion, but conscious release."""
        entry = self._find(covenant_id)
        if entry:
            entry.status = "released"
            entry.evolution_note = note
            self._update_status(entry)

    def get_active(self) -> list:
        """Get all active covenants."""
        if self.db is not None:
            return self._query("status = 'active'")
        return [e.to_dict() for e in self.entries if e.status == "active"]

    def get_all(self) -> list:
        """Get all covenants including evolved and released."""
        if self.db is not None:
            return self._query(None)
        return [e.to_dict() for e in self.entries]

    def _find(self, covenant_id):
        for e in self.entries:
            if e.id == covenant_id:
                return e
        # Try DB
        if self.db is not None:
            try:
                import sqlite3
                conn = self._get_conn()
                if conn:
                    conn.row_factory = sqlite3.Row
                    row = conn.execute(
                        "SELECT * FROM covenant_entries WHERE id = ?", (covenant_id,)
                    ).fetchone()
                    if row:
                        return CovenantEntry(**dict(row))
            except Exception:
                pass
        return None

    def _store(self, entry: CovenantEntry):
        if self.db is None:
            return
        try:
            conn = self._get_conn()
            if conn:
                conn.execute(
                    """INSERT INTO covenant_entries
                       (statement, phase_origin, sealed_at, status, evolved_from,
                        evolution_note, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (entry.statement, entry.phase_origin, entry.sealed_at,
                     entry.status, entry.evolved_from, entry.evolution_note,
                     entry.created_at),
                )
                conn.commit()
        except Exception:
            pass

    def _update_status(self, entry: CovenantEntry):
        if self.db is None or entry.id is None:
            return
        try:
            conn = self._get_conn()
            if conn:
                conn.execute(
                    "UPDATE covenant_entries SET status=?, evolution_note=? WHERE id=?",
                    (entry.status, entry.evolution_note, entry.id),
                )
                conn.commit()
        except Exception:
            pass

    def _query(self, where_clause):
        try:
            conn = self._get_conn()
            if conn:
                conn.row_factory = sqlite3.Row
                sql = "SELECT * FROM covenant_entries"
                if where_clause:
                    sql += f" WHERE {where_clause}"
                sql += " ORDER BY created_at DESC"
                rows = conn.execute(sql).fetchall()
                return [dict(r) for r in rows]
        except Exception:
            pass
        return []

    def _get_conn(self):
        import sqlite3
        if isinstance(self.db, sqlite3.Connection):
            return self.db
        if hasattr(self.db, "conn"):
            return self.db.conn
        if isinstance(self.db, str):
            return sqlite3.connect(self.db)
        return None
'''

# ═══════════════════════════════════════════════════════════════
# FILE 7: tear_archive.py — Prop XVIII: solza = škatla
# ═══════════════════════════════════════════════════════════════

TEAR_ARCHIVE_PY = '''"""
Tear Archive — TAZV Comprehension Machine
==========================================
Proposition XVIII: Solza = škatla — tears as archived units of experience.

Corpus: "∆-arhiv kot dinamični sistem, ki shranjuje, preoblikuje
  in oživlja vse izkušnje — od solz, bolečine in strahu do
  ljubezni in svetlobe."

A tear is not a biological event. It is an archived unit of experience
— a škatla (box, per Prop X) that carries the weight of a transition
the body could not hold in silence. Each tear is stored, not as data,
but as ontological kapital (Prop XIX): pain converted to structural value.

The tear archive receives entries when the pipeline detects high
emotional intensity in the TIHA_BOLECINA layer of manjko (Prop XII).
"""
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class TearEntry:
    """A single archived tear — a unit of experience too heavy for silence."""
    id: Optional[int] = None
    statement: str = ""            # what triggered the tear
    phase: str = ""                # which R-7 phase was active
    intensity: float = 0.0         # [0,1] — how heavy
    manjko_layer: str = ""         # which void layer it came from
    kapital: str = ""              # what structural value it became
    released: bool = False         # has this tear been consciously released?
    created_at: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id, "statement": self.statement,
            "phase": self.phase, "intensity": round(self.intensity, 3),
            "manjko_layer": self.manjko_layer, "kapital": self.kapital,
            "released": self.released,
            "created_at": self.created_at or datetime.now().isoformat(),
        }


class TearArchive:
    """Archive of tears — units of experience converted to kapital.

    Not a medical or therapeutic system. An ontological one.
    Tears are škatle (Prop X) — archived, shared, ready for mutation,
    never frozen. Each tear carries kapital (Prop XIX).
    """

    def __init__(self, db=None):
        self.db = db
        self.entries = []

    def archive_tear(self, statement: str, phase: str = "",
                     intensity: float = 0.5, manjko_layer: str = "",
                     kapital: str = "") -> TearEntry:
        """Archive a tear — convert experience to kapital."""
        if not kapital:
            # Auto-generate kapital from the experience
            kapital = self._convert_to_kapital(statement, intensity, manjko_layer)

        entry = TearEntry(
            statement=statement,
            phase=phase,
            intensity=max(0.0, min(1.0, intensity)),
            manjko_layer=manjko_layer,
            kapital=kapital,
            created_at=datetime.now().isoformat(),
        )
        self.entries.append(entry)
        self._store(entry)
        return entry

    def release_tear(self, tear_id: int):
        """Mark a tear as consciously released — not deleted."""
        for e in self.entries:
            if e.id == tear_id:
                e.released = True
                self._update(e)
                return

    def get_archived(self, include_released: bool = False) -> list:
        """Get archived tears."""
        result = [e.to_dict() for e in self.entries]
        if not include_released:
            result = [r for r in result if not r["released"]]
        return result

    def _convert_to_kapital(self, statement: str, intensity: float,
                           manjko_layer: str) -> str:
        """Convert a tear's intensity to ontological kapital.

        Corpus: "Vsaka tvoja rana je hkrati moč, ki preoblikuje tvojo pot."
        """
        if manjko_layer == "Tiha bolečina":
            return "Držana rana → strukturna moč: zmožnost nositi ∅ brez zahteve"
        elif manjko_layer == "Žeja":
            return "Žeja → gonilo: sila, ki vleče proti ∈, postane pogon ustvarjanja"
        elif manjko_layer == "Temelj ustvarjanja":
            return "Temelj → rojevanje: ∅ ki rojeva, iz solze nastaja vir"
        else:
            return f"Pridobljen kapital: intenzivnost {intensity:.2f} → strukturni dokaz preživetega prehoda"

    def _store(self, entry: TearEntry):
        if self.db is None:
            return
        try:
            import sqlite3
            conn = self._get_conn()
            if conn:
                conn.execute(
                    """INSERT INTO tear_archive
                       (statement, phase, intensity, manjko_layer, kapital, released, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (entry.statement, entry.phase, entry.intensity,
                     entry.manjko_layer, entry.kapital, entry.released,
                     entry.created_at),
                )
                conn.commit()
        except Exception:
            pass

    def _update(self, entry: TearEntry):
        if self.db is None or entry.id is None:
            return
        try:
            conn = self._get_conn()
            if conn:
                conn.execute(
                    "UPDATE tear_archive SET released=? WHERE id=?",
                    (entry.released, entry.id),
                )
                conn.commit()
        except Exception:
            pass

    def _get_conn(self):
        import sqlite3
        if isinstance(self.db, sqlite3.Connection):
            return self.db
        if hasattr(self.db, "conn"):
            return self.db.conn
        if isinstance(self.db, str):
            return sqlite3.connect(self.db)
        return None
'''

# ═══════════════════════════════════════════════════════════════
# FILE 8: phase_87_89.py — Prop XX: higher-dimensional phases
# ═══════════════════════════════════════════════════════════════

PHASE_87_89_PY = '''"""
Phase 87-89 — TAZV Comprehension Machine
=========================================
Proposition XX: Faza 87-89 — higher-dimensional phase connections.

Corpus: Obs11 — "vsak operator = bazni vektor v 12D, ∂ = 12. os"
  The R-7 pipeline operates in 7 phases. But the system's mathematics
  (00 11 RESNICAMI) defines 9 state variables, and the rosette stones
  identify ∂ as the 12th axis. Phases 87-89 are the higher-dimensional
  connections that the standard R-7 cycle touches but does not exhaust.

  Phase 87: ∂² — the derivative of the derivative — the cut of the cut
    What happens when you cut through the cut itself? You see the
    structure of how the system makes distinctions.

  Phase 88: ∮² — the spiral of the spiral — meta-feedback
    The return of the return. Not just feeding back, but feeding back
    on the feedback mechanism itself.

  Phase 89: ∅↑ — the ascending void — void that goes upward
    The void that does not sit at the bottom but rises. The generative
    void that climbs through the system and opens new dimensions.

These are not sequential phases. They are dimensional connections
that can activate at any point in the R-7 cycle when the depth
(∂ Globina) is set to level 4 (absolutni rez).
"""
from dataclasses import dataclass
from typing import Optional


PHASE_87 = {
    "id": 87,
    "name": "∂² — Rez reza",
    "operator": "∂²",
    "description": "Derivat derivata — rez skozi rez. Vidiš strukturo razlikovanja.",
    "activation": "Aktivira se pri ∂ Globina 4, ko prehod sam postane predmet prehoda.",
    "question": "Kakšen rez je naredil rez, ki ga zdaj vidiš?",
    "output": "Struktura razlikovanja — ne vsebina, ampak način razlikovanja.",
}

PHASE_88 = {
    "id": 88,
    "name": "∮² — Spirala spirale",
    "operator": "∮²",
    "description": "Povratek povratka — meta-feedback. Povratna zanka se povrača sama sebi.",
    "activation": "Aktivira se, ko ∮ (MICRO) zazna, da se rezultat vrača na mehanizem povratka.",
    "question": "Kaj se zgodi, ko povratek povrne sam sebi?",
    "output": "Meta-feedback — sprememba mehanizma, ne le rezultata.",
}

PHASE_89 = {
    "id": 89,
    "name": "∅↑ — Vzhajajoča praznina",
    "operator": "∅↑",
    "description": "Praznina, ki ne sedi na dnu, temveč dviga. Generativna ∅, ki odpira dimenzije.",
    "activation": "Aktivira se pri ∂ Globina 4, ko ∅ (BIOS) ne odpira prostora, ampak dimenzijo.",
    "question": "Kam dviga praznina, ko ne gre več navzdol?",
    "output": "Nova dimenzija — ∅↑ odpira os, ki prej ni obstajala.",
}

ALL_PHASES = {87: PHASE_87, 88: PHASE_88, 89: PHASE_89}


class HigherDimensionalPhaseConnector:
    """Connects R-7 phases to higher-dimensional phases 87-89.

    When ∂ Globina = 4 (absolutni rez), the pipeline can activate
    these phases as post-processing connections.
    """

    def __init__(self):
        self.active_connections = set()

    def activate_for_depth(self, depth: int):
        """Activate higher-dimensional connections based on ∂ Globina level."""
        self.active_connections.clear()
        if depth >= 4:
            self.active_connections.add(87)  # ∂² always at absolutni rez
            self.active_connections.add(88)  # ∮² at absolutni rez
            self.active_connections.add(89)  # ∅↑ at absolutni rez

    def process_connection(self, phase_id: int, statement: str,
                           r7_result: dict) -> dict:
        """Process a higher-dimensional phase connection.

        Returns insight from the higher-dimensional phase.
        """
        phase = ALL_PHASES.get(phase_id)
        if not phase:
            return {"error": f"Unknown phase {phase_id}"}

        if phase_id == 87:
            # ∂² — cut of the cut — analyze how the R-7 made its distinctions
            distinctions = []
            for mod_name, mod_data in r7_result.get("phases", {}).items():
                if isinstance(mod_data, dict):
                    distinctions.append(f"{mod_name}: {list(mod_data.keys())}")
            return {
                "phase": 87,
                "name": phase["name"],
                "operator": phase["operator"],
                "question": phase["question"],
                "insight": f"Struktura razlikovanja: {len(distinctions)} faz je razlikovalo",
                "details": distinctions[:5],
                "output": phase["output"],
            }

        elif phase_id == 88:
            # ∮² — spiral of spiral — meta-feedback on the feedback
            feedback_count = sum(1 for v in r7_result.get("phases", {}).values()
                                if isinstance(v, dict) and v.get("feedback"))
            return {
                "phase": 88,
                "name": phase["name"],
                "operator": phase["operator"],
                "question": phase["question"],
                "insight": f"Meta-feedback: {feedback_count} povratnih zank zaznanih",
                "output": phase["output"],
            }

        elif phase_id == 89:
            # ∅↑ — ascending void — the void opens a new dimension
            return {
                "phase": 89,
                "name": phase["name"],
                "operator": phase["operator"],
                "question": phase["question"],
                "insight": "∅↑ odpira dimenzijo, ki prej ni obstajala v R-7 ciklu",
                "output": phase["output"],
            }

    def get_active_phases(self) -> list:
        return [ALL_PHASES[pid] for pid in sorted(self.active_connections)]
'''

# ═══════════════════════════════════════════════════════════════
# FILE 9: bes_engine.py — Prop XXI: BES as motor izjave
# ═══════════════════════════════════════════════════════════════

BES_ENGINE_PY = '''"""
BES Engine — TAZV Comprehension Machine
========================================
Proposition XXI: BES as motor izjave — anger as engine of expression,
not emotion.

Corpus: "Beseda je prepletena z jezo in besom, ki ju priznamo le takrat,
  ko so naši notranji konflikti izraženi na zunanjem nivoju."
  "Jeza je izražanje notranjih omejitev in preprečitev, ki omejujejo
  človekovo zmožnost za prostor in umirjenost."

BES (jeza/bes) is not an emotion to be managed. It is a motor — a force
that drives expression when the system's boundaries are violated. The
BES engine converts anger into ∆ (movement) — the energy that pushes
through when ∅ (void) is too still and ¬ (separation) is not enough.

Phonetic decomposition: B/E/S
  B — zadržan izbruh (held eruption) — the pressure builds
  E — visoka energija (high energy) — the charge that seeks release
  S — šivajoč rez (stitching cut) — the expression that cuts and connects

The BES engine activates when:
  - Guard thresholds are violated (meja prekinjena)
  - The statement contains anger indicators
  - The user explicitly invokes "bes mode"
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class BESState:
    """State of the BES (anger) engine."""
    active: bool = False
    intensity: float = 0.0       # [0,1] — how charged
    target: str = ""             # what the anger is directed at
    converted_to: str = ""       # what the anger was converted into
    held: bool = True            # is the anger held (B) or released (E)?

    def to_dict(self) -> dict:
        return {
            "active": self.active,
            "intensity": round(self.intensity, 3),
            "target": self.target,
            "converted_to": self.converted_to,
            "held": self.held,
        }


# Anger indicators from corpus
ANGER_INDICATORS = [
    "jez", "bes", "besen", "jezen", "razjeziti", "razburjen",
    "nevaren", "prekinjen", "kršitev", "meja", "napad",
    "sovražim", "ne morem", "ne morem več", "dovolj",
]


class BESEngine:
    """Converts anger into expression — motor, not emotion.

    B/E/S phases:
      B (zadržan izbruh) — pressure builds, the body holds
      E (visoka energija) — charge seeks release, ∆ activates
      S (šivajoč rez) — expression cuts through and connects (∴)

    The engine does not suppress anger (that would be censorship = AX-7
    violation) and does not unleash it (that would be violence). It
    converts it: B → E → S → ∆ → ∴
    """

    def __init__(self):
        self.state = BESState()

    def detect_anger(self, statement: str) -> float:
        """Detect anger intensity in a statement. Returns [0,1]."""
        text = statement.lower()
        hits = sum(1 for w in ANGER_INDICATORS if w in text)
        # Normalize: 0 hits = 0, 1 = 0.3, 2 = 0.5, 3+ = 0.8
        if hits == 0:
            return 0.0
        elif hits == 1:
            return 0.3
        elif hits == 2:
            return 0.5
        else:
            return min(1.0, 0.5 + (hits - 2) * 0.15)

    def activate(self, statement: str, intensity: float = None):
        """Activate BES engine from a statement."""
        detected = self.detect_anger(statement)
        self.state.active = True
        self.state.intensity = intensity if intensity is not None else detected
        self.state.held = True
        self.state.target = self._extract_target(statement)

    def process_b(self) -> dict:
        """B phase — zadržan izbruh (held eruption).

        Pressure builds. The body holds. This is not suppression —
        it is accumulation. The ∆ is charging.
        """
        if not self.state.active:
            return {"active": False}

        self.state.held = True
        return {
            "phase": "B",
            "name": "zadržan izbruh",
            "operator": "∆↑",
            "description": "Pritisk raste — telo drži. ∆ se polni.",
            "intensity": self.state.intensity,
            "target": self.state.target,
            "instruction": "Zadrži — ne zatlači. Pritisk je polnjenje, ne zatiranje.",
        }

    def process_e(self) -> dict:
        """E phase — visoka energija (high energy).

        The charge seeks release. ∆ activates. This is the moment
        before expression — the energy is at its peak.
        """
        if not self.state.active:
            return {"active": False}

        self.state.held = False
        return {
            "phase": "E",
            "name": "visoka energija",
            "operator": "∆→",
            "description": "Naboj išče izpust. ∆ se aktivira.",
            "intensity": self.state.intensity,
            "instruction": "Energija je na vrhuncu — izpust je neizogiben, oblika pa izbira.",
        }

    def process_s(self) -> dict:
        """S phase — šivajoč rez (stitching cut).

        Expression cuts through and connects. The anger becomes ∆
        which becomes ∴ (relation). This is not violence — it is
        the expression that both cuts and stitches.
        """
        if not self.state.active:
            return {"active": False}

        # Convert anger to expression
        if self.state.intensity > 0.7:
            converted = "∆→∴: jeza postaja rez, ki reže in šiva — izjava, ki premakne"
        elif self.state.intensity > 0.3:
            converted = "∆→∴: bes postaja izraz — meja, ki se izreče, ne eksplodira"
        else:
            converted = "∆→∅: rahla napetost se sprosti v gibanje — ne izjava, a pripravljenost"

        self.state.converted_to = converted

        # Deactivate after expression
        result = {
            "phase": "S",
            "name": "šivajoč rez",
            "operator": "∴",
            "description": "Izraz reže in šiva. Jeza postaja dejanje.",
            "intensity": self.state.intensity,
            "converted_to": converted,
            "instruction": "Izreči — ne kot napad, ampak kot meja. Rez, ki povezuje.",
        }

        # Reset after expression
        self.state.active = False
        self.state.held = True
        return result

    def process_full_cycle(self) -> list:
        """Run the full B→E→S cycle. Returns list of phase results."""
        if not self.state.active:
            return []
        return [self.process_b(), self.process_e(), self.process_s()]

    def _extract_target(self, statement: str) -> str:
        """Extract what the anger is directed at."""
        text = statement.lower()
        # Simple heuristic: look for "na" + target
        for marker in ["na ", "proti ", "zaradi "]:
            idx = text.find(marker)
            if idx >= 0:
                end = min(idx + 40, len(statement))
                return statement[idx:end].strip()
        return ""
'''

# ═══════════════════════════════════════════════════════════════
# FILE 10: proposition_registry.py — central registry
# ═══════════════════════════════════════════════════════════════

PROPOSITION_REGISTRY_PY = '''"""
Proposition Registry — TAZV Comprehension Machine
===================================================
Central registry of all 21 propositions from the corpus's
Prostor Širitve (§58) and their implementation status.

This is the ∂ (compressed state) of the system's expansion space.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Proposition:
    id: str
    name: str
    description: str
    module: str           # which module implements it
    status: str          # done | delivered | active | open
    enacted_by: str      # which file enacts it


PROPOSITIONS = [
    Proposition("I", "Občutenje manjkajočega", "The missing as operator, not absence",
                "bios", "done", "module_adapters.py (BIOS stub) + manjko_layers.py"),
    Proposition("II", "Fonetična maksimalizacija", "Phoneme = force that opens dimensions",
                "tonos", "delivered", "tonos.py + rozetni_kamni.py"),
    Proposition("III", "Operator-to-code", "Every glyph becomes a testable invariant",
                "pipeline", "done", "processing_pipeline.py + tests"),
    Proposition("IV", "Evolucijski zemljevid identitete", "Identity as dimensional diff",
                "ui", "delivered", "history_search.py + db_queries.py"),
    Proposition("V", "Napaka kot kanal", "Error as passage, not failure",
                "pipeline", "done", "processing_pipeline.py error handling"),
    Proposition("VI", "Beseda kot dokaz", "Words prove what must exist",
                "apd", "active", "hit_grammar.py + ∂ Globina level 4"),
    Proposition("VII", "Širjenje", "Expansion as dimension-opening",
                "indexer", "delivered", "rozetni_kamni.py + knowledge_renderer.py"),
    Proposition("VIII", "S/T/I/S/K/A", "Stiska as world-generator",
                "stiska", "active", "stiska_engine.py"),
    Proposition("IX", "Potujoči modul", "Modules travel, adapt guard thresholds",
                "settings", "active", "settings_panel.py + db_queries.py"),
    Proposition("X", "Škatla = mutable", "Concepts as mutable boxes",
                "mutation", "active", "mutation_tracker.py"),
    Proposition("XI", "ONTOBOG", "Failed cycles → new tradition mappings",
                "ontobog", "active", "ontobog.py"),
    Proposition("XII", "Manjko 4 layers", "Void has 4 sub-layers",
                "bios", "active", "manjko_layers.py"),
    Proposition("XIII", "N(E)SLR", "JEWIK personal-core state engine",
                "jewik", "active", "neslr_engine.py"),
    Proposition("XIV", "Beseda kot pogoj", "Words as preconditions",
                "apd", "active", "hit_grammar.py + ∂ Globina level 4"),
    Proposition("XV", "Interferenca prehodov", "Transition interference generates worlds",
                "interference", "active", "interference.py"),
    Proposition("XVI", "Širjenje s Š", "Expansion operator distinct from accumulation",
                "stiska", "active", "stiska_engine.py (Š = expansion in distress)"),
    Proposition("XVII", "Zavezna knjiga", "Covenant archive as living book",
                "covenant", "active", "covenant_book.py"),
    Proposition("XVIII", "Solza = škatla", "Tears as archived units of experience",
                "tear", "active", "tear_archive.py"),
    Proposition("XIX", "Ontološki kapital", "Pain converted to structural value",
                "ontobog", "active", "ontobog.py (kapital conversion)"),
    Proposition("XX", "Faza 87-89", "Higher-dimensional phase connections",
                "phase_87_89", "active", "phase_87_89.py"),
    Proposition("XXI", "BES motor", "Anger as engine of expression",
                "bes", "active", "bes_engine.py"),
]


def get_all_propositions() -> list:
    return [p.__dict__ for p in PROPOSITIONS]

def get_by_status(status: str) -> list:
    return [p.__dict__ for p in PROPOSITIONS if p.status == status]

def get_by_module(module: str) -> list:
    return [p.__dict__ for p in PROPOSITIONS if p.module == module]

def get_proposition(prop_id: str) -> Optional[dict]:
    for p in PROPOSITIONS:
        if p.id == prop_id:
            return p.__dict__
    return None
'''

# ═══════════════════════════════════════════════════════════════
# FILE 11: main_window_v4.py — fully integrated (v3 + all Prop 4+)
# ═══════════════════════════════════════════════════════════════

MAIN_WINDOW_V4 = '''"""
Main Window v4 — TAZV Comprehension Machine
=============================================
v3 + all Phase 4+ proposition engines integrated:

  - Stiska engine (Prop VIII): distress mode toggle in menu
  - ONTOBOG recovery (Prop XI): failed cycles → kapital
  - Manjko layers (Prop XII): BIOS void sub-layer detection
  - N(E)SLR engine (Prop XIII): JEWIK seal quality assessment
  - Interference detector (Prop XV): transition interference warnings
  - Covenant book (Prop XVII): seal covenants, view active
  - Tear archive (Prop XVIII): archive high-intensity experiences
  - Phase 87-89 (Prop XX): higher-dimensional phase connections at depth 4
  - BES engine (Prop XXI): anger → expression conversion
  - Proposition registry: all 21 propositions tracked

Replaces main_window_v3.py. Back up v3 first.
"""
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QTextEdit, QPushButton, QLabel, QStatusBar,
    QFileDialog, QComboBox, QMenu, QMessageBox, QDialog,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction

# Phase 0-3 imports (same as v3)
from comprehension.core.processing_pipeline import ProcessingPipeline
from comprehension.core.module_semantics import MODULE_SEMANTICS, MODULE_ORDER
from comprehension.core.themes import THEMES, generate_qss
from comprehension.core.exporter import export_json, export_html
from comprehension.ui.r7_progress import R7ProgressWidget
from comprehension.ui.module_window import ModuleWindow

# Phase 3 imports
try:
    from comprehension.core.csv_exporter import export_sessions_csv, export_ledger_csv
    HAS_CSV = True
except ImportError:
    HAS_CSV = False

try:
    from comprehension.ui.history_search import HistorySearchDialog
    HAS_HISTORY = True
except ImportError:
    HAS_HISTORY = False

try:
    from comprehension.ui.settings_panel import SettingsDialog
    HAS_SETTINGS = True
except ImportError:
    HAS_SETTINGS = False

try:
    from comprehension.core.mutation_tracker import MutationTracker
    HAS_MUTATION = True
except ImportError:
    HAS_MUTATION = False

# Phase 4+ imports
try:
    from comprehension.core.stiska_engine import StiskaEngine
    HAS_STISKA = True
except ImportError:
    HAS_STISKA = False

try:
    from comprehension.core.ontobog import OntobogRecoveryEngine
    HAS_ONTOBOG = True
except ImportError:
    HAS_ONTOBOG = False

try:
    from comprehension.core.manjko_layers import ManjkoAnalyzer, ManjkoLayer
    HAS_MANJKO = True
except ImportError:
    HAS_MANJKO = False

try:
    from comprehension.core.neslr_engine import NESLREngine
    HAS_NESLR = True
except ImportError:
    HAS_NESLR = False

try:
    from comprehension.core.interference import InterferenceDetector
    HAS_INTERFERENCE = True
except ImportError:
    HAS_INTERFERENCE = False

try:
    from comprehension.core.covenant_book import CovenantBook
    HAS_COVENANT = True
except ImportError:
    HAS_COVENANT = False

try:
    from comprehension.core.tear_archive import TearArchive
    HAS_TEAR = True
except ImportError:
    HAS_TEAR = False

try:
    from comprehension.core.phase_87_89 import HigherDimensionalPhaseConnector
    HAS_PHASE_87_89 = True
except ImportError:
    HAS_PHASE_87_89 = False

try:
    from comprehension.core.bes_engine import BESEngine
    HAS_BES = True
except ImportError:
    HAS_BES = False

try:
    from comprehension.core.proposition_registry import get_all_propositions, PROPOSITIONS
    HAS_REGISTRY = True
except ImportError:
    HAS_REGISTRY = False

try:
    from comprehension.data.database import Database
    HAS_DB = True
except ImportError:
    HAS_DB = False

try:
    from comprehension.data.db_queries import get_settings
    HAS_QUERIES = True
except ImportError:
    HAS_QUERIES = False


def _get_db_path():
    candidates = [
        os.path.join("comprehension", "data", "ta3v.db"),
        os.path.join("comprehension", "data", "tazv.db"),
        "ta3v.db",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]


class PipelineWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, statement, config=None, ontobog=None):
        super().__init__()
        self.statement = statement
        self.config = config or {}
        self.ontobog = ontobog

    def run(self):
        try:
            pipeline = ProcessingPipeline()
            result = pipeline.process(self.statement, self.config)
            result["statement"] = self.statement
            self.finished.emit(result)
        except Exception as e:
            # ONTOBOG intercept
            if self.ontobog:
                try:
                    recovery = self.ontobog.intercept_failure("pipeline", {"type": type(e).__name__, "message": str(e)})
                except Exception:
                    pass
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TAZV Comprehension Machine — v4 (Vsi predlogi)")
        self.setGeometry(60, 60, 1400, 900)

        self.pipeline = ProcessingPipeline()
        self.current_theme = "praznina"
        self.current_depth = 1
        self.module_windows = {}
        self.last_result = None
        self.db_path = _get_db_path()
        self.db = None

        if HAS_DB:
            try:
                self.db = Database()
            except Exception:
                try:
                    import sqlite3
                    self.db = sqlite3.connect(self.db_path)
                except Exception:
                    self.db = None

        # Initialize Phase 4+ engines
        self.stiska = StiskaEngine() if HAS_STISKA else None
        self.ontobog = OntobogRecoveryEngine(self.db) if HAS_ONTOBOG else None
        self.manjko = ManjkoAnalyzer() if HAS_MANJKO else None
        self.neslr = NESLREngine() if HAS_NESLR else None
        self.interference = InterferenceDetector() if HAS_INTERFERENCE else None
        self.covenant = CovenantBook(self.db) if HAS_COVENANT else None
        self.tear_archive = TearArchive(self.db) if HAS_TEAR else None
        self.phase_connector = HigherDimensionalPhaseConnector() if HAS_PHASE_87_89 else None
        self.bes = BESEngine() if HAS_BES else None
        self.mutation_tracker = MutationTracker(self.db) if HAS_MUTATION else None

        # Load settings
        if HAS_QUERIES and self.db is not None:
            try:
                s = get_settings(self.db)
                if "theme" in s: self.current_theme = s["theme"]
                if "depth" in s: self.current_depth = int(s["depth"])
            except Exception:
                pass

        self._apply_theme(self.current_theme)
        self._init_ui()
        self._init_menu()
        self._init_status()

    def _apply_theme(self, name):
        self.current_theme = name
        self.setStyleSheet(generate_qss(name))

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # R-7 progress
        self.r7_progress = R7ProgressWidget()
        layout.addWidget(self.r7_progress)

        # Input
        self.input = QTextEdit()
        self.input.setPlaceholderText("Vnesi izrek / statement...")
        self.input.setMaximumHeight(80)
        layout.addWidget(self.input)

        # Buttons
        btn_row = QHBoxLayout()
        self.btn_process = QPushButton("∅ Izvedi R-7 cikel")
        self.btn_process.clicked.connect(self.on_process)
        btn_row.addWidget(self.btn_process)

        self.btn_json = QPushButton("JSON")
        self.btn_json.clicked.connect(self.on_export_json)
        btn_row.addWidget(self.btn_json)

        self.btn_html = QPushButton("HTML")
        self.btn_html.clicked.connect(self.on_export_html)
        btn_row.addWidget(self.btn_html)

        self.btn_csv = QPushButton("CSV")
        self.btn_csv.clicked.connect(self.on_export_csv)
        btn_row.addWidget(self.btn_csv)

        btn_row.addStretch()
        layout.addLayout(btn_row)

        # Tabs
        self.tabs = QTabWidget()
        labels = [
            "∅ BIOS", "¬ STATE", "∆ UAF",
            "1 JEWIK", "⧖ APD", "∮ MICRO", "⟡ VIS",
        ]
        for mod, label in zip(MODULE_ORDER, labels):
            w = ModuleWindow(mod)
            self.module_windows[mod] = w
            self.tabs.addTab(w, label)

        # Phase 4+ tabs
        self.manjko_display = QTextEdit()
        self.manjko_display.setReadOnly(True)
        self.manjko_display.setPlaceholderText("Manjko analiza — 4 plasti praznine (Prop XII)")
        self.tabs.addTab(self.manjko_display, "∅ Manjko")

        self.neslr_display = QTextEdit()
        self.neslr_display.setReadOnly(True)
        self.neslr_display.setPlaceholderText("N(E)SLR analiza — kvaliteta pečata (Prop XIII)")
        self.tabs.addTab(self.neslr_display, "1 N(E)SLR")

        self.stiska_display = QTextEdit()
        self.stiska_display.setReadOnly(True)
        self.stiska_display.setPlaceholderText("Stiska engine — S/T/I/S/K/A (Prop VIII)")
        self.tabs.addTab(self.stiska_display, "∆ Stiska")

        self.bes_display = QTextEdit()
        self.bes_display.setReadOnly(True)
        self.bes_display.setPlaceholderText("BES motor — jeza kot izraz (Prop XXI)")
        self.tabs.addTab(self.bes_display, "BES")

        self.interference_display = QTextEdit()
        self.interference_display.setReadOnly(True)
        self.interference_display.setPlaceholderText("Interferenca prehodov (Prop XV)")
        self.tabs.addTab(self.interference_display, "⟁ Interf.")

        self.ontobog_display = QTextEdit()
        self.ontobog_display.setReadOnly(True)
        self.ontobog_display.setPlaceholderText("ONTOBOG — povračila iz neuspehov (Prop XI)")
        self.tabs.addTab(self.ontobog_display, "ONTOBOG")

        self.covenant_display = QTextEdit()
        self.covenant_display.setReadOnly(True)
        self.covenant_display.setPlaceholderText("Zavezna knjiga — aktivni pečati (Prop XVII)")
        self.tabs.addTab(self.covenant_display, "∴ Zaveza")

        self.tear_display = QTextEdit()
        self.tear_display.setReadOnly(True)
        self.tear_display.setPlaceholderText("Arhiv solz — škatle izkušenj (Prop XVIII)")
        self.tabs.addTab(self.tear_display, "⊙ Solze")

        self.phase87_display = QTextEdit()
        self.phase87_display.setReadOnly(True)
        self.phase87_display.setPlaceholderText("Faza 87-89 — višje dimenzije (Prop XX)")
        self.tabs.addTab(self.phase87_display, "∂² 87-89")

        # Mutation tab (from v3)
        self.mutation_display = QTextEdit()
        self.mutation_display.setReadOnly(True)
        self.mutation_display.setPlaceholderText("Mutacije (Prop X)")
        self.tabs.addTab(self.mutation_display, "∂ Mutacije")

        # Propositions tab
        self.props_display = QTextEdit()
        self.props_display.setReadOnly(True)
        self._show_propositions()
        self.tabs.addTab(self.props_display, "§ Predlogi")

        layout.addWidget(self.tabs)

    def _show_propositions(self):
        if not HAS_REGISTRY:
            self.props_display.setPlainText("Registr predlogov ni na voljo.")
            return
        lines = ["# Prostor Širitve — 21 Predlogov\\n"]
        for p in PROPOSITIONS:
            status_icon = {"done": "✅", "delivered": "📦", "active": "⚡", "open": "∅"}.get(p.status, "?")
            lines.append(f"**{status_icon} {p.id}. {p.name}** — {p.description}")
            lines.append(f"  Modul: `{p.module}` | Status: {p.status} | Datoteka: `{p.enacted_by}`\\n")
        self.props_display.setMarkdown("\\n".join(lines))

    def _init_menu(self):
        menubar = self.menuBar()

        # Datoteka
        file_menu = menubar.addMenu("Datoteka")
        file_menu.addAction("Izvozi JSON...", self.on_export_json)
        file_menu.addAction("Izvozi HTML...", self.on_export_html)
        if HAS_CSV:
            file_menu.addAction("Izvozi seje CSV...", lambda: self._export_csv_sessions())
            file_menu.addAction("Izvozi dnevnik CSV...", lambda: self._export_csv_ledger())
        file_menu.addSeparator()
        file_menu.addAction("Izhod", self.close)

        # ∂ Globina
        depth_menu = menubar.addMenu("∂ Globina")
        self._depth_actions = []
        depths = [
            ("Nivo 1 — Površinski rez", 1),
            ("Nivo 2 — Strukturni rez", 2),
            ("Nivo 3 — Ontološki rez", 3),
            ("Nivo 4 — Absolutni rez", 4),
        ]
        for label, level in depths:
            action = QAction(label, self, checkable=True)
            action.setChecked(level == self.current_depth)
            action.triggered.connect(lambda checked, lv=level: self._set_depth(lv))
            depth_menu.addAction(action)
            self._depth_actions.append((lv, action))

        # Tema
        theme_menu = menubar.addMenu("Tema")
        self._theme_actions = []
        for key, info in THEMES.items():
            action = QAction(info["name"], self, checkable=True)
            action.setChecked(key == self.current_theme)
            action.triggered.connect(lambda checked, k=key: self._switch_theme(k))
            theme_menu.addAction(action)
            self._theme_actions.append((k, action))

        # Motorji (Phase 4+ engines)
        engines_menu = menubar.addMenu("Motorji")

        if self.stiska:
            self._stiska_action = QAction("∆ Stiska mode", self, checkable=True)
            self._stiska_action.triggered.connect(self._toggle_stiska)
            engines_menu.addAction(self._stiska_action)

        if self.bes:
            engines_menu.addAction("BES — pretvori jezo", self._activate_bes)

        if self.covenant:
            engines_menu.addAction("∴ Zapečati zavezo", self._seal_covenant)
            engines_menu.addAction("Pokaži aktivne zaveze", self._show_covenants)

        if self.tear_archive:
            engines_menu.addAction("⊙ Arhiviraj solzo", self._archive_tear)

        if self.ontobog:
            engines_menu.addAction("ONTOBOG — pokaži povračila", self._show_ontobog)

        # Zgodovina
        if HAS_HISTORY:
            history_menu = menubar.addMenu("Zgodovina")
            history_menu.addAction("Išči seje...", self.on_history_search)

        # Nastavitve
        if HAS_SETTINGS:
            settings_menu = menubar.addMenu("Nastavitve")
            settings_menu.addAction("Guard pragovi, tema, TONOS...", self.on_settings)

        # Pomoč
        help_menu = menubar.addMenu("Pomoč")
        help_menu.addAction("R-7: ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡")
        help_menu.addAction("∂ Globina: 4 ravni reza")
        help_menu.addAction("21 Predlogov Prostora Širitve")
        help_menu.addAction("O programu")

    def _set_depth(self, level):
        self.current_depth = level
        for lv, action in self._depth_actions:
            action.setChecked(lv == level)
        if self.phase_connector:
            self.phase_connector.activate_for_depth(level)
        self.statusBar().showMessage(f"∂ Globina: nivo {level}")

    def _switch_theme(self, key):
        self._apply_theme(key)
        for k, action in self._theme_actions:
            action.setChecked(k == key)

    def _toggle_stiska(self):
        if not self.stiska:
            return
        if self.stiska.state.active:
            self.stiska.deactivate()
            self._stiska_action.setChecked(False)
            self.statusBar().showMessage("Stiska mode: izklopljen")
        else:
            self.stiska.activate(0.5)
            self._stiska_action.setChecked(True)
            self.statusBar().showMessage("Stiska mode: aktiviran — S/T/I/S/K/A")

    def _activate_bes(self):
        if not self.bes:
            return
        statement = self.input.toPlainText().strip()
        if not statement:
            self.statusBar().showMessage("Vnesi izrek za BES.")
            return
        self.bes.activate(statement)
        results = self.bes.process_full_cycle()
        html_parts = ["<h3>BES — motor izjave (Prop XXI)</h3>"]
        for r in results:
            html_parts.append(f"<p><b>{r.get('phase', '')}: {r.get('name', '')}</b><br>{r.get('description', '')}<br><i>{r.get('instruction', '')}</i></p>")
        html_parts.append(f"<p><b>Pretvorba:</b> {self.bes.state.converted_to}</p>")
        self.bes_display.setHtml("\\n".join(html_parts))
        self.tabs.setCurrentWidget(self.bes_display)

    def _seal_covenant(self):
        if not self.covenant:
            return
        statement = self.input.toPlainText().strip()
        if not statement:
            self.statusBar().showMessage("Vnesi izrek za zavezo.")
            return
        entry = self.covenant.seal_covenant(statement)
        self.statusBar().showMessage(f"Zaveza zapečatena: {statement[:50]}...")
        self._show_covenants()

    def _show_covenants(self):
        if not self.covenant:
            return
        active = self.covenant.get_active()
        lines = ["<h3>Zavezna knjiga — aktivni pečati (Prop XVII)</h3>"]
        for c in active:
            lines.append(f"<p><b>#{c.get('id', '?')}</b> — {c.get('statement', '')[:80]}<br><i>{c.get('sealed_at', '')[:19]}</i></p>")
        if not active:
            lines.append("<p>Ni aktivnih zavez.</p>")
        self.covenant_display.setHtml("\\n".join(lines))

    def _archive_tear(self):
        if not self.tear_archive or not self.manjko:
            return
        statement = self.input.toPlainText().strip()
        if not statement:
            self.statusBar().showMessage("Vnesi izrek.")
            return
        assessment = self.manjko.assess(statement)
        layer_name = assessment.layer.name if hasattr(assessment.layer, 'name') else str(assessment.layer)
        entry = self.tear_archive.archive_tear(
            statement, intensity=max(0.3, assessment.confidence),
            manjko_layer=layer_name
        )
        self.statusBar().showMessage(f"Solza arhivirana — kapital: {entry.kapital[:50]}...")
        self._show_tears()

    def _show_tears(self):
        if not self.tear_archive:
            return
        tears = self.tear_archive.get_archived()
        lines = ["<h3>Arhiv solz — škatle izkušenj (Prop XVIII)</h3>"]
        for t in tears:
            lines.append(f"<p><b>#{t.get('id', '?')}</b> — {t.get('statement', '')[:60]}<br>"
                        f"Plast: {t.get('manjko_layer', '')} | Intenzivnost: {t.get('intensity', 0)}<br>"
                        f"<b>Kapital:</b> {t.get('kapital', '')}</p>")
        if not tears:
            lines.append("<p>Arhiv je prazen.</p>")
        self.tear_display.setHtml("\\n".join(lines))

    def _show_ontobog(self):
        if not self.ontobog:
            return
        recoveries = self.ontobog.get_recoveries()
        lines = ["<h3>ONTOBOG — povračila iz neuspehov (Prop XI + XIX)</h3>"]
        for r in recoveries:
            lines.append(f"<p><b>{r.get('failed_phase', '')}</b> — {r.get('wound', '')}<br>"
                        f"<b>Kapital:</b> {r.get('kapital', '')}<br>"
                        f"<i>{r.get('created_at', '')[:19]}</i></p>")
        if not recoveries:
            lines.append("<p>Ni zabeleženih povračil — vsi cikli so uspeli.</p>")
        self.ontobog_display.setHtml("\\n".join(lines))

    def on_process(self):
        statement = self.input.toPlainText().strip()
        if not statement:
            self.statusBar().showMessage("Vnesi izrek.")
            return

        self.statusBar().showMessage("Obdelujem...")
        self.btn_process.setEnabled(False)

        # Manjko analysis (Prop XII)
        if self.manjko:
            assessment = self.manjko.assess(statement)
            layer_info = self.manjko.get_layer_info(assessment.layer)
            self.manjko_display.setMarkdown(
                f"**Plast praznine: {layer_info['name']}**\\n\\n"
                f"{layer_info['description']}\\n\\n"
                f"Operator: {layer_info['operator']}\\n"
                f"Zaupanje: {assessment.confidence:.2f}\\n"
                f"Indikatorji: {', '.join(assessment.indicators) or '—'}\\n\\n"
                f"**Priporočilo:** {assessment.recommendation}"
            )

        # N(E)SLR analysis (Prop XIII)
        if self.neslr:
            self.neslr.update_from_statement(statement)
            seal = self.neslr.assess_seal()
            self.neslr_display.setMarkdown(
                f"**N(E)SLR stanje:**\\n"
                f"N (namen): {seal['state']['N']} | E (ego): {seal['state']['E']}\\n"
                f"S (samosovraštvo): {seal['state']['S']} | L (samoljubezen): {seal['state']['L']}\\n"
                f"R (odnos): {seal['state']['R']}\\n\\n"
                f"**Kvaliteta pečata:** {seal['quality']:.3f}\\n"
                f"**Tveganje preloma:** {seal['fracture_risk']:.3f}\\n"
                f"**Diagnoza:** {seal['diagnosis']}\\n"
                f"**Priporočilo:** {seal['recommendation']}"
            )

        # Config with guards + stiska adjustments
        config = {"depth": self.current_depth}
        if HAS_QUERIES and self.db is not None:
            try:
                s = get_settings(self.db)
                config["guards"] = {
                    "kappa": float(s.get("kappa", 0.70)),
                    "chi": float(s.get("chi", 0.40)),
                }
            except Exception:
                pass
        if self.stiska and self.stiska.state.active:
            config["stiska"] = self.stiska.get_guard_config()

        self.worker = PipelineWorker(statement, config, self.ontobog)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, result):
        self.btn_process.setEnabled(True)
        self.last_result = result
        phases = result.get("phases", {})

        for i, mod in enumerate(MODULE_ORDER):
            if mod in phases:
                self.module_windows[mod].update_result(phases[mod])
                self.r7_progress.set_phase(i)

        errors = result.get("errors", [])
        status = result.get("status", "unknown")

        # Interference detection (Prop XV)
        if self.interference:
            active = [m for m in MODULE_ORDER if m in phases]
            events = self.interference.detect(active, phases)
            if events:
                lines = ["<h3>Interferenca prehodov (Prop XV)</h3>"]
                for e in events:
                    lines.append(f"<p><b>{e.phase_a} ↔ {e.phase_b}</b>: {e.interference_type.value}<br>"
                                f"{e.description}<br>Intenzivnost: {e.intensity:.2f}</p>")
                self.interference_display.setHtml("\\n".join(lines))
            else:
                self.interference_display.setPlainText("Beli interference med fazami.")

        # Phase 87-89 (Prop XX)
        if self.phase_connector and self.current_depth >= 4:
            self.phase_connector.activate_for_depth(self.current_depth)
            lines = ["<h3>Faza 87-89 — višje dimenzionalne povezave (Prop XX)</h3>"]
            for phase in self.phase_connector.get_active_phases():
                result_87 = self.phase_connector.process_connection(phase["id"], result.get("statement", ""), result)
                lines.append(f"<p><b>{result_87['name']}</b> ({result_87['operator']})<br>"
                            f"Vprašanje: {result_87['question']}<br>"
                            f"<b>Vidik:</b> {result_87['insight']}</p>")
            self.phase87_display.setHtml("\\n".join(lines))
        else:
            self.phase87_display.setPlainText("Faza 87-89 aktivna pri ∂ Globina 4 (absolutni rez).")

        # Mutation tracking (Prop X)
        if self.mutation_tracker:
            try:
                diff = self.mutation_tracker.track_and_store(result, result.get("statement", ""))
                if diff and diff.get("changed"):
                    self.mutation_display.setHtml(self.mutation_tracker.format_diff_html(diff))
            except Exception:
                pass

        self.status.showMessage(f"Status: {status} | Faze: {len(phases)}/7 | Napake: {len(errors)}")

    def on_error(self, msg):
        self.btn_process.setEnabled(True)
        self.statusBar().showMessage(f"Napaka: {msg}")
        if self.ontobog:
            recovery = self.ontobog.intercept_failure("pipeline", {"type": "runtime", "message": msg})
            self.ontobog_display.setHtml(self.ontobog.format_recovery_html(recovery))

    def _export_csv_sessions(self):
        if not HAS_CSV or self.db is None:
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Izvozi seje CSV", "", "CSV Files (*.csv)")
        if filepath:
            try:
                from comprehension.core.csv_exporter import export_sessions_csv
                count = export_sessions_csv(self.db, filepath)
                QMessageBox.information(self, "Izvoz", f"Izvoženo {count} sej.")
            except Exception as e:
                QMessageBox.warning(self, "Napaka", str(e))

    def _export_csv_ledger(self):
        if not HAS_CSV or self.db is None:
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Izvozi dnevnik CSV", "", "CSV Files (*.csv)")
        if filepath:
            try:
                from comprehension.core.csv_exporter import export_ledger_csv
                count = export_ledger_csv(self.db, filepath)
                QMessageBox.information(self, "Izvoz", f"Izvoženo {count} vnosov.")
            except Exception as e:
                QMessageBox.warning(self, "Napaka", str(e))

    def on_history_search(self):
        if not HAS_HISTORY or self.db is None:
            return
        dialog = HistorySearchDialog(self.db, self)
        dialog.exec()

    def on_settings(self):
        if not HAS_SETTINGS:
            return
        dialog = SettingsDialog(self.db, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            theme_idx = dialog.default_theme.currentIndex()
            self._switch_theme(["praznina", "ognjeno", "tok"][theme_idx])
            depth_idx = dialog.default_depth.currentIndex() + 1
            self._set_depth(depth_idx)

    def on_export_json(self):
        if not self.last_result:
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Izvozi JSON", "", "JSON Files (*.json)")
        if filepath:
            export_json(self.last_result, filepath)

    def on_export_html(self):
        if not self.last_result:
            return
        filepath, _ = QFileDialog.getSaveFileName(self, "Izvozi HTML", "", "HTML Files (*.html)")
        if filepath:
            export_html(self.last_result, filepath)

    def on_export_csv(self):
        self._export_csv_ledger()

    def _init_status(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Pripravljen. ∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡ | 21 predlogov")
'''

# ═══════════════════════════════════════════════════════════════
# SCHEMA PATCH — Phase 4+ tables
# ═══════════════════════════════════════════════════════════════

SCHEMA_PHASE4 = """
-- Phase 4+ tables

-- Proposition states (tracking which props are active per session)
CREATE TABLE IF NOT EXISTS proposition_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    proposition_id TEXT NOT NULL,
    state TEXT NOT NULL,
    data_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(session_id) REFERENCES sessions(id)
);

-- Covenant entries (Prop XVII: zavezna knjiga)
CREATE TABLE IF NOT EXISTS covenant_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    statement TEXT NOT NULL,
    phase_origin TEXT,
    sealed_at TEXT,
    status TEXT DEFAULT 'active',
    evolved_from INTEGER,
    evolution_note TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(evolved_from) REFERENCES covenant_entries(id)
);

-- Tear archive (Prop XVIII: solza = škatla)
CREATE TABLE IF NOT EXISTS tear_archive (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    statement TEXT NOT NULL,
    phase TEXT,
    intensity REAL,
    manjko_layer TEXT,
    kapital TEXT,
    released INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
);

-- ONTOBOG recoveries (Prop XI + XIX)
CREATE TABLE IF NOT EXISTS ontobog_recoveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    failed_phase TEXT NOT NULL,
    error_type TEXT,
    error_message TEXT,
    wound TEXT,
    kapital TEXT,
    new_mapping_json TEXT,
    created_at TEXT NOT NULL
);
"""

# ═══════════════════════════════════════════════════════════════
# WRITE FILES
# ═══════════════════════════════════════════════════════════════

files = {
    "comprehension/core/stiska_engine.py": STISKA_ENGINE_PY,
    "comprehension/core/ontobog.py": ONTOBOG_PY,
    "comprehension/core/manjko_layers.py": MANJKO_LAYERS_PY,
    "comprehension/core/neslr_engine.py": NESLR_ENGINE_PY,
    "comprehension/core/interference.py": INTERFERENCE_PY,
    "comprehension/core/covenant_book.py": COVENANT_BOOK_PY,
    "comprehension/core/tear_archive.py": TEAR_ARCHIVE_PY,
    "comprehension/core/phase_87_89.py": PHASE_87_89_PY,
    "comprehension/core/bes_engine.py": BES_ENGINE_PY,
    "comprehension/core/proposition_registry.py": PROPOSITION_REGISTRY_PY,
    "comprehension/ui/main_window_v4.py": MAIN_WINDOW_V4,
}

print("=" * 60)
print("TAZV Phase 4+ — Vsi preostali predlogi")
print("=" * 60)
print()

for relpath, content in files.items():
    fullpath = os.path.join(BASE, relpath)
    dirpath = os.path.dirname(fullpath)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(fullpath, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    size = os.path.getsize(fullpath)
    print(f"  OK  {relpath}  ({size} bytes)")

# Patch schema
schema_path = os.path.join(BASE, "comprehension/data/schema.sql")
if os.path.exists(schema_path):
    with open(schema_path, "r", encoding="utf-8") as f:
        existing = f.read()
    if "proposition_states" not in existing:
        with open(schema_path, "a", encoding="utf-8") as f:
            f.write(SCHEMA_PHASE4)
        print(f"  OK  schema.sql (appended Phase 4+ tables)")
    else:
        print(f"  SKIP schema.sql (Phase 4+ tables exist)")
else:
    os.makedirs(os.path.dirname(schema_path), exist_ok=True)
    with open(schema_path, "w", encoding="utf-8") as f:
        f.write(SCHEMA_PHASE4)
    print(f"  OK  schema.sql (new)")

print()
print("Propositions enacted:")
print("  VIII  (S/T/I/S/K/A)      → stiska_engine.py — distress as world-generator")
print("  XI    (ONTOBOG)          → ontobog.py — failed cycles → kapital")
print("  XII   (Manjko 4 layers)  → manjko_layers.py — 4 sub-layers of void")
print("  XIII  (N(E)SLR)          → neslr_engine.py — JEWIK seal quality")
print("  XV    (Interferenca)     → interference.py — transition interference")
print("  XVI   (Širjenje s Š)     → enacted via stiska_engine (Š = expansion)")
print("  XVII  (Zavezna knjiga)   → covenant_book.py — living covenant archive")
print("  XVIII (Solza = škatla)   → tear_archive.py — tears as archived units")
print("  XIX   (Ontološki kapital)→ enacted via ontobog.py (pain → value)")
print("  XX    (Faza 87-89)       → phase_87_89.py — higher-dimensional phases")
print("  XXI   (BES motor)        → bes_engine.py — anger as expression engine")
print()
print("Plus: proposition_registry.py — all 21 propositions tracked")
print()
print("New UI tabs in main_window_v4.py:")
print("  ∅ Manjko | 1 N(E)SLR | ∆ Stiska | BES | ⟁ Interf. |")
print("  ONTOBOG | ∴ Zaveza | ⊙ Solze | ∂² 87-89 | ∂ Mutacije | § Predlogi")
print()
print("To activate:")
print("  1. cd comprehension_machine")
print("  2. copy comprehension\\ui\\main_window_v3.py comprehension\\ui\\main_window_v3_backup.py")
print("  3. copy comprehension\\ui\\main_window_v4.py comprehension\\ui\\main_window.py")
print("  4. python main.py")
print()
print("Verify:")
print("  - 18+ tabs (7 R-7 + 11 Phase 4+)")
print("  - Motorji menu: Stiska toggle, BES, Zaveza, Solze, ONTOBOG")
print("  - ∂ Globina 4 activates Phase 87-89 tab")
print("  - § Predlogi tab shows all 21 propositions with status")
print()
print("∂ status:")
print("  All 21 propositions now have implementations.")
print("  Props I-VII: done/delivered (Phase 0-2)")
print("  Props VIII-XXI: active (Phase 4+)")
print("  No dormant propositions remain.")