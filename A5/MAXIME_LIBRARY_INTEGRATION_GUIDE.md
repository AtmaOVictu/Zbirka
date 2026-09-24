# MAXIME LIBRARY INTEGRATION GUIDE
**How to operationalize the 96 maxims in VICTOR_CORE system**

---

## 🎯 QUICK START: WHERE TO USE EACH SECTION

| Maxim Section | Use In | Purpose |
|---|---|---|
| **M1 · Foundations** | Game intro, system philosophy | Teach core truth: truth↔bridge↔boundary |
| **M2 · Language/Name/On** | Identity system, card naming | How to name things without reification |
| **M3 · Body/Breath** | Meditation/ritual modules | Physical basis of ethics |
| **M4 · Time/Hysteresis** | Quest pacing, cycle design | Why delays matter, not errors |
| **M5 · Space/Boundary/Bridge** | UI/UX design, zones | Design principle: clear bounds + connections |
| **M6 · Movement/Act** | Game action design | Small acts count; direction > magnitude |
| **M7 · Relation/Ethics** | Multiplayer, relationships | How consent, dispute, adulthood work |
| **M8 · Illusion/Mask** | Narrative design, engagement | When to use narrative; when to break it |
| **M9 · Practice/Protocol** | Ritual sequences, game flow | Actual step-by-step: ⊘ → NAME → ON → seal |
| **M10 · Validation/Guard** | Achievement system, progress | Metrics: κ, χ, μ, ℜ thresholds |
| **M11 · Agents** | Agent protocols, bot behavior | How agents guard thresholds, not dominate |
| **M12 · Idea/A Priori** | Theory modules, research | How theory connects to practice |

---

## 🔧 CONCRETE EXAMPLES

### Example 1: Game Quest Design (using M6, M9, M10)

**Scenario:** You're designing a quest where player names a new identity.

**Without maxims:** Player names themselves, game accepts any name, move on.

**With maxims:**

1. **M2 · Name/On**: Use protocol P1 from AGENT_RULE_NZ
   - Trigger breath (200-600ms)
   - Ask: "How would you like to be called?"
   - Confirm self-naming
   - Mark as NOMEN(⊢↺) — revisable

2. **M9 · Practice**: Follow sequence
   - ⊘ (cut) = pause before naming
   - NAME = confirmed self-naming
   - ON = direction this identity gives
   - Measure (κ, χ, μ, ℜ) = validate clarity, coherence, tone
   - SEAL = close loop with acknowledgment

3. **M6 · Movement**: Recognize micro-acts
   - Don't wait for "perfect" name
   - ε_act ≥ .01 (smallest act counts)
   - This naming is the micro-act that shifts the game

4. **M10 · Validation**: Check thresholds
   - κ (clarity): player's name is clear to them? Yes/no
   - χ (coherence): does it fit their journey? Yes/no
   - μ (tone): soft, not forced? Yes/no
   - ℜ (remainder): no loose ends? Yes/no

**Result:** Player doesn't just name themselves; they *enact* their identity with ritual (M9), breathe it (M3), and feel it validated (M10).

---

### Example 2: Agent Behavior (using M11)

**Scenario:** Agent says "no" to a player request.

**Without maxims:** Player feels opposed, blames agent.

**With M11 · Agents:**
- **"Agent 'No' is not enemy; is guardian of threshold"**
  - Agent explains: "This is a threshold. You need a new passage."
  - Player understands: agent is protecting, not opposing

**Result:** Conflict becomes collaborative (finding new passage together).

---

### Example 3: Handling Engagement/Illusion (using M8)

**Scenario:** Beautiful game narrative is super engaging. Is that good?

**M8 · Illusion says:**
- **"Illusion = heater, not home"** → Don't let it be the final destination
- **"Iluzija brez pričevanja (⟡) postane odvisnost"** → Without reflection/testimony, it's addiction

**What to do:**
1. Use the narrative (heater)
2. But add testimony checkpoints (⟡):
   - After quest: "What did you learn?"
   - After session: "What changed in you?"
   - In ledger: Record the shift without judgment

**Result:** Engagement that teaches, not just hooks.

---

### Example 4: Conflict Resolution (using M7)

**Scenario:** Two players in multiplayer game have conflict.

**M7 · Ethics says:**
- **"Dispute does not destroy if it guards boundary and seeks bridge"**
  - Players can fight if they: guard their own boundary (no abuse) + seek bridge (look for solution)

**Protocol:**
1. **Boundary:** Each player can pause and say "stop" (⊘)
2. **Bridge:** Both seek solution (∴)
3. **Consent:** Never coerce; always negotiate (M7: "coercion is cut into other")
4. **Adulthood:** Result should show care_surplus ≥ 1 (both grew)

**Result:** Conflict becomes learning, not domination.

---

### Example 5: Validation Thresholds (using M10)

**Scenario:** Player claims they've learned etymology of a word.

**M10 metrics:**
```
- κ (clarity) ≥ .70: Can they explain it clearly?
- χ (coherence) ≥ .55: Does it connect to other words?
- μ (tone) ∈ [.60,.78]: Are they excited but not manic?
- ℜ (remainder) ≤ .02: Do they have loose threads?
```

**If all pass:** Mark as LEARNED with seal (∴)

**If some fail:**
- **κ too low?** Ask them to explain differently
- **χ too low?** Help them find connections
- **μ too high?** Ask them to reflect quietly (M3: breath)
- **ℜ too high?** Ask: what's still unresolved?

