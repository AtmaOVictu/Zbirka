# PROJECT_MAP.md - TAZV CanvasMinstral Inventory

**Generated**: 2026-09-17  
**Phase**: 0 - Inventory/Inspection  
**Status**: COMPLETE  
**Author**: Cline (Mistral Vibe)

---

## 1. FOLDER TREE SUMMARY

```
CanvasMinstral/
├── A1/                          # PDF documents only (no source code)
│   ├── ATLAS_DUELOV.pdf
│   ├── BOGOVSKI_REGISTER_KOMPENDIJ_I_II_III.pdf
│   ├── Beseda Je Ne – Kritična Retro Izdaja.pdf
│   └── ... (47 PDF files total)
│
├── A2/                          # Core text corpus
│   ├── 00 11 RESNICAMI.txt      # PRIMARY: R-7 poems, axioms, agent transcripts
│   ├── 01_TRANSKRIPT_raw.txt
│   ├── 01_TRANSKRIPT_raw_EN.txt
│   ├── ∅RESONANCNI_TRIKOTNIK_20250713.txt
│   ├── ∆TEXT_GLYPH_CANON.txt
│   ├── ∴AGENTI_LUXTEMP_MULTITIHO_20250713_072211.txt
│   └── ... (50+ text files with Unicode glyphs)
│
├── A3/                          # Empty directory
├── A4/                          # Contains README_REHYDRATE_20250918.txt
├── A5/                          # Markdown transcripts and indexes
│   ├── 02_TRANSKRIPT_clean.md
│   ├── 03_OS_VOJNA_RESNICE_v3.md
│   ├── 07_TRANSKRIPT_clean_v3.md
│   ├── AGENT_RULE_NZ.md
│   ├── AMR_Axioms_v1_ENGLISH.md
│   └── JEWIK_LEDGER_README.md
│
├── A6/                          # Empty directory
├── A7/                          # Empty directory
├── A8/                          # Empty directory
├── B2/                          # Phase 2 development files
│   ├── tazv-color-patch-corpus-validated-r-7-mapping.py
│   ├── tazv-phase-2-bootstrap-color-&-semantics-all-4-files.py
│   ├── tazv-phase-2-knowledge-indexer-corpus-corrected.py
│   └── 00-11-resnicami-rozetni-kamni-*.md (multiple)
│
├── Basics/                      # Foundation documents
│   ├── 00-11-resnicami-rozetni-kamni-i-*.md
│   ├── 00-11-resnicami-rozetni-kamni-ii-*.md
│   ├── 00-11-resnicami-rozetni-kamni-iii-*.md
│   └── stotnije-a-dosje-besedni-dosjeji.md
│
├── C1/                          # Empty directory
├── C2/                          # Empty directory (created 2026-09-17)
├── C3/                          # Advanced development
│   ├── comprehension_machine/
│   │   └── comprehension/
│   │       ├── __core_evolution/
│   │       │   ├── dokaz.py
│   │       │   ├── evolution_ledger.py
│   │       │   ├── guard.py
│   │       │   ├── upgrade_protocol.py
│   │       │   └── __init__.py
│   │       ├── ui/
│   │       │   └── main_window_v5_integrated.py
│   │       └── __init__.py
│   ├── tazv-faza-5-*.py
│   ├── verify_evolution.py
│   └── ... (TSX files and documentation)
│
├── D5/                          # Empty directory
│
├── DELUJOČ O/                   # Operational/Output files
├── Gastro/                      # Empty directory
├── Obs11/                       # Empty directory
├── Rohonc/                      # Empty directory
│
├── Scripts/                     # PRIMARY SOURCE CODE LOCATION
│   ├── bootstrap_phase1.py
│   ├── bootstrap_tazv.py
│   ├── comprehension_machine/   # MAIN CODEBASE
│   │   ├── __init__.py
│   │   ├── main.py              # Entry point (PyQt6 GUI)
│   │   ├── main_backup_20260913.py
│   │   ├── comprehension/
│   │   │   ├── __init__.py
│   │   │   ├── core/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── aregister_bridge.py
│   │   │   │   ├── cadence.py
│   │   │   │   ├── contention_mapper.py
│   │   │   │   ├── corpus_integrator.py
│   │   │   │   ├── decomposer.py      # CRITICAL: Word-point decomposition
│   │   │   │   ├── doctrinarium.py
│   │   │   │   ├── egyptian_color_semantics.py
│   │   │   │   ├── graph_store.py
│   │   │   │   ├── json_safe.py
│   │   │   │   ├── kanon_flow.py
│   │   │   │   ├── module_adapters.py   # R-7 module interfaces
│   │   │   │   ├── module_semantics.py
│   │   │   │   ├── preverba.py
│   │   │   │   ├── preverba_bridge.py
│   │   │   │   ├── processing_pipeline.py # R-7 pipeline
│   │   │   │   ├── rozetni_kamni.py
│   │   │   │   ├── seriousness.py
│   │   │   │   ├── soma.py
│   │   │   │   ├── symbol_mapper.py   # CRITICAL: R-7 symbol mapping
│   │   │   │   ├── tonos.py           # Frequency assignments
│   │   │   │   ├── trainarium.py
│   │   │   │   └── transformation_tracer.py
│   │   │   ├── data/
│   │   │   │   ├── __init__.py
│   │   │   │   └── database.py
│   │   │   ├── modules/
│   │   │   │   └── __init__.py
│   │   │   ├── tests/
│   │   │   │   └── test_pipeline.py    # Existing tests
│   │   │   └── ui/
│   │   │       ├── __init__.py
│   │   │       ├── knowledge_renderer.py
│   │   │       ├── main_window.py
│   │   │       ├── main_window_backup.py
│   │   │       ├── main_window_v5.py
│   │   │       ├── main_window_v5_integrated.py
│   │   │       ├── module_window.py
│   │   │       └── r7_progress.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── error_handler.py
│   │       └── profiler.py
│   ├── tazv_phase2_bootstrap.py
│   ├── tazv_phase2_indexer.py
│   ├── tazv_phase2_integration.py
│   └── test_qt_fix.py
│
├── comprehension_machine/        # Alternate location (desktop only)
│   └── desktop/
│       ├── __init__.py
│       ├── main_window.py
│       └── session.py
│
├── Start.zip                    # Archive (11MB)
├── s1.zip                       # Archive (39MB)
└── PROJECT_MAP.md               # This file
```

