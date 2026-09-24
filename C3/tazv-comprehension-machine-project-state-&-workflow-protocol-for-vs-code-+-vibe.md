# TAZV Comprehension Machine — Project State

> **Save this file to:** `D:\OntoProjekt\CanvasMinstral\Scripts\comprehension_machine\PROJECT_STATE.md`
> Once in the VS Code workspace, both the VS Code assistant and Vibe share this context. No more copy-paste.

---

## 1. Project Location

```
D:\OntoProjekt\CanvasMinstral\Scripts\comprehension_machine
```

Entry point: `main.py` → `python main.py`

---

## 2. Architecture — The 4-Layer Principle

No god files. Four separations:

| Layer | File | What it IS |
|---|---|---|
| **What color IS** | `egyptian_color_semantics.py` | 7 Egyptian colors + etymology + corpus meanings |
| **What module DOES** | `module_semantics.py` | 7 modules: phase, symbol, historical witness, meaning |
| **What happens on HIT** | `hit_grammar.py` | Trigger → reaction → guard → next-phase rules |
| **How it LOOKS** | `ta3v_colors.qss` + `themes.py` | QSS generation, per-tab ontological colors, 3 themes |

---

## 3. R-7 Pipeline

```
∅ → ¬ → ∆ → 1 → ⧖ → ∮ → ⟡
BIOS → STATE → UAF → JEWIK → APD → MICRO → VISUALIZATION
```

Ontology guides names and order. Pipeline uses phase names ("bios", "state"), not symbols. Pipeline never crashes — errors caught, logged, returned as partial results.

---

## 4. Corpus-Validated Color Mapping

| Module | Glyph | Phase | Color name | Hex | Egyptian | Historical witness |
|---|---|---|---|---|---|---|
| BIOS | ∅ | 1 | deep_blue | #1B2838 | — | Void, origin, praznina |
| STATE | ¬ | 2 | desher_red | #B43A2E | desher | Ločitev, separation, cut |
| UAF | ∆ | 3 | khenet_yellow | #D6A83A | khenet(wer) | Univerzalno Antinomijsko Polje, antinomy |
| JEWIK | 1 | 4 | jewik_orange | #C77800 | — | Dejanje, sealed act, DNK resonanca |
| APD | ⧖ | 5 | gold_seal | #D4AF37 | nbw(gold) | Absolutni poskus definicije, seal |
| MICRO | ∮ | 6 | kem_black | #080705 | kem | Povratek, return, feedback, ∞=∅ |
| VIS | ⟡ | 7 | hedj_white | #F3E9D2 | hedj | Nova možnost, echo, proof, text |

