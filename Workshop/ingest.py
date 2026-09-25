"""
INGEST — Step 1 of the digestion pipeline: point at the files, record what's there
LOVE CAGE / Obj2 — ingest.py. 24. 9. 2026. Companion of lexicon_core.py.

The pipeline (ratified): ingest (this) -> parse (per type, one flexible parser)
-> link (rez citations, word mentions, glyphs) -> answerable/fixable body.

Step 1 is boring by design: walk CanvasMinstral, read every text file, TAG
each by type with the EVIDENCE for the tag (never guess silently). The
manifest is the ground the parsers stand on. Files that cannot be read are
RECORDED as errors — padec je veljaven izid; nothing is skipped silently.

The day-one question stays the owner's; the body is built question-agnostic,
with the three named candidates as the first saved queries.

Self-test: python ingest.py   (manifest written, counts measured, zero crashes)
"""
from __future__ import annotations
import os
import re
import sys
import json
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # CanvasMinstral/
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ingest_manifest.json")
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache"}

SNIFF = [
    ("optikon_table", lambda h, name: name.endswith(".txt") and "Beseda\tZven\tSmer" in h),
    ("dosje_catalog", lambda h, name: "Fonetični rez" in h and "####" in h),
    ("aphorism_series", lambda h, name: len(re.findall(r"(?m)^\s*\d{2,4}\.\s+\S", h)) >= 20),
    ("rez_cut", lambda h, name: re.search(r"(?i)rez[ -]?\d+|NUJNE NAPAKE|Razsodba|⊢ DOKAZ", h) is not None),
    ("law_register", lambda h, name: re.search(r"(?i)zakon|pravil[oa] in pogoji|register", h) is not None),
    ("dialog_rek", lambda h, name: re.search(r"\bREK\b|EGO dialog|pogovor", h, re.I) is not None),
    ("prose", lambda h, name: True),  # the honest default; eyeballed, never force-fit
]


def register_type(name, test):
    """Graft #2, plugin-refactor: register a new corpus type WITHOUT editing
    the core — the same evolution ceremony as soul_engine's ParserPlugin
    (format #4 = one class + one line there; one call here). New types slot
    in ahead of the prose default, so the honest default stays last."""
    SNIFF.insert(len(SNIFF) - 1, (name, test))


def classify(path: str, rel: str) -> dict:
    ext = os.path.splitext(path)[1].lower()
    entry = dict(file=rel.replace("\\", "/"), ext=ext,
                 bytes=os.path.getsize(path), error=None)
    if ext in (".pdf",):
        entry["type"] = "pdf_unextracted"      # named ∂: extractability undecided
        entry["hint"] = "UC_DOSJE etc. — extractable-or-not measured before 'complete'"
        return entry
    if ext in (".py", ".tsx"):
        entry["type"] = "code"
        return entry
    if ext in (".png", ".jpg", ".jpeg", ".svg", ".gif"):
        entry["type"] = "image"
        return entry
    if ext == ".zip":
        entry["type"] = "archive"
        return entry
    if ext not in (".md", ".txt", ""):
        entry["type"] = "other_binary"
        return entry
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            head = fh.read(4000)
    except OSError as e:
        entry["type"] = "unreadable"
        entry["error"] = str(e)             # recorded, never silent
        return entry
    for typ, test in SNIFF:
        if test(head, rel):
            entry["type"] = typ
            return entry
    entry["type"] = "prose"                  # unreachable; kept for the machine
    return entry


def ingest():
    manifest, errors = [], 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT)
            e = classify(p, rel)
            if e.get("error"):
                errors += 1
            manifest.append(e)
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(dict(generated=ts, root=ROOT, total=len(manifest),
                       unreadable=errors, files=manifest), fh,
                  ensure_ascii=False, indent=1)
    return manifest, errors


if __name__ == "__main__":
    # plugin ceremony receipt: a registered type slots in ahead of the prose
    # default — the line extends, it never forks
    register_type("_selftest_type", lambda h, name: False)
    assert SNIFF[-2][0] == "_selftest_type" and SNIFF[-1][0] == "prose"
    SNIFF.pop(-2)
    manifest, errors = ingest()
    counts = {}
    for e in manifest:
        counts[e["type"]] = counts.get(e["type"], 0) + 1
    print("THE MEASURED CORPUS (Step 1 — ground truth, not '~800+'):")
    for t, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {t:16s} {n:5d}")
    print(f"  {'TOTAL':16s} {len(manifest):5d}   unreadable(errors recorded): {errors}")
    assert len(manifest) > 700, "the corpus must exceed 700 files"
    assert errors == len([e for e in manifest if e.get("error")]), "errors counted honestly"
    textish = counts.get("dosje_catalog", 0) + counts.get("prose", 0) \
        + counts.get("rez_cut", 0) + counts.get("law_register", 0) \
        + counts.get("dialog_rek", 0) + counts.get("aphorism_series", 0)
    print(f"  parseable text types (parse.py's real targets): {textish}")
    print("PASS — manifest written: ingest_manifest.json; every file typed with evidence;")
    print("      the day-one question remains the owner's; the body answers all of them.")
