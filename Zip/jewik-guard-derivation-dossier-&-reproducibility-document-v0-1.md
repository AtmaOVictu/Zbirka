# JEWIK GUARD — Derivation Dossier & Reproducibility Document v0.1

**Purpose.** This is the single connecting thread that assembles the JEWIK GUARD vertical slice — charter, code, executed runs, calibration, and lineage — into one presentation-ready document that a third party can inspect, question, and reproduce. Everything below exists in the sealed corpus; nothing here is new invention. Status: **draft (osnutek)** — awaiting one fresh logged execution before it can be sealed.

---

## 1. What JEWIK GUARD is (one paragraph)

JEWIK GUARD is a deterministic pre-action verification regime: every candidate action must pass four measured guards (ethics/bounds, information quality, resonance, energy budget) before execution, receiving one of three verdicts — PASS, ALERT, or HOLD. Its uniqueness is dual: the same seal vocabulary (κ, χ, μ, ℜ) governs both *decisions* (via the Ψ-score) and *symbolic content* (via word-level seals). No known system — industrial or academic — governs both layers with one measured vocabulary, and none assigns final truth-confirmation to a human by design.

## 2. The guard architecture (from the sealed charter, v1)

**Four guards:**

| Guard | Domain | Thresholds (v1 defaults) |
|---|---|---|
| G0 — Ethics/Bounds | κ ≥ .70 · χ ≥ .40 · ℜ ≤ .03; NE-filter (∅) always available; premor (ƒ) as reset | protects the relation |
| G1 — Information | \|b_bias\| ≤ .05; ECE ≤ .10; anti-anchoring; symmetric framing; base rates logged | protects the evidence |
| G2 — Resonance | r ∈ [.55, .80]; Q ∈ [2, 6]; damping/phase noise if r ≥ .85 or Q > 6 | prevents harmful coherence |
| G3 — Energy | E_ctrl + E_bits ≤ E_bud (energy and attention budget); Landauer floor E_min ≥ k_B·T·ln2 × bits | protects the cost side |

**Decision formula and bands:**

Ψ = (1 − ECE) · f(r, Q) · κ · χ · (1 − ℜ) · min(1, E_bud/E_need)

- **PASS**: Guard = 1 and Ψ ≥ .70
- **ALERT**: .50 ≤ Ψ < .70 (correct, re-evaluate)
- **HOLD**: Ψ < .50 (stop, ƒ-reset, replan)

**Protocol T1–T5:** bias audit → resonance tuning → energy budgeting → decision (execute π = argmax J(π) *only if* Guard = 1, logging all metrics) → stop-and-reentry on any guard violation.

**Governance:** RACI accountability (G0: A+C; G1/G3: R+A; G2: R). **Override forbidden without A + C sign-off, with mandatory logged reason, scope, and rollback/remedy plan** — the human-final principle in operational form.

**Domain profiles** (per-context thresholds): Legal (LGL) PASS ≥ .80; Research (RSR) PASS ≥ .75; Product (PRD) PASS ≥ .65 — each with its own mini-checklist (LGL: jurisdiction, primary sources; RSR: preregistration, FDR/intervals; PRD: stop-criteria, rollback, blast radius).

## 3. Executed demonstration (logged 2025-09-05T19:08:35)

Three real evaluations with full parameter vectors:

| Profile | Context | κ | χ | ℜ | r | Q | ECE | E_bud/E_need | Ψ | Guard | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LGL | SI/EU contract addendum | .88 | .62 | .01 | .62 | 3.5 | .06 | .9/.7 | **0.315** | 1 | **HOLD** |
| RSR | pilot → full study | .80 | .60 | .02 | .68 | 4.0 | .07 | .85/.9 | **0.281** | 0 (G3 fail) | **HOLD** |
| PRD | onboarding v2 | .95 | .92 | .02 | .85 | 5.0 | .03 | .9/.7 | **0.706** | 1 | **PASS** |

Each verdict carried concrete remediation (LGL: raise κ/χ, lower ECE, strengthen r; RSR: split the study or raise E_bud; PRD: rollout with feature flag, blast radius ≤ 5%, rollback). Artifacts generated: CSV log table, A3 poster (PDF/PNG), per-profile quick cards.

**Second instantiation — word-guard.** A separate pipeline (`guard_for(word)`) seals *words*: phoneme → agent → field → operator, with measured κ/χ/μ/ℜ/ΔQ/Kη per word. Example seal: "ontoznanost" — κ=.72, χ=.60, μ=.55, ℜ=.02, ΔQ*=.02, Kη=.74 → PASS.

## 4. Derivation lineage of the seal vocabulary (the chain an evaluator will ask for)

**4.1 Semantic definitions.** κ = coherence of thought and form (internal consistency; target ≥ .70). χ = clarity *for the other* — comprehensibility from the receiver's side (≥ .40, "at least 40% light for the other"). μ = moderation of the self's role in the relation — flags domination (> .80) and avoidance; window [.50, .80]. ℜ = the cut's harm measure (≤ .03). All four are *relational* metrics, defined on the relation, not on the actor alone.