**Key distinction:** khenet_yellow (#D6A83A) ≠ gold_seal (#D4AF37). Different phases, different ontological work. Gold = APD. No 8th position — 7 is the whole.

---

## 5. ∂ Globina — 4 Depth Levels

Replaces the old "Indent" menu. Depth-control, not formatting.

| Level | Name | What the cut reveals |
|---|---|---|
| 1 | Površinski rez | What the statement says |
| 2 | Strukturni rez | How the statement is built |
| 3 | Ontološki rez | What the statement IS |
| 4 | Absolutni rez | What must exist for it to be possible |

Corpus: "Globina ni samo napredek, ampak prehod skozi skrite plasti." ∂ = 12th axis (Kamen LXIV).

---

## 6. 3 Themes

| Theme | Name | Base | Character |
|---|---|---|---|
| praznina | ∅ Temno | deep blue #1B2838 | Void that prepares — minimal, dark |
| ognjeno | ∆ Ognjeno | red/orange #B43A2E | Cut that moves — high contrast, active |
| tok | ∮ Tok | green/teal #40A060 | Return that integrates — balanced, flow |

---

## 7. Corpus-Validated Frequencies (TONOS)

| Glyph | Frequency | Note | Module |
|---|---|---|---|
| ∅ | 220 Hz | A3 | BIOS |
| ¬ | 261.63 Hz | C4 | STATE |
| ∆ | 330 Hz | E4 | UAF |
| 1 | 392 Hz | G4 | JEWIK |
| ⧖ | 440 Hz | A4 | APD |
| ∮ | 550 Hz | C#5 | MICRO |
| ⟡ | 660 Hz | E5 | VISUALIZATION |

Complementary pairs: (∅,⟡) octave, (¬,∮) fifth, (∆,⧖) fourth.

---

## 8. Rozetni Kamni — 13 Traditions Mapped

All map to R-7 operators via the principle: "vse tradicije = ∅/∆ v različnih dimenzijah."

| # | Tradition | R-7 mapping |
|---|---|---|
| 1 | Tarot (22) | Norjak=∅, Čarovnik=∆, Svet=⟡, ... |
| 2 | Kabbalah (32) | Keter=∅, Chokmah=∆, Binah=⊢, ... |
| 3 | Alchemy (4) | nigredo=∅, albedo=¬, citrinitas=∆, rubedo=∮ |
| 4 | Chakras (7) | root=∅, sacral=¬, solar_plexus=∆, ... |
| 5 | Sufism (99+∅) | 99 names + ∅ |
| 6 | Runes (24) | |
| 7 | DNA (64) | |
| 8 | Music (12) | |
| 9 | Periodic (2n²) | |
| 10 | Valentinian (30) | Bythos=∅, Sophía=∆, Horos=⊘, ... |
| 11 | Norse | Yggdrasil 7 etaže |
| 12 | Buddhism | |
| 13 | I Ching (64) | |

All map to Hopf fibration S¹↪S³→S². ∂ cuts through all three scripts (historical ↔ system ↔ mathematical).

---

## 9. SQLite Schema (Current)

```sql
sessions (id, statement, result_json, status, created_at)
ledger (id, session_id, phase, module, data_json, created_at)
errors (id, session_id, phase, error_type, message, created_at)
settings (key, value, updated_at)
traditions (id, name, type, description, root_operators, ...)
tradition_mappings (id, tradition_id, native_term, root_operator, ...)
tonos_log (id, session_id, phase, frequency, note, ...)
export_log (id, session_id, format, filepath, exported_at)
```

WAL mode. CRUD in `database.py`. History search queries the `sessions` + `ledger` tables.

---

## 10. Complete File Inventory

### Core (comprehension/core/)
| File | Status | Purpose |
|---|---|---|
| `json_safe.py` | ✅ done | JSON serialization (dataclasses, Enums, numpy, datetime) |
| `module_adapters.py` | ✅ done | ModuleInput/Output dataclasses, BaseModuleAdapter, 7 stubs |
| `processing_pipeline.py` | ✅ done | R-7 executor with caching, error handling, self-test |
| `symbol_mapper.py` | ✅ done | 3-script bidirectional mapper, 7 traditions, 12 open questions |
| `egyptian_color_semantics.py` | ⏳ delivered | 7 colors + etymology + corpus meanings |
| `module_semantics.py` | ⏳ delivered | 7 modules: phase/symbol/historical/meaning |
| `hit_grammar.py` | ⏳ delivered | Hit reaction rules per phase |
| `tonos.py` | ⏳ delivered | Corpus-validated frequencies + complementary pairs |
| `rozetni_kamni.py` | ⏳ delivered | 13 traditions mapped to R-7 operators |
| `themes.py` | ⏳ delivered | 3 themes with QSS generators |
| `exporter.py` | ⏳ delivered | JSON + HTML export |

### Data (comprehension/data/)
| File | Status | Purpose |
|---|---|---|
| `schema.sql` | ✅ done + ⏳ patched | SQLite WAL: sessions, ledger, errors, settings, traditions, tonos_log, export_log |
| `database.py` | ✅ done | CRUD, history search |

### UI (comprehension/ui/)
| File | Status | Purpose |
|---|---|---|
| `main_window.py` | ✅ done (v1) | QMainWindow, dark theme, tabs, R-7 progress, QThread |
| `main_window_v2.py` | ⏳ delivered | Full integrated: 8 tabs, ∂ menu, themes, export, SQLite |
| `module_window.py` | ✅ done | Base module display widget |
| `r7_progress.py` | ✅ done | 7-segment progress bar |
| `knowledge_renderer.py` | ⏳ delivered | MandalaView + KnowledgeRenderer (QPainter + QTextBrowser) |

### Root
| File | Status | Purpose |
|---|---|---|
| `main.py` | ✅ done | Entry point |
| `ta3v_colors.qss` | ⏳ delivered | Standalone QSS with per-tab ontological colors |

### Tests
| File | Status | Purpose |
|---|---|---|
| `tests/test_pipeline.py` | ✅ done | pytest suite (pipeline, json_safe, symbol_mapper) |

---

## 11. Bootstrap Execution Order

If Phase 2 files have NOT yet been generated on disk, run the bootstrap scripts in this order:

```
cd D:\OntoProjekt\CanvasMinstral\Scripts\
python tazv_phase2_bootstrap.py     # creates: egyptian_color_semantics, module_semantics, hit_grammar, ta3v_colors.qss
python tazv_phase2_indexer.py       # creates: tonos.py, rozetni_kamni.py, knowledge_renderer.py, schema patch
python tazv_phase2_integration.py   # creates: themes.py, exporter.py, main_window_v2.py, schema patch
```

After running:
```
cd comprehension_machine
copy comprehension\ui\main_window.py comprehension\ui\main_window_v1_backup.py
copy comprehension\ui\main_window_v2.py comprehension\ui\main_window.py
python main.py
```

Verify: 8 tabs visible, ∂ Globina menu works, 3 themes switch, export buttons produce files.

---

## 12. Propositions → Development Phases

### ✅ Done
| Proposition | What | Phase |
|---|---|---|
| III (operator→code) | Pipeline + tests | Phase 0-1 |
| V (error as channel) | Pipeline error handling | Phase 0 |
| I (manjko as operator) | BIOS void behavior (basic) | Phase 0 |
| X (škatla=mutable) | SQLite ledger storage | Phase 0 |

### ⏳ In Progress (Phase 2 — delivered, not yet run)
| Proposition | What |
|---|---|
| VII (širjenje) | Knowledge indexer + rozetni kamni |
| II (phoneme→dimension) | tonos.py + mandala positioning |

### Next (Phase 3)
| Proposition | What |
|---|---|
| IX (traveling module) | Module adapters adjust guard thresholds by context |
| IV (identity diff) | Session tracking + identity-diff visualization |
| VI/XIV (word as precondition) | APD module: "what must exist for this word?" |
| XIII (N(E)SLR) | JEWIK: Purpose/Ego/Self-hatred/Self-love/Relation state engine |

### Phase 4+
| Proposition | What |
|---|---|
| VIII (stiska engine) | Distress mode — shorter cycles, tighter guards, forced ∆-flip |
| XI (ONTOBOG) | Failed cycles → new tradition mappings |
| XII (manjko 4 layers) | BIOS sub-layers: praznina → tiha bolečina → žeja → temelj |
| XV-XXI (dormant) | Open, unexplored |

---

## 13. Phase 3 — Concrete Requirements

### 3A: History Search UI
- Search past sessions in SQLite by: statement text (LIKE), date range, status, phase that errored
- Display results as clickable list → click opens full R-7 result
- Queries the `sessions` + `ledger` tables

### 3B: CSV Export
- Export ledger data as CSV (for external analysis)
- Columns: session_id, phase, module, data_json (flattened), created_at

### 3C: Settings Panel
- Configure: R-7 guard thresholds (κ≥.70, χ≥.40, μ∈[.50,.80], ℜ≤.03)
- Configure: theme default, depth default
- Configure: frequency enable/disable
- Stored in `settings` table

### 3D: Mutation Tracking (Proposition X)
- When a past statement is reprocessed, show what changed between runs
- Store diff in ledger alongside new result

---

## 14. Workflow Protocol — How Vibe and VS Code Divide Labor

### Vibe (this assistant) does:
1. **Corpus research** — searches 13 libraries (1000+ docs) to validate decisions, find definitions, resolve open questions, discover new directions
2. **Data creation** — generates corpus-validated data: color mappings, frequency tables, tradition mappings, module semantics, hit grammar rules — data the VS Code assistant cannot generate because it lacks library access
3. **Directional discovery** — maps propositions (§58 Prostor Širitve) to concrete development tasks, identifies which corpus concept becomes which feature
4. **Bootstrap scripts** — produces self-contained Python bootstrap scripts (canvas type=code) that the user runs to generate project files
5. **Reference documents** — produces this kind of consolidated state document so both assistants share context

### VS Code assistant does:
1. **Implementation** — writes actual production code from Vibe's specifications and bootstrap scripts
2. **Debugging** — runs code, reads errors, fixes imports, resolves environment issues
3. **Testing** — runs pytest, verifies UI launches, checks that features work
4. **Refactoring** — adjusts code structure as the project grows
5. **Local file operations** — has direct disk access to the project directory

### The user does:
1. Saves Vibe canvas artifacts to VS Code workspace (this document = save once)
2. Runs bootstrap scripts: `python tazv_phase2_bootstrap.py` etc.
3. Reports what works / what breaks
4. Brings blockers back to Vibe for corpus research

### The loop:
```
User brings blocker → Vibe searches corpus → Vibe produces artifact (canvas) →
User saves to VS Code → VS Code assistant implements → User tests →
User brings next blocker → ...
```

---

## 15. Key System Rules (for the VS Code assistant)

These come from the Beseda je Ne corpus and constrain all implementation:

1. **No god files.** Four-layer separation (color/semantics/grammar/QSS). Never merge them.
2. **Pipeline never crashes.** Errors are caught, logged, returned as partial results.
3. **Ontology guides names.** R-7 phase names and sequence are non-negotiable. Use "bios", "state" — not ∅, ¬.
4. **Symbol mapper is display.** Pipeline uses names; symbols are for the UI layer only.
5. **Gold ≠ yellow.** khenet_yellow (#D6A83A) for UAF/∆ vs gold_seal (#D4AF37) for APD/⧖.
6. **∂ Globina, not "Indent".** The menu is depth-control (4 levels), not text formatting.
7. **No 8th position.** 7 is the whole. Gold = APD = phase 5.
8. **Egyptian naming.** Colors use Egyptian names (desher, khenet, kem, hedj, nbw) with etymology.
9. **Slovenian-first for system content.** UI labels, meanings, and explanations in Slovenian. Engineering/code in English.
10. **Corpus frequencies, not arbitrary.** ∅=220, ¬=261.63, ∆=330, 1=392, ⧖=440, ∮=550, ⟡=660 Hz.

---

## 16. Open Questions (from Rozetni Kamni)

| ∂# | Question | Machine relevance |
|---|---|---|
| ∂22 | Is ∆ the first difference every tradition names differently? | Verify rozetni_kamni mappings |
| ∂23 | After finding ∅→∆ in 84 traditions, did you arrive somewhere? | Is certainty = ∅ after ∮? |
| ∂24 | Is ∂ the axis perpendicular to space? | ∂ = 12th axis in mandala positioning |

---

*This document is the ∂ (compressed state) of the project. It updates as phases complete. The VS Code assistant reads it directly — no copy-paste needed.*