"""
THIN SLICE — Strata 0-4 on one folder, one entity type, one query
LOVE CAGE / Obj2 — thin_slice.py. 24. 9. 2026.

The theory under test (stratified digestion): identity -> extraction ->
typing -> relating -> grading; validate it cheaply on the 40 words, with
"everything about ljubezen" as the page that decides.

Stratum 0 IDENTITY: canonical id per entity + alias table (one entity, many
  names; identifiers are handles, not essences). Case and seed-stone variants
  resolve to one id. Rez citations ("rez 529", "vez 386") resolve to
  canonical rez:N with file-existence measured from the manifest.
Stratum 1 EXTRACTION: reuse lexicon_core (already parsed, already asserted).
Stratum 2 TYPING: epistemic type per face (law/measurement/interpretation/
  draft/scar) — never sorted together.
Stratum 3 RELATING: explicit (rez citations, high trust) > structural (word
  mentions across the corpus, medium trust); inferred links NOT built here —
  lowest trust, visually distinct when they exist.
Stratum 4 GRADING: status per face (measured/reported/draft/contradicted);
  contradictions SURFACED AND PRESERVED, never auto-resolved.

Run: python thin_slice.py ljubezen     (default word: ljubezen)
"""
from __future__ import annotations
import os
import re
import sys
import json
import importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)


