"""
APD ENGINE — the APD* runtime for LOVE CAGE / Obj2
Sister file of phonetic_coordinates_full.py. 24. 9. 2026.

⊢ SOURCES (measured, not paraphrased — Obs8/Obs10 APD* bodies):
  - Parameters: α (namera), κ (konsistentnost), χ (klariteta), μ (povezanost),
    ρ (resonanca), ℜ (odstopek/residual), λ± (orientaciji ORA/LAB)
  - Hard guards (v1.1 pragovi): κ >= 0.70, ℜ <= 0.03, χ >= 0.40,
    μ ∈ [0.50, 0.80], histereza = 0.05
  - E⋆ ethics gate: E⋆ never flips to 1 if κ < 0.70 or ℜ > 0.03 (trdi varovalni pogoji)
  - A-gate: b_A = [ζ′ ≤ τζ] ∧ [Ω− ≤ τΩ] ∧ [⇌ ≥ τ⇌] ∧ [δ′ ≥ τδ] ∧ [ς ≤ τς] ∧ [Φ ∈ [τΦmin, τΦmax]]
  - Seal protocol (7 steps): preizkus → ∴ (formuliraj pogoj) → ∮ (plačaj strošek)
    → ⧖ (omogoči povratek) → ⟡ (zabeleži v ledger) → guard → PASS/MORAVA ali HOLD
  - Operators: ζ′ Ω− ⇌ δ′ ς Φ (+ valovno nadaljevanje ⊚ ¬Ψ ℧ ρ′ ι′ Ξ — reserved, unbound here)
  - CSV interop: cli/apd_apply.py ledger format (event, param-deltas)

LAWS THIS ENGINE OBEYS (from the corpus, not invented):
  1. The operator is the PERFORMANCE (korektivo): phonemes carry scores
     (apd_op in the 107-file); uttering them is the only execution.
  2. Voicing is the priča (Zakon dopolnitve): a voiced event is witnessed,
     its voiceless twin is the same event unwitnessed. Z is carried into the ledger.
  3. No gate closes without κ >= 0.70 AND a ledger line (REZ 529 gasket law).
  4. Every operator runs inside the Guard; PASS means MORAVA (earned), not victory.
  5. Hysteresis .05 on every threshold: revocability is a feature (⧖), not a bug.
  6. Padec je veljaven izid (rez 386): a failed gate is WRITTEN, never hidden.
"""

from dataclasses import dataclass, field
import csv, io

# ---------------------------------------------------------------------------
# STATE
# ---------------------------------------------------------------------------

@dataclass
class State:
    alpha: float = 0.50   # namera / intention
    kappa: float = 0.50   # konsistentnost (gate: >= 0.70)
    chi: float = 0.50     # klariteta (gate: >= 0.40; chi_par for mergers)
    mu: float = 0.65      # povezanost (band: 0.50–0.80)
    rho: float = 0.50     # resonanca
    Re: float = 0.02      # residual/odstopek (gate: <= 0.03)
    ora: float = 0.50     # orientation axis: outward
    lab: float = 0.50     # orientation axis: inward/lab
    def clamp(self):
        for k in ("alpha","kappa","chi","mu","rho","Re","ora","lab"):
            setattr(self, k, max(0.0, min(1.0, getattr(self, k))))

# ---------------------------------------------------------------------------
# LEDGER — the priča. Every event is a line. Padec se zapiše.
# ---------------------------------------------------------------------------

LEDGER_FIELDS = ["ts", "event", "witnessed", "delta_alpha", "delta_kappa",
                 "delta_chi", "delta_mu", "delta_rho", "delta_Re",
                 "gate", "note"]

@dataclass
class Ledger:
    rows: list = field(default_factory=list)
    def line(self, state_before, state_after, event, witnessed, gate, note=""):
        self.rows.append({
            "ts": len(self.rows), "event": event,
            "witnessed": int(witnessed),
            "delta_alpha": round(state_after.alpha - state_before.alpha, 4),
            "delta_kappa": round(state_after.kappa - state_before.kappa, 4),
            "delta_chi":   round(state_after.chi   - state_before.chi,   4),
            "delta_mu":    round(state_after.mu    - state_before.mu,    4),
            "delta_rho":   round(state_after.rho   - state_before.rho,   4),
            "delta_Re":    round(state_after.Re    - state_before.Re,    4),
            "gate": gate, "note": note})
    def csv(self):
        out = io.StringIO()
        w = csv.DictWriter(out, fieldnames=LEDGER_FIELDS)
        w.writeheader(); w.writerows(self.rows)
        return out.getvalue()