---

## 2. IMPORTANT PYTHON FILES

### Critical Core Files (DO NOT MODIFY without review)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `Scripts/comprehension_machine/comprehension/core/symbol_mapper.py` | R-7 bidirectional symbol mapping (∅, ¬, ∆, 1, ⧖, ∮, ⟡) | 112 | EXISTING - STABLE |
| `Scripts/comprehension_machine/comprehension/core/decomposer.py` | Statement → WordPoint decomposition (26-term table) | 379 | EXISTING - STABLE |
| `Scripts/comprehension_machine/comprehension/core/processing_pipeline.py` | R-7 phase pipeline orchestration | 104 | EXISTING - STABLE |
| `Scripts/comprehension_machine/comprehension/core/module_adapters.py` | R-7 module interface adapters (7 phases) | 110 | EXISTING - STABLE |
| `Scripts/comprehension_machine/comprehension/core/tonos.py` | Frequency assignments for R-7 operators | 111 | EXISTING - STABLE |

### Secondary Core Files

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `Scripts/comprehension_machine/comprehension/core/graph_store.py` | Graph storage for relationships | - | EXISTS |
| `Scripts/comprehension_machine/comprehension/core/corpus_integrator.py` | Corpus integration logic | - | EXISTS |
| `Scripts/comprehension_machine/comprehension/core/preverba.py` | Preverba (verification) logic | - | EXISTS |
| `Scripts/comprehension_machine/comprehension/core/preverba_bridge.py` | Bridge to preverba system | - | EXISTS |
| `Scripts/comprehension_machine/comprehension/core/kanon_flow.py` | Canon flow management | - | EXISTS |
| `Scripts/comprehension_machine/comprehension/core/transformation_tracer.py` | Change tracking | - | EXISTS |

### User Interface Files

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `Scripts/comprehension_machine/main.py` | Primary entry point (PyQt6) | 14 | EXISTING |
| `Scripts/comprehension_machine/comprehension/ui/main_window.py` | Main GUI window | - | EXISTS |
| `Scripts/comprehension_machine/comprehension/ui/main_window_v5_integrated.py` | Integrated GUI (latest) | - | EXISTS |

