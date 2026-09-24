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
| THE GUI | obj2_cockpit.py (4 tabs, stdlib) | SMOKE PASS; no other GUI gets built |
| review launcher | run_reviews.bat (CRLF) | witnessed by Luka |
| phonetic lattice | phonetic_coordinates_full.py (107) | PASS |
| phonetic runtime | apd_engine (Ledger/Guard/E⋆) | PASS |
| chain classifier | wordlist_validator.py | PASS |

## REJECTED AS CLUTTER (already existed)
- cockpit_gui.py proposal — third+ duplicate of obj2_cockpit.py + soul_engine gui
- any new engine/scanner/DB — spine is ingest.py + soul.db; nothing parallel

## GRAFT QUEUE (extends existing lines, replaces nothing)
1. REVIEW room: keypress rulings (k/c/m/s) INSIDE obj2_cockpit.py — the one GUI
2. plugin-refactor + ledger table + near-dup detector — onto ingest.py/soul_engine
3. LIBRARY browsing — a tab in the cockpit, reading soul.db
4. export — soul_engine's export (already built) = the Godot surface, LAST