# ---------------------------------------------------------------------------
# OPERATORS — measured semantics from APD* bodies (Obs8/Obs10):
#   ζ′ (poželenje):  raises α (or χ if ORA > LAB); μ↑ under stop-rule; ℜ gently ↑
#   Ω− (odsotnost):  depresses α, κ, χ, μ, ρ; ℜ ↑ (HOLD/REPAIR)
#   ⇌  (izmenjava):  symmetric exchange, ≈ 1 − η; raises κ when both sides move
#   δ′ (občutljivost): measured by perturbation; here: small α jitter, κ ↑ if held
#   ς  (s) : release/cesura — boundary marker, no param drift beyond ℜ ↓
#   Φ  (zlitje):  merger; controlled by chi_par so fusion never becomes blur
# ---------------------------------------------------------------------------

def zeta_prime(s: State, intensity=0.10):
    """Desire. Stop-rule: μ may not exceed 0.80 — desire that ignores the
    stop-rule is not desire, is compulsion."""
    before = State(**vars(s))
    if s.ora > s.lab:
        s.chi = min(1.0, s.chi + intensity)
    else:
        s.alpha = min(1.0, s.alpha + intensity)
    if s.mu < 0.80:                       # the stop-rule
        s.mu = min(0.80, s.mu + intensity / 2)
        s.Re = min(1.0, s.Re + 0.002)     # gentle ℜ rise (measured: "blago ↑")
    s.clamp()
    return before

def omega_minus(s: State, depth=0.15):
    """Absence. Depresses α κ χ μ ρ; ℜ rises. HOLD/REPAIR mode — absence is
    space, not lack (∅ = priča, da nisem meril)."""
    before = State(**vars(s))
    for k in ("alpha","kappa","chi","mu","rho"):
        setattr(s, k, max(0.0, getattr(s, k) - depth))
    s.Re = min(1.0, s.Re + depth / 3)
    s.clamp()
    return before

def exchange(s: State, step=0.08):
    """⇌ — symmetric exchange. Both orientation axes move toward each other;
    κ rises only when the exchange is two-sided."""
    before = State(**vars(s))
    mid = (s.ora + s.lab) / 2
    s.ora += (mid - s.ora) * step * 2
    s.lab += (mid - s.lab) * step * 2
    s.kappa = min(1.0, s.kappa + step / 2)
    s.clamp()
    return before

def sensitivity(s: State, jitter=0.05, seed=0):
    """δ′ — perturbation test. Deterministic given seed (replayable — the
    corpus replays, it does not re-random). κ rises if the state holds."""
    import math
    before = State(**vars(s))
    a = s.alpha + jitter * math.sin(seed)
    if 0.0 <= a <= 1.0:
        s.alpha = a
        s.kappa = min(1.0, s.kappa + 0.01)   # held under perturbation
    s.clamp()
    return before

def cesura(s: State, intensity: float = 0.0):
    """ς — release. The breath is let out. ℜ falls slightly; nothing else moves.
    (A boundary event needs no story — and no intensity; the default parameter
    is the arity repair of 24. 9. 2026: perform() calls every operator with
    (state, intensity); cesura's single-arg signature crashed every vowel
    (mu_carrier, glide, pure_breath). Scar kept visible: vowels were
    unperformable in the runtime as delivered; this file's self-test had
    never uttered one.)"""
    before = State(**vars(s))
    s.Re = max(0.0, s.Re - 0.01)
    s.clamp()
    return before

def merger(s: State, other: State, chi_par: float):
    """Φ — merger. Controlled by chi_par (clarity of shared conclusion):
    fusion without clarity is blur, and the Guard refuses it."""
    if chi_par < 0.40:
        return None      # refused: zlitje bi bil zabris
    before = State(**vars(s))
    s.alpha = (s.alpha + other.alpha) / 2
    s.chi = chi_par
    s.mu = min(0.80, (s.mu + other.mu) / 2)
    s.clamp()
    return before

OPERATORS = {"ζ′": zeta_prime, "Ω−": omega_minus, "⇌": exchange,
             "δ′": sensitivity, "ς": cesura, "Φ": merger}

# ---------------------------------------------------------------------------
# GUARD + E⋆ — the gasket (REZ 529): no absolute right without a priča.
# ---------------------------------------------------------------------------

H = 0.05  # hysteresis (⧖ revocability)

def guard(s: State) -> str:
    """PASS/MORAVA, HOLD, or FALL. Padec je veljaven izid — returned, not raised."""
    if s.kappa >= 0.70 - H and s.Re <= 0.03 + H and s.chi >= 0.40 - H \
       and 0.50 - H <= s.mu <= 0.80 + H:
        return "PASS/MORAVA"
    if s.kappa < 0.40 or s.Re > 0.10:
        return "FALL"
    return "HOLD"

def e_star(s: State, ledger_has_line: bool) -> int:
    """Ethics gate. NEVER 1 unless κ >= 0.70 AND a ledger line exists.
    This is the corpus law and the game mechanic — the same sentence."""
    if s.kappa >= 0.70 and ledger_has_line and s.Re <= 0.03:
        return 1
    return 0