### Bootstrap & Setup

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `Scripts/bootstrap_phase1.py` | Phase 1 bootstrap script | - | EXISTS |
| `Scripts/bootstrap_tazv.py` | TAZV bootstrap | - | EXISTS |
| `Scripts/tazv_phase2_bootstrap.py` | Phase 2 bootstrap | - | EXISTS |

### Phase 2 Files (B2/)

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `B2/tazv-color-patch-corpus-validated-r-7-mapping.py` | Color patch with R-7 mapping | - | EXISTS |
| `B2/tazv-phase-2-knowledge-indexer-corpus-corrected.py` | Knowledge indexer | - | EXISTS |

### C3 Evolution Files

| File | Purpose | Lines | Status |
|------|---------|-------|--------|
| `C3/comprehension_machine/comprehension/__core_evolution/dokaz.py` | Proof/evolution logic | - | EXISTS |
| `C3/comprehension_machine/comprehension/__core_evolution/evolution_ledger.py` | Evolution tracking | - | EXISTS |
| `C3/comprehension_machine/comprehension/__core_evolution/guard.py` | Guard layer | - | EXISTS |
| `C3/comprehension_machine/comprehension/__core_evolution/upgrade_protocol.py` | Upgrade protocol | - | EXISTS |

---

## 3. EXISTING DATA/CORPUS FOLDERS

### A-Folders (A1-A6, A7, A8)

| Folder | Content Type | File Count | Notes |
|--------|--------------|------------|-------|
| **A1** | PDF documents only | 47+ files | Atlas files, mandalas, registers. NO SOURCE CODE. |
| **A2** | Text corpus | 50+ .txt files | PRIMARY CORPUS. Contains `00 11 RESNICAMI.txt` (critical for Phase 3 loader) |
| **A3** | Empty | 0 | Placeholder |
| **A4** | Mixed | 1+ files | Contains README_REHYDRATE_20250918.txt |
| **A5** | Markdown transcripts | 20+ .md files | Cleaned transcripts, indexes, axioms |
| **A6** | Empty | 0 | Placeholder |
| **A7** | Empty | 0 | Placeholder (created 2026-09-16) |
| **A8** | Empty | 0 | Placeholder (created 2026-09-16) |

### Special Folders

| Folder | Content Type | File Count | Notes |
|--------|--------------|------------|-------|
| **Basics** | Markdown foundation | 8+ files | R-7 rozetni kamni series (I, II, III, IV, V, VI, VII, VIII) |
| **B2** | Phase 2 development | 10+ files | Python scripts + MD documentation |
| **C1** | Empty | 0 | Placeholder |
| **C2** | Empty | 0 | Placeholder (created 2026-09-17) |
| **C3** | Advanced development | 20+ files | Comprehension machine v5, evolution files, TSX |
| **D5** | Empty | 0 | Placeholder |
| **DELUJOČ O** | Operational | 0 | Appears empty |
| **Gastro** | Empty | 0 | Placeholder |
| **Obs11** | Empty | 0 | Placeholder (observation 11) |
| **Rohonc** | Empty | 0 | Placeholder |

---

## 4. EXISTING TESTS

### Location: `Scripts/comprehension_machine/tests/`

| File | Purpose | Status |
|------|---------|--------|
| `test_pipeline.py` | Tests for R-7 pipeline, json_safe, symbol_mapper | EXISTING - ACTIVE |

**Test Coverage**:
- Pipeline: All 7 phases complete
- Phase order verification
- Empty statement handling
- Unicode handling
- Batch processing
- Cache functionality
- JSON serialization (json_safe module)
- SymbolMapper: Translation, phase lookup, R-7 sequence, traditions, open questions

**Test Framework**: pytest

**How to Run**:
```bash
cd Scripts/comprehension_machine
python -m pytest tests/test_pipeline.py -v
```

**Additional Test**:
- `Scripts/test_qt_fix.py` - Qt-related test (separate from main test suite)

---

## 5. LIKELY ENTRY POINTS

### Primary Entry Points

