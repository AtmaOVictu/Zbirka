"""
LEXICON CORE — Cut 3: the schema, the parsers, the earned index
LOVE CAGE / Obj2 — lexicon_core.py. 24. 9. 2026.

Built on the reconciliation pass (lexicon-schema-reconciliation-pass.md,
commit 045fb14) and its SEALED decisions:
  - Praktična uporaba demoted to annotation (guidance, not a measure)
  - ONE glyph register: dosje glyphs carried as written, machine-checkable
    against the R-7/APD vocabulary (∂: the mapping table is the next pass)
  - world face DEFERRED (smer + provenance carry placement)

THE TWELVE FACES (each with its warrant — see the reconciliation pass):
  word            Stotnije heading / OPTIKON col 1 (the geslo)
  phonemes        the lattice's chain — measured, graphemic split corrected
                  (lj is one sound, ʎ; c is t͡s). Survivor #1 consumed.
  source_form     the graphemic split AS THE SOURCES WROTE IT (preserved)
  ontoloski_pomen dosje component 2
  antinoma        dosje component 3
  sinteza         dosje component 4
  glyph           dosje glyph field (one register, collisions checkable)
  smer            OPTIKON col 3 (spatial — proto-placement)
  custvo          OPTIKON col 4
  funkcija        OPTIKON col 5
  provenance      every source, entry id, ingest timestamp
  ledger_id       apd_engine Ledger — every future edit a ledger line
                  (survivor #2; the edit ledger itself is Cut 4's wiring)

G2P HONESTY: Slovenian orthography is nearly phonemic; this core carries a
small digraph-aware mapper for unknown words. Where a MEASURED chain already
exists (the seed stone), it overrides the mapper and provenance says so.
Where the mapper guesses e vs ɛ, the entry carries e and an ambiguity flag —
resolving it is a dissection, i.e. a human act, i.e. Cut 5's job.

BACKLOG (∂ named, per the correction of 24. 9.):
  - A3/Lukova_sesta_stotnija_501_550.txt is APHORISMS (50 numbered cuts),
    a different organ — in the ingestion backlog as what it measurably is,
    NOT force-parsed into dosjes.
  - A2/UC_DOSJE_Luka*.pdf: extractable-or-not must be DECIDED before any
    ingestion pass claims "complete." No stdlib PDF reader exists here;
    the ∂ stays open until measured.

Self-test: python lexicon_core.py  (parse fidelity: 40 unique words with
provenance, every dosje's four components found, zero silent drops, and the
12 overlaps asserted consistent-or-conflicted — the parser's real stress test)
"""

from __future__ import annotations
import json
import os
import re
import sys
import datetime
import importlib.util

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)  # CanvasMinstral/


def _load(fname, base=_HERE):
    spec = importlib.util.spec_from_file_location(fname.replace("-", "_").split(".")[0],
                                                  os.path.join(base, fname))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


VALIDATOR = _load("wordlist_validator.py")   # pulls lattice + engine + pass3
LATTICE = VALIDATOR.LATTICE

STOTNIJE_PATH = os.path.join(_ROOT, "Basics", "stotnije-a-dosje-besedni-dosjeji.md")
OPTIKON_PATH = os.path.join(_ROOT, "A3", "OPTIKON_complete.txt")
LEXICON_JSON = os.path.join(_HERE, "lexicon.json")

# ---------------------------------------------------------------------------
# G2P-lite (Slovenian, digraph-aware; honest about e/ɛ)
# ---------------------------------------------------------------------------

DIGRAPHS = {"lj": "ʎ", "nj": "ɲ", "dž": "d͡ʒ"}
G2P = {"c": "t͡s", "č": "t͡ʃ", "š": "ʃ", "ž": "ʒ", "g": "ɡ", "h": "x",
       "a": "a", "e": "e", "i": "i", "o": "o", "u": "u",
       "r": "r", "k": "k", "p": "p", "b": "b", "t": "t", "d": "d",
       "f": "f", "v": "v", "z": "z", "s": "s", "m": "m", "n": "n",
       "l": "l", "j": "j"}


def sl_g2p(word: str):
    """Letter-split -> phoneme chain (candidate). Returns (chain, ambiguities).
    e/ɛ split is unmeasured here: e is emitted and flagged; resolving it is a
    dissection (a human act, ledgered in Cut 4)."""
    w = word.lower()
    chain, ambiguities = [], []
    i = 0
    while i < len(w):
        two = w[i:i + 2]
        if two in DIGRAPHS:
            chain.append(DIGRAPHS[two])
            i += 2
            continue
        ch = w[i]
        if ch not in G2P:
            return None, [f"unmapped letter {ch!r}"]
        chain.append(G2P[ch])
        if ch == "e":
            ambiguities.append(len(chain) - 1)  # e vs ɛ unresolved
        i += 1
    return chain, ambiguities


