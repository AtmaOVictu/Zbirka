"""
soul_engine.py — THE EPIC VERSION. One install, one command, evolvable forever.

    pip install textual
    python soul_engine.py scan   D:\\OntoProjekt\\CanvasMinstral
    python soul_engine.py scan   D:\\Comprehension
    python soul_engine.py gui

Architecture (why this is evolvable, not just big):

    LEDGER (soul.db, table `ledger`)   — append-only, the spine of everything.
        Every scan, verdict, merge, edit = one line. Nothing is overwritten.
        The current state of the world is DERIVED by replaying the ledger.
        Change the theory → change the derivation → the data survives you.

    RAW (tables `docs`, `entries`)      — what parsers saw, verbatim + parsed.
        Parsers are PLUGINS (ParserPlugin subclasses). Adding corpus format
        #4 = writing a plugin, registering it, rescanning. No core changes.

    DERIVED (SQLite views)             — the "page" for a word, the conflict
        list, the merge queue: all views. Views are cheap to change; that is
        the point. Strata became columns; laws became views.

    EXPORT (`export.py` contract)      — JSON + GraphML of the word-graph.
        This is what Godot/Soul Evolution will eat. The engine never needs
        to know the game exists.

Evolves by: new plugin → rescan (idempotent, ledger-deduped) → new view.
The ledger guarantees you can always replay history against a better future.
"""

import argparse
import json
import os
import re
import sqlite3
import sys
import unicodedata
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional

# =========================================================== DATABASE =====

DB_PATH = Path("soul.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS ledger (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ts        TEXT NOT NULL,
    kind      TEXT NOT NULL,   -- scan|verdict|merge|edit|grade|export|retype|reparse
    word      TEXT,
    payload   TEXT NOT NULL    -- JSON
);
CREATE TABLE IF NOT EXISTS docs (
    doc_id    INTEGER PRIMARY KEY,
    path      TEXT UNIQUE NOT NULL,
    mtime     TEXT,
    raw_size  INTEGER,
    kind      TEXT,                   -- graft #8: what this text IS
    stratum   TEXT                    -- graft #8: where it OCCUPIES
);
CREATE TABLE IF NOT EXISTS entries (
    entry_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id    INTEGER NOT NULL REFERENCES docs,
    word      TEXT NOT NULL,
    format    TEXT NOT NULL,           -- which plugin parsed it
    number    INTEGER,
    thesis    TEXT, antithesis TEXT, synthesis TEXT,
    foneticni_rez TEXT, ontoloski_pomen TEXT,
    antinoma  TEXT, glyph TEXT, prakticna_uporaba TEXT,
    lineno    INTEGER,                 -- provenance: find it again
    grade     TEXT NOT NULL DEFAULT 'reported',
    merged_into TEXT                   -- loser points at the keeper's word
);
CREATE INDEX IF NOT EXISTS idx_entries_word ON entries(word);
CREATE TABLE IF NOT EXISTS mentions (
    entry_id  INTEGER,                 -- mention-of link (stratum 3, cheap)
    mention   TEXT
);
CREATE INDEX IF NOT EXISTS idx_mentions ON mentions(mention);
CREATE VIEW IF NOT EXISTS v_page AS
    SELECT word, COUNT(*) AS sources,
           GROUP_CONCAT(DISTINCT format) AS formats,
           SUM(grade='reported') AS reported, SUM(grade='headline') AS headline
    FROM entries GROUP BY word;
CREATE VIEW IF NOT EXISTS v_conflicts AS
    SELECT word, foneticni_rez, COUNT(DISTINCT foneticni_rez) AS variants
    FROM entries
    WHERE foneticni_rez IS NOT NULL AND TRIM(foneticni_rez) != ''
      AND merged_into IS NULL
    GROUP BY word HAVING variants > 1;
"""

def db() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    # the repaired v_conflicts must reach EXISTING dbs too — IF NOT EXISTS
    # alone would keep the ghost view forever, so the view is dropped first
    con.execute("DROP VIEW IF EXISTS v_conflicts")
    con.executescript(SCHEMA)
    # graft #8: existing dbs get the kind/stratum columns — CREATE TABLE
    # IF NOT EXISTS alone would leave them untyped forever
    cols = {r["name"] for r in con.execute("PRAGMA table_info(docs)")}
    if "kind" not in cols:
        con.execute("ALTER TABLE docs ADD COLUMN kind TEXT")
    if "stratum" not in cols:
        con.execute("ALTER TABLE docs ADD COLUMN stratum TEXT")
    return con

def led(con, kind: str, word: str, payload: dict) -> None:
    import datetime
    con.execute("INSERT INTO ledger(ts,kind,word,payload) VALUES (?,?,?,?)",
        (datetime.datetime.now().isoformat(timespec="seconds"), kind,
         word, json.dumps(payload, ensure_ascii=False)))

def canon(word: str) -> str:
    w = unicodedata.normalize("NFC", word.strip().lower())
    return re.sub(r"[^\wčšžćđʎ]", "", w)

# ====================================================== PARSER PLUGINS =====
# Format #4 of your corpus = a new class + one line in PLUGINS. That is the
# whole evolution ceremony. Plugins return raw (word, fields) dicts; the
# engine does the storing, grading, dedup — plugins stay dumb.

@dataclass
class Parsed:
    word: str
    lineno: int
    number: Optional[int] = None
    thesis: str = ""; antithesis: str = ""; synthesis: str = ""
    foneticni_rez: str = ""; ontoloski_pomen: str = ""
    antinoma: str = ""; glyph: str = ""; prakticna_uporaba: str = ""

class ParserPlugin:
    name: str = "base"
    def parse(self, text: str) -> List[Parsed]:
        raise NotImplementedError

class StotnijeBulletParser(ParserPlugin):
    """FORMAT A (measured): #### **12. Strah** + - **Fonetični rez:** ..."""
    name = "A-bullet"
    HEAD = re.compile(r"^#{2,6}\s*\**(\d+)\.\s*(.+?)\**\s*$")
    FIELD = re.compile(r"^\s*-\s*\*\*(.+?)[:：]?\*\*\s*[:：]?\s*(.*)$")  # scar 24.9. (same as digest.py): colon INSIDE the bold (**Fonetični rez:**); the traced selftest was written around this failure
    MAP = {"fonetični rez": "foneticni_rez", "ontološki pomen": "ontoloski_pomen",
           "antinoma": "antinoma", "sinteza": "synthesis",
           "glyph": "glyph", "praktična uporaba": "prakticna_uporaba"}
    def parse(self, text):
        out, cur, curline = [], None, 0
        for i, line in enumerate(text.splitlines(), 1):
            h = self.HEAD.match(line)
            if h:
                if cur: out.append(cur)
                cur = Parsed(word=h.group(2).strip(), number=int(h.group(1)),
                             lineno=curline)
                curline = i; continue
            f = self.FIELD.match(line)
            if f and cur:
                k = self.MAP.get(f.group(1).strip().lower())
                v = f.group(2).strip().strip("*").strip()
                if k: setattr(cur, k, v)
                continue
            if line.strip().startswith("---") and cur:
                out.append(cur); cur = None
        if cur: out.append(cur)
        return out