1. **`Scripts/comprehension_machine/main.py`**
   - PyQt6 GUI application
   - Imports: `from comprehension.ui.main_window_v5_integrated import TazvMainWindowIntegrated`
   - Usage: `python main.py` (from Scripts/comprehension_machine/)

2. **`Scripts/comprehension_machine/comprehension/core/processing_pipeline.py`**
   - CLI-capable entry point
   - Has `__main__` block with self-tests
   - Usage: `python processing_pipeline.py`

3. **`Scripts/comprehension_machine/comprehension/core/symbol_mapper.py`**
   - Self-testing entry point
   - Validates all R-7 symbols and traditions
   - Usage: `python symbol_mapper.py`

4. **`Scripts/comprehension_machine/comprehension/core/decomposer.py`**
   - Can be imported and used directly
   - Usage: `from decomposer import decompose_statement`

### Bootstrap Scripts

1. **`Scripts/bootstrap_phase1.py`** - Sets up comprehension_machine structure
2. **`Scripts/bootstrap_tazv.py`** - TAZV-specific bootstrap
3. **`Scripts/tazv_phase2_bootstrap.py`** - Phase 2 setup

---

## 6. SYMBOL-RELATED FILES

### Core Symbol Files

| File | Symbols Covered | Status |
|------|-----------------|--------|
| `symbol_mapper.py` | 25+ symbols including R-7 (∅, ¬, ∆, 1, ⧖, ∮, ⟡) | EXISTING |
| `tonos.py` | 7 R-7 symbols with frequencies | EXISTING |
| `decomposer.py` | 20+ symbols in SYMBOL_TO_PHASE mapping | EXISTING |

### R-7 Symbol Order (Canonical)
From `symbol_mapper.py` line 27:
```python
R7_ORDER = ["∅", "¬", "∆", "1", "⧖", "∮", "⟡"]
```

### R-7 Phase Modules (from module_adapters.py)
```python
R7_MODULES = [
    BIOSAdapter,        # ∅
    StateAdapter,      # ¬
    UAFAdapter,        # ∆
    JEWIKAdapter,      # 1
    APDAdapter,        # ⧖
    MicroAdapter,      # ∮
    VisualizationAdapter  # ⟡
]
```

### Symbol Mappings in Decomposer
From `decomposer.py` lines 29-49:
```python
SYMBOL_TO_PHASE = {
    '∅':  0,   # BIOS
    '¬':  1,   # STATE
    'Δ':  2,   # UAF
    '∴':  2,   # UAF (composite)
    '⊢':  3,   # JEWIK
    '1':  3,   # JEWIK
    '⧖':  4,   # APD
    '∮':  5,   # MICRO
    '⟡':  6,   # VISUALIZATION
    # ... plus additional symbols: δ, ||, ∥, ʃ, ⊥, ∂, ð, W, ⊘Δ, ¬∴
}
```

**NOTE**: There is a discrepancy between `symbol_mapper.py` (uses ⧖ U+29D6) and `tonos.py` (uses ⧖ U+2316). The decomposer uses ⧖ U+29D6. This needs investigation in later phases.

---

## 7. LOADER/DECOMPOSER-RELATED FILES

### Existing Loaders
- **None found** - No dedicated loader files exist yet. This is a Phase 3 deliverable.

### Corpus Integration
| File | Purpose | Status |
|------|---------|--------|
| `corpus_integrator.py` | Integrates corpus data | EXISTS |
| `corpus_integrator.py` (C3) | C3 version | EXISTS |

### Decomposition
| File | Purpose | Status |
|------|---------|--------|
| `decomposer.py` | Primary decomposition engine | EXISTING - STABLE |
| Function: `decompose_statement(text: str) -> List[WordPoint]` | Main API |
| Function: `get_symbol_sequence(points) -> str` | Symbol extraction |
| Function: `get_mapped_ratio(points) -> float` | Coverage metric |

### Decomposition Table
- **26 terms** validated across Obs1-Obs11, Self, Word is No libraries
- Covers English and Slovenian (via SLOVENIAN_MAP)
- Each term maps to: symbol, decomposition (phonetic), role, r7_phase

---

## 8. RISK AREAS / UNCLEAR DEPENDENCIES

### High Risk