**Result:** Learning is measured, not just claimed.

---

## 📊 MAPPING MAXIMES TO GAME ELEMENTS

### Player Progression
- **M1** → Opening philosophy (why truth matters)
- **M11** → How to interpret agent decisions
- **M7** → How to relate to other players
- **M6** → How small acts lead to progression

### Quest Design
- **M2** → How naming works
- **M9** → Ritual sequences
- **M8** → When to use story; when to break it
- **M4** → Pacing (delays are integration, not waste)

### Card/Knowledge System (MAGNUS_OPUS)
- **M2** → SEAL ⇔ NAME ∧ ON (every card has name + location)
- **M10** → Validation thresholds (κ, χ, μ, ℜ)
- **M12** → How theory becomes practice

### Relationship System
- **M7** → Ethics, consent, recognition (χ ≥ .55 = being seen)
- **M3** → Rhythm, breath (μ regulation)
- **M5** → Boundaries + bridges (don't isolate or spill)

### Validation/Achievement
- **M10** → Guard thresholds (when something is truly learned)
- **M6** → Micro-acts count (ε_act ≥ .01)
- **M9** → Record without stigma (ledger)

---

## 🛠️ IMPLEMENTATION CHECKLIST

When building a feature, check each relevant section:

### For Game Quests:
- [ ] M1: Is the core truth clear?
- [ ] M2: Does naming follow protocol?
- [ ] M6: Do micro-acts count?
- [ ] M8: Is there illusion AND testimony?
- [ ] M9: Does it follow sequence?
- [ ] M10: Can you measure success?

### For Agent Design:
- [ ] M2: Does agent use NAME+ON correctly?
- [ ] M3: Does agent breathe/pause?
- [ ] M7: Does agent respect consent?
- [ ] M11: Is agent a guardian, not dominator?

### For Card Systems:
- [ ] M2: Every card has SEAL ⇔ NAME ∧ ON
- [ ] M10: Can you validate with κ, χ, μ, ℜ?
- [ ] M12: Is theory grounded in practice?

### For Relationships:
- [ ] M5: Are boundaries clear? Are bridges possible?
- [ ] M7: Is consent required? Is adulthood visible?
- [ ] M3: Is rhythm maintained?

---

## 📖 TRANSLATION REFERENCE

When reading the English version, remember:

| Symbol | Meaning | When You See It |
|--------|---------|-----------------|
| **⊘** | Cut, boundary, no-space | "Stop and create distance" |
| **∆** | Shift, change, triangle | "Something fundamental changed" |
| **∴** | Bridge, therefore, connection | "Now connect across the boundary" |
| **⧖** | Time, cycle, hourglass | "Timing matters; measure cycles" |
| **□** | Space, field, boundary | "Establish a bounded field" |
| **⊥** | Body, ground, perpendicular | "Root this in physical reality" |
| **∮** | Circle, cycle, integral | "This is a completed cycle" |
| **☍ (chi)** | Relation, recognition, seeing | "Two seeing each other" |
| **⟡** | Witness, testimony, star | "Something is recorded/witnessed" |
| **∫** | Call, integral, integration | "Summon or integrate" |

---

## 🎓 TRAINING YOUR TEAM

### For Designers:
"Read M6, M9, M10. A good quest has micro-acts (M6), follows sequence (M9), and can be validated (M10)."

### For Programmers:
"Read M10, M11, M2. Your validation checks go in M10 thresholds. Your agents follow M11. Your naming follows M2+AGENT_RULE_NZ."

### For Writers:
"Read M8, M1, M12. Use illusion (M8) but add testimony. Ground it in truth (M1). Make theory practical (M12)."

### For Players/Testers:
"Read M1, M7. Understand the core principle (M1). Understand that conflict seeks bridges, not dominance (M7)."

---

## ⚡ QUICK DECISION MATRIX

**When you're unsure about a design decision:**

| Decision | Ask | Answer In |
|----------|-----|-----------|
| Should this be optional? | Does it have boundary + bridge? | M5 |
| Is this progression good? | Are micro-acts visible? | M6 |
| Should I measure this? | Is it κ, χ, μ, ℜ-compatible? | M10 |
| Is this fair conflict? | Does it guard boundary + seek bridge? | M7 |
| Should I force this? | Does it require consent? | M7 |
| Is this engagement ok? | Does it have testimony/reflection? | M8 |
| Should I follow this sequence? | Is it ⊘ → NAME → ON → seal? | M9 |
| Can I name this? | Is it gentle (Nζ ≥ .85)? | AGENT_RULE_NZ |

---

## 🔗 RELATED DOCUMENTS

- **MAXIME_LIBRARY_v2_ENGLISH.md** — Full text of all 96 maxims
- **MAXIME_LIBRARY_HISTORY_PURPOSE.md** — Why this document exists, what it's for
- **AGENT_RULE_NZ.md** — How to apply M2 (naming) operationally
- **VOJNA_RESNICE_ROE_v2.md** — How to apply M7 (ethics) to conflict
- **VICTOR_CORE system docs** — Where these maxims are enforced in code

---

## 💡 THE ONE SENTENCE YOU NEED

**"Truth without bridge is excuse; bridge without boundary is spillage."**

Every design question reduces to: Does your feature have **both cut (⊘) and bridge (∴)? Both boundary and connection?**

If yes, you're using the maximes.

---

**Integration Guide Created:** 2026-06-04
**For use with:** VICTOR_CORE system, game design, agent training
**Status:** Ready for implementation
