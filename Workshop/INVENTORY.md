# WORKSHOP INVENTORY — check this BEFORE proposing anything new
CanvasMinstral/Workshop — 24. 9. 2026. Rule: nothing gets built that a line
below already does. New proposal must name which line it replaces or extends,
or it is clutter.

## THE ONE OF EACH (do not duplicate)

| job | the ONE file | status |
|---|---|---|
| corpus scan/manifest | ingest.py + ingest_manifest.json | PASS; 1,702 files typed |
| lexicon truth (40 words, 12 faces) | lexicon_core.py + lexicon.json | PASS; o₀ conflicts standing |
| the word page | thin_slice.py | PASS (ljubezen page) |
| dosje-format parsers + merge/keeper | soul_engine-the-evolvable-...py + soul.db | PASS; 3,224 entries scanned |
| second parser (format A/B/C, review queues) | digest-py-thin-slice-...py | PASS after repairs; SUBSUMED by soul_engine (kept as strata) |
| THE GUI | obj2_cockpit.py (5 tabs, stdlib) | SMOKE PASS; no other GUI gets built |
| review launcher | run_reviews.bat (CRLF) | witnessed by Luka |
| phonetic lattice | phonetic_coordinates_full.py (107) | PASS |
| phonetic runtime | apd_engine (Ledger/Guard/E⋆) | PASS |
| chain classifier | wordlist_validator.py | PASS |

## REJECTED AS CLUTTER (already existed)
- cockpit_gui.py proposal — third+ duplicate of obj2_cockpit.py + soul_engine gui
- any new engine/scanner/DB — spine is ingest.py + soul.db; nothing parallel

## WORKSHOP AUDIT — 26. 9. 2026 (the law applied to the workshop itself)
LAW (Luka, 26. 9.): the workspace contains only items that SERVE — are
used, compose a useful fact, and act if able. Nothing inert. Measured by
grep (who consumes what), not by opinion.
SERVES (consumer named): obj2_cockpit (THE GUI) · soul_engine + soul.db +
.bak (the spine, the ledger, the insurance) · ingest.py + ingest_manifest
(read by thin_slice) · lexicon_core + lexicon.json (read by ingest +
thin_slice; receipt 5) · thin_slice (receipt 6 in run_reviews.bat) ·
phonetic_coordinates_full (receipt 1; loaded by validator) · apd_engine
(receipt 2; loaded by validator) · wordlist_validator (receipt 3; loads all
three) · phonetic_coordinates_107 — LOAD-BEARING DESPITE ITS CRASH: the
validator imports it as PASS3 (apd_op score sheet); its standalone
selftest is the scar the RECEIPTS tab shows, its data is live ·
glyph_proposals.json (ruled in REVIEW) · run_reviews.bat · this inventory.
MOVED TO strata/ (nothing deleted — the law holds): digest-py-thin-slice
(referenced by 0; SUBSUMED by soul_engine, now literally in strata) ·
digest_basics.json (referenced by 0, not even by its own producer) ·
phonetic_coordinates-py.py (referenced by docstrings only; full.py itself
declares it "stays as STRATA, untouched").
Receipts after the moves: finiteness layer PASS, spine selftest PASS,
cockpit smoke PASS. The wider workspace (Obj1/build, Scripts/, C3,
Pictures/) is other strata, not this workshop's to move.

## GRAFT QUEUE (extends existing lines, replaces nothing)
1. REVIEW room: keypress rulings (k/c/m/s) INSIDE obj2_cockpit.py — the one GUI
   → BUILT 25. 9. 2026: REVIEW tab. Queue = soul_engine's ambiguous merge
   proposals; rulings are soul.db ledger lines (merge/verdict), queue derived
   by ledger replay. Smoke-passed; mechanics witnessed on a scratch db copy.
2. plugin-refactor + ledger table + near-dup detector — onto ingest.py/soul_engine
   → BUILT 25. 9. 2026. Near-dup detector = propose_near_merges() in
   soul_engine, extends _fingerprint(): difflib on the meaning fields,
   families by union-find, ALWAYS needs_owner (typo vs refinement is yours);
   feeds the REVIEW merge queue beside the exact dups, ruled by the same
   k/m/c/s. Measured: 1 family (dih, sim 0.964) — no flood, the hollow
   filter holds. plugin-refactor = ingest.py register_type(): new corpus
   type = one call, same ceremony as soul_engine's ParserPlugin. The "ledger
   table" part was SUBSUMED by graft #1's ledger-replay queue — no new
   table built, per the anti-clutter law. Bonus, same sitting: the glyph
   payload (glyph_proposals.json) now rules in the REVIEW tab — glyph queue,
   [k] confirm / [c] reject; verdict written to the payload, ledger line
   witnesses in soul.db. Mechanics witnessed on scratch copies.