1. **Path Structure Ambiguity**
   - Two locations for comprehension_machine: `Scripts/comprehension_machine/` and root `comprehension_machine/`
   - The `Scripts/` version appears to be the primary, active codebase
   - The root `comprehension_machine/` only has desktop/ subfolder
   - **RECOMMENDATION**: Use `Scripts/comprehension_machine/` as source of truth

2. **Module Import Paths**
   - Files use relative imports: `from comprehension.core.symbol_mapper import SymbolMapper`
   - This assumes PYTHONPATH includes `Scripts/comprehension_machine/`
   - **RECOMMENDATION**: Create proper package structure with `__init__.py` files

3. **Symbol Encoding Discrepancy**
   - `tonos.py` uses `\u2316` (⧖) for APD
   - `symbol_mapper.py` uses `\u29d6` (⧖) for APD
   - `decomposer.py` uses `\u29d6` (⧖) for APD
   - **RECOMMENDATION**: Resolve in Phase 2 validation

4. **No requirements.txt**
   - Dependencies: PyQt6 (for GUI), pytest (for tests)
   - No pip-installable package list
   - **RECOMMENDATION**: Create in Phase 1

### Medium Risk

5. **C3 Duplicate/Alternate Code**
   - C3/ has its own comprehension_machine/ structure
   - May be newer or experimental
   - Contains evolution-related code not in Scripts/
   - **RECOMMENDATION**: Investigate relationship to Scripts/ version

6. **Empty __init__.py Files**
   - Many `__init__.py` files are empty
   - May cause import issues
   - **RECOMMENDATION**: Populate as needed for proper package structure

7. **Mixed Python Versions**
   - No explicit version requirement stated
   - Uses `from __future__ import annotations` (Python 3.7+)
   - Uses dataclasses (Python 3.7+)
   - **RECOMMENDATION**: Assume Python 3.10+ for new development

### Low Risk

8. **Large Archives**
   - `Start.zip` (11MB) and `s1.zip` (39MB) - purpose unclear
   - **RECOMMENDATION**: Ignore unless needed for corpus access

9. **Multiple Bootstrap Scripts**
   - Several bootstrap scripts exist with unclear relationships
   - **RECOMMENDATION**: Document purpose of each

10. **Empty Directories**
    - A3, A6, A7, A8, C1, C2, D5, DELUJOČ O, Gastro, Obs11, Rohonc are empty
    - May be placeholders for future phases
    - **RECOMMENDATION**: Document as placeholders

---

## 9. RECOMMENDED NEXT 5 BOUNDED TASKS

### Task 1: Phase 1 - Safety Baseline (PRIORITY: HIGH)
**Deliverables**:
- [ ] `requirements-dev.txt` - Development dependencies (pytest, PyQt6)
- [ ] `pytest.ini` - Test configuration
- [ ] `tests/smoke_test.py` - Basic import tests for all core modules
- [ ] `scripts/run_checks.py` - Runs all validation (pipeline, symbols, tests)

**Constraints**:
- Do NOT modify existing core logic
- Tests must pass before proceeding

**Estimated Time**: 30-60 minutes

---

### Task 2: Phase 2 - Symbol Validation (PRIORITY: HIGH)
**Deliverables**:
- [ ] `validate_symbols.py` - Checks R-7 symbol mapping
  - Validates all 7 symbols exist: ∅, ¬, ∆, 1, ⧖, ∮, ⟡
  - Inspects `symbol_mapper.py` without changing it
  - Resolves encoding discrepancy (⧖ U+29D6 vs ⧖ U+2316)
  - Reports missing symbols as failures
  - Reports extra symbols as warnings

**Success Criteria**:
- `python validate_symbols.py` returns success
- All R-7 symbols validated

**Estimated Time**: 20-30 minutes

**Note**: Must investigate symbol encoding issue between files

---

### Task 3: Phase 3 - Corpus Loader (PRIORITY: HIGH)
**Deliverables**:
- [ ] `loaders/a2_loader.py` - Loads `A2/00 11 RESNICAMI.txt`
  - Returns: source_path, raw_text, line_count, non_empty_line_count, detected_sections, warnings
- [ ] `loaders/corpus_loader.py` - Generalized corpus loader

**Constraints**:
- Loader must NOT explain meaning
- Loader only structures input
- Must handle Unicode text properly