# Measured chains (the seed stone + the wordlist's hand-verified entries) —
# these OVERRIDE the mapper; provenance records the source.
SEEDED_CHAINS = {}
for _w, _c in VALIDATOR.WORDLIST.get("sl", {}).items():
    SEEDED_CHAINS[_w.lower()] = ("wordlist_validator.WORDLIST(sl)", _c)
for _lang, _d in LATTICE.LOVE_EQUIVALENTS.items():
    if isinstance(_d, dict) and _lang == "sl":
        SEEDED_CHAINS["ljubezen"] = ("seed stone LOVE_EQUIVALENTS(sl)", _d["phonemes"])


# ---------------------------------------------------------------------------
# PARSERS — zero silent drops, provenance on every face
# ---------------------------------------------------------------------------

def _entry_shell(word):
    return dict(word=word, phonemes=None, source_form=None, ontoloski_pomen=None,
                antinoma=None, sinteza=None, glyph=None, smer=None, custvo=None,
                funkcija=None, provenance=[], ledger_id=None,
                annotations={}, g2p_ambiguities=[])


def parse_stotnije() -> dict:
    src = open(STOTNIJE_PATH, encoding="utf-8").read()
    blocks = re.split(r"^####\s+", src, flags=re.M)[1:]
    entries, drops = {}, []
    for b in blocks:
        m = re.match(r"\*?\*?(\d+)\.?\s*([^\n*]+?)\*?\*?\s*$", b.splitlines()[0])
        if not m:
            drops.append(b.splitlines()[0][:40])
            continue
        num, word = int(m.group(1)), m.group(2).strip()
        def field(name, block=b):
            mm = re.search(r"\*\*" + name + r":\*\*\s*(.+?)(?=\n-\s\*\*|\n\n|\Z)",
                           block, re.S)
            return mm.group(1).strip() if mm else None
        e = _entry_shell(word)
        rez = field("Fonetični rez")
        e["source_form"] = rez
        e["ontoloski_pomen"] = field("Ontološki pomen")
        e["antinoma"] = field("Antinoma")
        e["sinteza"] = field("Sinteza")
        e["glyph"] = field("Glyph")
        pu = re.search(r"\*\*Praktična uporaba:\*\*(.+?)(?=\n---|\n####|\Z)", b, re.S)
        e["annotations"]["prakticna_uporaba"] = pu.group(1).strip() if pu else None
        e["provenance"].append(dict(source="Basics/stotnije-a-dosje-besedni-dosjeji.md",
                                    entry=f"stotnija#{num}"))
        entries[word.lower()] = e
    return entries, drops


def parse_optikon(entries: dict) -> tuple:
    lines = open(OPTIKON_PATH, encoding="utf-8").read().splitlines()
    header = lines[0].split("\t")
    assert header == ["Beseda", "Zven", "Smer", "Čustvo", "Funkcija"], header
    rows, drops = 0, []
    for line in lines[1:]:
        if not line.strip():
            continue
        cols = line.split("\t")
        if len(cols) != 5:
            drops.append(line[:50])
            continue
        beseda, zven, smer, custvo, funkcija = (c.strip() for c in cols)
        rows += 1
        key = beseda.lower()
        e = entries.setdefault(key, _entry_shell(beseda))
        e["word"] = e["word"] or beseda
        if e["source_form"] is None:
            e["source_form"] = zven
        else:
            # NEVER silently drop the overlapping face (the correction of
            # 24. 9.: overlap is the parser's real stress test):
            e["annotations"]["optikon_zven"] = zven
        e["smer"] = smer
        e["custvo"] = custvo
        e["funkcija"] = funkcija
        e["provenance"].append(dict(source="A3/OPTIKON_complete.txt", entry=f"row:{beseda}"))
    return entries, rows, drops


def ingest() -> dict:
    entries, drops1 = parse_stotnije()
    entries, rows, drops2 = parse_optikon(entries)
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    for key, e in entries.items():
        # phonemes: measured chain if seeded, else the mapper's candidate
        if key in SEEDED_CHAINS:
            src_note, chain = SEEDED_CHAINS[key]
            e["phonemes"] = chain
            e["provenance"].append(dict(source=src_note, entry="measured chain"))
        else:
            chain, amb = sl_g2p(e["word"])
            e["phonemes"] = chain
            e["g2p_ambiguities"] = amb
            if chain is not None:
                e["provenance"].append(dict(source="lexicon_core.sl_g2p",
                                            entry="candidate (e/ɛ unresolved)" if amb else "candidate"))
        e["ledger_id"] = key  # Cut 4 wires the apd_engine Ledger onto this id
        e["ingested"] = ts
    return entries, drops1 + drops2, rows


def save_lexicon(entries):
    with open(LEXICON_JSON, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=1, sort_keys=True)