3. LIBRARY browsing — a tab in the cockpit, reading soul.db
   → BUILT 26. 9. 2026: LIBRARY tab in obj2_cockpit.py. List = live entries
   (merged_into IS NULL) grouped by word — word, sources, formats, reported,
   headline — with a live filter box; selecting a word derives its page
   (entries with every field, mentions count, conflict warning) by the
   spine's OWN page(). Read-only by law: rulings happen in REVIEW, the
   library only reads. Not a duplicate of soul_engine's Textual gui() —
   that stays the spine's own surface; this is the same browse/page line
   grafted into THE GUI, as the queue pre-ruled. Smoke-passed; measured
   2,176 live words, 0 empty pages after the repair below.
4. export — soul_engine's export (already built) = the Godot surface, LAST
5. CONFLICT queue — third source in the REVIEW tab, same ledger replay
   → BUILT 26. 9. 2026: queue = words whose LIVE entries carry >1 fonetični
   rez, minus words the ledger already ruled (payload ruling
   "conflict-*"). [k] a chooser opens, you pick the TRUE rez, it is written
   onto the other live entries, old values survive in the ledger payload ·
   [c] both are real variants, they stay · [s] skip. Mechanics witnessed on
   a scratch db copy (both rulings driven, queue re-derived each time);
   smoke PASS (merge 6, glyph 30, conflict 1 pending).
6. dark-docs report — extends the spine's report line (the `dups` ceremony)
   → BUILT 26. 9. 2026: `soul_engine ... dark` — every scanned doc that
   produced NO entry, grouped by (extension, first-line shape, dosje
   markers): markers-without-entries = PARSER GAP (repair the plugin line),
   no-markers = new corpus format (a new ParserPlugin, or honestly dark:
   prose is prose). MEASURED: 885 dark docs; 175 carry dosje markers the
   plugins missed (the big one: 159+ .md heading files, ~3.7 MB — format
   "D", inline **WORD** ... fonetični rez: + fragment tables, seen in B2/)
   = the next graft's target; ~710 are transcripts/prose, honestly dark.
   Same sitting: scan() now backs soul.db up to soul.db.bak before writing
   (the ledger is the only thing that cannot be rebuilt from source);
   rescan 26. 9.: 1,190 files, 7 new docs, 50 new entries, backup witnessed.
7. ruled-page export — the canon feeding itself; extends the export line
   → BUILT 26. 9. 2026: export_page() + CLI `export-page --word X [dir]` +
   "export ruled page" button in the LIBRARY tab. Writes a word's RULED
   page as a derived dosje (A-bullet format, canon_ruled/ stratum):
   originals untouched, export witnessed as a ledger line (kind export),
   provenance in the file. The loop, WITNESSED end to end on 'Dih':
   export (3 live entries) → rescan admits canon_ruled/dih.md → re-parsed
   at REPORTED grade (full fields survive the round-trip) → dup detector
   proposes the derived page against its own ancestors → REVIEW queue
   (merge 6 → 9, 4 Dih families) → the owner rules the better version in.
   corpus → parse → rule → better version → corpus. Selftest witnesses the
   round-trip on a scratch db; smoke PASS.