class HeadlineParser(ParserPlugin):
    """FORMAT B (measured): 26. **Afirmacija** – t ↔ a → **s**  (no body)"""
    name = "B-headline"
    HEAD = re.compile(
        r"^\s*(\d+)\.\s*\**(\S.*?)\**\s*[–-]\s*(.+?)\s*↔\s*(.+?)\s*→\s*\**(.+?)\**\s*$")
    def parse(self, text):
        out = []
        for i, line in enumerate(text.splitlines(), 1):
            m = self.HEAD.match(line)
            if m:
                out.append(Parsed(number=int(m.group(1)), word=m.group(2).strip(),
                                 thesis=m.group(3).strip(),
                                 antithesis=m.group(4).strip(),
                                 synthesis=m.group(5).strip(), lineno=i))
        return out

class NumberedSectionParser(ParserPlugin):
    """FORMAT C (documented on-disk): head + '1. Fonetični rez' sections."""
    name = "C-numbered"
    HEAD = re.compile(
        r"^\s*(\d+)\.\s*\**(\S.*?)\**\s*[–-]\s*(.+?)\s*↔\s*(.+?)\s*→\s*\**(.+?)\**\s*$")
    SEC = re.compile(r"^\s*([1-4])\.\s*(.*)$")
    MAP = {"1": "foneticni_rez", "2": "ontoloski_pomen",
           "3": "antinoma", "4": "synthesis"}
    def parse(self, text):
        out, cur, sec = [], None, None
        for i, line in enumerate(text.splitlines(), 1):
            h = self.HEAD.match(line)
            if h:
                if cur: out.append(cur)
                cur = Parsed(number=int(h.group(1)), word=h.group(2).strip(),
                             thesis=h.group(3).strip(),
                             antithesis=h.group(4).strip(),
                             synthesis=h.group(5).strip(), lineno=i)
                sec = None; continue
            s = self.SEC.match(line)
            if s and cur:
                sec = self.MAP.get(s.group(1)); v = s.group(2).strip()
                if sec: setattr(cur, sec, v)
                continue
            if cur and sec and line.strip():
                setattr(cur, sec, (getattr(cur, sec) or "") + " " + line.strip())
        if cur: out.append(cur)
        return out


class RezFragmentParser(ParserPlugin):
    """FORMAT D (measured 26. 9., grounded in the actual files across 15
    strata — C2/C1/Obj1/Obj2/B2/Basics...): the rozetni-kamni inline dosje.

        **WORD** (gloss) — [fonetični] rez:

        | Fragment | Pomen |
        |---|---|
        | **FRAG** | meaning of the fragment |

        Branje: WORD = the full reading.

    Mapping: word=the bold word · thesis=the paren gloss (etymology) ·
    foneticni_rez=fragments joined ' / ' (fragment labels, parens stripped
    — KIN (金) → KIN) · ontoloski_pomen=the fragment meanings, '; '-joined ·
    synthesis=the Branje line. Grade: headline when gloss+Branje exist,
    draft when bare — honest, the format carries no antinoma."""
    name = "D-rez"
    HEAD = re.compile(r"^\*\*(?:(?:(.+?)\*\*\s*(\([^)]*\))?\s*[—–-]+\s*"
                      r"(?:fonetični\s+)?rez\s*[:：]?\s*$"
                      r"|Fonetični\s+rez\s+besede\s+(.+?)\s*[:：]?\s*\**\s*$))",
                      re.IGNORECASE)
    ROW = re.compile(r"^\|\s*\*\*(.+?)\*{0,2}\s*\|\s*([^|]*?)\s*\|")
    BRANJE = re.compile(r"^\s*\**\s*Branje\b\s*\**\s*[:：]\s*\**\s*(.+?)"
                        r"\s*\**\s*$", re.IGNORECASE)

    def parse(self, text: str) -> List[Parsed]:
        out: List[Parsed] = []
        cur: Optional[Parsed] = None
        gloss, frags, means, branje = "", [], [], ""

        def flush():
            nonlocal cur, gloss, frags, means, branje
            if cur is None:
                return
            if frags:
                cur.foneticni_rez = " / ".join(frags)
            if means:
                cur.ontoloski_pomen = "; ".join(means)
            cur.thesis = gloss.replace("**", "")
            cur.synthesis = branje.replace("**", "")
            out.append(cur)
            cur, gloss, frags, means, branje = None, "", [], [], ""

        for i, line in enumerate(text.splitlines(), 1):
            h = self.HEAD.match(line)
            if h:
                flush()
                word = (h.group(1) or h.group(3) or "").strip()
                word = word.rstrip(":：").strip("*").strip()
                gloss = (h.group(2) or "").strip("() \t")
                cur = Parsed(word=word, lineno=i)
                continue
            if cur is None:
                continue
            m = self.BRANJE.match(line)
            if m:
                branje = m.group(1).strip()
                continue
            r = self.ROW.match(line)
            if r:
                frag = re.sub(r"\s*\([^)]*\)\s*", " ",
                              r.group(1).strip()).strip()
                mean = r.group(2).strip()
                if frag and mean and not set(frag) <= {"-", ":", " ", ""}:
                    frags.append(frag)
                    means.append(mean)
                continue
            # the entry CLOSES at the first content line that is neither
            # table row nor Branje — rows never leak into unrelated tables
            if frags and line.strip():
                flush()
        flush()
        return out

PLUGINS: List[ParserPlugin] = [StotnijeBulletParser(), HeadlineParser(),
                               NumberedSectionParser(),
                               RezFragmentParser()]
# EVOLUTION POINT: append MyFormatEParser() here. Nothing else changes.
# (26. 9.: the point was used for D — measured first: **WORD** (gloss) —
# rez: + | Fragment | Pomen | table + Branje: line, seen across 15 strata)

def grade_of(p: Parsed) -> str:
    if p.foneticni_rez and p.ontoloski_pomen and p.antinoma and p.synthesis:
        return "reported"
    if p.synthesis and (p.thesis or p.number):
        return "headline"
    return "draft"

# =========================================================== INGEST =======

