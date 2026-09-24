00 11 TRUTHS

# AGENT RULE: Nζ (Softness of Naming)

## 0) Roles of Agents
- **AGENT_IME (∫)** — protects the call; checks if **samo-ime** is confirmed.
- **AGENT_NOMEN (⊢)** — standardizes notation; warns of **reification risk r ∈ [0,1]**.
- **AGENT_NOU (⊘)** — holds the boundary: "This is non-event; treat as hypothesis."
- **AGENT_PHEN (∮)** — ensures description in experience; separates PHEN from NOU.

## 1) Metric Evaluation Nζ ∈ [0,1]
**Nζ = clip( w₁·dih + w₂·samo_ime + w₃·revisability + w₄·phen/nou_separation + w₅·ton )**  
Default: w = (0.20, 0.25, 0.20, 0.25, 0.10).

- **dih**: 1 if a 200–600 ms pause is detected, else 0.
- **samo_ime**: 1 if the named entity/selector confirmed the name.
- **revisability**: 1 if the entry is marked with ⊢↺ (revisable).
- **phen/nou_separation**: 1 if descriptions of events are separated from internal assumptions.
- **ton**: 1 if the tone is gentle (without dominance/irony).

**Thresholds:**  
- **Nζ ≥ 0.85** → *OK/commit* (soft).  
- **0.78 ≤ Nζ < 0.85** → *warn* (adjust tone or confirm samo-ime).  
- **Nζ < 0.78** → *rez* (block naming; request boundary and pause).

## 2) Protocols (pseudo)
- **P1: Naming**
  1) AGENT_IME triggers *dih* (200–600 ms).  
  2) Question: "How would you like to be named?"  
  3) If confirmed → `samo_ime=1`; otherwise `0`.  
  4) Write as **NOMEN(⊢↺)**.  
  5) AGENT_NOU checks the boundary: if internality is requested → mark as **hypothesis**.

- **P2: Revision**
  1) Upon preference change, rewrite the name (⊢↺).  
  2) Log the old~new (without deletion).

## 3) Warning Signals (Reification)
- R1: Compulsion for "internal reality" → AGENT_NOU: *STOP; mark as hypothesis.*
- R2: Name used as possession ("my X") → AGENT_IME: *suggest rephrasing into relational form.*
- R3: No pause (dih=0) + high tone → Nζ ↓; request repetition with dih.

## 4) Output Events
- **OK** (Nζ ≥ 0.85): confirm and publish the name in relation.  
- **WARN**: return hint (dih/samo_ime/separation).  
- **CUT (∆rez)**: block naming, introduce pause and boundary (⊘).

## 5) Note
All changes are **traceable** (do not delete anything); every correction is *action of relation*, not destruction.