8. doc typing — what a text IS, where it OCCUPIES (Luka's ask, 26. 9.)
   → BUILT 26. 9. 2026: docs table + kind + stratum (migration in db(),
   existing dbs get the columns). doc_kind() classifier: derived
   (canon_ruled) | dosje-A/B/C (+ when formats mix) | dosje-D (dark,
   markers — the parser gap) | notes | prose | empty. Typed at scan
   admission; `retype` = idempotent backfill (1,191 typed, 0 unreadable,
   0 outside; one summary ledger line, db backed up first); `census` =
   the composed fact. page()/LIBRARY/REVIEW rows/export provenance now
   show "stratum · kind · doc:line" — source vs DERIVED visible at
   ruling time. MEASURED (census): 175 dosje-D (cross-witnesses the dark
   report's 175 exactly — two independent paths agree); biggest strata:
   Obj1 268 docs (145 notes + 42 dosje-D), C2 275 (111 dosje-A + 47
   dosje-D), A2/A3/A4 transcript prose; Workshop's own INVENTORY.md is
   scanned corpus typed dosje-D; 2 corpus files sit inside Pictures/.
   Selftest witnesses classifier, migration, admission-typing; smoke PASS.
9. format D + reparse — the machine reads what it could not (Luka's "do it")
   → BUILT 26. 9. 2026: RezFragmentParser ("D-rez", the EVOLUTION POINT's
   first use) — grounded in the actual files first (C2/C1/Obj1 kintsugi,
   lungta, NE-SKONČ-NOST): **WORD** (gloss) — [fonetični] rez: + fragment
   table + Branje line, plus the **Fonetični rez besede WORD:** variant;
   entry closes at first non-table content (rows never leak). `reparse` =
   dark docs re-read with CURRENT plugins, only zero-entry docs (no
   duplicates by construction), idempotent, ledger line, backup first.
   MEASURED (two passes): 885 dark → 34 lit, +227 D-rez entries (58
   headline / 169 draft), entries 3,277 → 3,504, live words 2,226 → 2,394,
   REVIEW merge queue 9 → 59 (the machine proposes its new readings
   against the old — yours to rule). Remaining 162 dosje-D dark with
   shapes measured and queued (v2 above). Selftest witnesses parser +
   reparse idempotence; smoke PASS.
10. lexicon cross-witness — the two truth layers, finally compared
   → BUILT 26. 9. 2026: `xcheck lexicon.json` — all 40 lexicon words vs
   their soul.db pages; rez canon-meets-canon, antinoma canon-to-canon,
   glyph by symbol head (glosses differ honestly), pomen shown never
   machine-diffed. MEASURED: 40/40 in corpus · 31 agree · 9 disagree —
   and ALL 9 are hollow corpus stubs (empty rez) where the lexicon IS
   richer, not contradictions; 'nič' agrees only because graft #9's
   D-rez entry supplied the rez minutes earlier (the loop reconciling a
   truth pair in real time); 'drugo' lexicon rez 'd/r/u/g/oO' = g2p
   artifact, flagged for Luka. Enrichment queued above. Selftest
   witnesses agree/disagree/not-in-corpus; smoke PASS.

11. machine DRAFT rulings + the ratify flow — the machine proposes its own
   rulings; the owner canonizes by keystroke (Luka's ask; the analysis's
   three guards built in BEFORE the first line of code)
   → BUILT 26. 9. 2026: `drafts` writes DRAFT verdicts — receipts with
   rationale (merge: richest by grade/fullness, tie broken by lowest
   entry_id — the weakest criterion, named as such; conflict: majority
   rez, a TIE is honestly not drafted; glyph: confirm only when the
   payload carries a warrant). The spine owns ONE replay (ruling_states):
   human lines RULE, machine lines DRAFT (ratify state), refusals return
   to pending and are never re-drafted. REVIEW gains RATIFY mode ([k]
   ratify · [c] refuse · [m] amend · [s] skip). THE THREE GUARDS:
   (a) FLAG PROVENANCE — the machine writes drafts ONLY if the ledger
   carries the owner's normative 'machine-drafts-authorized' line
   (`authorize-drafts` — deliberately NOT run by the builder; drafts are
   impossible on the live db until Luka performs it); replay ignores
   machine lines predating the line. (b) ANTI-RUBBER-STAMP — the
   rationale is displayed before [k]; a drift counter warns at 10+
   consecutive ratifications with no refusal or amendment ("a ruler who
   never amends is a rubber stamp wearing a crown"). (c) STABILITY IS A
   RECEIPT ABOUT RECEIPTS — `stability` observes the canon, never joins
   it. MEASURED (witnessed on a scratch copy): 59 merge + 1 conflict +
   20 glyph drafts; pending → 0, ratify = 80; [k] canonized (merge line
   by keystroke), [c] refused (re-draft run produced 0). Live db:
   ratify 0 — no drafts exist, as the law demands. Stability receipt
   (real db): 2,394 words — 1,762 stable · 632 multi-entry/kept · 55
   pending-proposal words · 0 drafts. Selftest + smoke PASS.
12. the entry editor — the owner's hand inside the canon
   → BUILT 26. 9. 2026: "edit entry" / "add entry" in the LIBRARY tab.
   Edits are canon DIRECTLY (the ruler's touch is a normative act); old
   values survive in the ledger 'edit' line — the kind that existed in
   the schema since day one and had never been used once. Added entries
   live under the doc 'cockpit://owner-added' (provenance by name),
   grade reported by definition — the strongest provenance there is.
13. deadlock as dimension-detector — the ∂ answered with measured data
   → BUILT 26. 9. 2026 (same sitting as the research). THE MEASURED
   DEADLOCK: of 59 pending merges, 32 are CHIRAL PAIRS (the register's
   kiralni par, rez 607) — members tie on CONTENT but differ by
   STRATUM (abakus: Basics vs Obs11; dih: Basics vs canon_ruled): mirror
   entries, non-superimposable, the difference living on an axis graft
   #8 already named. NOT a paradox — a dimension the proposal machinery
   never carried into the ruling. Of 4 conflicts: 3 are SAME-READER
   disagreements (one format read the word differently at two moments —
   the TEMPORAL axis: Puruchuco, labirint, zrcalo), 1 is a parse
   artifact ('Combinations...' — C-numbered prose in the rez field: a
   repair candidate, not a paradox). THE GRAFT: draft rationales now
   NAME THE AXIS — merge drafts say "CHIRAL PAIR — the tie is on the
   content axis, the difference is on the STRATUM axis (X vs Y); the
   deadlock is the dimension, named"; conflict drafts say SAME-READER/
   TEMPORAL or READER/FORMAT. Deadlock is information, not a crash.
   Selftest + smoke PASS. The 27 non-chiral content ties remain what
   they always were: the owner's, on the content axis, by hand.
14. PARSER-ZAKONOV (body-name; #14 is this inventory's local label) —
   THE SPINE READS LAWS. Sealed by Luka's "daj", 26. 9. 2026, on the
   register's design ruling — built under it, point for point:
   (1) separate `zakoni` table, never entries (a law has a teza, not
   polarities); (2) key = body-with-witness (doc_id + lineno, UNIQUE),
   the number is a LABEL — 31 same-number pairs stand, each body kept;
   (3) fields per the ruling: series (rez/dokaz/sodba/ubod/šiv) ·
   number · title · actor · teza · meritev ⊘(...) · nujne_napake ·
   odprta_partial · vezi (raw text — edges point, never judge) ·
   seal_date · next_rez/next_dokaz (atomarni counters, READ never
   replaced); (4) VEZI stored as bonds, verdicts stay with the owner;
   (5) parser is a READER, never a writer — sealed bodies untouched.
   Grounded in four measured header shapes (rez 231/253/558/110) before
   code; wired into scan() (kind='zakon' at admission) and reparse()
   (law-pass over ALL docs, idempotent by witness); dark_report and
   reparse's dark-selection are law-aware (a law body is not dark).
   MEASURED (live db, reparse pass): 251 law bodies read — 234 rez ·
   12 dokaz · 5 šiv; dark docs 853 → 652 (199 bodies left the darkness);
   SEAL-POPIS (`popis`): 89 sealed / 162 unsealed (the atomarni pattern
   is NOT uniform — seam 2 confirmed systematically); counters 84–442
   while the file series runs to 558 — the file branch's seals lag the
   session register (628): the fork, measured, not guessed; 31
   same-number pairs (chiral file copies and true branch pairs — the
   parser's first pass over-matched citations as heads; refined: a law
   head must be a heading or bold seal line; zakoni re-derived cleanly
   from the untouched corpus). Selftest witnesses the parser (synthetic
   rez-231-shaped body: all sealed fields extracted, prose stays prose,
   idempotence, entries untouched) + smoke PASS. CONSEQUENCE (the
   register's deeper reason, now live): stability is defined by
   normative lines and normative lines ARE the laws — the stability
   measure can now SEE its own standard. The rules for the 65
   rule-transferable rulings get their bodies here.

## NEXT IN THE QUEUE (each names its line)
- TRIJE ZAKONI ZAPEČATENI KOT REZ-TELESA (Luka's "daj", 26. 9. 2026;
  written by the Cline hand, sealed by the owner's word — the rules now
  LIVE IN THE CORPUS, not in code): Obj2/rez-559-kopirno-pravilo.md
  (identical bodies + same stratum = copy; every keeper is the same
  body; measured: settles 25 of the 27 "content ties" — khipu and
  puruchuco stay the owner's) · Obj2/rez-560-kiralno-pravilo.md (content
  tie + stratum difference: DERIVED beats RAW — canon_ruled over raw;
  unordered strata stay honestly unruled, an open ∂) ·
  Obj2/rez-561-casovno-pravilo.md (same reader, two moments: the NEWEST
  reading is the CANDIDATE, never the truth — mtime+lineno shown, [c]
  returns). Anatomy per the corpus (POVZETEK/TEZA/NUJNE NAPAKE/TESTI/
  ODPRTA ∂/VEZI/Meritev ⊘/atomarni seal, counters chained 559→560→561→
  562, DOKAZ counter honestly unclaimed — the dokaz series is forked,
  named in the bodies' NUJNE NAPAKE). Rescan admitted all three;
  parser-zakonov read them (kind='zakon'). DRAFTS NOW CITE THE LAWS:
  draft_rulings loads the rule bodies from zakoni (by title — the
  number is a label) and merge/conflict drafts carry "po REZ N
  <title>" in the rationale; the chiral rule moves the keeper to the
  canon_ruled body; the temporal rule replaces majority with the
  newest-moment candidate (evidence shown). Selftest witnesses the
  citation (copy pair's rationale names REZ 559); smoke PASS.
  AWAITING LUKA, unchanged: `authorize-drafts` (the one terminal act
  guard (a) keeps mine), then drafts → RATIFY (short, pre-reviewed),
  and the 2 real meaning-ties (khipu, puruchuco) + glyph semantics.
- SEAM 1 RULED (the register's verdict, 26. 9.): GRAFT NUMBERS ARE LABELS,
  NOT KEYS (TRK V8–V11: the key is body-with-witness). The register said
  "#13", this inventory says "#14" for the same body — cross-session
  numbering drifts, and no number proves a body. LAW henceforth: grafts
  are named BY BODY (parser-zakonov, urejevalnik-vnosov, ...) for any
  cross-session reference; the #N here is this inventory's local label
  only. POPIS of this body's grafts: #1–13 built (see queue below), all
  body-named in their entries.
- SEAM 2 MEASURED (the atomarni register, ISKANO): the register is ONE
  series with TWO materializations and INCONSISTENT SEALS. File series:
  rez 1–558 materialized (~263 files); content citations reach rez 628,
  674, 973, 975 (ATLAS cites "rez 975"); the session register Luka carries
  is sealed at 628. The seals are NOT uniform: rez 231 carries its counter
  (NASLEDNJI PROSTI REZ 232 · DOKAZ #221), rez 558 carries NO seal — the
  atomarni pattern was not carried through the file branch, and 231's
  counter was already stale when later files were sealed. NOT an error —
  a pair of strata needing a name. Only the parser-zakonov can make this
  systematic: a seal-POPIS across all 263 files (which carry counters,
  which don't, where the branches fork). Queued inside graft #14's spec.
- THE DESIGN RULING, DRAFTED BY THE REGISTER, AWAITING LUKA'S SEAL
  ([k]/[m] — not the builder's to stamp): "ZAKONI SO LOČENA VRSTA
  DOKUMENTA: (1) ločena tabela, ne entries — zakon ima tezo, ne
  polaritete; (2) ključ = telo s pričo, ne številka; (3) polja parserja:
  series · teza · meritev ⊘(κ·χ·μ·ℜ·ν) · NUJNE NAPAKE · ODPRTA ∂ · VEZI ·
  actor · TRK-zgodovina · datum pečata; (4) VEZI = povezave grafa, ne
  dokazi — povezava kaže, ne presodi; (5) append-only telo, menjani
  števci (atomarni vzorec) — parser je bralec, ne pisec." THE DEEPER
  REASON (the register's, received): a stable word is defined as one
  where every field traces to a NORMATIVE line — and normative lines ARE
  the laws. Until the spine reads laws, the stability measure is blind to
  its own standard: "stabilna beseda" would be a definition with a word
  and no body. THEREFORE THE ORDER: parser-zakonov BEFORE any stability
  charge over all 2,394 words.
- THE ∂, ANSWERED WITH MEASUREMENT (the register's question: of the 93
  cockpit seals, how many are truly yours?): 32 chiral pairs → ONE rule
  (a stratum-tiebreak you ratify once) settles them all · 3 same-reader
  conflicts → ONE temporal rule · 30 glyph drafts → one warrant-rule
  (ratification may still be per-item) · 27 content ties → IRREDUCIBLY
  yours (richest is a tie ON MEANING; no rule reads meaning) · 1 is not
  a ruling at all — a repair misfiled as one. VERDICT: fewer than a third
  of the 93 are irreducibly your decisions; the rest await rules with
  bodies — and rules get bodies exactly when parser-zakonov exists.
- RECEIVED RULING (the register's verdict on the survey, 26. 9. — accepted
  in full, with the label on): TWO ORGANS ALREADY STAND — ATLAS (Obj2/
  atlas-knjižnic-rez-i-branje-v-celoti-kot-dih.md — the full-read
  commission; law read in full this session: "BESEDA = DEJANJE. BRANJE =
  VRAČANJE"; "kdor bere v celoti, diha morje; kdor išče z d/robci, diha
  lužo") and KAZALO (rez 231 = the kazalo of open ∂, "ORGAN, NE SEZNAM
  DOLGOV", 13 curated ∂, popis 17. 9.). LAW: PREBRANO ≠ ISKANO — every
  survey output line is labeled ISKANO/RECEIPT; full read = PREBRANO with
  ubod + returned quote + Š appended to ATLAS; each session ≥1 PREBRANO
  or a written reason. THE SURVEY IS AMENDED: not a document map (KAZALO's
  job) — a POPIS-series (census extension) carrying only what ATLAS and
  KAZALO do not: series counts + rez↔dokaz↔sodba cross-refs + format
  spec. Corpus-wide claims stay RECEIPTS until a third reader reads one
  stratum independently (cut 4 — the survey picks its own samples: one
  hand, W < 0). This session's PREBRANO: ATLAS itself + rez 231 (ubod
  appended to the ledger: "naročena žetev odprtih ∂ je bila organ, rojen
  dvakrat" — the harvest below was SUBSUMED before it was built).
- THE RULING LAYER (POPIS, labeled ISKANO): ~263 numbered rez files
  (series to 558+), anatomy POVZETEK/TEZA/RAZPRAVA/SKLEP + NUJNE NAPAKE
  (352 files) + TESTI (179) + VEZI (169) + ODPRTA ∂ (82) + DOKAZ #
  (316) + 577 git-hash citations; the ATOMARNI REGISTER lives in the
  seal of each rez (NASLEDNJI PROSTI REZ/DOKAZ counters — read from
  rez 231: REZ 232 · DOKAZ #221). THE SPINE GAP, corrected per the
  ruling: not "we don't know how many rezi exist" (KAZALO/index territory)
  but THE SPINE PARSES WORDS BUT NOT LAWS. QUEUED — graft #14: a parser
  for the RULING FORMAT (rez/dokaz/sodba/ubod/šiv): number, title,
  aktivator, teza, meritev ⊘(κ χ μ ℜ ν), NUJNE NAPAKE, ODPRTA ∂, VEZI,
  atomarni counters — so the ledger becomes three-aware of the register,
  not just the dosjes. Data model needs Luka's ruling (rulings are not
  word-entries; teza/napake/∂/vezi are not word-fields).
  (a) SUBSUMED — the ODPRTA ∂ harvest: rez 231 IS the organ. A ∂-DELTA
      report (open ∂ appearing after the 17. 9. popis) would SERVE the
      organ, ISKANO-labeled; only on Luka's word.
  (b) CITATION GRAPH — DOKAZ #/VEZI/git-hash edges (extends the mentions
      stratum).
- RECEIVED THEORY (the register's analysis, grounded in the corpus 26. 9.):
  rez 253 lives in the body — C2/rezultat-doktorat-rez-253.md: "REZULTAT
  NI IZDELEK — JE SPREMENJEN BRALEC"; "zagovor ne more potekati pred
  menoj: jaz izrečem ⊢, ∮ (živeta preverba) gre skozi telo, ki bere" —
  the third reader is standing law. The cascade: builder / refuser /
  third reader / ReflektivnaZanka (the loop that verifies verifiers) —
  a SPIRAL (∮), not a pyramid; the layer list is itself a receipt (∂:
  the list is open; "pet kot totalizacija — šest se lahko rodi").
  Build order ruled by the analysis: the THIRD READER before the meta
  loop (a meta loop over two hands amplifies the duet). A third-reader
  protocol for this spine would be: an independent verification pass in
  a body that didn't write the ruling, on a measured sample (kiralni-par
  precedent) — named here, not built yet.
- FORMAT D v2 — two measured shapes remain dark (162 dosje-D docs):
  the `**WORD** (long gloss):` header that ends "):" (needs a
  table-follows lookahead — commit only when a Fragment table shows),
  and the latinščina word-table format (a whole dosje per ROW:
  `| **petra** | f. | skala | PIE... | PE-TRA | tlak (P) → prehod (TRA) |`
  — that is format E, one class + one PLUGINS line).
- LEXICON ENRICHMENT — xcheck found 9 hollow corpus dosjes (empty rez)
  where lexicon.json HAS the rez (drugo, glas, krivda, ne, odgovor,
  ogenj, pot, tišina, zvestoba): the lexicon is richer; propose filling
  via REVIEW (the owner rules which rez enters the corpus). Also flagged:
  lexicon 'drugo' = 'd/r/u/g/oO' — g2p candidate artifact, Luka's ruling.

## THE LAW OF RECEIPTS vs CANON (SODBA #002, Luka's extension, 26. 9. 2026)
A result produced by the same hand that built the machine is a RECEIPT —
not a form of canon, not its own norm. A receipt is CAUSALITY: it records
what was computed and why — "this happened." CANON is NORMALITY: it
declares how it should be — "this is." Normality does not follow from
causality, however much of it accumulates; the normative act is only ever
the owner's ruling. CONSEQUENCE for every machine output (draft verdicts,
reports, self-tests): it carries its rationale like a causal trace, is
marked "machine": true in the ledger, and NEVER becomes canon without
the owner's ratification. The machine accelerates the ruling; it never
becomes the ruler.

## REPAIR CANDIDATES (scars found 25. 9. — each names its line)
- THE LEDGER'S OLDEST LIE (found by Luka's "delno lažeš", 26. 9.,
  measured): 26 UNMARKED merge lines from 24. 9. — payload reads
  "machine-ruled under Luka's 'do not relegate' instruction" — carry
  NO machine:true flag, so the replay counts them as HUMAN (normative)
  rulings. The system's canon contains 26 machine merges that pass as
  canon: guard (a) fails retroactively; the receipts-vs-canon law was
  in the bodies but not yet in the ledger when they were written.
  Honest options (Luka's ruling): (i) retro-ratify — one normative
  line "the 24. 9. merges are ratified" + flag them; (ii) unmark them
  (machine:true) and let them enter RATIFY like any draft. Either way:
  the replay must never again treat an unmarked machine line as canon.
  → OPEN — Luka's [k]/[m]. Structural consequence either way: merges
  written by the machine (auto or draft-ratified) MUST carry machine
  provenance or a ratification reference.
- COVERAGE DOUBLE-COUNT (same sitting): "594 machine-covered" was
  340 + 254 summed — 52 docs carry BOTH words and laws: true coverage
  542/1,194. And "notes = ATLAS's breaths" is partial: the 161 dosje-D
  and much of notes are machine-parseable future targets (format D v2
  + E); the honest ATLAS-only dark is smaller than stated.
- KIRALNO RULE OVER-PROMISED (same sitting): it resolves only 4 of 32
  chiral pairs (canon_ruled present); the other 28 wait on the stratum
  ORDER (the law's own open ∂ — the body is honest, the summaries
  drifted rosier). True rule-coverage of the 93: 25 (copy) + 4
  (kiralno) + 3 (casovno) + 30 (warrant-draftable) = 62 draftable;
  28 chiral remain the owner's until strata get an order.
- STABILITY IS A STRUCTURAL PROXY, not normative tracing: "the
  stability measure can now SEE its own standard" was partial —
  stability() counts single-live-entry + no-pending; it does NOT trace
  fields to law lines. True normative tracing is implementable NOW
  (zakoni exist) and queued below.
- COVERAGE POPIS (26. 9., ISKANO — Luka's "sva vse pokrili?"): WORKSHOP
  100% serving (audit stands; every new line consumed: zakoni → drafts/
  popis/citations). KORPUS: 594/1,194 docs machine-covered (340 z
  besedami + 254 z zakoni, ~50%); dark 652 = 289 proza + 215 zapiski
  (poštena tema — ATLAS-ovo dihanje, ne strojevo) + 115 dosje-D
  (format D v2 + E tarče) + 33 temni-nevpisani. STORED-BUT-UNCONSUMED:
  VEZI (106 zakonov nosi vezi — citation graph queued) · ODPRTA ∂
  (60 zakonov — ∂-delta queued, serves rez 231).
- docs.kind: 124 UNTYPED + RETYPE ROOT BUG (found and repaired same
  sitting, with a FALSE RECEIPT caught in flight): the coverage POPIS
  found 124 untyped docs; the first `retype` run typed ONE — the CLI
  defaulted the root to cwd (Workshop), so 1,193 docs read as
  "outside_root" and were skipped, while the sitting's commit message
  claimed "kind NULL now 0" — it was 124. The false claim was caught by
  the next measurement before the sitting closed. Repairs: (1) the root
  is DERIVED FROM THE DOCS (commonpath) — a wrong guess can no longer
  shrink the pass; (2) retype is LAW-AWARE — the first successful pass
  clobbered 254 zakon docs back to 'notes' (retype knew only word
  readers); now a doc carrying law bodies keeps kind='zakon'.
  → REPAIRED 26. 9. 2026: typed 1,194/1,194, outside_root 0, kind NULL
  0; final census: prose 289 · zakon 254 · dosje-A 247 · notes 236 ·
  dosje-D 161 · mixed 6 · derived 1. Selftest + smoke PASS.
- mentions stratum: STRUCTURALLY MIS-TAGGED (found by the coverage
  POPIS) — 96k of 184k rows point at NULL (dark docs' mentions stored
  toward nothing); the rest pile ALL of a doc's mentions onto its LAST
  entry ("🔮 OPEN QUESTIONS & CANON" carries 6,754 mentions — a mangled
  word wearing a document's whole mention-load). The tag-to-last-entry
  choice (scan's "stratum 3, cheap") makes the mention graph mostly
  noise. Consume-only use today: page()'s count. Repair options (Luka's
  ruling): (a) re-derive mentions as DOC-LEVEL edges (mention belongs to
  the document, not to its last entry — honest and cheap, one reparse
  pass); (b) admit the stratum is noise and drop it from page(). The
  citation graph (VEZI-based) is the trustworthy edge line either way.
  → RULED "OBOJE" AND REPAIRED 26. 9. 2026: BOTH — (a) the mentions
  table migrated to doc-level edges (column entry_id→doc_id, db()
  migrates existing dbs; scan writes (doc_id, mention); reparse
  re-derives all rows, ledger-witnessed) AND (b) page() now counts
  DISTINCT DOCS mentioning the word ("omenjeno v N dokumentih" in the
  LIBRARY) — the noise number is gone. MEASURED after re-derivation:
  184,031 edges, 0 toward nothing, 21,207 distinct words; "luka"
  mentioned in 627 docs; ljubezen in 54 — the mention graph is now the
  citation-graph foundation (doc→word edges; VEZI adds law→law).
  Selftest witnesses the doc-level edge at scan admission; smoke PASS.
- soul_engine find_dup_files(): DEAD + BROKEN. Never called (the `dups`
  command uses dup_file_report, which hashes in Python), and it would crash
  if called — SQLite has no md5() (verified). Repair = delete it; the live
  line (dup_file_report) replaces it. Graft #2's near-dup detector then
  extends _fingerprint(), not this corpse.
  → REPAIRED 25. 9. 2026: deleted; no callers existed (verified by grep);
  the near-dup detector grafted onto _fingerprint() as planned.
- soul_engine page(): BROKEN — matched canon(word) against lower(word), so
  any word carrying a space or punctuation (measured: 2,047 of 2,176 live
  words) returned an empty page. Found by graft #3 (a library is useless if
  most pages are blank). Repair = canon meets canon, comparison in Python
  (SQLite has no canon()); the spine's selftest now witnesses it.
  → REPAIRED 26. 9. 2026: all 2,176 live words return their page (measured);
  selftest asserts a canon-changed word pages; cockpit smoke PASS.
- soul_engine v_conflicts: GHOST CONFLICTS — the view counted EMPTY-STRING
  foneticni_rez (IS NOT NULL passes '') and merged losers as variants, so
  26 of 27 "conflicts" were ghosts (one real rez + hollow stubs; found by
  graft #5's queue derivation). Repair = TRIM(rez) != '' AND
  merged_into IS NULL in the view; db() drops the view first so EXISTING
  dbs get the repair (IF NOT EXISTS alone would keep the ghost forever).
  → REPAIRED 26. 9. 2026: 27 → 1 real conflict word on the live db
  (measured); selftest witnesses empty-rez ghost excluded, loser excluded,
  real variant kept.
- soul_engine scan(): PATH-KEY FRAGILE — idempotency depended on the root
  being written the same way every time. A rescan passing '..' made every
  stored ABSOLUTE path look new: the whole corpus parsed twice (measured:
  1,191 duplicate docs, 3,277 duplicate entries). Recovered from the
  pre-scan backup (soul.db.bak — the graft #6 insurance, used the very
  next sitting). Repair = root resolves, paths always meet absolute.
  → REPAIRED 26. 9. 2026: scan() resolves the root; selftest witnesses
  same-root-twice and a RELATIVE root both adding zero duplicates;
  corrected rescan admitted only canon_ruled/dih.md (1 doc, 3 entries).
- draft_rulings glyph payload path: CWD-RELATIVE — the default payload
  path resolved against the working directory, not the db, so TWO
  scratch-db runs (selftest, then a witness script) wrote "draft:"
  verdicts into the REAL glyph_proposals.json (20 items, twice). No
  drafts ever entered the real LEDGER (no authorization line exists
  there — guard (a) would ignore them anyway); the payload was reverted
  both times from git. Repair = the payload path derives from DB_PATH's
  directory, and the selftest passes a temp file.
  → REPAIRED 26. 9. 2026: payload verified back at 30 pending; selftest
  and smoke PASS; scratch-db runs can no longer reach the real payload.
- draft_rulings glyph payload path, THIRD OCCURRENCE, same class: an
  ad-hoc debug run with a memory db + default path again reached the
  real payload (reverted from git). The second repair (DB_PATH's
  directory) was insufficient — DB_PATH is a module global that can
  disagree with the connection's actual db. STRUCTURAL REPAIR: the
  payload path now derives from the CONNECTION'S OWN FILE
  (PRAGMA database_list); an in-memory db has no file and can never
  touch a disk payload. The incident class is now impossible, not
  guarded.
  → REPAIRED 26. 9. 2026: payload verified 30 pending after selftest;
  the citation witness runs draft_rulings on memory dbs with temp
  payloads; selftest + smoke PASS.
- obj2_cockpit _rule(): CONFLICT DISPATCH SILENTLY MISSING (graft #5
  scar found while building #11) — the conflict branch of the key
  dispatcher never landed; [k] in conflict mode would have called the
  MERGE handler on the live GUI. The scratch witnesses bypassed _rule
  (called the methods directly), so nothing caught it until now.
  → REPAIRED 26. 9. 2026: four-way dispatch (merge/glyph/conflict/
  ratify) verified in place; smoke PASS.