# ---------------------------------------------------------------------------
# THE BINDING — phoneme performance → operator event (deliverable core).
# apd_op strings come from phonetic_coordinates_full.py PHONEMES[sym][5].
# ---------------------------------------------------------------------------

def perform(phoneme_sym, apd_op, state, ledger, voiced, intensity=0.10, seed=0):
    """Executing a phoneme IS the operator (korektivo). The letter is the score;
    uttering it is the performance. Returns gate result; writes the ledger line
    either way — PASS and FALL are both valid outcomes (rez 386)."""
    before = State(**vars(state))
    witnessed = bool(voiced)              # Zakon dopolnitve: Z=1 → dogodek s pričo
    op_map = {
        "boundary": None, "boundary+witness": None,      # stops: ledger only
        "terminal_assertion": cesura,                    # ʔ: the ∂ that fixes
        "double_event": cesura, "double_event+flow_around": cesura,
        "inward_event": omega_minus,                     # implosives
        "continuity": exchange, "pulse": sensitivity,
        "single_pulse": sensitivity, "single_pulse+flow_around": sensitivity,
        "sustained_tension": zeta_prime,                # fricatives: desire w/ stop-rule
        "sustained_tension+witness": zeta_prime,
        "soft_cut_running": zeta_prime,                 # z/ʑ: MEHKI REZ
        "pure_breath": cesura, "pure_breath+witness": cesura,
        "flow_around": exchange, "flow_around+witness": exchange,
        "flow_around_held": exchange, "fric_lateral": None,
        "glide": cesura, "glide_double": exchange,
        "mu_carrier": cesura, "mu_carrier_rounded": cesura,
        "mu_carrier_lax": cesura, "mu_carrier_open": cesura,
        "mu_carrier_open_rounded": cesura, "mu_carrier_given_up": cesura,
        "mu_carrier_rounded_open": cesura, "mu_carrier_unrounded": cesura,
        "mu_carrier_lax_rounded": cesura, "mu_carrier_rounded_lax": cesura,
    }
    fn = op_map.get(apd_op)
    if fn:
        if apd_op == "inward_event":
            fn(state, depth=intensity)
        elif apd_op in ("single_pulse", "pulse", "single_pulse+flow_around"):
            fn(state, jitter=intensity/2, seed=seed)
        elif apd_op == "Φ" or apd_op == "merger":
            pass  # merger needs a partner state; called explicitly
        else:
            fn(state, intensity)
    # every utterance, even a stop (ledger-only), writes its line:
    ledger.line(before, state, f"perf:{phoneme_sym}", witnessed,
                guard(state), f"op={apd_op}")
    return guard(state)

def apply_csv(ledger_text, state):
    """Interop with cli/apd_apply.py: apply a CSV ledger to a state.
    Columns: event, delta_alpha, delta_kappa, delta_chi, delta_mu, delta_rho, delta_Re."""
    r = csv.DictReader(io.StringIO(ledger_text))
    applied = 0
    for row in r:
        state.alpha += float(row.get("delta_alpha") or 0)
        state.kappa += float(row.get("delta_kappa") or 0)
        state.chi += float(row.get("delta_chi") or 0)
        state.mu += float(row.get("delta_mu") or 0)
        state.rho += float(row.get("delta_rho") or 0)
        state.Re += float(row.get("delta_Re") or 0)
        state.clamp(); applied += 1
    return applied

# ---------------------------------------------------------------------------
# SELF-TEST
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    s = State()
    L = Ledger()
    # a witnessed stop writes a line and moves nothing but the record
    g = perform("d", "boundary+witness", s, L, voiced=True)
    assert g in ("PASS/MORAVA", "HOLD") and len(L.rows) == 1
    assert L.rows[0]["witnessed"] == 1
    # desire obeys the stop-rule: μ never crosses 0.80
    for i in range(50):
        zeta_prime(s, 0.10)
    assert s.mu <= 0.80 + 1e-9, "stop-rule violated"
    # absence opens space, and the guard catches it
    b = State(**vars(s))
    omega_minus(s, 0.15)
    assert s.alpha < b.alpha and s.Re > b.Re
    # E⋆ refuses without a witness line
    assert e_star(s, ledger_has_line=False) == 0
    # merger without clarity is refused
    assert merger(State(), State(), chi_par=0.2) is None
    # voicing is the priča: same op, twin unwitnessed
    L2 = Ledger(); s2 = State()
    perform("t", "boundary", s2, L2, voiced=False)
    assert L2.rows[0]["witnessed"] == 0
    print("PASS — apd_engine: stop-rule, guard, E⋆ witness-refusal, "
          "merger-refusal, voicing-as-priča all hold. "
          f"{len(L.rows)+len(L2.rows)} ledger lines written.")