# ---------------------------------------------------------------------------
# SELF-TEST — parse fidelity, zero silent drops, the ljubezen regression
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)
        return cond

    entries, drops, optikon_rows = ingest()
    # -- parse fidelity: 30 dosjes, all four components + glyph + source rez --
    from_stotnije = [e for e in entries.values()
                     if any(p["source"].endswith("stotnije-a-dosje-besedni-dosjeji.md")
                            for p in e["provenance"])]
    check(len(from_stotnije) == 30, f"30 dosjes — got {len(from_stotnije)}")
    for e in from_stotnije:
        for face in ("source_form", "ontoloski_pomen", "antinoma", "sinteza", "glyph"):
            check(e[face] not in (None, ""), f"{e['word']}: face {face} missing")
    check(optikon_rows == 22, f"22 OPTIKON rows — got {optikon_rows}")
    check(len(drops) == 0, f"ZERO silent drops — got {len(drops)}: {drops[:3]}")
    # -- every entry: phonemes + provenance --
    for e in entries.values():
        check(e["phonemes"] is not None and len(e["phonemes"]) > 0,
              f"{e['word']}: no phoneme chain")
        check(len(e["provenance"]) >= 1, f"{e['word']}: no provenance")
        # every phoneme is a prisoner of the lattice (the rez face is honest)
        for p in e["phonemes"]:
            check(p in LATTICE.PHONEMES,
                  f"{e['word']}: phoneme {p!r} is not a prisoner of the lattice")
    # -- ljubezen: the first scar's regression (seed stone chain) --
    lj = entries["ljubezen"]
    check(lj["phonemes"] == ["ʎ", "u", "b", "e", "z", "ɛ", "n"],
          f"ljubezen chain must equal the seed stone's [ʎ u b e z ɛ n] — got {lj['phonemes']}")
    check(lj["source_form"] is not None and "l / j / u" in lj["source_form"],
          "ljubezen source_form preserved as written (graphemic)")
    check(lj["antinoma"] == "sovraštvo", "ljubezen antinoma: sovraštvo")
    check(lj["smer"] == "znotraj / nad / skozi", "ljubezen smer from OPTIKON")
    check(lj["glyph"] is not None, "ljubezen glyph present")
    # -- inventory: 30 + 22 with 12 overlap = 40 unique words --
    check(len(entries) == 40, f"40 unique words (30+22, 12 overlap) — got {len(entries)}")
    def _src_count(e):
        return len([p for p in e["provenance"]
                    if p["source"].endswith((".md", ".txt"))])
    both = [e["word"] for e in entries.values() if _src_count(e) >= 2]
    check(len(both) == 12, f"12 words with BOTH sources — got {len(both)}: {both}")

    # -- THE 12 OVERLAPS: consistent-or-conflicted (the parser's real stress
    #    test — overlap is where prose schemas drift from tables; conflicts
    #    are scars to report, not surprises to hide) --
    def _norm_rez(s):
        if not s:
            return None
        return re.sub(r"[\s/]+", "", s)
    comparisons, conflicts = 0, []
    for e in entries.values():
        if _src_count(e) < 2:
            continue
        comparisons += 1
        dosje_form = _norm_rez(e["source_form"])
        optikon_form = _norm_rez(e["annotations"].get("optikon_zven"))
        if dosje_form != optikon_form:
            conflicts.append(f"{e['word']}: dosje '{e['source_form']}' "
                             f"vs OPTIKON '{e['annotations'].get('optikon_zven')}'")
    check(comparisons == 12, f"12 overlap comparisons made — got {comparisons}")
    print(f"OVERLAP STRESS TEST: {comparisons} compared, "
          f"{comparisons - len(conflicts)} consistent, {len(conflicts)} CONFLICTED")
    for c in conflicts:
        print("   CONFLICT:", c)
    # -- the system's own name-words have no dosje yet (register's measure-me list)
    for w in ("ne", "nič"):
        check(w in entries, f"{w!r} ingested from OPTIKON")
        check("Antinoma" not in str(entries[w]), f"{w!r} still dosje-less (known)")
    # -- glyph register: one table, machine-checkable --
    glyphs = [e["glyph"] for e in entries.values() if e["glyph"]]
    check(len(glyphs) == 30, f"30 glyphs carried as written — got {len(glyphs)}")
    print(f"glyph register: {len(set(glyphs))} distinct glyphs across 30 dosjes "
          f"(duplicates visible, mapped to R-7/APD in the next pass)")

    save_lexicon(entries)
    print(f"lexicon.json written: {len(entries)} entries "
          f"({len(both)} dual-sourced, 30 dosjes, 22 OPTIKON rows, 0 silent drops)")
    amb = sum(1 for e in entries.values() if e["g2p_ambiguities"])
    print(f"G2P candidates with e/ɛ ambiguity (each is a pending dissection): {amb}")
    print(f"ljubezen regression: chain == seed stone [ʎ u b e z ɛ n] — "
          f"{'PASS' if lj['phonemes'] == ['ʎ','u','b','e','z','ɛ','n'] else 'FAIL'}")
    if failures:
        print("FAILURES:")
        for f in failures[:20]:
            print("  -", f)
        sys.exit(1)
    print("PASS — parse fidelity holds: every dosje's four components found, "
          "zero silent drops, the earned index begins.")