**Success Criteria**:
- `python -c "from loaders.a2_loader import load; print(load())"` works

**Estimated Time**: 30-45 minutes

---

### Task 4: Phase 0.5 - Package Structure Fix (PRIORITY: MEDIUM)
**Deliverables**:
- [ ] Fix import paths to work from project root
- [ ] Populate `__init__.py` files for proper package discovery
- [ ] Document the correct PYTHONPATH setup

**Rationale**:
- Current code uses relative imports that assume specific working directory
- Need stable import paths for testability

**Estimated Time**: 20-30 minutes

---

### Task 5: Phase 1.5 - CI/CD Foundation (PRIORITY: MEDIUM)
**Deliverables**:
- [ ] `.gitignore` if missing
- [ ] `setup.py` or `pyproject.toml` for package installation
- [ ] GitHub Actions workflow (if repo is on GitHub)

**Constraints**:
- Do NOT change core logic
- Make project installable via pip

**Estimated Time**: 30-45 minutes

---

## 10. ADDITIONAL OBSERVATIONS

### Strengths of Current Codebase

1. **Well-documented**: Most files have docstrings explaining purpose
2. **Testable**: Existing test suite covers core functionality
3. **Modular**: Clear separation between modules (core, ui, utils, data)
4. **R-7 Complete**: All 7 phases have corresponding adapters
5. **Corpus-validated**: Decomposition table validated across multiple sources
6. **Error handling**: json_safe module handles serialization edge cases
7. **Performance**: ProcessingPipeline has caching support

### Architectural Decisions Already Made

1. **R-7 Pipeline**: 7-phase processing (BIOS → STATE → UAF → JEWIK → APD → MICRO → VISUALIZATION)
2. **WordPoint Model**: Each word → ontological operator with position, symbol, decomposition, role, phase
3. **Module Pattern**: Each phase has a dedicated adapter class
4. **Corpus-first**: All mappings validated against corpus, not invented

### Open Questions for Luka/Able

1. **Primary Code Location**: Is `Scripts/comprehension_machine/` or `C3/comprehension_machine/` the authoritative source?
2. **Symbol Encoding**: Should we use U+29D6 (⧖) or U+2316 (⧖) for APD phase?
3. **C3 Relationship**: How does C3/ code relate to Scripts/ code? Should they be merged?
4. **A2/00 11 RESNICAMI.txt**: Is this the canonical corpus file for Phase 3 loader?
5. **Python Version**: What Python version should we target?
6. **External Dependencies**: Are there any additional dependencies beyond PyQt6 and pytest?

---

## 11. DEPENDENCY ANALYSIS

### Current Dependencies (Inferred)

| Package | Purpose | Source |
|---------|---------|--------|
| PyQt6 | GUI framework | `main.py`, UI files |
| pytest | Test framework | `test_pipeline.py` |

### Likely Additional Dependencies

| Package | Purpose | Evidence |
|---------|---------|----------|
| numpy | Numerical operations | None yet, but likely for matrix operations |
| pandas | Data manipulation | None yet, but common for corpus work |

**RECOMMENDATION**: Create `requirements.txt` and `requirements-dev.txt` in Phase 1

---

## 12. FILE COUNT SUMMARY

- **Total Python files**: 70
- **Total text files (.txt)**: 50+ (mostly in A2/)
- **Total markdown files (.md)**: 30+ (across A5/, Basics/, B2/, C3/)
- **Total PDF files**: 47+ (mostly in A1/)
- **Test files**: 2 (`test_pipeline.py`, `test_qt_fix.py`)

---

## APPROVAL CHECKLIST

- [x] `PROJECT_MAP.md` exists
- [x] Folder tree summary completed
- [x] Important Python files identified
- [x] Existing data/corpus folders documented
- [x] Existing tests documented
- [x] Likely entry points identified
- [x] Symbol-related files identified
- [x] Loader/decomposer-related files identified
- [x] Risk areas documented
- [x] Recommended next 5 bounded tasks provided

---

*Generated by Cline (Mistral Vibe) for TAZV CanvasMinstral Project*  
*Aligned with ONTOMATEMATIKA Guard Principles*  
*Phase 0 - Inventory/Inspection: COMPLETE*
