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

## NEXT IN THE QUEUE (each names its line)
- FORMAT D plugin — a new ParserPlugin (one class + one PLUGINS line) for
  the 175 marker-carrying dark docs. Until then the library misses ~3.7 MB
  of real dosje content. NOTE: dark docs are already scanned, so scan()
  skips them — the plugin needs the reparse line below with it.
- REPARSE — a spine command to parse DARK docs with the CURRENT plugins
  (scan() only admits new files; the already-scanned dark corpus stays
  dark forever without this). Extends scan()'s line, ledger-witnessed.

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