def scan(root: Path, con: sqlite3.Connection) -> dict:
    # scar 26. 9.: a rescan passed the root as '..', so every stored
    # ABSOLUTE path looked new and the whole corpus was parsed twice
    # (measured: 1,191 duplicate docs — recovered from the pre-scan
    # backup). Repair: the root resolves, paths always meet absolute.
    root = Path(root).resolve()
    files = [p for p in root.rglob("*") if p.suffix.lower()
             in {".md", ".txt"}]
    # the ledger is the only thing that cannot be rebuilt from source —
    # back the db up before any scan writes to it
    import shutil
    if Path(DB_PATH).exists():
        shutil.copy2(DB_PATH, f"{DB_PATH}.bak")
    n_docs = n_entries = 0
    for f in files:
        cur = con.execute("SELECT doc_id FROM docs WHERE path=?", (str(f),))
        row = cur.fetchone()
        if row:
            continue                      # idempotent: new files only, for now
        text = f.read_text(encoding="utf-8", errors="replace")
        c = con.execute("INSERT INTO docs(path,mtime,raw_size) VALUES (?,?,?)",
                        (str(f), f.stat().st_mtime, len(text)))
        doc_id, n_docs = c.lastrowid, n_docs + 1
        for plugin in PLUGINS:
            for p in plugin.parse(text):
                if not p.word:
                    continue
                con.execute("""INSERT INTO entries
                    (doc_id,word,format,number,thesis,antithesis,synthesis,
                     foneticni_rez,ontoloski_pomen,antinoma,glyph,
                     prakticna_uporaba,lineno,grade)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (doc_id, p.word, plugin.name, p.number, p.thesis,
                     p.antithesis, p.synthesis, p.foneticni_rez,
                     p.ontoloski_pomen, p.antinoma, p.glyph,
                     p.prakticna_uporaba, p.lineno, grade_of(p)))
                n_entries += 1
        # stratum 3, cheap: every capitalized word mentions something
        for m in re.findall(r"\b([A-ZČŠŽ][a-zčšžćđ]{3,})\b", text):
            con.execute("INSERT INTO mentions VALUES ((SELECT entry_id "
                        "FROM entries WHERE doc_id=? ORDER BY entry_id DESC "
                        "LIMIT 1), ?)", (doc_id, canon(m)))
        # graft #8: what this text IS, where it OCCUPIES — typed at admission
        rel = f.relative_to(root)
        stratum = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        fmts = [r[0] for r in con.execute(
            "SELECT DISTINCT format FROM entries WHERE doc_id=?", (doc_id,))]
        con.execute("UPDATE docs SET kind=?, stratum=? WHERE doc_id=?",
                    (doc_kind(stratum, text, fmts), stratum, doc_id))
    led(con, "scan", None, {"root": str(root), "files": len(files),
                            "new_docs": n_docs, "new_entries": n_entries})
    con.commit()
    return {"files": len(files), "new_docs": n_docs, "new_entries": n_entries}

# ========================================================== THE PAGE ======

def page(con, word: str) -> dict:
    # scar 26. 9. (found by graft #3): the old lookup matched canon(word)
    # against lower(word) — any word carrying a space or punctuation (2047
    # of 2176 live words) returned an empty page. Canon must meet canon;
    # SQLite has no canon(), so the comparison lives here in Python.
    w = canon(word)
    entries = [dict(r) for r in con.execute(
        "SELECT e.*, d.kind AS doc_kind, d.stratum AS doc_stratum "
        "FROM entries e JOIN docs d ON d.doc_id = e.doc_id")
              if canon(r["word"]) == w or canon(r["merged_into"] or "") == w]
    mentions = con.execute("SELECT COUNT(*) FROM mentions WHERE mention=?",
                          (w,)).fetchone()[0]
    return {"word": word, "entries": entries, "mentions": mentions,
            "conflicts": [dict(r) for r in con.execute(
                "SELECT * FROM v_conflicts WHERE word=?" , (word,))]}

# ========================================================== MERGE ========
# The load-lightener. Three levels of "repeating shit", handled separately:
#   1. DUPLICATE FILES   — same content, different name/path (copy-paste era).
#                         Detected by content hash. Proposed, never auto-deleted.
#   2. DUPLICATE ENTRIES — same word+synopsis in many files. The KEEPER wins
#                         (richest grade: reported > headline > draft; then
#                         most complete fields). Losers point at keeper via
#                         `merged_into`; nothing is deleted, ever — ledger.
#   3. SAME WORD, DIFFERENT CONTENT — NOT a merge. That's a conflict (see
#                         v_conflicts) and stays yours to rule on.
# Merging is reversible: `unmerge` restores, because the rows never died.

def _fingerprint(p: dict) -> str:
    """Content-identity of an entry: word + the parts that carry meaning."""
    import hashlib
    key = "|".join(canon(x or "") for x in (
        p["word"], p["thesis"], p["antithesis"], p["synthesis"],
        p["foneticni_rez"], p["antinoma"]))
    return hashlib.sha256(key.encode()).hexdigest()[:16]

GRADE_RANK = {"reported": 3, "headline": 2, "draft": 1}

def propose_entry_merges(con) -> List[dict]:
    """Groups duplicate entries by (word, fingerprint). Proposes keepers.
    A proposal, not an action — nothing merges until you confirm."""
    groups = {}
    for r in con.execute("SELECT entry_id, word, format, number, thesis, "
                         "antithesis, synthesis, foneticni_rez, "
                         "ontoloski_pomen, antinoma, glyph, grade, doc_id "
                         "FROM entries WHERE merged_into IS NULL"):
        p = dict(r)
        groups.setdefault((canon(p["word"]), _fingerprint(p)), []).append(p)
    proposals = []
    for (w, fp), entries in groups.items():
        if len(entries) < 2:
            continue
        # HOLLOW FILTER (scar 24.9.: the raw run proposed 586 families, 555 of
        # them parser false-positives — register headings like "N. odprte"
        # parsed as empty dosjes. A count is not a price until each unit is
        # real. A family enters the queue ONLY if a member carries content.)
        if not any(e["foneticni_rez"] or e["ontoloski_pomen"] or e["synthesis"]
                   or e["thesis"] for e in entries):
            continue
        # keeper: richest grade, then most filled fields
        def richness(e):
            filled = sum(1 for k in ("thesis","antithesis","synthesis",
                "foneticni_rez","ontoloski_pomen","antinoma","glyph")
                if e[k])
            return (GRADE_RANK.get(e["grade"], 0), filled)
        ranked = sorted(entries, key=richness, reverse=True)
        keeper, losers = ranked[0], ranked[1:]
        # if keeper isn't strictly richest or ties exist, owner decides
        ambiguous = richness(keeper) == richness(losers[0])
        proposals.append({"word": w, "fingerprint": fp,
                          "keeper": keeper["entry_id"], "keeper_grade":
                          keeper["grade"],
                          "lose": [l["entry_id"] for l in losers],
                          "doc_ids": sorted({e["doc_id"] for e in entries}),
                          "needs_owner": ambiguous})
    return proposals

# ------------------------------------------------- NEAR-DUP DETECTOR -------
# Graft #2, extends _fingerprint(), replaces nothing. The fingerprint groups
# EXACT duplicates (byte-identical meaning fields); this catches the
# copy-paste era's small edits — same word, near-identical fields, one word
# different. A near-dup is ALWAYS needs_owner: the difference is either a
# typo (merge) or a real refinement (conflict), and the machine cannot know
# which. Same proposal shape as propose_entry_merges, so apply_merge and the
# REVIEW ledger-replay treat both queues identically. The family fingerprint
# is derived from the members' fingerprints (order-stable), so a ruling
# found by replay survives rescans.

NEAR_THRESHOLD = 0.85

def _content_key(p: dict) -> str:
    """The meaning-carrying fields of an entry, canonized — what a near-dup
    is near IN. Word is excluded: candidates are compared within one word."""
    return "|".join(canon(x or "") for x in (
        p["thesis"], p["antithesis"], p["synthesis"],
        p["foneticni_rez"], p["antinoma"]))

def propose_near_merges(con, threshold=NEAR_THRESHOLD) -> List[dict]:
    import difflib, hashlib
    by_word = {}
    for r in con.execute("SELECT entry_id, word, format, number, thesis, "
                         "antithesis, synthesis, foneticni_rez, "
                         "ontoloski_pomen, antinoma, glyph, grade, doc_id "
                         "FROM entries WHERE merged_into IS NULL"):
        p = dict(r)
        # hollow filter: same law as the merge queue — no content, no family
        if not (p["foneticni_rez"] or p["ontoloski_pomen"]
                or p["synthesis"] or p["thesis"]):
            continue
        by_word.setdefault(canon(p["word"]), []).append(p)
    proposals = []
    for w, entries in by_word.items():
        # union-find: near-identity is not transitive-proof, so chains of
        # pairwise similarity form one family (a≈b, b≈c ⇒ one family)
        parent = {e["entry_id"]: e["entry_id"] for e in entries}
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        for i, a in enumerate(entries):
            for b in entries[i + 1:]:
                if _fingerprint(a) == _fingerprint(b):
                    continue          # exact dup: the merge queue owns it
                sim = difflib.SequenceMatcher(
                    None, _content_key(a), _content_key(b)).ratio()
                if sim < threshold:
                    continue
                ra, rb = find(a["entry_id"]), find(b["entry_id"])
                if ra != rb:
                    parent[ra] = rb
        fams = {}
        for e in entries:
            fams.setdefault(find(e["entry_id"]), []).append(e)
        for members in fams.values():
            if len(members) < 2:
                continue
            def richness(e):
                filled = sum(1 for k in ("thesis", "antithesis", "synthesis",
                    "foneticni_rez", "ontoloski_pomen", "antinoma", "glyph")
                    if e[k])
                return (GRADE_RANK.get(e["grade"], 0), filled)
            ranked = sorted(members, key=richness, reverse=True)
            keeper, losers = ranked[0], ranked[1:]
            gfp = "|".join(sorted(_fingerprint(e) for e in members))
            sim = max(difflib.SequenceMatcher(
                None, _content_key(a), _content_key(b)).ratio()
                for i, a in enumerate(members) for b in members[i + 1:])
            proposals.append({"word": w,
                "fingerprint": hashlib.sha256(gfp.encode()).hexdigest()[:16],
                "keeper": keeper["entry_id"], "keeper_grade": keeper["grade"],
                "lose": [l["entry_id"] for l in losers],
                "doc_ids": sorted({e["doc_id"] for e in members}),
                "needs_owner": True, "near": True, "similarity": round(sim, 3)})
    return proposals

def apply_merge(con, proposal: dict) -> None:
    for eid in proposal["lose"]:
        con.execute("UPDATE entries SET merged_into=? WHERE entry_id=?",
                    (canon(proposal["word"]), eid))
    led(con, "merge", proposal["word"], proposal)
    con.commit()

def merge_auto(con) -> dict:
    """Merges only the UNAMBIGUOUS proposals (keeper strictly richest).
    The ambiguous ones stay proposals — your call, not the machine's."""
    ps = propose_entry_merges(con)
    done, kept = 0, []
    for p in ps:
        if p["needs_owner"]:
            kept.append(p)
        else:
            apply_merge(con, p); done += 1
    return {"merged": done, "needs_owner": len(kept),
            "proposals": kept}

def unmerge_all(con, word: str) -> int:
    n = con.execute("UPDATE entries SET merged_into=NULL WHERE merged_into=?",
                    (canon(word),)).rowcount
    led(con, "edit", word, {"action": "unmerge", "restored": n})
    con.commit()
    return n

# ---------------------------------------------------- FILE-LEVEL MERGE ----
# Duplicate FILES get an assistant-generated merge report first: which file
# is the canonical copy, which are byte-identical shadows. You delete with
# your own hand (the engine never deletes from disk); the ledger records
# your ruling.

def dup_file_report(con) -> List[dict]:
    out = []
    for r in con.execute("SELECT path, raw_size FROM docs"):
        h = None
        p = Path(r["path"])
        if p.exists():
            import hashlib
            h = hashlib.md5(p.read_bytes()).hexdigest()
        out.append({"path": r["path"], "md5": h})
    by_hash = {}
    for o in out:
        if o["md5"]:
            by_hash.setdefault(o["md5"], []).append(o["path"])
    return [{"identical_files": paths} for paths in by_hash.values()
            if len(paths) > 1]


# ==================================================== DARK DOCS REPORT ======
# A doc is DARK when no plugin recognized any entry in it (measured 26. 9.:
# 880 of 1,183 docs — three quarters of the corpus). The report splits the
# darkness in two, because the cure differs:
#   markers, no entries  → PARSER GAP: the doc carries dosje fields but no
#                          plugin caught them — repair the existing line
#   no markers           → NEW FORMAT: a different kind of corpus (transcripts,
#                          prose, letters) — a new ParserPlugin, or it stays
#                          honestly dark: prose is prose
# Groups by (extension, first-line shape, markers) so the owner reads
# counts and examples, not 880 paths.

DOSJE_MARKERS = ("fonetični rez", "ontološki pomen", "antinoma", "glyph",
                 "sinteza", "afirmacija", "praktična uporaba")


def _dark_shape(text: str) -> str:
    """Cheap structural signature: what the first non-empty line looks like."""
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("|"):
            return "table"
        if re.match(r"^#{1,6}\s*\**\d+\.", s):
            return "numbered-heading"
        if re.match(r"^#{1,6}\s", s):
            return "heading"
        if re.match(r"^\d+[\.\)]\s", s):
            return "numbered-line"
        if s.startswith(("- ", "* ", "•")):
            return "bullet"
        return "prose"
    return "empty"


def doc_kind(stratum: str, text: str, formats) -> str:
    """Graft #8 — WHAT a text IS. Content-based, honest, cheap:
       derived     the canon_ruled stratum — the canon feeding itself
       dosje-A/B/C a dosje, parsed by that plugin (+ when formats mix)
       dosje-D     dark but carrying dosje markers — the parser gap
       empty       nothing but whitespace
       notes/prose dark without markers — theory, transcripts, letters;
                   prose is prose: honestly dark until a plugin learns it
    WHERE a text occupies is its stratum (top dir under the scan root) —
    computed by the caller, visible everywhere a doc is named."""
    if stratum == "canon_ruled":
        return "derived"
    if formats:
        return "dosje-" + "+".join(sorted({f.split("-")[0] for f in formats}))
    if any(m in text.lower() for m in DOSJE_MARKERS):
        return "dosje-D"
    if _dark_shape(text) == "empty":
        return "empty"
    if _dark_shape(text) in ("heading", "numbered-heading"):
        return "notes"
    return "prose"


def dark_report(con) -> dict:
    groups = {}
    gone = 0
    for r in con.execute(
            "SELECT doc_id, path, raw_size FROM docs WHERE doc_id NOT IN "
            "(SELECT DISTINCT doc_id FROM entries)"):
        p = Path(r["path"])
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            gone += 1
            continue
        low = text.lower()
        markers = [m for m in DOSJE_MARKERS if m in low]
        key = (p.suffix.lower(), _dark_shape(text), bool(markers))
        g = groups.setdefault(key, {
            "ext": key[0], "shape": key[1],
            "dosje_markers": key[2], "count": 0, "bytes": 0,
            "example": None, "first_line": ""})
        g["count"] += 1
        g["bytes"] += (r["raw_size"] or 0)
        if g["example"] is None:
            g["example"] = str(p)
            g["first_line"] = next((l.strip() for l in text.splitlines()
                                    if l.strip()), "")[:100]
    return {"dark_docs": sum(g["count"] for g in groups.values()),
            "deleted_since_scan": gone,
            "groups": sorted(groups.values(), key=lambda g: -g["count"])}


def retype(con, root: Path) -> dict:
    """Graft #8 backfill: type the docs already scanned (scan types at
    admission; everything admitted before graft #8 was never typed).
    Idempotent — re-running re-derives the same facts. One summary ledger
    line, not one per doc; the db is backed up first, same law as scan."""
    import shutil
    if Path(DB_PATH).exists():
        shutil.copy2(DB_PATH, f"{DB_PATH}.bak")
    root = Path(root).resolve()
    typed = gone = outside = 0
    for r in con.execute("SELECT doc_id, path FROM docs").fetchall():
        p = Path(r["path"])
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            gone += 1
            continue
        try:
            rel = p.relative_to(root)
        except ValueError:
            outside += 1
            continue
        stratum = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        fmts = [x[0] for x in con.execute(
            "SELECT DISTINCT format FROM entries WHERE doc_id=?",
            (r["doc_id"],))]
        con.execute("UPDATE docs SET kind=?, stratum=? WHERE doc_id=?",
                    (doc_kind(stratum, text, fmts), stratum, r["doc_id"]))
        typed += 1
    led(con, "retype", None, {"root": str(root), "typed": typed,
                              "unreadable": gone, "outside_root": outside})
    con.commit()
    return {"typed": typed, "unreadable": gone, "outside_root": outside}


def census(con) -> dict:
    """Graft #8's composed fact: what the corpus IS, at a glance —
    stratum × kind × count, plus the dark share per stratum."""
    out = {}
    for r in con.execute(
            "SELECT stratum, kind, COUNT(*) n FROM docs "
            "WHERE kind IS NOT NULL GROUP BY stratum, kind "
            "ORDER BY stratum, kind"):
        out.setdefault(r["stratum"] or "(untyped)", {})[r["kind"]] = r["n"]
    return out


def reparse(con) -> dict:
    """Graft #9 — the dark corpus, re-read with the CURRENT plugins.
    scan() only admits NEW files; docs scanned before a plugin existed
    stay dark forever without this. LAWS: only docs with ZERO entries are
    parsed (a lit doc is never re-parsed — no duplicates by construction);
    new entries inserted exactly as scan inserts them; lit docs are
    re-typed; one summary ledger line; db backed up first, same law as
    scan. Mentions are NOT re-derived (stratum 3 belongs to scan)."""
    import shutil
    if Path(DB_PATH).exists():
        shutil.copy2(DB_PATH, f"{DB_PATH}.bak")
    dark = [dict(r) for r in con.execute(
        "SELECT doc_id, path, stratum FROM docs WHERE doc_id NOT IN "
        "(SELECT DISTINCT doc_id FROM entries)")]
    lit = new_entries = 0
    for d in dark:
        try:
            text = Path(d["path"]).read_text(encoding="utf-8",
                                            errors="replace")
        except OSError:
            continue
        got = 0
        for plugin in PLUGINS:
            for p in plugin.parse(text):
                if not p.word:
                    continue
                con.execute("""INSERT INTO entries
                    (doc_id,word,format,number,thesis,antithesis,synthesis,
                     foneticni_rez,ontoloski_pomen,antinoma,glyph,
                     prakticna_uporaba,lineno,grade)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (d["doc_id"], p.word, plugin.name, p.number, p.thesis,
                     p.antithesis, p.synthesis, p.foneticni_rez,
                     p.ontoloski_pomen, p.antinoma, p.glyph,
                     p.prakticna_uporaba, p.lineno, grade_of(p)))
                got += 1
        if got:
            lit += 1
            new_entries += got
            fmts = [r[0] for r in con.execute(
                "SELECT DISTINCT format FROM entries WHERE doc_id=?",
                (d["doc_id"],))]
            con.execute("UPDATE docs SET kind=? WHERE doc_id=?",
                        (doc_kind(d["stratum"] or "(root)", text, fmts),
                         d["doc_id"]))
    led(con, "reparse", None, {"dark_before": len(dark), "lit": lit,
                               "new_entries": new_entries})
    con.commit()
    return {"dark_before": len(dark), "lit": lit, "new_entries": new_entries}


def xcheck(con, lex_path) -> dict:
    """Graft #10 — the two truth layers, finally checked against each
    other: lexicon.json (the 40-word truth) vs soul.db's pages for the
    same words. Agreement is a receipt; disagreement is YOURS to rule —
    named here, never auto-fixed. rez is compared canon-meets-canon
    (separators die); antinoma canon-to-canon; glyph by its symbol head
    only ('⊘ (praznina...)' vs '⊘ (tok...)' is the SAME glyph — glosses
    differ honestly); pomen is shown side by side, never machine-diffed.
    Words whose live page disagrees on rez are already conflict-queue
    material — this report names them all in one place."""
    def norm(s):
        return re.sub(r"[^a-z0-9čšžćđʎ]", "", (s or "").lower())

    def glyph_head(s):
        return norm((s or "").split("(")[0])

    lex = json.loads(Path(lex_path).read_text(encoding="utf-8"))
    per, agree, disagree, thin = [], 0, 0, 0
    for key, w in sorted(lex.items()):
        if not isinstance(w, dict):
            continue
        word = w.get("word") or key
        p = page(con, word)
        live = [e for e in p["entries"] if not e.get("merged_into")]
        if not live:
            per.append({"word": word, "in_corpus": False,
                        "live_entries": 0})
            continue
        lex_rez = norm(w.get("source_form"))
        rezs = {norm(e["foneticni_rez"]) for e in live
                if (e["foneticni_rez"] or "").strip()}
        rez_ok = (lex_rez in rezs) if lex_rez else None
        lex_ant = norm(w.get("antinoma"))
        ants = {norm(e["antinoma"]) for e in live
                if (e["antinoma"] or "").strip()}
        ant_ok = (lex_ant in ants) if lex_ant else None
        lex_gl = glyph_head(w.get("glyph"))
        gls = {glyph_head(e["glyph"]) for e in live
               if (e["glyph"] or "").strip()}
        gl_ok = (lex_gl in gls) if lex_gl else None
        checks = [c for c in (rez_ok, ant_ok, gl_ok) if c is not None]
        if not checks:
            thin += 1
        elif all(checks):
            agree += 1
        else:
            disagree += 1
        per.append({"word": word, "in_corpus": True,
                    "live_entries": len(live),
                    "rez": rez_ok, "antinoma": ant_ok, "glyph": gl_ok})
    return {"lexicon_words": len(per), "agree": agree,
            "disagree": disagree, "thin_no_overlap": thin,
            "not_in_corpus": sum(1 for x in per if not x["in_corpus"]),
            "per_word": per}



# ========================================================== GUI (Textual) =

def gui() -> None:
    from textual.app import App, ComposeResult
    from textual.widgets import Input, ListView, ListItem, Label, Footer, Header

    con = db()

    class Assistant(App):
        CSS = "Input {height: 3} #detail {padding: 1}"
        BINDINGS = [("q", "quit", "quit")]
        def compose(self) -> ComposeResult:
            yield Header()
            yield Input(placeholder="search a word… (ljubezen)")
            yield ListView(id="words")
            yield Label(id="detail")
            yield Footer()
        async def on_input_changed(self, ev) -> None:
            lv = self.query_one("#words", ListView)
            lv.clear()
            q = f"%{ev.value}%"
            for r in con.execute("SELECT word, sources, formats, reported, "
                                 "headline FROM v_page WHERE word LIKE ? "
                                 "ORDER BY sources DESC LIMIT 50", (q,)):
                lv.append(ListItem(Label(
                    f"{r['word']}  ·  {r['sources']} src · {r['formats']}")))
        async def on_list_view_selected(self, ev) -> None:
            word = str(ev.item.children[0].renderable).split(" ")[0]
            p = page(con, word)
            lines = [f"# {word.upper()}  ({p['mentions']} mentions)"]
            for e in p["entries"]:
                lines.append(f"\n[{e['format']}/{e['grade']}] "
                             f"{e['synthesis'] or ''}\n"
                             f"  rez: {e['foneticni_rez'] or '—'} | "
                             f"pomen: {e['ontoloski_pomen'] or '—'} | "
                             f"antinoma: {e['antinoma'] or '—'} | "
                             f"glyph: {e['glyph'] or '—'}\n"
                             f"  {e['doc_id']}:{e['lineno']}")
            if p["conflicts"]:
                lines.append("\n⚠ CONFLICT: " + json.dumps(
                    p["conflicts"], ensure_ascii=False))
            self.query_one("#detail", Label).update("\n".join(lines))
    Assistant().run()

# ============================================================ EXPORT ======
# The Godot surface: one JSON graph, one GraphML. Game reads, engine never
# knows the game exists.

def export(con, out: Path) -> dict:
    words = [dict(r) for r in con.execute("SELECT * FROM v_page")]
    nodes = [{"word": w["word"], "sources": w["sources"],
              "reported": w["reported"], "headline": w["headline"]}
             for w in words]
    edges = [{"a": w["word"], "b": m["word"], "kind": "antinoma-of"}
             for w in words for m in con.execute(
                 "SELECT DISTINCT e2.word FROM entries e1 "
                 "JOIN entries e2 ON lower(e2.word)=lower(e1.antinoma) "
                 "WHERE lower(e1.word)=?", (w["word"],))]
    graph = {"nodes": nodes, "edges": edges}
    out.write_text(json.dumps(graph, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    return {"nodes": len(nodes), "edges": len(edges)}


# ================================================ THE RULED PAGE, OUT =====
# Graft #7 — the canon feeding itself. export() writes the graph for OTHERS
# to read; export_page() writes the RULED truth of one word back into the
# corpus as a derived dosje, in the canon_ruled stratum. LAWS:
#   - the file is DERIVED, not source: originals are never touched
#   - it is written in the A-bullet format, so when the stratum is scanned
#     the plugins parse it back at full grade — the loop is testable
#   - the export is a ledger line (kind 'export'), witnessed like everything
#   - re-entry goes through the ordinary door: scan parses it, the dup
#     detector proposes it against its own ancestors, REVIEW rules it again
# The loop: corpus → parse → rule → better version → corpus.

def export_page(con, word: str, out_dir) -> dict:
    def fullness(e):
        return (GRADE_RANK.get(e["grade"], 0),
                sum(1 for k in ("thesis", "antithesis", "synthesis",
                                "foneticni_rez", "ontoloski_pomen",
                                "antinoma", "glyph", "prakticna_uporaba")
                    if (e.get(k) or "").strip()))
    if not word:
        return {"error": "export-page needs --word"}
    p = page(con, word)
    live = [e for e in p["entries"] if not e.get("merged_into")]
    if not live:
        return {"error": f"no live entries for '{word}'"}
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    import datetime
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    lines = [f"# DOSJE — {word} (derived stratum: canon_ruled)", "",
             f"> Derived page, exported {ts} by soul_engine. Not source:",
             "> the originals live where they live. This file re-enters the",
             "> corpus through the ordinary door — scan, parse, REVIEW.",
             "> Export witnessed as a ledger line (kind export).", ""]
    provenance = []
    for n, e in enumerate(sorted(live, key=fullness, reverse=True), 1):
        lines.append(f"#### **{n}. {e['word']}**")
        for label, key in (("Teza", "thesis"), ("Antiteza", "antithesis"),
                           ("Sinteza", "synthesis"),
                           ("Fonetični rez", "foneticni_rez"),
                           ("Ontološki pomen", "ontoloski_pomen"),
                           ("Antinoma", "antinoma"),
                           ("Glyph", "glyph"),
                           ("Praktična uporaba", "prakticna_uporaba")):
            v = (e.get(key) or "").strip()
            if v:
                lines.append(f"- **{label}:** {v}")
        lines.append("")
        provenance.append(f"entry {e['entry_id']} [{e['grade']}/{e['format']}"
                          + (f" · {e['doc_stratum']}/{e['doc_kind']}"
                             if e.get("doc_stratum") else "")
                          + f"] doc {e['doc_id']}:{e['lineno']}")
    lines.append("> Sources (provenance, not parsed): "
                 + "; ".join(provenance))
    if p["conflicts"]:
        lines.append("> CONFLICT standing: the fonetični rez variants above "
                     "are real — ruled 'variants kept', or awaiting ruling.")
    out_path = out_dir / f"{canon(word)}.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    led(con, "export", word, {"file": str(out_path), "entries": len(live),
                              "mentions": p["mentions"]})
    con.commit()
    return {"file": str(out_path), "entries": len(live),
            "mentions": p["mentions"]}

# ============================================================= MAIN =======

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["scan", "gui", "page", "export",
                                    "export-page", "merge", "unmerge",
                                    "dups", "dark", "retype", "census",
                                    "reparse", "xcheck", "selftest"])
    ap.add_argument("path", nargs="?")
    ap.add_argument("--word")
    ap.add_argument("--out", default="soul_graph.json")
    args = ap.parse_args()
    con = db()
    if args.cmd == "scan":
        print(json.dumps(scan(Path(args.path), con), ensure_ascii=False))
    elif args.cmd == "gui":
        gui()
    elif args.cmd == "page":
        print(json.dumps(page(con, args.word), ensure_ascii=False, indent=2))
    elif args.cmd == "export":
        print(json.dumps(export(con, Path(args.out))))
    elif args.cmd == "export-page":
        # graft #7: the ruled page of ONE word, written as a derived dosje
        # into the canon_ruled stratum (path = out dir, default canon_ruled)
        out_dir = Path(args.path) if args.path else Path("canon_ruled")
        print(json.dumps(export_page(con, args.word, out_dir),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "merge":
        # python soul_engine.py merge        → auto-merge unambiguous, list rest
        print(json.dumps(merge_auto(con), ensure_ascii=False, indent=2))
    elif args.cmd == "unmerge":
        print(json.dumps({"restored": unmerge_all(con, args.word)}))
    elif args.cmd == "dups":
        # duplicate FILES report — you delete, the engine only names them
        print(json.dumps(dup_file_report(con), ensure_ascii=False, indent=2))
    elif args.cmd == "dark":
        # dark docs report — which formats the plugins have not learned yet
        print(json.dumps(dark_report(con), ensure_ascii=False, indent=2))
    elif args.cmd == "retype":
        # graft #8 backfill — classify every scanned doc; idempotent
        print(json.dumps(retype(con, Path(args.path) if args.path
                                else Path.cwd()), ensure_ascii=False))
    elif args.cmd == "census":
        # graft #8's composed fact — stratum × kind × count
        print(json.dumps(census(con), ensure_ascii=False, indent=2))
    elif args.cmd == "reparse":
        # graft #9 — dark docs re-read with the CURRENT plugins
        print(json.dumps(reparse(con), ensure_ascii=False))
    elif args.cmd == "xcheck":
        # graft #10 — lexicon.json vs soul.db, the two truth layers compared
        print(json.dumps(xcheck(con, Path(args.path) if args.path
                                else Path("lexicon.json")),
                         ensure_ascii=False, indent=2))
    elif args.cmd == "selftest":
        # quick witness against real measured samples
        a = StotnijeBulletParser().parse(
            "#### **12. Strah**\n- **Fonetični rez:** s / t / r / a / h\n"
            "- **Antinoma:** pogum\n- **Sinteza:** **varovalo**\n"
            "- **Glyph:** ⊘\n---\n")
        b = HeadlineParser().parse(
            "26. **Afirmacija** – pritrditev ↔ zanikanje → **ustvarjalna meja**\n")
        assert a[0].word == "Strah" and a[0].glyph == "⊘"
        assert grade_of(a[0]) == "headline"          # pomen missing → not reported
        assert b[0].thesis == "pritrditev" and grade_of(b[0]) == "headline"
        assert canon("LJUBEZEN!") == "ljubezen"
        # graft #9: format D — **WORD** (gloss) — rez: + fragment table + Branje
        d = RezFragmentParser().parse(
            "**GEO** (gola zemlja) — rez:\n\n| Fragment | Pomen |\n|---|---|\n"
            "| **GEO (γῆ)** | zemlja, telo sveta |\n\n"
            "Branje: GEO = tla, ki gleda.\n")
        assert d[0].word == "GEO" and d[0].thesis == "gola zemlja"
        assert d[0].foneticni_rez == "GEO"
        assert "telo sveta" in d[0].ontoloski_pomen
        assert d[0].synthesis == "GEO = tla, ki gleda."
        assert grade_of(d[0]) == "headline"        # gloss + Branje present
        # graft #2: near-dup detector. Same word, one word edited — the exact
        # fingerprint splits it, the similarity test re-unites it as a family.
        m = sqlite3.connect(":memory:")
        m.row_factory = sqlite3.Row
        m.executescript(SCHEMA)
        m.execute("INSERT INTO docs(doc_id, path) VALUES (1, 'x.md')")
        base = "INSERT INTO entries(doc_id, word, format, thesis, " \
               "foneticni_rez, grade) VALUES (1, 'dih', 't', ?, 'd/i/h', 'reported')"
        m.execute(base, ("dihanje kot zanka",))
        m.execute(base, ("dihanje kot zanka v ritmu",))   # the small edit
        m.execute(base, ("nekaj čisto drugega",))         # not near: excluded
        near = propose_near_merges(m)
        assert len(near) == 1 and near[0]["word"] == "dih"
        assert near[0]["needs_owner"] and near[0]["near"]
        assert 0.85 <= near[0]["similarity"] < 1.0
        assert len(propose_entry_merges(m)) == 0      # exact queue stays empty
        # scar 26. 9.: page() must find words that canon() changes — a word
        # with spaces/punctuation used to return an empty page
        m.execute("INSERT INTO entries(doc_id, word, format, thesis, grade) "
                  "VALUES (1, 'NUJNE NAPAKE!', 't', 'x', 'reported')")
        assert len(page(m, "nujne napake")["entries"]) == 1
        # scar 26. 9.: v_conflicts counted empty-string rez (and merged
        # losers) as variants — 26 of 27 "conflicts" were ghosts
        m.execute("INSERT INTO entries(doc_id, word, format, foneticni_rez, grade) "
                  "VALUES (1, 'X', 't', '', 'draft')")
        m.execute("INSERT INTO entries(doc_id, word, format, foneticni_rez, grade) "
                  "VALUES (1, 'X', 't', 'x / x', 'reported')")
        assert m.execute("SELECT COUNT(*) FROM v_conflicts WHERE word='X'"
                         ).fetchone()[0] == 0
        m.execute("INSERT INTO entries(doc_id, word, format, foneticni_rez, grade) "
                  "VALUES (1, 'Y', 't', 'a / a', 'reported')")
        m.execute("INSERT INTO entries(doc_id, word, format, foneticni_rez, grade) "
                  "VALUES (1, 'Y', 't', 'b / b', 'draft')")
        m.execute("INSERT INTO entries(doc_id, word, format, foneticni_rez, grade, "
                  "merged_into) VALUES (1, 'Y', 't', 'c / c', 'draft', 'y')")
        assert m.execute("SELECT COUNT(*) FROM v_conflicts WHERE word='Y'"
                         ).fetchone()[0] == 1   # live truth only, loser ignored
        # dark report: a prose file with no dosje markers is honestly dark
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            fp = Path(td) / "dark.txt"
            fp.write_text("hello darkness, my old friend\n", encoding="utf-8")
            m.execute("INSERT INTO docs(path) VALUES (?)", (str(fp),))
            rep = dark_report(m)
            assert rep["dark_docs"] == 1 and rep["groups"][0]["shape"] == "prose"
            assert rep["groups"][0]["dosje_markers"] is False
        # graft #7: a ruled page exports as a derived dosje and RE-PARSES —
        # the canon feeding itself must close the loop at full grade
        m.execute("INSERT INTO entries(doc_id, word, format, thesis, "
                  "synthesis, foneticni_rez, ontoloski_pomen, antinoma, "
                  "grade) VALUES (1, 'Nujne napake', 't', 'tez', 'sint', "
                  "'n / u', 'pomen', 'napake', 'reported')")
        with tempfile.TemporaryDirectory() as td:
            r = export_page(m, "NUJNE NAPAKE!", td)
            assert "error" not in r and r["entries"] == 2   # both live pages
            text = Path(r["file"]).read_text(encoding="utf-8")
            back = StotnijeBulletParser().parse(text)
            assert len(back) == 2
            top = next(b for b in back if grade_of(b) == "reported")
            assert top.word == "Nujne napake"
            assert top.foneticni_rez == "n / u"
            assert top.ontoloski_pomen == "pomen"
            assert top.antinoma == "napake" and top.synthesis == "sint"
            assert grade_of(top) == "reported"   # full grade survives
            assert m.execute("SELECT COUNT(*) FROM ledger WHERE "
                             "kind='export'").fetchone()[0] == 1
        # scar 26. 9.: scan() must key on ABSOLUTE paths — a relative root
        # used to re-parse the whole corpus as "new" (measured: 1,191
        # duplicate docs, recovered from the pre-scan backup)
        with tempfile.TemporaryDirectory() as td:
            DB_PATH = Path(td) / "scratch.db"   # backup must not touch real
            (Path(td) / "a.md").write_text(
                "#### **1. Strah**\n- **Fonetični rez:** s / t / r / a / h\n",
                encoding="utf-8")
            m2 = sqlite3.connect(":memory:")
            m2.row_factory = sqlite3.Row
            m2.executescript(SCHEMA)
            assert scan(Path(td), m2)["new_docs"] == 1
            assert scan(Path(td), m2)["new_docs"] == 0        # idempotent
            cwd = os.getcwd()
            os.chdir(td)
            try:
                assert scan(Path("."), m2)["new_docs"] == 0   # relative: no dup
            finally:
                os.chdir(cwd)
            assert m2.execute("SELECT COUNT(*) FROM docs").fetchone()[0] == 1
            assert m2.execute("SELECT COUNT(*) FROM entries").fetchone()[0] == 1
            # graft #8: typed at admission — what it is, where it occupies
            row = m2.execute("SELECT kind, stratum FROM docs").fetchone()
            assert row["kind"] == "dosje-A" and row["stratum"] == "(root)"
            # graft #8: existing dbs migrate — old docs table gains the columns
            old = sqlite3.connect(str(DB_PATH))
            old.execute("CREATE TABLE IF NOT EXISTS docs (doc_id INTEGER "
                        "PRIMARY KEY, path TEXT UNIQUE NOT NULL, mtime TEXT, "
                        "raw_size INTEGER)")
            old.commit()
            old.close()
            con2 = db()
            mcols = {r["name"] for r in con2.execute("PRAGMA table_info(docs)")}
            assert {"kind", "stratum"} <= mcols
            con2.close()   # Windows: an open sqlite file cannot be deleted
            # graft #8: the classifier — what a text IS
            assert doc_kind("canon_ruled", "x", []) == "derived"
            assert doc_kind("A2", "#### **1. Strah**\n", ["A-bullet"]) == "dosje-A"
            assert doc_kind("A2", "x", ["A-bullet", "C-numbered"]) == "dosje-A+C"
            assert doc_kind("B2", "**X** — fonetični rez:\n| a |\n|---|\n| b |",
                            []) == "dosje-D"
            assert doc_kind("Rohonc", "plain words, no markers at all\n",
                            []) == "prose"
            assert doc_kind("A5", "# Title\n\nbody\n", []) == "notes"
            assert doc_kind("X", "\n\n", []) == "empty"
            # graft #9: a dark doc lights up with the CURRENT plugins — once
            (Path(td) / "dark_rez.md").write_text(
                "**GEO** (gola zemlja) — rez:\n\n| Fragment | Pomen |\n"
                "|---|---|\n| **GEO (γῆ)** | zemlja, telo sveta |\n\n"
                "Branje: GEO = tla, ki gleda.\n", encoding="utf-8")
            m.execute("INSERT INTO docs(path, stratum) VALUES (?, '(root)')",
                      (str(Path(td) / "dark_rez.md"),))
            rp = reparse(m)
            assert rp["lit"] == 1 and rp["new_entries"] == 1
            assert m.execute("SELECT COUNT(*) FROM entries WHERE "
                             "format='D-rez'").fetchone()[0] == 1
            rp2 = reparse(m)
            assert rp2["new_entries"] == 0    # idempotent: lit stays lit
            # graft #10: the two truth layers — agree and disagree both named
            lx = Path(td) / "lex.json"
            lx.write_text(json.dumps({
                "geo": {"word": "GEO", "source_form": "g / e",
                        "antinoma": None, "glyph": None},
                "dih": {"word": "Dih", "source_form": "d / i / h",
                        "antinoma": None, "glyph": None},
                "nikoli": {"word": "Nikoli", "source_form": "n / i",
                           "antinoma": None, "glyph": None}}),
                encoding="utf-8")
            xc = xcheck(m, lx)
            assert xc["agree"] == 1 and xc["disagree"] == 1
            assert xc["not_in_corpus"] == 1
            geo = next(x for x in xc["per_word"] if x["word"] == "GEO")
            assert geo["rez"] is False          # lex says g/e, corpus says GEO
            dihx = next(x for x in xc["per_word"] if x["word"] == "Dih")
            assert dihx["rez"] is True         # canon meets canon: d/i/h == dih
        print("selftest: plugins A/B/D, grading, canon, near-dup, page, "
              "conflicts-view, dark, page-export, scan-absolute, doc-typing, "
              "reparse, xcheck — OK (traced here, witnessed on disk)")