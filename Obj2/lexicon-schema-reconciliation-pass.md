# LEXICON SCHEMA — RECONCILIATION PASS (measured, before schema)
LOVE CAGE / Obj2 — lexicon-schema-reconciliation-pass.md. 24. 9. 2026.
Prepared per the revised build order: "schema reconciliation before schema —
the machine wins, not the document." Every claim below was measured against
the disk this date. Baseline git commit 7453ed1 (1675 files) precedes this
document — the canon has history; this pass is its second receipt.

## SOURCES MEASURED

- Basics/stotnije-a-dosje-besedni-dosjeji.md — the Stotnija A-DOSJE catalog
- A3/OPTIKON_complete.txt (+ A4 EN/full exports) — the OPTIKON table
- Obj2 rez cuts — canon presence, per word (grep, file counts)
- SPREMLJEVALNA BESEDA v5 (canvas) — prose claims, reconciled below

## MEASURED FINDINGS

1. THE STOTNIJE CATALOG: 30 dosje entries, NOT "50+" as its own header says
   (prose slip, recorded). Every one of the 30 is structurally complete:
   Fonetični rez / Ontološki pomen / Antinoma / Sinteza / Glyph /
   Praktična uporaba. The format is uniform and machine-parseable as-is.

2. OPTIKON: exactly 22 rows (the "22 catalogued words" claim VERIFIED).
   A five-column TSV: Beseda / Zven / Smer / Čustvo / Funkcija.
   The Smer column is SPATIAL (e.g. ljubezen: "znotraj / nad / skozi";
   resnica: "nad / desno / skozi") — this is the measured source of the
   v5 canvas's "direction/coordinates" faces, and the natural seed of the
   future world's placement system.

3. HEADLINE DISCREPANCY — THE REZ IS GRAPHICMIC, NOT PHONEMIC (systemic):
   Both sources write the "Fonetični rez" as a LETTER split:
   ljubezen = l / j / u / b / e / z / e / n  (8 segments, graphemic)
   The true phonemic rez, measured by the parked lattice:
   ljubezen = [ʎ u b e z ɛ n]  (7 phonemes — lj is ONE sound, ʎ)
   CONSEQUENCE FOR THE SCHEMA: the fonetični_rez face has TWO layers:
   - source_form: the graphemic split, as the sources wrote it (preserved,
     provenance-honest)
   - phonemes: the lattice's chain (the measured rez — consumes the parked
     survivor by name: phonetic_coordinates_full.py)
   The seed stone already holds ljubezen's chain; the dosjes' rez faces
   inherit it.

4. THE WORD INVENTORY (the lexicon's seed, measured):
   - 30 dosjes (Abakus ... Intuicija) + 22 OPTIKON rows
   - 12 words in BOTH (the deep seed): Dih, Jaz, Ljubezen, Misel, Resnica,
     Smeh, Strah, Telo, Tok, Upanje, Volja, Žalost
   - 10 OPTIKON-only: drugo, glas, krivda, ne, nič, odgovor, ogenj, pot,
     tišina, zvestoba (note: ne and nič — the system's own name-words —
     have OPTIKON rows but no dosje yet: the register's own "measure me" list)
   - 18 dosje-only

5. CANON PRESENCE (Obj2 rez cuts, file counts): beseda 60, resnica 45,
   dvom 16, ljubezen 9. All candidates are present; depth differs.

## THE SCHEMA, PROPOSED (each face with its warrant)

| face | warrant (measured source) | note |
|---|---|---|
| word | Stotnije #### heading; OPTIKON col 1 | the geslo |
| phonemes | parked lattice chain | the measured rez; consumes survivor #1 |
| source_form | Stotnije "Fonetični rez"; OPTIKON Zven | graphemic split, preserved as written |
| ontoloski_pomen | dosje component 2 | |
| antinoma | dosje component 3 | |
| sinteza | dosje component 4 | |
| glyph | dosje Glyph field | reconcile with R-7/APD vocabulary — ∂ |
| smer | OPTIKON col 3 | spatial; proto-coordinates for the world |
| custvo | OPTIKON col 4 | |
| funkcija | OPTIKON col 5 | |
| provenance | build order demand | source file, entry id, ubod, ingest ts |
| ledger_id | apd_engine Ledger | every edit a ledger line; consumes survivor #2 |

## OPEN ∂ (measured against disk; none invented)

1. v5 canvas "world" face: NOT FOUND on disk. Where does it live, or is it
   born only when the world renderer exists?
2. "five measures": OPTIKON carries four (Zven/Smer/Čustvo/Funkcija). The
   fifth is either the word itself or the v5 canvas's addition — unsealed.
3. Praktična uporaba (dosjes have it; OPTIKON does not): keep as face or
   demote to annotation?
4. Glyph vocabulary vs the R-7/APD operator set (∅ ¬ ∆ 1 ⧖ ∮ ⟡ and the
   ζ′ Ω− ⇌ δ′ ς Φ family): one glyph system or two registers?

## THE FIRST SCAR — MEASURED BASIS FOR THE WORD PICK (pick is Luka's)

| candidate | dosje | OPTIKON | rez-cut files | extra |
|---|---|---|---|---|
| ljubezen | #11 ✓ | row ✓ | 9 | the seed stone's own word (love across 5 dimensions); opens with /ʎ/, the phoneme the reading's slip omitted and the reconciliation caught |
| resnica | #10 ✓ | row 1 ✓ | 45 | deepest canon presence of all candidates |
| dvom | #7 ✓ | — | 16 | epistemic load; the single-player priča's own name |
| beseda | #5 ✓ | — | 60 | the system's name; most present, least named |

All four satisfy the criteria (dosje + rez cuts). Two (ljubezen, resnica)
are in all three sources. The pick is the owner's. On "go": the lexicon
core + Stotnija parser + DISSECT tab get built on the chosen word; its
dissection becomes the workbench's first scar and first regression.