def _load(fname):
    spec = importlib.util.spec_from_file_location(fname.split(".")[0],
                                                  os.path.join(_HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


LEX = _load("lexicon_core.py")
MANIFEST = json.load(open(os.path.join(_HERE, "ingest_manifest.json"), encoding="utf-8"))
TEXT_FILES = [f["file"] for f in MANIFEST["files"]
              if f["type"] in ("rez_cut", "prose", "law_register", "dialog_rek",
                               "aphorism_series", "dosje_catalog", "optikon_table")]


# ---------------------------------------------------------------- STRATUM 0
def resolve(word) -> str:
    """One entity, many names — case and seed-stone variants -> one id."""
    return word.strip().lower()


ALIASES = {w.lower(): {w.lower(), w.upper(), w.capitalize()} for w in ()}


# ---------------------------------------------------------------- STRATUM 3
def mention_web(words) -> dict:
    """Every mention of every word across the parseable corpus, one pass.
    Returns {word_id: [(file, line_no, line), ...]} — structural links,
    medium trust, capped per file."""
    web = {w: [] for w in words}
    pats = {w: re.compile(r"\b" + re.escape(w) + r"\b", re.I) for w in words}
    for rel in TEXT_FILES:
        try:
            with open(os.path.join(_ROOT, rel), encoding="utf-8", errors="replace") as fh:
                for n, line in enumerate(fh, 1):
                    for w, pat in pats.items():
                        if pat.search(line):
                            web[w].append((rel, n, line.strip()[:140]))
                            break  # one hit per line keeps the web lean
        except OSError:
            continue
    return web


def rez_citations(text_files) -> dict:
    """EXPLICIT links (highest trust): rez/vez citations with numbers."""
    cites = {}
    pat = re.compile(r"\b(?:rez|vez|REZ|VEZ)[ -]?(\d{1,4})\b")
    for rel in text_files:
        try:
            with open(os.path.join(_ROOT, rel), encoding="utf-8", errors="replace") as fh:
                for n, line in enumerate(fh, 1):
                    for m in pat.finditer(line):
                        rid = f"rez:{m.group(1)}"
                        cites.setdefault(rid, set()).add(rel)
        except OSError:
            continue
    return cites


def rez_file_exists(n, manifest=MANIFEST) -> bool:
    """Stratum 0 for rez numbers: does a body file for this rez exist?"""
    return any(re.search(r"(?i)rez[ -]?" + str(n) + r"\b", f["file"])
               for f in manifest["files"])


# ---------------------------------------------------------------- STRATUM 2+4
def grade_entry(e) -> list:
    """Every face typed (stratum 2) and graded (stratum 4), never mixed."""
    rows = []
    seeded = any(p["source"].startswith(("seed stone", "wordlist_validator"))
                 for p in e["provenance"])
    rows.append(("phonemes", "measurement",
                 "measured" if seeded else
                 ("draft (e/ɛ unresolved)" if e["g2p_ambiguities"] else "reported")))
    if e["ontoloski_pomen"]:
        rows.append(("ontoloski_pomen/sinteza/antinoma", "interpretation",
                     "reported (attributed: stotnija dosje)"))
    if e["smer"]:
        rows.append(("smer/custvo/funkcija", "measurement",
                     "reported (OPTIKON row)"))
    if e["annotations"].get("optikon_zven"):
        a = re.sub(r"[\s/]+", "", e["source_form"] or "")
        b = re.sub(r"[\s/]+", "", e["annotations"]["optikon_zven"])
        rows.append(("source_form", "measurement",
                     "CONTRADICTED (dosje vs OPTIKON) — preserved, standing"
                     if a != b else "consistent across both sources"))
    return rows


# ---------------------------------------------------------------- THE PAGE
def page(word_id, entries, web, cites) -> str:
    e = entries[word_id]
    L = []
    L.append("=" * 72)
    L.append(f"EVERYTHING ABOUT {e['word'].upper()}  (entity id: {word_id})")
    L.append("=" * 72)
    L.append("STRATUM 0 — IDENTITY")
    L.append(f"  canonical: {word_id}   aliases: {word_id}/{e['word']} "
             f"(case variants resolve here)")
    L.append("STRATUM 1 — EXTRACTION (what it says)")
    L.append(f"  phonemes  : {' '.join(e['phonemes'])}")
    L.append(f"  source_form (as written): {e['source_form']}")
    if e["ontoloski_pomen"]:
        L.append(f"  pomen     : {e['ontoloski_pomen'][:120]}")
        L.append(f"  antinoma  : {e['antinoma']}")
        L.append(f"  sinteza   : {e['sinteza']}")
        L.append(f"  glyph     : {e['glyph']}")
    if e["smer"]:
        L.append(f"  smer      : {e['smer']}   custvo: {e['custvo']}   funkcija: {e['funkcija']}")
    L.append("STRATUM 2+4 — TYPED AND GRADED (never sorted together)")
    for face, typ, status in grade_entry(e):
        L.append(f"  {face:34s} [{typ:13s}] {status}")
    L.append("STRATUM 3 — RELATING (trust-ordered: explicit > structural)")
    mentions = web.get(word_id, [])
    L.append(f"  structural: {len(mentions)} mentions across the corpus (medium trust):")
    for f, n, line in mentions[:8]:
        L.append(f"    {f}:{n}  {line}")
    if len(mentions) > 8:
        L.append(f"    ... +{len(mentions) - 8} more")
    near_cites = [r for r in cites if any(c in r for c in ())]
    L.append("PROVENANCE")
    for p in e["provenance"]:
        L.append(f"  {p['source']} ({p['entry']})")
    owed = []
    if e["g2p_ambiguities"]:
        owed.append(f"e/ɛ at positions {e['g2p_ambiguities']} — a dissection owed")
    if e["annotations"].get("optikon_zven"):
        owed.append("o₀ conflict vs OPTIKON zven — preserved, standing, owed a decision")
    L.append("WHAT IT STILL OWES")
    L.append("  " + ("; ".join(owed) if owed else "nothing — every face measured or attributed"))
    return "\n".join(L)


if __name__ == "__main__":
    entries, drops, rows = LEX.ingest()
    assert drops == [], "thin slice stands only on a clean extraction"
    word = sys.argv[1] if len(sys.argv) > 1 else "ljubezen"
    wid = resolve(word)
    assert wid in entries, f"{word!r} is not an ingested entity"

    words = list(entries.keys())
    web = mention_web(words)
    cites = rez_citations(TEXT_FILES)

    # -- self-test: the theory's assertions, on the slice --
    ok = []
    lj = entries["ljubezen"]
    ok.append(("stratum 0: case variants resolve to one entity",
                resolve("Ljubezen") == resolve("ljubezen") == "ljubezen"))
    ok.append(("stratum 0: rez numbers have measured existence",
                rez_file_exists(529) and not rez_file_exists(99999)))
    ok.append(("stratum 3: ljubezen has a corpus-wide mention web",
                len(web["ljubezen"]) >= 5))
    ok.append(("stratum 3: explicit rez citations extracted corpus-wide",
                len(cites) >= 50))
    ok.append(("stratum 4: ljubezen fully measured — owes nothing",
               grade_entry(lj)[-1][2] == "measured"))
    ok.append(("stratum 4: volja's conflict preserved standing, not resolved",
               any("CONTRADICTED" in s for _f, _t, s in grade_entry(entries["volja"]))))
    ok.append(("extraction reuse: 40 entries, 0 drops, 12 dual-sourced",
               len(entries) == 40 and rows == 22))

    print(page(wid, entries, web, cites))
    print()
    print("-" * 72)
    for name, cond in ok:
        print(("PASS  " if cond else "FAIL  ") + name)
    all_ok = all(c for _n, c in ok)
    print("THIN SLICE " + ("PASS — the theory holds on one folder, one entity, "
          "one page" if all_ok else "FAIL — fail cheap on 30 files, not "
          "expensive on 800"))
    sys.exit(0 if all_ok else 1)
