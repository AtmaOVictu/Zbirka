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

## NEXT IN THE QUEUE (each names its line)
- THE RULING LAYER (survey 26. 9., Luka's "what else besides all this"):
  the corpus contains a SECOND body the spine has never modeled — ~263
  numbered rez files (series runs to 558+; C2 119, Obj1 104, C1 24...),
  each with anatomy POVZETEK/TEZA/RAZPRAVA/SKLEP + NUJNE NAPAKE (352 files
  self-name their errors) + TESTI (179) + VEZI bonds (169) + ODPRTA ∂
  (82 files carry the OPEN QUESTION) + DOKAZ # cross-refs (316) + 577
  git-commit-shaped evidence citations. FINDING: the inventory's format
  is ISOMORPHIC to the rez anatomy — NEXT QUEUE ≈ ODPRTA ∂, REPAIR
  CANDIDATES ≈ NUJNE NAPAKE, receipts ≈ TESTI, provenance ≈ VEZI. The
  workshop re-derived the corpus's own law. QUEUED, needs Luka's ruling
  on the data model first:
  (a) FORMAT R — the ruling body as a corpus type (register_type()
      ceremony exists; entries-table vs a rulings model is a design
      ruling: rez fields are teza/napake/odprta∂/vezi, not word-fields);
  (b) CITATION GRAPH — DOKAZ #/VEZI/git-hash edges (extends the
      mentions stratum);
  (c) ODPRTA ∂ HARVEST — collect all 82 open questions into one report:
      the corpus's own NEXT IN THE QUEUE, readable in one place. Cheapest
      first move; rez 253's law demands a body can FIND the open ∂s.
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
- obj2_cockpit _rule(): CONFLICT DISPATCH SILENTLY MISSING (graft #5
  scar found while building #11) — the conflict branch of the key
  dispatcher never landed; [k] in conflict mode would have called the
  MERGE handler on the live GUI. The scratch witnesses bypassed _rule
  (called the methods directly), so nothing caught it until now.
  → REPAIRED 26. 9. 2026: four-way dispatch (merge/glyph/conflict/
  ratify) verified in place; smoke PASS.
