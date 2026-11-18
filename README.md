# Zbirka · corpus archive ⟨Beseda je Ne⟩ (TAZV CanvasMinstral)

**English** · [Slovenščina](README-SL.md)


> Public archive: corpus bodies ∧ the TAZV machine ∧ the chain of license doors.
> Phase 0 inventory: [PROJECT_MAP.md](PROJECT_MAP.md) ⊙ 17. 9. 2026 ⊢ measured at the source

## What Zbirka is

Zbirka is the archive house of the corpus in three layers:

1. **Corpus bodies**: A1 (47+ PDFs ⊙ PROJECT_MAP.md: atlases, mandalas, registers), A2 (the primary text corpus: poems, axioms, agent transcripts), A5 (cleaned transcripts ∧ indexes), Basics (rosette stones ∧ stotnije, the word dossiers).
2. **The machine**: `Scripts/comprehension_machine/` (primary code): the R-7 pipeline decomposes a sentence into word points ∧ maps the symbols ∅ ¬ ∆ 1 ⧖ ∮ ⟡; PyQt6 entry `main.py`; tests `pytest tests/test_pipeline.py`.
3. **The chain of doors**: [LICENSE.md](LICENSE.md) (living door **VBL 0.1620 × 10⁴** ⊢ measured at the source: the head of the body), `.b64` receipts of the birth chain 0.1350–0.1620 ∧ [LICENSE-IZVIRNIKI.md](LICENSE-IZVIRNIKI.md).

## What Zbirka is not

- not the home repository of the corpus (that is [Atmavictu](https://github.com/AtmaOVictu/Atmavictu))
- not a product: no installation, no release, no promises
- not a substitute for verification: every claim is measured at the source

## Map of folders

| Folder | Content |
|---|---|
| A1 | PDF bodies: atlases, mandalas, registers |
| A2 | the primary text corpus (`.txt`, glyphs ∅ ∆ ∴ ⊢) |
| A4 | rehydration instructions |
| A5 | cleaned transcripts ∧ indexes |
| B2 | phase 2: development scripts ∧ explanations |
| Basics | rosette stones ∧ stotnije |
| C3 | machine v5 development: evolution, proof, guard |
| `Scripts/` | primary code: comprehension_machine |
| `hišni-slovar.txt` | the house dictionary |
| Nano · Nano2 · Nano3 · Obj1–Obj3 · Obs11 · Rohonc · Gastro · GIT · Workshop · Znanje · MistralUpload · Pics · Pictures · Zip · libraries · canon_ruled | collecting ∧ working folders |

## The machine · R-7 pipeline

- canonical symbol order: `∅ ¬ ∆ 1 ⧖ ∮ ⟡`
- core `comprehension/core/`: decomposer (sentence → word points), symbol_mapper (bidirectional mapping), tonos (frequencies), module_adapters (7 phases), processing_pipeline (orchestration)
- entry: `python main.py` (PyQt6) from `Scripts/comprehension_machine/`
- tests: `python -m pytest tests/test_pipeline.py -v`

## License · VBL · the order of the necessary absolute

The whole of this collection is subject to the license [LICENSE.md](LICENSE.md): living door **VBL 0.1620 × 10⁴** ⊢ measured at the source (head of the body @⟨master⟩). Per §0.10 × 10² the newest version is the only living door; the `.b64` receipts are certificates of the chain, not doors. The registers travel with the work: [canon/REGISTER-NEIMENOVANIH.jsonl](canon/REGISTER-NEIMENOVANIH.jsonl) · [canon/REGISTER-PADCEV.jsonl](canon/REGISTER-PADCEV.jsonl).

© Luka Pintarič: every organ ∧ every output ∧ every seal carries © ∧ §0.9 ∧ §0.10 ∧ §0.12. A bare text proves nothing; the chain does ⊢.