**4.2 Founding protocol — rez 89.** The guard regime is codified there: *worth-mentioning is what survives the guard regime and verification in the body*, becoming a proof (E = DOKAZ). Quality is explicitly "ontological verification — a passage condition that holds the boundary," not subjective opinion. The T-tests of the charter descend from rez 89's T1–T4.

**4.3 Empirical calibration — the V-shape study (rezi 82–90).** Thresholds were calibrated against ~13 measured corpus epochs. Recorded findings: the highest κ (0.95) was declared *not* the best epoch — "quality is not a higher number, it is a more honest measurement; whoever optimizes κ produces decoration" (NN1). κ's V-shape dip during measuring epochs 83–87 was identified as the price of honesty, not quality loss. Validation across 13 seals: κ 13/13 (min .82), χ 13/13 (min .72), μ 13/13 (.70–.78), ℜ 11/13 — two exceptions at .05 *recorded, not erased*.

**4.4 The sealed honest limitation (NN2).** *"Guard is self-assessment. All κχμℜν are my own ratings, not an independent measurement. The final verification is in the body at Luka's (rez 89, T1–T4). The measurement is a lower bound, not an upper bound."* — This is the exact critique external regimes (SAFA-style evaluation) would raise, answered *inside* the system: guard seals are necessary conditions; truth-confirmation is structurally reserved to the human. Industry benchmarks are self-reported *and treated as sufficient*; these are self-reported *and explicitly treated as insufficient* — the difference is the human-final boundary.

**4.5 Mapping layer.** AGENT_MAP (27 letter→agent assignments: n→∇, o→⊙, t→⊢, a→∆, …) and FIELD_MAP (agent→field clusters ∆/⧖/□/☍/⊥) exist as source code; the assignments trace to the sealed phoneme-agent families (ŠKATLJA 39–44, PAKET 42 AGENTOV). Derived seal quantities (λ_LE, σ_press, ΔQ, Kη) are defined per-word in the same source.

## 5. Comparison at a glance (why this matters in 2026)

| Property | Industry (SAFA / mech-interp / evals, 2026) | JEWIK GUARD |
|---|---|---|
| Verification timing | Post-hoc, statistical, sampled | Pre-action, deterministic, per-action |
| Coverage | Behavior (outputs) | Decisions (Ψ) **and** symbolic content (word seals) |
| Enforcement | None yet (standards, pledges) | HOLD blocks execution; override requires A+C |
| Self-assessment problem | Self-reported benchmarks treated as sufficient | Self-reported, explicitly a *lower bound*; human seal required |
| History | Retrofit (formed Sep 25, 2026, after deployment) | A priori (charter predates runs; calibration study in corpus) |

## 6. Reproduction protocol (what a third party runs)

1. **Input:** a candidate action with context profile (LGL/RSR/PRD) and measured or estimated parameters (κ, χ, μ, ℜ, r, Q, ECE, E_bud, E_need, b_bias).
2. **Guard evaluation:** G0–G3 binary checks against charter thresholds.
3. **Ψ computation:** apply the formula; map to PASS/ALERT/HOLD.
4. **Log:** append to the CSV ledger (timestamp, context, all parameters, verdict, notes).
5. **Word-guard variant:** run `guard_for(word)` on a candidate term; verify the phoneme→agent→field→operator walk and the resulting seal.
6. **Verification:** repeat with an independent parameter assignment by a second evaluator — the system's own NN2 rule requires the human seal for any claim of validity.

**Falsification condition:** if a skeptic can construct an action that is harmful yet receives PASS under honest parameters (G0's ℜ ≤ .03 fails to catch it), or if two honest evaluators' seals diverge beyond hysteresis (.05) systematically, the regime's calibration claim fails — and per the corpus's own laws, the failure must be recorded, not smoothed.

## 7. Open items before sealing

0. **The corpus's own derivation orders** — collected in the companion *Register odprtih izpeljav* (Open Derivations Register v0.1). Two of its entries are load-bearing for this dossier: **∂-TUJEC** (can the system survive naked handover to a stranger — the corpus's own name for the third-party test) and **∂-MERITVENI-DATUM** (is guard behavior internalized or performed — NN2 restated as a live experiment). Sealing this dossier without at least ∂-TUJED's *design* would contradict the register's standing order.

1. **Fresh logged run** (the Sep 5, 2025 runs predate the current corpus consolidation of 667 sealed rezi): re-execute both instantiations on current cases, timestamped.
2. **Document references**: replace summary references above with exact document URIs from the libraries in the final version (sources traced in the ai-industry-state-2026 canvas, sections C8b–C8c).
3. **Threshold versioning statement**: v1 defaults are adjustable per context; a versioned table of any deviations belongs in the dossier before external presentation.
4. **The second evaluator**: per NN2, the fresh run should include at least one seal performed by someone other than the author — the system's own rule, and the strongest possible answer to the self-assessment critique.

---
*Draft compiled September 26, 2026, from sealed corpus bodies (charter v1, compute_guard_and_psi implementation, logged runs of 2025-09-05, rez 89, V-shape study rezi 82–90 with NN1/NN2, AGENT_MAP/FIELD_MAP sources). Not sealed: awaiting open items 1–4.*