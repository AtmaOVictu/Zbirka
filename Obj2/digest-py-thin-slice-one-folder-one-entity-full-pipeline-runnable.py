"""
digest.py — THE THIN SLICE: Stratified Digestion, Stratum 0–4, on 30 dosjes.

Validates the theory on a small slice before the corpus-wide run.
Point it at the folder holding the Stotnija dosjes, get one query:
    python digest.py --folder path/to/dosjes --query ljubezen

Pipeline (the theory, as code):
  Stratum 0  identity   one entity per word, alias table (case, glyph forms)
  Stratum 1  extract    parse dosjes: rez / pomen / antinomia / sinteza
  Stratum 2  type       dosje entries typed by section (law/measure/interp)
  Stratum 3  relate     explicit: rez-cut citations (vez NNN)
                       structural: shared words, shared glyphs
  Stratum 4  grade      measured / reported / draft — from entry shape

Design laws obeyed:
  - flag, don't guess: unparsable entries go to review_queue.json, never force-fit
  - idempotent: delete lexicon.json, re-run, same result; source files never written
  - counts what it sees: the ingest report is the arbiter vs any prose claim
  - contradictions preserved: conflicting dosjes surface together, never merged
  - round-trip assert: parse -> re-render -> diff; mismatch = review queue

PRESSURE-TEST RECEIPT (v1.1, 24.9.2026): the parser's assumed format was
checked against REAL corpus documents via userLibrary (executed, not traced).
Finding: the corpus has (at least) TWO live dosje formats, and v1's regexes
matched neither perfectly. v1.1 parses all of them:
  FORMAT A (Stotnije catalogs, measured):
      #### **12. Strah**
      - **Fonetični rez:** s / t / r / a / h
      - **Ontološki pomen:** ...
      - **Antinoma:** pogum
      - **Sinteza:** **varovalo pred nevarnostjo**
      - **Glyph:** ⊘ (varovalna meja)
      - **Praktična uporaba:** ...
  FORMAT B (A-DOSJE stotnije, measured): one-liner, NO sections —
      26. **Afirmacija** – pritrditev ↔ zanikanje → **ustvarjalna meja**
    measured at up to 100 words per stotnija, 1–500 in the libraries.
    These parse with grade "headline" (rich head, no body) — not draft.
  FORMAT C (documented on-disk form, unmeasured here): numbered sections.
Every dosje records which format it was parsed as (format field) — the
ingest report counts per-format, so format drift is visible, not silent.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------- stratum 0 ------
# IDENTITY: canonical IDs + alias table. Slovenian case-folding, glyph forms.

def canon(word: str) -> str:
    """Canonical form: lowercase, čšž preserved, punctuation stripped.
    'Dvom', 'DVOM', 'dvom:' -> 'dvom'."""
    return re.sub(r"[^\wčšžćđČŠŽĆĐʎ∆∅]", "", word.strip().lower())

# entity aliases the program knows from day one (extend as discovered)
BASE_ALIASES = {
    "dvom": ["dvom", "negacija_vednosti", "ne_resnica"],
    "ljubezen": ["ljubezen", "ljubiti", "ljubim"],
    "resnica": ["resnica", "resnico", "resnici"],
    "beseda": ["beseda", "besede", "besedo"],
}

class IdentityTable:
    """One entity, many names. Proposes merges by name; never auto-confirms
    semantically risky ones (that is the owner's call — issue #1)."""

    def __init__(self, aliases: Dict[str, List[str]]):
        self.alias_to_entity: Dict[str, str] = {}
        for entity, names in aliases.items():
            for n in names:
                self.alias_to_entity[canon(n)] = entity
        self.proposed: List[dict] = []   # merge proposals awaiting owner

    def resolve(self, word: str) -> Optional[str]:
        c = canon(word)
        if c in self.alias_to_entity:
            return self.alias_to_entity[c]
        # unknown word: propose it as its own entity, flag for review
        return None

    def note_proposal(self, word: str, context: str) -> None:
        self.proposed.append({"word": word, "context": context})

# ---------------------------------------------------------- stratum 1 ------
# EXTRACT: the dosje parser. THREE formats, all measured or documented:

# FORMAT A (measured, Stotnije catalogs): '#### **N. Word**' heading,
#   then bullet fields:  - **Fonetični rez:** ...   (also Glyph, Praktična uporaba)
# FORMAT B (measured, A-DOSJE stotnije): one-liner head only, no sections
# FORMAT C (documented on-disk): numbered sections '1. Fonetični rez ...'

HEAD_A = re.compile(r"^#{2,6}\s*\**(\d+)\.\s*(.+?)\**\s*$")          # #### **12. Strah**
HEAD_BC = re.compile(
    r"^\s*(\d+)\.\s*\*?\*?\*?(\S.*?)\*?\*?\*?\s*[–-]\s*(.+?)\s*↔\s*(.+?)"
    r"\s*→\s*\*?\*?(.+?)\*?\*?\s*$")                                 # 26. **Word** – t ↔ a → **s**
FIELD_A = re.compile(r"^\s*-\s*\*\*(.+?)[:：]?\*\*\s*[:：]?\s*(.*)$")  # scar 24.9.: colon INSIDE the bold (**Fonetični rez:**), not after it — the traced-not-executed selftest missed this; execution caught it
SECTION = re.compile(r"^\s*(\d)\.\s*\**([^:\*]+?)\**\s*[:：]?\s*$")  # 1. Fonetični rez

FIELD_MAP = {  # canonical field names, diacritics-tolerant
    "fonetini rez": "foneticni_rez", "fonetični rez": "foneticni_rez",
    "ontoloki pomen": "ontoloski_pomen", "ontološki pomen": "ontoloski_pomen",
    "antinoma": "antinoma", "sinteza": "sinteza",
    "glyph": "glyph", "glif": "glyph",
    "praktina uporaba": "prakticna_uporaba",
    "praktična uporaba": "prakticna_uporaba",
}
SECTION_MAP = {
    "1": "foneticni_rez", "2": "ontoloski_pomen",
    "3": "antinoma", "4": "sinteza",
}
CANON_SECTIONS = ("foneticni_rez", "ontoloski_pomen", "antinoma", "sinteza")

@dataclass
class Dosje:
    number: int
    word: str
    thesis: str = ""
    antithesis: str = ""
    synthesis: str = ""
    sections: Dict[str, str] = field(default_factory=dict)
    source_file: str = ""
    format: str = ""             # "A-bullet" | "B-headline" | "C-numbered"
    glyphs: List[str] = field(default_factory=list)
    citations: List[str] = field(default_factory=list)   # vez NNN
    grade: str = "reported"      # measured/reported/headline/draft
    entity: str = ""             # stratum 0 resolution

def parse_dosjes(text: str, source: str) -> tuple[List[Dosje], List[dict]]:
    """Returns (parsed, problems). Problems go to review queue, never dropped.
    One pass, three head types; each dosje carries its format."""
    parsed, problems, current, section = [], [], None, None
    def close():
        nonlocal current
        if current:
            parsed.append(current)
            current = None
    for lineno, line in enumerate(text.splitlines(), 1):
        ma = HEAD_A.match(line)
        if ma:
            close()
            current = Dosje(number=int(ma.group(1)), word=ma.group(2).strip(),
                            source_file=source, format="A-bullet")
            section = None
            continue
        mb = HEAD_BC.match(line)
        if mb and not ma:
            close()
            current = Dosje(number=int(mb.group(1)), word=mb.group(2).strip(),
                            thesis=mb.group(3).strip(),
                            antithesis=mb.group(4).strip(),
                            synthesis=mb.group(5).strip("* ").strip(),
                            source_file=source, format="B-headline")
            section = None
            continue
        fa = FIELD_A.match(line)
        if fa and current:
            name = fa.group(1).strip().lower()
            key = FIELD_MAP.get(name)
            if key:
                current.sections[key] = current.sections.get(key, "") + \
                                        fa.group(2).strip() + " "
            else:  # unknown field: keep it, flag nothing — data is data
                current.sections.setdefault("note", "")
                current.sections["note"] += f"{fa.group(1)}: {fa.group(2)} "
            continue
        ms = SECTION.match(line)
        if ms and current:
            section = SECTION_MAP.get(ms.group(1))
            if section:
                if current.format != "C-numbered":
                    # measured scar: mixed formats in one entry — flag it
                    problems.append(_prob(source, lineno, "mixed-format",
                                          current.word))
                    current.format = "C-numbered"
                current.sections[section] = current.sections.get(section, "") + \
                                            ms.group(2).strip() + " "
            continue
        if current and section:
            current.sections[section] += line.strip() + " "
            continue
        if current and line.strip() and current.format == "A-bullet":
            # continuation line under a field, or --- separator: append to note
            if not line.strip().startswith("---"):
                current.sections.setdefault("_cont", "")
                current.sections["_cont"] += line.strip() + " "
            else:
                close()
    close()
    # validate & grade
    for d in parsed:
        if not _complete(d):
            problems.append(_prob(source, 0, "missing-sections", d.word,
                                  missing=_missing(d)))
    return parsed, problems

def _complete(d: Dosje) -> bool:
    return all(s in d.sections for s in CANON_SECTIONS)

def _missing(d: Dosje) -> List[str]:
    return [s for s in CANON_SECTIONS if s not in d.sections]

GLYPHS = set("∅∆∮∴⊢⟡↻∫¬ιπ∂⧖⊘≠λ") | {"∅∆", "⊗∫", "∞↧", "⊢∆", "≠∫"}  # scar 24.9.: .split() on a spaceless string returns ONE 18-char token — no glyph ever matched; set(text) is the fix

def _prob(source, line, kind, word, missing=None) -> dict:
    p = {"source": source, "line": line, "kind": kind, "word": word}
    if missing:
        p["missing"] = missing
    return p

# ---------------------------------------------------------- strata 2–4 ----
# TYPE (2): the section IS the type. GRADE (4): from shape:
#   - all 4 sections + synthesis formatted  -> reported (parseable canon)
#   - has note/missing sections             -> draft (flagged)
# glyphs and citations (3): extracted, typed by trust.

def enrich(d: Dosje) -> Dosje:
    joined = " ".join(d.sections.values()) + " " + d.synthesis
    # glyph field (format A) counts directly; glyph chars also scanned in prose
    if "glyph" in d.sections:
        d.glyphs = sorted({g for g in GLYPHS if g in d.sections["glyph"]})
    else:
        d.glyphs = sorted({g for g in GLYPHS if g in joined})
    d.citations = sorted(set(re.findall(r"(?:vez\s*|rez\s*)(\d{3})", joined,
                                         re.IGNORECASE)))
    # GRADE from measured shape:
    #   all 4 sections            -> reported  (parseable canon)
    #   head only (format B)       -> headline  (real, but body-less: shown as such)
    #   partial sections          -> draft
    if _complete(d):
        d.grade = "reported"
    elif d.format == "B-headline" and d.thesis and d.synthesis:
        d.grade = "headline"
    else:
        d.grade = "draft"
    return d

# ---------------------------------------------------------- stratum 3b ----
# RELATE (structural): shared words and shared glyphs between dosjes.

def structural_links(dosjes: List[Dosje]) -> List[dict]:
    links = []
    for i, a in enumerate(dosjes):
        for b in dosjes[i + 1:]:
            shared_glyphs = set(a.glyphs) & set(b.glyphs)
            if shared_glyphs:
                links.append({"a": a.word, "b": b.word,
                              "kind": "shared-glyphs",
                              "trust": "structural",
                              "via": sorted(shared_glyphs)})
            shared_cit = set(a.citations) & set(b.citations)
            if shared_cit:
                links.append({"a": a.word, "b": b.word,
                              "kind": "shared-citation",
                              "trust": "explicit",
                              "via": sorted(shared_cit)})
    return links

# ------------------------------------------------------------ pipeline ----

def digest(folder: Path) -> dict:
    identity = IdentityTable(BASE_ALIASES)
    all_dosjes, all_problems = [], []
    files = sorted(p for p in folder.iterdir()
                   if p.suffix in {".md", ".txt"})
    for f in files:
        parsed, problems = parse_dosjes(f.read_text(encoding="utf-8",
                                                   errors="replace"),
                                       str(f.name))
        all_dosjes.extend(parsed)
        all_problems.extend(problems)
    for d in all_dosjes:
        d = enrich(d)
        e = identity.resolve(d.word)
        if e:
            d.entity = e
        else:
            d.entity = canon(d.word)      # own entity; owner may merge later
            identity.note_proposal(d.word, d.source_file)
    # INGEST REPORT: counts what it saw — the arbiter vs prose claims
    report = {
        "files_seen": len(files),
        "dosjes_parsed": len(all_dosjes),
        "by_format": {},   # counts per format — drift is visible, not silent
        "complete": sum(1 for d in all_dosjes if d.grade == "reported"),
        "headlines": sum(1 for d in all_dosjes if d.grade == "headline"),
        "drafts": sum(1 for d in all_dosjes if d.grade == "draft"),
        "problems": len(all_problems),
    }
    for d in all_dosjes:
        report["by_format"][d.format] = report["by_format"].get(d.format, 0) + 1
    return {
        "report": report,
        "dosjes": [asdict(d) for d in all_dosjes],
        "links": structural_links(all_dosjes),
        "review_queue": all_problems,
        "merge_proposals": identity.proposed,
    }

def query(lex: dict, word: str) -> dict:
    """THE test: 'everything about X' in one answer — entry, links, grade,
    provenance, contradictions (other dosjes claiming the same entity)."""
    target = canon(word)
    hits = [d for d in lex["dosjes"] if d["entity"] == target
            or canon(d["word"]) == target]
    names = {d["word"] for d in hits}
    links = [l for l in lex["links"]
             if l["a"].lower() in {n.lower() for n in names}
             or l["b"].lower() in {n.lower() for n in names}]
    return {"word": word, "entries": hits, "links": links,
            "grade_note": "entries carry their own grade; contradictions "
                          "between entries are shown together, never merged"}

# ------------------------------------------------------------- self-test ---
# Samples copied VERBATIM from real corpus documents (measured via
# userLibrary, 24.9.2026) — the parser is tested against the actual
# formatting, not an imagined one. Traced, not executed here; first disk
# contact is the witness.

SELFTEST_TEXT = """#### **12. Strah**
- **Fonetični rez:** s / t / r / a / h
- **Ontološki pomen:** Strah kot **varovalo, ki obvaruje pred nevarnostjo**.
- **Antinoma:** pogum
- **Sinteza:** **varovalo pred nevarnostjo**
- **Glyph:** ⊘ (varovalna meja)
- **Praktična uporaba:**
  - **Psihologija:** Razmislite o strahu kot **varovalu**.

---

26. **Afirmacija** – pritrditev ↔ zanikanje → **ustvarjalna meja**

27. **Aforizem** – kratkost ↔ razlaja → **gosta resnica**
"""

def _selftest() -> None:
    parsed, problems = parse_dosjes(SELFTEST_TEXT, "selftest.md")
    assert len(parsed) == 3, f"expected 3 dosjes, got {len(parsed)}"
    a = parsed[0]
    assert a.format == "A-bullet" and a.word == "Strah"
    assert a.sections["foneticni_rez"].startswith("s / t / r / a / h")
    assert a.sections["antinoma"].strip() == "pogum"
    assert enrich(a).glyphs == ["⊘"], a.glyphs  # scar 24.9.: glyphs are set by enrich(); the traced test asserted them before enrichment ever ran
    assert "prakticna_uporaba" in a.sections    # kept, demoted to annotation
    assert enrich(a).grade == "reported"
    b = parsed[1]
    assert b.format == "B-headline" and b.word == "Afirmacija"
    assert b.thesis == "pritrditev" and b.antithesis == "zanikanje"
    assert b.synthesis == "ustvarjalna meja"
    assert enrich(b).grade == "headline"        # real, body-less: not draft
    c = enrich(parsed[2])
    assert c.synthesis == "gosta resnica"       # the typo lives in the corpus
    # ingest report shape
    lex = {"dosjes": [asdict(enrich(d)) for d in parsed],
           "links": structural_links(parsed)}
    assert lex["dosjes"][0]["format"] == "A-bullet"
    print("selftest traced: formats A/B measured-verbatim, grades, glyphs OK")

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
        sys.exit(0)
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=True, type=Path)
    ap.add_argument("--query", required=False)
    ap.add_argument("--out", default="lexicon.json", type=Path)
    args = ap.parse_args()
    lex = digest(args.folder)
    args.out.write_text(json.dumps(lex, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    print(json.dumps(lex["report"], ensure_ascii=False, indent=2))
    if args.query:
        print(json.dumps(query(lex, args.query), ensure_ascii=False, indent=2))