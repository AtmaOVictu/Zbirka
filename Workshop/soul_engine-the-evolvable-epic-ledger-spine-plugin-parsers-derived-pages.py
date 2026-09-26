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
    kind      TEXT NOT NULL,   -- scan|verdict|merge|edit|grade|export|retype|reparse|drafts
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
    ipa       TEXT,                   -- the MEASURED pronunciation (Luka's
                                     -- "v celoti v IPA", 26. 9.): a SECOND
                                     -- organ beside foneticni_rez (the CUT
                                     -- stays native — d/i/h is the rez, /diː/
                                     -- is the izmera; two organs, two fields)
    lineno    INTEGER,                 -- provenance: find it again
    grade     TEXT NOT NULL DEFAULT 'reported',
    merged_into TEXT                   -- loser points at the keeper's word
);
CREATE INDEX IF NOT EXISTS idx_entries_word ON entries(word);
-- mentions: DOC-LEVEL edges (Luka's "oboje", 26. 9. 2026 — the old
-- entry-tagging piled a doc's whole mention-load onto its LAST entry,
-- 96k rows pointed at nothing: noise). A mention belongs to the
-- DOCUMENT; page() counts docs mentioning the word. Edges point, they
-- never judge — the citation-graph foundation.
CREATE TABLE IF NOT EXISTS mentions (
    doc_id    INTEGER,               -- the document that mentions
    mention   TEXT
);
CREATE INDEX IF NOT EXISTS idx_mentions ON mentions(mention);
-- graft: parser-zakonov (sealed by Luka's 'daj', 26. 9. 2026): ZAKONI SO
-- LOČENA VRSTA DOKUMENTA — a separate table, never entries. The key is
-- the BODY WITH ITS WITNESS (doc + line); the number is a LABEL (parallel
-- sessions may seal the same number — both bodies stay). VEZI are graph
-- edges: they point, they never judge. The parser is a reader, never a
-- writer (append-only bodies, swapped counters — atomarni).
CREATE TABLE IF NOT EXISTS zakoni (
    zid           INTEGER PRIMARY KEY AUTOINCREMENT,
    doc_id        INTEGER NOT NULL REFERENCES docs,
    series        TEXT NOT NULL,       -- rez | dokaz | sodba | ubod | šiv
    number        INTEGER,            -- LABEL, never the key
    title         TEXT,
    actor         TEXT,
    teza          TEXT,
    meritev       TEXT,               -- ⊘(κ · χ · μ · ℜ · ν) — as written
    nujne_napake  TEXT,
    odprta_partial TEXT,
    vezi          TEXT,               -- bonds: raw text, edges not verdicts
    seal_date     TEXT,
    next_rez      INTEGER,            -- atomarni counters, if the seal has them
    next_dokaz    INTEGER,
    lineno        INTEGER NOT NULL,    -- the witness: where the body stands
    UNIQUE (doc_id, lineno)
);
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
    # mentions migration ("oboje"): existing dbs carry the old entry_id
    # column — rename to doc_id; reparse re-derives the rows honestly
    mcols = {r["name"] for r in con.execute("PRAGMA table_info(mentions)")}
    if "entry_id" in mcols and "doc_id" not in mcols:
        con.execute("ALTER TABLE mentions RENAME COLUMN entry_id TO doc_id")
    # ipa layer (Luka's "daj", 26. 9. 2026): existing dbs get the column —
    # the measured pronunciation lives BESIDE the rez (the cut), never
    # replacing it
    ecols = {r["name"] for r in con.execute("PRAGMA table_info(entries)")}
    if "ipa" not in ecols:
        con.execute("ALTER TABLE entries ADD COLUMN ipa TEXT")
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
    # D v2: the bare "**WORD** (long gloss):" head — committed ONLY when
    # a fragment table follows within the lookahead window (measured
    # shape: rez C1 dar-kula, **DAR** (rodovnik: ...): then | Fragment |)
    HEAD_BARE = re.compile(r"^\*\*(.+?)\*\*\s*(\(.*\))?\s*[:：]\s*$")
    LOOKAHEAD = 6
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
                # D v2: the bare "**WORD** (gloss):" head — tentative
                # until a fragment table shows in the lookahead window;
                # a colon line WITHOUT a following table is not a dosje
                hb = self.HEAD_BARE.match(line)
                if hb:
                    window = text.splitlines()[i:i + self.LOOKAHEAD]
                    if any(l.lstrip().startswith("|") and "**" in l
                           for l in window):
                        word = hb.group(1).strip()
                        gloss = (hb.group(2) or "").strip("() \t")
                        cur = Parsed(word=word, lineno=i)
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

class LatinTableParser(ParserPlugin):
    """FORMAT E (measured 26. 9., grounded in C1 latinščina I–VII): a
    whole dosje per TABLE ROW. The table is recognized by its HEADER
    carrying 'Fonetični rez'; columns map by header name:
    Beseda→word · Pomen→thesis · Etimologija→thesis (appended, ·-sepa-
    rated) · Fonetični rez→foneticni_rez · Ontološki pomen→ontoloski_
    pomen · Spol/other columns skipped (edges point, they don't judge).
    Grade: draft honestly (rez + pomen, no antinoma in this format)."""
    name = "E-tabela"
    HEADMARK = "fonetični rez"

    @staticmethod
    def _cells(line):
        return [c.strip() for c in line.strip().strip("|").split("|")]

    def parse(self, text: str) -> List[Parsed]:
        out: List[Parsed] = []
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            cells = self._cells(lines[i])
            if len(cells) > 2 and any(self.HEADMARK in c.lower()
                                      for c in cells):
                header = [c.lower() for c in cells]
                i += 1
                if i < len(lines) and set(lines[i].replace("|", "").strip()) \
                        <= {"-", ":", " "}:
                    i += 1               # separator row
                while i < len(lines):
                    row = self._cells(lines[i])
                    if len(row) < 2 or not lines[i].lstrip().startswith("|"):
                        break
                    vals = dict(zip(header, row))
                    word = (vals.get("beseda") or
                            (row[0] if row else "")).replace("**", "").strip()
                    if not word:
                        i += 1
                        continue
                    p = Parsed(word=word, lineno=i + 1)
                    p.foneticni_rez = (vals.get("fonetični rez") or
                                       "").replace("**", "").strip()
                    p.ontoloski_pomen = (vals.get("ontološki pomen") or
                                         "").replace("**", "").strip()
                    th = [v.replace("**", "").strip()
                          for k, v in vals.items()
                          if k in ("pomen", "etimologija") and v.strip()]
                    p.thesis = " · ".join(th)
                    out.append(p)
                    i += 1
            i += 1
        return out


class UnovSeciravaParser(ParserPlugin):
    """FORMAT F (measured 26. 9. 2026, grounded in Obj3 rozetni kamni —
    the izvajalka's word-secirave, another hand's readings of the same
    corpus the workshop canonizes; the third truth layer's entry point):

        ### word (gloss / activation note, dated)
        **Sloj 1 — IZMERA (⊢):** measured layer: gesla, IPA ⚠/⊢, nizi...
        **Sloj 2 — POSKUS (APD ↑):** the attempt layer...
        ... Hrana katere rane: X.

    Mapping: word=heading minus the paren gloss · ontoloski_pomen=the
    paren gloss (provenance by name) · thesis=Sloj 1 (izmera) ·
    synthesis=Sloj 2 (poskus) · foneticni_rez=first /IPA/ token found in
    Sloj 1 (many carry ⚠ honestly — stays empty then) ·
    prakticna_uporaba=the 'Hrana katere rane:' sentence when present.
    The SECTION DISCRIMINATOR is the Sloj pair: a ### heading without
    a Sloj 1 line (Tri pisave, h-rana closers, V.*, REZ-name sections)
    is NOT a word-secirava — prose stays prose. Grade: headline
    (thesis+synthesis), never reported (the format carries no antinoma
    — honest)."""
    name = "F-unov"
    HEAD = re.compile(r"^#{2,3}\s*(?![.#])\s*(.+?)\s*$")
    GLOSS = re.compile(r"^(.*?)\s*\(([^)]*)\)\s*$")
    SLOJ1 = re.compile(r"^\s*\*{0,2}\s*Sloj\s*1\s*[—–-]+\s*IZMERA.*$",
                       re.IGNORECASE)
    SLOJ2 = re.compile(r"^\s*\*{0,2}\s*Sloj\s*2\s*[—–-]+\s*POSKUS.*$",
                       re.IGNORECASE)
    # the Sloj content may live ON the marker line (one-paragraph style,
    # measured) — take the tail after the marker's colon
    SLOJ_TAIL = {"1": re.compile(r"^\s*\*{0,2}\s*Sloj\s*1\s*[—–-]+\s*"
                                 r"IZMERA[^:：]*[:：]\s*(.*)$", re.IGNORECASE),
                 "2": re.compile(r"^\s*\*{0,2}\s*Sloj\s*2\s*[—–-]+\s*"
                                 r"POSKUS[^:：]*[:：]\s*(.*)$", re.IGNORECASE)}
    # the word's own IPA: a bold word followed by /ipa/ — the word's rez,
    # not a phoneme of it; the token must carry a non-ASCII IPA sign (an
    # all-ASCII token is a URL or a path — /libraries/ measured, killed)
    IPA_WORD = re.compile(r"\*[^*]+\*\s*/([^/\s]{2,24})/")
    HRANA = re.compile(r"(Hrana\s+katere\s+rane[:：]\s*.+?)"
                       r"(?:\.\s*$|\n|$)", re.IGNORECASE)

    def parse(self, text: str) -> List[Parsed]:
        out: List[Parsed] = []
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            h = self.HEAD.match(lines[i])
            if not h:
                i += 1
                continue
            # scan to the next heading; a section is a word-secirava
            # only when it carries BOTH Sloj lines before that heading
            j, sloj1_at, sloj2_at = i + 1, None, None
            while j < len(lines) and not lines[j].lstrip().startswith("#"):
                if sloj1_at is None and self.SLOJ1.match(lines[j]):
                    sloj1_at = j
                elif sloj2_at is None and self.SLOJ2.match(lines[j]):
                    sloj2_at = j
                j += 1
            if sloj1_at is None or sloj2_at is None:
                i = j if j > i else i + 1
                continue
            head = h.group(1).strip().strip("*").strip()
            gloss = ""
            mg = self.GLOSS.match(head)
            if mg:
                head, gloss = mg.group(1).strip(), mg.group(2).strip()
            if not head:
                i = j
                continue
            # one-paragraph style: the content starts ON the marker line
            def tail_of(line, rx):
                mt = rx.match(line)
                if not mt:
                    return ""
                t = mt.group(1).strip()
                if t.startswith("**"):    # the marker's own closing bold
                    t = t[2:].lstrip()
                return t
            tail1 = tail_of(lines[sloj1_at], self.SLOJ_TAIL["1"])
            tail2 = tail_of(lines[sloj2_at], self.SLOJ_TAIL["2"])
            sloj1 = " ".join([tail1] + [x.strip() for x in
                                        lines[sloj1_at + 1: sloj2_at]
                                        if x.strip()])
            sloj2 = " ".join([tail2] + [x.strip() for x in
                                        lines[sloj2_at + 1: j]
                                        if x.strip()])
            s1 = sloj1.strip()
            s2 = sloj2.strip()
            p = Parsed(word=head, number=None, lineno=i + 1,
                       thesis=s1[:2000], synthesis=s2[:2000],
                       ontoloski_pomen=gloss[:300])
            m = self.IPA_WORD.search(s1)
            if m and any(ord(ch) > 127 for ch in m.group(1)):
                p.foneticni_rez = "/" + m.group(1) + "/"
            mh = self.HRANA.search(s2)
            if mh:
                p.prakticna_uporaba = mh.group(1).strip()[:500]
            out.append(p)
            i = j
        return out


PLUGINS: List[ParserPlugin] = [StotnijeBulletParser(), HeadlineParser(),
                               NumberedSectionParser(),
                               RezFragmentParser(),
                               LatinTableParser(),
                               UnovSeciravaParser()]
# EVOLUTION POINT: append MyFormatFParser() here. Nothing else changes.
# (26. 9.: used for D and E — both measured first: D = inline rez +
# fragment table (+ the bare"): "head, table-lookahead committed);
# E = latinščina word-tables, one dosje per ROW, columns mapped by
# header: Beseda→word · Pomen→thesis · Etimologija→thesis (appended) ·
# Fonetični rez→foneticni_rez · Ontološki pomen→ontoloski_pomen)

def grade_of(p: Parsed) -> str:
    if p.foneticni_rez and p.ontoloski_pomen and p.antinoma and p.synthesis:
        return "reported"
    if p.synthesis and (p.thesis or p.number):
        return "headline"
    return "draft"


# ================================================ PARSER-ZAKONOV (graft) ==
# Sealed by Luka's 'daj', 26. 9. 2026: ZAKONI SO LOČENA VRSTA DOKUMENTA.
# The spine reads LAWS as a separate kind — separate table, separate shape.
# LAWS OF THE PARSER: the key is the BODY WITH ITS WITNESS (doc + line),
# the number is a LABEL; VEZI point, they never judge; the parser is a
# READER, never a writer — sealed bodies are append-only and the counters
# (atomarni) are read, never replaced here. Grounded in four measured
# header shapes (rez 231/253/558, C1 rez 110) before one line was written.

ZAKON_SERIES = r"(rez|dokaz|sodba|ubod|šiv)"
ZAKON_NUM = re.compile(ZAKON_SERIES + r"\b[·#:*\s]*(\d{1,4})", re.IGNORECASE)
ZAKON_H1 = re.compile(r"^#\s*(.+?)\s*[—–·-]\s*$|^#\s*(.+)$")
ZAKON_MERITEV = re.compile(r"⊘\s*\(([^)]*)\)")
ZAKON_NEXT_REZ = re.compile(r"NASLEDNJI PROSTI REZ[:\s*]*#?(\d+)",
                             re.IGNORECASE)
ZAKON_NEXT_DOKAZ = re.compile(r"NASLEDNJI PROSTI DOKAZ[:\s*]*#?(\d+)",
                              re.IGNORECASE)
ZAKON_AKTIVATOR = re.compile(r"aktivator[:\s]*(»[^«]*«)", re.IGNORECASE)
ZAKON_DATE = re.compile(r"(\d{1,2}\.\s*\d{1,2}\.\s*\d{4})")
ZAKON_SECTION = re.compile(r"^#{2,3}\s*(.*)$")
# MULTI-LAW heads (the named ∂ from the Obj3 reading, 26. 9. 2026): one
# body may carry MANY laws — secirave hold 7–12 ubodi, the kroglja holds
# REZ #24–28, C3 holds DOKAZ #1–2. A head beyond the doc-head territory is
# a heading naming series+number, or a bold line OPENING with series+
# number and carrying a title separator right after (a bare "**REZ N**
# pravi…" citation has no separator — it stays a VEZI, measured)
ZAKON_MH_HEAD = re.compile(r"^#{1,6}\s*\**\s*" + ZAKON_SERIES +
                           r"\b[·#:*\s]*(\d{1,4})\b\s*(?:\([^)]*\)\s*)?"
                           r"[—–·:]*\s*(.*)$", re.IGNORECASE)
ZAKON_MH_BOLD = re.compile(r"^\*\*\s*" + ZAKON_SERIES +
                           r"\b[·#:*\s]*(\d{1,4})\s*(?:\([^)]*\)\s*)?"
                           r"[—–·:]\s*(.+?)\*{0,2}\s*$",
                           re.IGNORECASE)
# the ZAKONIK series (Luka's "da, uzakonodaji vse to", register (2), 26. 9.
# 2026): one-line sealed laws — the WHOLE body lives on the head line,
# the rest-of-line is the teza. Ten bodies (Z-1..Z-10), previously dark
# to the table (the series enum knew rez/dokaz/sodba/ubod/šiv only).
ZAKON_Z_HEAD = re.compile(r"^\*\*\s*Z[-–]\s*(\d{1,3})\s+(.+?)\*\*"
                          r"\s*[—–:]?\s*(.*)$")

# sections we carry, by keyword in the heading (the anatomy, measured)
ZAKON_SECTIONS = (("NUJNE NAPAKE", "nujne_napake"),
                  ("ODPRTA", "odprta_partial"),
                  ("VEZI", "vezi"),
                  ("TEZA", "teza"),
                  ("AKTIVATOR", "actor_section"))


def parse_zakon(text: str) -> List[dict]:
    """One law body, or []. A doc is a law when its head (first 8 lines)
    names a series and a number — prose stays prose, honestly. Returns the
    law as a dict of the sealed fields; the caller stores it with its
    witness (doc + lineno)."""
    lines = text.splitlines()
    head_lines = lines[:8]
    series = number = title = None
    for i, line in enumerate(head_lines, 1):
        # a law HEAD is a heading or a bold seal line — a doc that merely
        # CITES a law number in prose is not that law's body (POPIS-measured
        # over-match, refined twice: a bold line counts as a seal only when
        # the series opens it — "**REZ 231 · ...**" is a head, "**Telo:**
        # ... (ubod #4 ...)" is a citation wearing bold; found by Obj3's
        # secirava, measured: ghost ubod-4 from line 4 of a body whose
        # seven real ubodi stayed unread — the citation is a VEZI, not a head)
        if not line.lstrip().startswith(("#", "**")):
            continue
        if line.lstrip().startswith("**"):
            m = re.match(r"\*\*\s*" + ZAKON_SERIES +
                         r"\b[·#:*\s]*(\d{1,4})", line, re.IGNORECASE)
        else:
            m = ZAKON_NUM.search(line)
        if m:
            series, number = m.group(1).lower(), int(m.group(2))
            h1 = re.match(r"^#\s*(.+)$", line)
            if h1:                      # "# REZ 558 — TITLE"
                t = re.split(r"[—–·]", h1.group(1), maxsplit=1)
                title = (t[1].strip() if len(t) > 1 else
                         (t[0].strip() if series == "rez" else ""))
                title = title if title and not ZAKON_NUM.search(title) else ""
            break
    if series is None:
        multi = _multi_laws(text)   # no doc-head: deeper bodies may stand
        return multi
    law = {"series": series, "number": number, "title": title or "",
           "lineno": i, "actor": "", "teza": "", "meritev": "",
           "nujne_napake": "", "odprta_partial": "", "vezi": "",
           "seal_date": "", "next_rez": None, "next_dokaz": None,
           "actor_section": ""}
    # a body may carry MANY laws — the first law's block ends at the next
    # head, so later ubodi/rezi never leak into it (measured: secirave,
    # kroglja, C3 dokazi)
    heads = [(i, series, number)] + [(h[0], h[1], h[2])
                                     for h in _multi_head_positions(text)
                                     if h[0] != i]
    _fill_law_block(law, lines, i, heads[1][0] if len(heads) > 1
                    else len(lines) + 1)
    out = [law] + [z for z in _multi_laws(text) if z["lineno"] != i]
    return out


def _multi_head_positions(text: str) -> List[tuple]:
    """[(lineno, series, number, title, rest), …] for every multi-law head
    in the body. Headings anywhere; bold lines only with the title separator
    right after the number (the citation guard, measured); Z-heads carry
    their one-line body as the rest-of-line (the zakonik's own shape)."""
    out = []
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        m = ZAKON_Z_HEAD.match(line)
        if m:
            out.append((n, "zakon", int(m.group(1)),
                        m.group(2).strip().rstrip(":").strip(),
                        m.group(3).strip()))
            continue
        m = ZAKON_MH_HEAD.match(line) or ZAKON_MH_BOLD.match(line)
        if not m:
            continue
        t = (m.group(3) if m.lastindex and m.lastindex >= 3 else "")
        t = t.strip().strip("*").strip().rstrip(":").strip()
        out.append((n, m.group(1).lower(), int(m.group(2)), t, ""))
    return out


def _fill_law_block(law: dict, lines: List[str], start: int, end: int):
    """Fill one law's sealed fields from its block (start..end), the same
    ceremony the single-law reader always used — now bounded. A body with
    no explicit TEZA section carries its own prose as teza (measured: the
    ubodi/kroglja bodies hold their content in prose); prose stops at the
    FIRST heading — fields never leak across sections (measured: the
    zakonik's '### VELJA' section must not become Z-5's teza)."""
    block = "\n".join(lines[start - 1: end - 1])
    cur = None
    prose: List[str] = []
    prose_open = True     # prose closes at the first heading — no leaks
    for line in lines[start - 1: end - 1]:
        if re.match(r"^#{1,6}\s", line):
            prose_open = False
        h = ZAKON_SECTION.match(line)
        if h:
            cur = None
            head = h.group(1).upper()
            for key, field in ZAKON_SECTIONS:
                if key in head:
                    cur = field
                    break
            continue
        if cur:
            law[cur] = (law[cur] + "\n" if law[cur] else "") + line.strip()
        elif line.strip() and line is not lines[start - 1] and prose_open:
            prose.append(line.strip())
    if not law["teza"] and prose:
        law["teza"] = "\n".join(prose)[:2000]
    m = ZAKON_MERITEV.search(block)
    if m:
        law["meritev"] = m.group(1).strip()
    m = ZAKON_AKTIVATOR.search(block)
    if m:
        law["actor"] = m.group(1).strip("»« ")
    if not law["actor"] and law.get("actor_section"):
        law["actor"] = law["actor_section"].strip()[:300]
    law.pop("actor_section", None)
    m = ZAKON_NEXT_REZ.search(block)
    if m:
        law["next_rez"] = int(m.group(1))
    m = ZAKON_NEXT_DOKAZ.search(block)
    if m:
        law["next_dokaz"] = int(m.group(1))
    m = ZAKON_DATE.search(block[:2000])
    if m:
        law["seal_date"] = m.group(1).replace(" ", "")


def _multi_laws(text: str) -> List[dict]:
    """Every multi-law head becomes a body with its witness — each kept,
    each carried with its own block's sealed fields. The Z-heads seed
    their teza from the rest of the head line (the zakonik's one-line
    bodies — without it the law would be a number with no body)."""
    lines = text.splitlines()
    out = []
    positions = _multi_head_positions(text)
    for k, (lineno, series, number, title, rest) in enumerate(positions):
        end = positions[k + 1][0] if k + 1 < len(positions) else len(lines) + 1
        law = {"series": series, "number": number, "title": title or "",
               "lineno": lineno, "actor": "", "teza": (rest or "")[:2000],
               "meritev": "", "nujne_napake": "", "odprta_partial": "",
               "vezi": "", "seal_date": "", "next_rez": None,
               "next_dokaz": None, "actor_section": ""}
        _fill_law_block(law, lines, lineno, end)
        out.append(law)
    return out


def _insert_zakon(con, doc_id: int, z: dict) -> int:
    """Store one law with its witness (doc + line). Idempotent: the same
    body at the same line is never stored twice (INSERT OR IGNORE).
    Returns 1 if a NEW law body entered the table, 0 otherwise."""
    cur = con.execute("""INSERT OR IGNORE INTO zakoni
        (doc_id, series, number, title, actor, teza, meritev,
         nujne_napake, odprta_partial, vezi, seal_date, next_rez,
         next_dokaz, lineno)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (doc_id, z["series"], z["number"], z["title"], z["actor"],
         z["teza"], z["meritev"], z["nujne_napake"], z["odprta_partial"],
         z["vezi"], z["seal_date"], z["next_rez"], z["next_dokaz"],
         z["lineno"]))
    return cur.rowcount


def retro_mark(con) -> dict:
    """THE LEDGER'S OLDEST LIE, REPAIRED WITH WITNESS, NOT LAUNDERED:
    the 24. 9. machine merges (26 lines, ruled 'under Luka's do not
    relegate instruction') carried no machine flag — the replay counted
    them as human rulings. NORMATIVE ACT this rides on: Luka's 24. 9.
    instruction (in the payloads) + his 26. 9. 'vse skušaj'. The lines
    get machine:true AND a ratified_by reference to a witness line that
    names both acts — they become canon THROUGH their ratification,
    visible forever, never silent."""
    led(con, "verdict", None, {
        "ruling": "retro-ratification-of-24.9-merges",
        "by": "Luka: 24. 9. 'do not relegate' instruction "
              "+ 26. 9. 'vse skušaj'",
        "note": "the 26 machine merges were ruled under instruction "
                "before guards existed; ratified WITH provenance"})
    ref = con.execute("SELECT MAX(id) FROM ledger").fetchone()[0]
    marked = 0
    for r in con.execute(
            "SELECT id, payload FROM ledger WHERE kind='merge' AND "
            "payload NOT LIKE '%\"machine\": true%'"):
        p = json.loads(r["payload"])
        p["machine"] = True
        p["ratified_by"] = f"ledger#{ref}"
        con.execute("UPDATE ledger SET payload=? WHERE id=?",
                    (json.dumps(p, ensure_ascii=False), r["id"]))
        marked += 1
    con.commit()
    return {"marked": marked, "ratification_line": ref}


def graf(con) -> dict:
    """THE CITATION GRAPH (the stored-unconsumed lines, consumed —
    Luka's 'vse skušaj'): doc→word edges (mentions, honest since
    'oboje'), law→law edges (VEZI refs: rez N / DOKAZ #M, parsed from
    the bonds), commit-evidence counts (hash-shaped strings in law
    bodies). EDGES POINT, THEY NEVER JUDGE (the sealed ruling, point 4)."""
    live = {canon(r["word"]) for r in con.execute(
        "SELECT DISTINCT word FROM entries WHERE merged_into IS NULL")}
    doc_word = con.execute(
        "SELECT COUNT(*) FROM (SELECT DISTINCT doc_id, mention "
        "FROM mentions)").fetchone()[0]
    # honest: distinct (doc,mention) pairs whose mention is a live word
    pairs = [(r["doc_id"], r["mention"]) for r in con.execute(
        "SELECT DISTINCT doc_id, mention FROM mentions")]
    real = sum(1 for _d, m in pairs if m in live)
    law_law = []
    for z in con.execute("SELECT series, number, vezi FROM zakoni "
                         "WHERE TRIM(vezi) != ''"):
        src = f"{z['series']} {z['number']}"
        for m in re.finditer(r"(?:rez|dokaz)\s*[#·]?\s*(\d+)",
                             z["vezi"], re.IGNORECASE):
            law_law.append((src, m.group(0).lower()))
    commits = 0
    k_edges = 0
    for z in con.execute("SELECT vezi, teza, nujne_napake, "
                         "odprta_partial FROM zakoni"):
        blob = " ".join(str(x or "") for x in z)
        commits += len(re.findall(r"\b[0-9a-f]{7,8}\b", blob))
        # the K-SERIES (the third register materialization, measured in
        # the Obj3 reading): 'REZ #N (K#)' — a chapter-bond of the
        # kroglja's own graph. The bonds live in the bodies' prose (the
        # kroglja cites REZ #23 (K1) inside its teza), so they are counted
        # across the law fields — like commit evidence, unlike VEZI
        # (stored bonds). Edges point, they never judge.
        k_edges += len(re.findall(r"rez\s*#\s*\d+\s*\(K\d+\)",
                                  blob, re.IGNORECASE))
    return {"doc_word_edges": doc_word,
            "doc_word_citing_live_words": real,
            "live_words": len(live),
            "law_law_edges": len(law_law),
            "k_series_edges": k_edges,
            "commit_evidence_in_laws": commits,
            "sample_law_law": law_law[:5]}


def odprta_delta(con) -> dict:
    """SERVES REZ 231 (the kazalo of open ∂ — the organ): every open ∂
    carried by a law body, with its source law. The organ's next popis
    reads here; the kazalo itself stays Luka's. ISKANO-labeled receipt."""
    out = []
    for z in con.execute(
            "SELECT series, number, title, odprta_partial, seal_date "
            "FROM zakoni WHERE TRIM(odprta_partial) != '' "
            "ORDER BY number"):
        items = [l.strip("- ·\t") for l in
                 z["odprta_partial"].splitlines() if l.strip()]
        out.append({"law": f"{z['series']} {z['number']}",
                    "title": (z["title"] or "")[:60],
                    "open": items[:5], "seal_date": z["seal_date"]})
    return {"laws_with_open_delta": len(out),
            "total_open": sum(len(o["open"]) for o in out),
            "per_law": out}


def popis_zakoni(con) -> dict:
    """The seal-POPIS (seam 2's systematic answer, ISKANO-labeled receipt):
    series counts, which law bodies carry atomarni seals and which don't,
    the counter range, DOKAZ cross-edges — the register's fork, measured
    instead of guessed. The number is a LABEL: same-number bodies from
    parallel branches are counted each, never merged."""
    out = {"series": {}, "sealed": 0, "unsealed": 0,
           "next_rez_range": None, "next_dokaz_range": None,
           "same_number_pairs": 0}
    for r in con.execute("SELECT series, COUNT(*) n FROM zakoni "
                         "GROUP BY series"):
        out["series"][r["series"]] = r["n"]
    for r in con.execute("SELECT number, COUNT(*) n FROM zakoni "
                         "WHERE number IS NOT NULL GROUP BY number "
                         "HAVING n > 1"):
        out["same_number_pairs"] += 1
    rez = [r["next_rez"] for r in con.execute(
        "SELECT DISTINCT next_rez FROM zakoni WHERE next_rez IS NOT NULL "
        "ORDER BY next_rez")]
    dok = [r["next_dokaz"] for r in con.execute(
        "SELECT DISTINCT next_dokaz FROM zakoni WHERE next_dokaz IS NOT NULL "
        "ORDER BY next_dokaz")]
    out["next_rez_range"] = [rez[0], rez[-1]] if rez else None
    out["next_dokaz_range"] = [dok[0], dok[-1]] if dok else None
    out["sealed"] = con.execute(
        "SELECT COUNT(*) FROM zakoni WHERE next_rez IS NOT NULL OR "
        "next_dokaz IS NOT NULL").fetchone()[0]
    out["unsealed"] = con.execute(
        "SELECT COUNT(*) FROM zakoni WHERE next_rez IS NULL AND "
        "next_dokaz IS NULL").fetchone()[0]
    return out

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
        # stratum 3, honest since "oboje": doc-level mention edges — the
        # document mentions the word; the edge points, it never judges
        for m in re.findall(r"\b([A-ZČŠŽ][a-zčšžćđ]{3,})\b", text):
            con.execute("INSERT INTO mentions VALUES (?, ?)",
                        (doc_id, canon(m)))
        # parser-zakonov: the spine reads LAWS too — separate kind, never
        # entries; idempotent by body-with-witness
        is_law = sum(_insert_zakon(con, doc_id, z) > 0
                     for z in parse_zakon(text))
        # graft #8: what this text IS, where it OCCUPIES — typed at admission
        rel = f.relative_to(root)
        stratum = rel.parts[0] if len(rel.parts) > 1 else "(root)"
        if is_law:
            kind = "zakon"
        else:
            fmts = [r[0] for r in con.execute(
                "SELECT DISTINCT format FROM entries WHERE doc_id=?",
                (doc_id,))]
            kind = doc_kind(stratum, text, fmts)
        con.execute("UPDATE docs SET kind=?, stratum=? WHERE doc_id=?",
                    (kind, stratum, doc_id))
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
    mentions = con.execute("SELECT COUNT(DISTINCT doc_id) FROM mentions "
                          "WHERE mention=?",
                          (w,)).fetchone()[0]   # DOCS mentioning (honest
                                                # since "oboje"; was noise)
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
            "(SELECT DISTINCT doc_id FROM entries UNION "
            "SELECT DISTINCT doc_id FROM zakoni)"):
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


def retype(con, root=None) -> dict:
    """Graft #8 backfill: type the docs already scanned (scan types at
    admission; everything admitted before graft #8 was never typed).
    Idempotent — re-running re-derives the same facts. One summary ledger
    line, not one per doc; the db is backed up first, same law as scan.
    root=None: the root is DERIVED FROM THE DOCS (commonpath) — a caller
    guessing the wrong root (scar 26. 9.: the CLI defaulted to cwd=Workshop
    and 1,193 docs read as 'outside_root', typing nothing while the
    receipt claimed success) can no longer shrink the pass."""
    import shutil
    if Path(DB_PATH).exists():
        shutil.copy2(DB_PATH, f"{DB_PATH}.bak")
    if root is None:
        paths = [r["path"] for r in con.execute("SELECT path FROM docs")]
        root = (Path(os.path.commonpath(paths)) if paths else Path.cwd())
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
        # law-aware: a doc that carries law bodies is 'zakon' — retype
        # may not clobber it back to 'notes' (scar 26. 9., found by the
        # coverage POPIS's own re-run)
        if con.execute("SELECT COUNT(*) FROM zakoni WHERE doc_id=?",
                       (r["doc_id"],)).fetchone()[0]:
            kind = "zakon"
        else:
            fmts = [x[0] for x in con.execute(
                "SELECT DISTINCT format FROM entries WHERE doc_id=?",
                (r["doc_id"],))]
            kind = doc_kind(stratum, text, fmts)
        con.execute("UPDATE docs SET kind=?, stratum=? WHERE doc_id=?",
                    (kind, stratum, r["doc_id"]))
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


# ============================== IPA LAYER (Luka's "daj", 26. 9. 2026) ===
# ZAKON IPA (sealed on Luka's own ukaz, Obj3 register): "nikoli ne
# preskoči IPA — poišči na spletu izvor in izgovor" + "spomin ni izmera".
# CONSEQUENCE for this machine (no web): a rule-based g2p is BY
# DEFINITION izmera iz glave (the register's rod 1) — it can propose
# only DRAFTS (machine:true, ⚠, never ⊢); canon enters through the
# owner's ratification, ideally after checking a source (fran.si /
# SSKJ² / Wiktionary) or commissioning the izvajalka (ZAKON IPA is
# HER standing law too, measured in her own register).

G2P_MAP = {
    "a": "a", "b": "b", "c": "t͡s", "č": "t͡ʃ", "d": "d", "e": "ɛ",
    "f": "f", "g": "ɡ", "h": "x", "i": "i", "j": "j", "k": "k",
    "l": "l", "m": "m", "n": "n", "o": "ɔ", "p": "p", "r": "ɾ",
    "s": "s", "š": "ʃ", "t": "t", "u": "u", "v": "ʋ", "z": "z",
    "ž": "ʒ", "ć": "t͡ɕ", "đ": "d͡ʑ", "w": "w", "q": "q", "x": "ks",
    "y": "i",
}
G2P_DIGRAPHS = {"lj": "ʎ", "nj": "ɲ", "dž": "d͡ʒ"}


def slo_g2p(word: str) -> str:
    """Rule-based Slovenian grapheme→IPA (phoneme level, no stress —
    Slovenian stress is unpredictable without a dictionary, so it is
    HONESTLY omitted; no assimilation — phonemic, not phonetic). A DRAFT
    MACHINE, never an izmera: ZAKON IPA forbids ⊢ from this hand."""
    w = unicodedata.normalize("NFC", word.strip().lower())
    out, i = [], 0
    while i < len(w):
        two = w[i:i + 2]
        if two in G2P_DIGRAPHS:
            out.append(G2P_DIGRAPHS[two])
            i += 2
            continue
        if w[i] in G2P_MAP:
            out.append(G2P_MAP[w[i]])
        i += 1
    return "/" + "".join(out) + "/"


def ipa_popis(con) -> dict:
    """The honest gap, measured on demand (extends the census line):
    how many live words carry the MEASURED pronunciation (ipa), how
    many carry the CUT (foneticni_rez — the fragment organ, native,
    never replaced), how many carry neither. ISKANO receipt."""
    rez_words, ipa_words, empty = set(), set(), set()
    for r in con.execute("SELECT word, foneticni_rez, ipa FROM entries "
                         "WHERE merged_into IS NULL"):
        if (r["ipa"] or "").strip():
            ipa_words.add(canon(r["word"]))
        if (r["foneticni_rez"] or "").strip():
            rez_words.add(canon(r["word"]))
        if not (r["ipa"] or "").strip():
            empty.add(canon(r["word"]))
    live = rez_words | ipa_words | empty
    return {"live_words": len(live),
            "with_ipa": len(ipa_words),
            "with_rez_cut": len(rez_words - ipa_words),
            "with_nothing": len(empty - rez_words - ipa_words),
            "ipa_coverage":
                round(len(ipa_words) / len(live), 4) if live else 0.0,
            "NOTE": "rez = the CUT (native organ, stays); ipa = the "
                    "MEASURED pronunciation (a second organ, beside it)"}


def ipa_drafts(con, lex_path=None) -> dict:
    """G2P DRAFTS — the machine proposes, the owner canonizes (the same
    ceremony as merge/conflict/glyph/enrich drafts). GUARD (a): the
    normative 'machine-drafts-authorized' line must stand in the ledger
    first — the machine cannot authorize itself. Targets (honest scope,
    no 2,242-word flood): live entries of words that MATTER first — the
    lexicon's 40 + every word that already carries a cut (fragment rez);
    composite words ( / + etc.) are skipped honestly (g2p reads single
    words). Every candidate carries the ⚠ of its own kind: izmera iz
    glave, ZAKON IPA forbids ⊢; stress omitted (unpredictable without
    a dictionary — named, not hidden)."""
    auth = con.execute(
        "SELECT COUNT(*) FROM ledger WHERE kind='verdict' AND "
        "payload LIKE '%machine-drafts-authorized%'").fetchone()[0]
    if not auth:
        return {"error": "no normative authorization line — the owner "
                         "must deliberately run `authorize-drafts` first; "
                         "the machine cannot authorize itself"}
    st = ruling_states(con)
    seen = st["human_fp"] | st["machine_fp"] | st["refused_fp"]
    # honest target set: lexicon words + words that carry a cut
    targets = set()
    for r in con.execute("SELECT word, foneticni_rez FROM entries "
                         "WHERE merged_into IS NULL"):
        if (r["foneticni_rez"] or "").strip():
            targets.add(canon(r["word"]))
    if lex_path and Path(lex_path).exists():
        lex = json.loads(Path(lex_path).read_text(encoding="utf-8"))
        targets |= {canon(k) for k in lex
                    if isinstance(lex[k], dict) or True}
    drafted, skipped = 0, 0
    for e in con.execute(
            "SELECT entry_id, word, foneticni_rez, ipa FROM entries "
            "WHERE merged_into IS NULL ORDER BY entry_id"):
        if (e["ipa"] or "").strip():
            continue
        w = canon(e["word"])
        if w not in targets:
            continue
        # the guard measured on the first witness: canon() launders a
        # mangled word ('Combinations transform, ... — [ThoughtCo]') into
        # bare letters and g2p would transcribe garbage with a straight
        # face. The RAW word must be one plain word — letters only.
        if not re.fullmatch(r"[A-Za-zČčŠšŽžĆćĐđ]{1,20}",
                            (e["word"] or "").strip()):
            skipped += 1
            continue
        fp = f"ipa-{e['entry_id']}"
        if (canon(e["word"]), fp) in seen:
            continue
        led(con, "verdict", e["word"], {
            "ruling": "draft-ipa", "machine": True,
            "fingerprint": fp, "entry_id": e["entry_id"],
            "ipa": slo_g2p(e["word"]),
            "rationale": "g2p pravilen — IZMERA IZ GLAVE (ZAKON IPA: "
                         "spomin ni izmera): ⚠ dokler ne preveriš proti "
                         "viru (fran.si / SSKJ² / Wiktionary) ali "
                         "komisijiš izvajalko; naglas pošteno izpuščen "
                         "(brez slovarja nepredvidljiv); fonemsko, brez "
                         "asimilacij. Rez (rez) ostane domači organ — "
                         "ta plast je izmera ob njem."})
        drafted += 1
    con.commit()
    led(con, "drafts", None, {"ipa": drafted, "ipa_skipped_composite":
                              skipped})
    con.commit()
    return {"ipa_drafts": drafted, "skipped_composite": skipped}


def le_cenzus(con) -> dict:
    """ZAKON LE (psiho-aksiomi VII, measured in the corpus 26. 9. 2026):
    "le" is a pra-set of five lenses, and "popis 'le' je cenzus ali ni
    nič — vzorec, prikazan kot celota, je sam minimizem." So this is a
    WHOLE-corpus census, never a sample. MACHINE-HONEST CLASSES — the
    patterns decide only what patterns can decide: IZTOČNICA ("ne le …
    ampak" — separates, does not limit) · MEJA (an alternative is NAMED
    in the same sentence — the lens binds with rules) ·
    MINIMIZEM-KANDIDAT (no alternative found by pattern — a READER
    confirms or frees it; the machine does not judge meaning, and the
    class says kandidat, not sodba). ISKANO receipt; ŠIV is not
    machine-resolvable and is honestly not counted."""
    NELE = re.compile(r"\bne\s+(?:le|samo|zgolj)\b", re.IGNORECASE)
    ALT = re.compile(r"\b(ampak|temveč|marveč|pa\s+tudi|in\s+tudi|"
                     r"a\s+tudi|saj\s+tudi|nego)\b", re.IGNORECASE)
    TOKEN = re.compile(r"\b(?:le|samo|zgolj)\b", re.IGNORECASE)
    SENT = re.compile(r"(?<=[.!?;])\s+")
    counts = {"iztočnica": 0, "meja": 0, "minimizem_kandidat": 0}
    per_doc, samples, total, docs = [], [], 0, 0
    for d in con.execute("SELECT path, stratum FROM docs"):
        try:
            text = Path(d["path"]).read_text(encoding="utf-8",
                                            errors="replace")
        except OSError:
            continue
        docs += 1
        doc_n = 0
        for sent in SENT.split(text):
            hits = TOKEN.findall(sent)
            if not hits:
                continue
            cls = ("iztočnica" if NELE.search(sent) else
                   "meja" if ALT.search(sent) else "minimizem_kandidat")
            for _ in hits:
                counts[cls] += 1
                doc_n += 1
                total += 1
            if cls == "minimizem_kandidat" and len(samples) < 24:
                s = " ".join(sent.split())
                samples.append({"doc": d["path"].split("CanvasMinstral")[-1],
                                "context": s[:180]})
        if doc_n:
            per_doc.append((doc_n, d["path"].split("CanvasMinstral")[-1]))
    per_doc.sort(reverse=True)
    return {"docs_scanned": docs, "total_occurrences": total,
            "classes": counts,
            "top_docs": [{"doc": p, "occurrences": n}
                         for n, p in per_doc[:10]],
            "minimizem_candidates_sample": samples,
            "NOTE": "ZAKON LE (psiho-aksiomi VII): cenzus ali ni nič. "
                    "MINIMIZEM-KANDIDAT is not a sodba — a reader names "
                    "the Alt or frees the lens; ŠIV is not "
                    "machine-resolvable and honestly not counted."}


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
        "(SELECT DISTINCT doc_id FROM entries UNION "
        "SELECT DISTINCT doc_id FROM zakoni)")]
    lit = new_entries = new_laws = 0
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
        # parser-zakonov: laws read on the same pass — a law body that is
        # also a dosje stays BOTH kinds; never entries
        got_law = 0
        for z in parse_zakon(text):
            cur = _insert_zakon(con, d["doc_id"], z)
            got_law += cur
            new_laws += cur
        if got or got_law:
            lit += 1
            new_entries += got
            if got_law:
                con.execute("UPDATE docs SET kind='zakon' WHERE doc_id=?",
                            (d["doc_id"],))
            elif got:
                fmts = [r[0] for r in con.execute(
                    "SELECT DISTINCT format FROM entries WHERE doc_id=?",
                    (d["doc_id"],))]
                con.execute("UPDATE docs SET kind=? WHERE doc_id=?",
                            (doc_kind(d["stratum"] or "(root)", text, fmts),
                             d["doc_id"],))
    # laws also live in docs that are NOT dark (a rez body may carry
    # dosjes too) - one law-pass over every doc, idempotent by witness
    # (new_laws carries the dark pass's laws too — a law admitted in the
    # dark loop must not vanish from the receipt; found by rez 562's
    # delete+re-derive, measured: row existed, counter said 0)
    for d in con.execute("SELECT doc_id, path FROM docs").fetchall():
        try:
            text = Path(d["path"]).read_text(encoding="utf-8",
                                            errors="replace")
        except OSError:
            continue
        for z in parse_zakon(text):
            if _insert_zakon(con, d["doc_id"], z):
                new_laws += 1
                con.execute("UPDATE docs SET kind='zakon' WHERE doc_id=? "
                            "AND kind != 'zakon'", (d["doc_id"],))
    # mentions re-derivation ("oboje"): the old rows were noise (a doc's
    # whole load piled on its last entry, 96k rows toward nothing) —
    # delete and re-derive as DOC-LEVEL edges; the count in page()
    # becomes honest (docs mentioning the word)
    con.execute("DELETE FROM mentions")
    new_mentions = 0
    for d in con.execute("SELECT doc_id, path FROM docs").fetchall():
        try:
            text = Path(d["path"]).read_text(encoding="utf-8",
                                            errors="replace")
        except OSError:
            continue
        for m in re.findall(r"\b([A-ZČŠŽ][a-zčšžćđ]{3,})\b", text):
            con.execute("INSERT INTO mentions VALUES (?, ?)",
                        (d["doc_id"], canon(m)))
            new_mentions += 1
    led(con, "reparse", None, {"dark_before": len(dark), "lit": lit,
                               "new_entries": new_entries,
                               "new_laws": new_laws,
                               "mentions_rederived": new_mentions})
    con.commit()
    return {"dark_before": len(dark), "lit": lit,
            "new_entries": new_entries, "new_laws": new_laws,
            "mentions_rederived": new_mentions}


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


# ============================================ THE REPLAY + MACHINE DRAFTS ==
# Graft #11 — machine DRAFT rulings, under the law of receipts vs canon
# (SODBA #002, Luka's extension): a receipt records causality (what was
# computed and why); canon declares normality (how it should be). Normality
# never follows from causality — so a machine draft NEVER rules. States:
#   PENDING ──machine──▶ DRAFT (receipt, rationale attached, machine:true)
#                          └─[k]─▶ CANON   (owner ratifies)
#                          └─[c]─▶ PENDING  (draft refused; never re-drafted)
#                          └─[m]─▶ CANON, the owner's way
# GUARD (a) — FLAG PROVENANCE: "machine": true is itself machine-written.
# The replay trusts it ONLY if the ledger carries the owner's NORMATIVE
# authorization line (ruling 'machine-drafts-authorized', created solely
# by the owner deliberately running `authorize-drafts`). Drafts written
# before that line are ⚠ and the replay ignores them — a receipt may not
# forge its own birth certificate.
# GUARD (c) — the stability measure (below) is a receipt about receipts:
# it observes the canon, it never joins it.

def ruling_states(con) -> dict:
    """THE replay — one line for queues and drafts alike (the spine owns
    it; the cockpit reads it). Classifies every ledger merge/verdict line:
    human lines RULE, machine lines DRAFT (ratify state), refusals return
    the draft's subject to pending while forbidding re-drafting."""
    st = {"human_fp": set(), "machine_fp": set(), "refused_fp": set(),
          "human_conflict": set(), "machine_conflict": set(),
          "refused_conflict": set()}
    auth = con.execute(
        "SELECT MIN(id) FROM ledger WHERE kind='verdict' AND "
        "payload LIKE '%machine-drafts-authorized%'").fetchone()[0]
    for r in con.execute("SELECT id, word, payload FROM ledger "
                         "WHERE kind IN ('merge','verdict')"):
        try:
            p = json.loads(r["payload"])
        except (ValueError, TypeError):
            continue
        if not isinstance(p, dict):
            continue
        if auth is not None and r["id"] is not None and r["id"] < auth:
            continue          # GUARD (a): pre-authorization machine lines
                              # are untrusted — no birth certificate
        w = canon(r["word"] or "")
        fp = p.get("fingerprint")
        ruling = str(p.get("ruling", ""))
        if ruling == "draft-refused":
            if fp:
                st["refused_fp"].add((w, fp))
            elif p.get("conflict"):
                st["refused_conflict"].add(canon(p["conflict"]))
            continue
        machine = bool(p.get("machine"))
        # v2 (Luka's "vse skušaj"): a RATIFIED machine line is CANON —
        # machine:true + a ratification reference (the owner's seal,
        # cited) is normative; unratified machine lines stay DRAFTS.
        ratified = bool(p.get("ratified_by") or p.get("ratified"))
        canon_line = (not machine) or ratified
        if fp:
            (st["human_fp"] if canon_line
             else st["machine_fp"]).add((w, fp))
        if ruling.startswith("conflict"):
            (st["human_conflict"] if canon_line
             else st["machine_conflict"]).add(w)
    return st


def _fullness(e: dict) -> int:
    return sum(1 for k in ("thesis", "antithesis", "synthesis",
                          "foneticni_rez", "ontoloski_pomen", "antinoma",
                          "glyph", "prakticna_uporaba")
               if (e.get(k) or "").strip())


def draft_rulings(con, glyph_path=None) -> dict:
    """The machine drafts its rulings for every PENDING item — receipts
    with rationale, never rulings. Merge: richest keeper by grade rank,
    then field fullness, then lowest entry_id (deterministic default —
    the weakest criterion, named as such). Conflict: majority rez among
    live entries; a tie is honestly NOT drafted. Glyph: confirm only when
    the payload carries a warrant. Refused drafts are never re-drafted."""
    # GUARD (a) — flag provenance: no normative authorization line, no
    # drafts. The machine cannot authorize itself.
    auth = con.execute(
        "SELECT COUNT(*) FROM ledger WHERE kind='verdict' AND "
        "payload LIKE '%machine-drafts-authorized%'").fetchone()[0]
    if not auth:
        return {"error": "no normative authorization line — the owner "
                         "must deliberately run `authorize-drafts` first; "
                         "the machine cannot authorize itself"}
    st = ruling_states(con)
    # THE SEALED RULES — bodies in zakoni, cited by body (the number is a
    # label): kopirno (rez 559), kiralno (rez 560), časovno (rez 561).
    # Drafts cite the law; the law lives in the corpus, not in the code.
    rules = {}
    for r in con.execute("SELECT number, title FROM zakoni WHERE "
                         "series='rez'"):
        t = (r["title"] or "").upper()
        key = ("kopirno" if "KOPIRNO" in t else
               "kiralno" if "KIRALNO" in t else
               "casovno" if "ČASOVNO" in t or "CASOVNO" in t else None)
        if key and key not in rules:
            rules[key] = f"REZ {r['number']} {(r['title'] or '').strip()}"
    ruled = st["human_fp"] | st["machine_fp"] | st["refused_fp"]
    drafted_m = 0

    def full_key(e):
        return (GRADE_RANK.get(e["grade"], 0), _fullness(e), -e["entry_id"])

    for p in pending_merges(con):
        if (p["word"], p["fingerprint"]) in ruled:
            continue
        rows = [dict(r) for r in con.execute(
            "SELECT e.*, d.stratum AS doc_stratum, d.kind AS doc_kind "
            "FROM entries e JOIN docs d ON d.doc_id = e.doc_id "
            "WHERE e.entry_id IN (%s)" %
            ",".join("?" * (1 + len(p["lose"]))),
            [p["keeper"]] + list(p["lose"]))]
        if not rows:
            continue
        rows.sort(key=full_key, reverse=True)
        keeper, losers = rows[0], rows[1:]
        reason = []
        top = full_key(rows[0])
        nxt = full_key(rows[1]) if len(rows) > 1 else None
        if nxt and top[:2] == nxt[:2]:
            reason.append("richest is a TIE — broken by lowest entry_id, "
                          "the weakest criterion, named as such")
        else:
            reason.append(f"richest: grade {rows[0]['grade']}, "
                          f"{_fullness(rows[0])} filled fields")
        # graft #13 — DEADLOCK AS DIMENSION-DETECTOR: when the members tie
        # on content but differ by stratum, the deadlock is not about
        # content at all — it is a CHIRAL PAIR (the register's kiralni
        # par): mirror entries, non-superimposable, the difference living
        # on the stratum axis. The draft NAMES the axis instead of
        # pretending the tie is the question.
        strata = {r.get("doc_stratum") or "?" for r in rows}
        if len(strata) > 1:
            reason.append("CHIRAL PAIR — the tie is on the content axis, "
                          "the difference is on the STRATUM axis ("
                          + " vs ".join(sorted(strata)) +
                          "); the deadlock is the dimension, named")
        # THE SEALED RULES APPLIED — a draft cites the law's body:
        # kiralno (rez 560): derived beats raw; kopirno (rez 559):
        # identical bodies, same stratum — any keeper is the same body
        if rules.get("kiralno") and "canon_ruled" in strata:
            derived = [r for r in rows
                       if r.get("doc_stratum") == "canon_ruled"]
            if derived:
                keeper = derived[0]
                losers = [r for r in rows if r is not keeper]
                reason.append(f"po {rules['kiralno']}: izpeljava "
                              "zmerge nad surovim — keeper iz canon_ruled")
        elif rules.get("kopirno") and len(strata) == 1:
            zfields = ("thesis", "antithesis", "synthesis",
                       "foneticni_rez", "ontoloski_pomen", "antinoma",
                       "glyph", "prakticna_uporaba")
            vals = [tuple((r.get(k) or "").strip() for k in zfields)
                    for r in rows]
            if all(v == vals[0] for v in vals):
                reason.append(f"po {rules['kopirno']}: identični telesi, "
                              "ista stratuma — vsak keeper je isto telo; "
                              "najnižji ID je dovolj")
        if p.get("near"):
            reason.append(f"near-dup, similarity {p['similarity']}")
        led(con, "verdict", p["word"], {
            "ruling": "draft-merge", "machine": True,
            "fingerprint": p["fingerprint"],
            "keeper": keeper["entry_id"],
            "lose": [l["entry_id"] for l in losers],
            "rationale": "; ".join(reason)})
        drafted_m += 1
    # conflicts: majority rez; a tie is honestly not drafted
    ruled_c = st["human_conflict"] | st["machine_conflict"] | \
        st["refused_conflict"]
    drafted_c = 0
    for w in [r["word"] for r in con.execute(
            "SELECT word, COUNT(DISTINCT foneticni_rez) v FROM entries "
            "WHERE merged_into IS NULL AND foneticni_rez IS NOT NULL "
            "AND TRIM(foneticni_rez) != '' GROUP BY word HAVING v > 1")]:
        if canon(w) in ruled_c:
            continue
        counts, vfmt = {}, {}
        for r in con.execute(
                "SELECT foneticni_rez, format, COUNT(*) n FROM entries "
                "WHERE word=? AND merged_into IS NULL "
                "AND TRIM(foneticni_rez) != '' "
                "GROUP BY foneticni_rez, format", (w,)):
            counts[r["foneticni_rez"]] = counts.get(r["foneticni_rez"], 0) + r["n"]
            vfmt.setdefault(r["foneticni_rez"], set()).add(r["format"])
        best = max(counts.values())
        winners = [k for k, n in counts.items() if n == best]
        if len(winners) != 1:
            continue               # majority tie — no draft, honestly
        fmts = {f for s in vfmt.values() for f in s}
        axis = ("SAME-READER disagreement — one format read the word "
                "differently at different moments (TEMPORAL axis)"
                if len(fmts) == 1 else
                "READER disagreement — formats " + "+".join(sorted(fmts)) +
                " read the word differently (FORMAT axis)")
        # THE SEALED RULE APPLIED — časovno (rez 561): same reader,
        # two moments → the NEWEST reading is the candidate (a candidate,
        # never the truth: regression can masquerade as refinement —
        # the owner's [c] returns it). Evidence (mtime, lineno) is shown.
        rule_note = ""
        if len(fmts) == 1 and rules.get("casovno"):
            latest = {}
            for r in con.execute(
                    "SELECT e.foneticni_rez, d.mtime, e.lineno FROM "
                    "entries e JOIN docs d ON d.doc_id = e.doc_id "
                    "WHERE e.word=? AND e.merged_into IS NULL AND "
                    "TRIM(e.foneticni_rez) != ''", (w,)):
                k = (str(r["mtime"] or ""), r["lineno"] or 0)
                if r["foneticni_rez"] not in latest \
                        or k > latest[r["foneticni_rez"]]:
                    latest[r["foneticni_rez"]] = k
            if latest:
                winners = [max(latest, key=latest.get)]
                rule_note = (f"po {rules['casovno']}: kandidat je "
                             "najnovejše branje (mtime "
                             + str(latest[winners[0]][0]) + ", lineno "
                             + str(latest[winners[0]][1])
                             + ") — kandidat, ne resnica; [c] vrača")
        if rule_note:
            rationale = f"{rule_note}; {axis}"
        else:
            rationale = (f"majority {winners[0]!r}: {best} of "
                         f"{sum(counts.values())} live entries; {axis}")
        led(con, "verdict", w, {
            "ruling": "conflict-true-rez-draft", "machine": True,
            "true_rez": winners[0], "counts": counts,
            "rationale": rationale})
        drafted_c += 1

    # glyphs: draft confirm only when the payload carries a warrant.
    # THE PAYLOAD BELONGS TO THE DB — its path derives from the db's OWN
    # file (PRAGMA database_list), never from CWD; an in-memory db owns
    # no file and can never touch a disk payload. (Scar 26. 9., third
    # occurrence of the same class — now structurally impossible: a
    # scratch db has no file, and a db without a file owns no glyphs.)
    drafted_g = 0
    main_file = ""
    for r in con.execute("PRAGMA database_list"):
        if r[1] == "main":
            main_file = r[2] or ""
    gp = (Path(glyph_path) if glyph_path else
          (Path(main_file).parent / "glyph_proposals.json"
           if main_file else None))
    if gp and gp.exists():
        data = json.loads(gp.read_text(encoding="utf-8"))
        for w, p in sorted(data.items()):
            if (isinstance(p, dict)
                    and p.get("verdict") == "confirm/reject"):
                if not (p.get("warrant") or "").strip():
                    continue         # nothing to stand on — no draft
                data[w]["verdict"] = "draft: confirm"
                led(con, "verdict", w, {
                    "ruling": "draft-glyph-confirm", "machine": True,
                    "glyph": p.get("glyph"),
                    "proposed_operator": p.get("proposed_operator"),
                    "rationale": f"warrant present: {p['warrant'][:120]}"})
                drafted_g += 1
        gp.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                      encoding="utf-8")
    # lexicon enrichment: HOLLOW corpus stubs (empty rez) where the
    # lexicon CARRIES the rez — the lexicon is the owner's truth layer
    # (xcheck-measured: hollow, not contradictory). The draft proposes
    # FILLING from the lexicon, provenance cited; ratify = the owner's
    # [k]; refused = never re-drafted (synthetic fingerprint channel).
    drafted_e = 0
    if main_file:
        lex_path = Path(main_file).parent / "lexicon.json"
        if lex_path.exists():
            lex = json.loads(lex_path.read_text(encoding="utf-8"))
            seen_e = st["human_fp"] | st["machine_fp"] | st["refused_fp"]
            for e in con.execute(
                    "SELECT entry_id, word, foneticni_rez FROM entries "
                    "WHERE merged_into IS NULL AND "
                    "(foneticni_rez IS NULL OR TRIM(foneticni_rez) = '')"):
                w = canon(e["word"])
                lx = next((v for k, v in lex.items()
                           if isinstance(v, dict) and canon(k) == w), None)
                if not lx or not (lx.get("source_form") or "").strip():
                    continue
                fp = f"enrich-{e['entry_id']}"
                if (w, fp) in seen_e:
                    continue
                led(con, "verdict", e["word"], {
                    "ruling": "draft-enrich-rez", "machine": True,
                    "fingerprint": fp, "entry_id": e["entry_id"],
                    "rez": lx["source_form"],
                    "rationale": "votel dosje, leksikon nosi rez "
                    f"(lexicon.json, {lx.get('provenance', 'owner layer')}; "
                    "xcheck: korpus votel, ne protislovno)"})
                drafted_e += 1
    con.commit()
    led(con, "drafts", None, {"merge": drafted_m, "conflict": drafted_c,
                              "glyph": drafted_g, "enrich": drafted_e})
    con.commit()
    return {"merge_drafts": drafted_m, "conflict_drafts": drafted_c,
            "glyph_drafts": drafted_g, "enrich_drafts": drafted_e}


def preveri(con) -> dict:
    """∮ PREVERI — the loop that verifies the verifiers (ReflektivnaZanka
    seed; Luka's 'predelaj še več po izvedbi in testiranju'): the FULL
    draft→ratify pipeline run on a SCRATCH COPY of the db and returned
    as one receipt. The live db is never touched; the owner's future
    queue is pre-reviewed — every guard and every law-citation tested
    before his keystrokes. TESTS: T1 guards (no authorization → no
    drafts) · T2 drafts cite the sealed laws · T3 the chiral keeper is
    the derived body · T4 refusal returns and never re-drafts · T5
    idempotence (a second draft run adds nothing) · T6 the replay never
    counts an unratified machine line as canon."""
    import shutil, tempfile
    ok, fails = [], []

    def t(name, cond):
        (ok if cond else fails).append(name)

    main_file = ""
    for r in con.execute("PRAGMA database_list"):
        if r[1] == "main":
            main_file = r[2] or ""
    if not main_file:
        return {"error": "preveri needs a file-backed db (the live one)"}
    with tempfile.TemporaryDirectory() as td:
        scratch = Path(td) / "preveri.db"
        shutil.copy2(main_file, scratch)
        # the payloads belong to the db: copy them beside the scratch so
        # the preview matches what the owner's real queue will hold
        for aux in ("lexicon.json", "glyph_proposals.json"):
            src_aux = Path(main_file).parent / aux
            if src_aux.exists():
                shutil.copy2(src_aux, Path(td) / aux)
        sc = sqlite3.connect(scratch)
        sc.row_factory = sqlite3.Row
        sc.execute("DROP VIEW IF EXISTS v_conflicts")
        sc.executescript(SCHEMA)
        # T1 — guards hold: no authorization, no drafts
        r1 = draft_rulings(sc)
        t("T1 brez pooblastila ni osnutkov (varovalka a)",
          "error" in r1)
        led(sc, "verdict", None, {
            "ruling": "machine-drafts-authorized",
            "by": "preveri — stand-in for the owner's deliberate act"})
        sc.commit()
        d1 = draft_rulings(sc)
        # T5 idempotentnost: the SECOND run must CREATE nothing (scar of
        # the loop's own first version: it compared return-dicts and
        # failed a correct implementation — the test was the bug)
        t("T5 idempotentnost: drugi zagon ne doda ničesar",
          all(v == 0 for v in draft_rulings(sc).values()))
        # T2 — merge drafts cite the sealed laws where they apply
        merges = [json.loads(r["payload"]) for r in sc.execute(
            "SELECT payload FROM ledger WHERE kind='verdict' AND payload "
            "LIKE '%\"ruling\": \"draft-merge\"%'")]
        citing = sum(1 for p in merges
                     if "po REZ" in (p.get("rationale") or ""))
        t(f"T2 osnutki citirajo zakone ({citing}/{len(merges)} spajanj)",
          len(merges) == 0 or citing > 0)
        # T3 — the chiral keeper is the derived body
        chiral_ok = True
        for p in merges:
            if "kiralno" in (p.get("rationale") or "").lower():
                row = sc.execute(
                    "SELECT d.stratum FROM entries e JOIN docs d "
                    "ON d.doc_id=e.doc_id WHERE e.entry_id=?",
                    (p["keeper"],)).fetchone()
                if not row or row["stratum"] != "canon_ruled":
                    chiral_ok = False
        t("T3 kiralni keeper je izpeljano telo", chiral_ok)
        # T4 — refusal returns, never re-drafts
        if merges:
            p0 = merges[0]
            led(sc, "verdict", p0.get("word"), {
                "ruling": "draft-refused",
                "fingerprint": p0.get("fingerprint")})
            sc.commit()
            before = sc.execute(
                "SELECT COUNT(*) FROM ledger WHERE kind='verdict' AND "
                "payload LIKE '%\"ruling\": \"draft-merge\"%'").fetchone()[0]
            draft_rulings(sc)
            after = sc.execute(
                "SELECT COUNT(*) FROM ledger WHERE kind='verdict' AND "
                "payload LIKE '%\"ruling\": \"draft-merge\"%'").fetchone()[0]
            t("T4 zavrnjen se nikoli ne predlaga znova", after == before)
        # T6 — the replay never canonizes an unratified machine line:
        # no machine:true fingerprint may sit in human_fp
        st = ruling_states(sc)
        bad = 0
        for r in sc.execute("SELECT word, payload FROM ledger "
                            "WHERE kind IN ('merge','verdict')"):
            p = json.loads(r["payload"])
            if (isinstance(p, dict) and p.get("machine")
                    and p.get("fingerprint")
                    and not (p.get("ratified_by") or p.get("ratified"))):
                if (canon(r["word"] or ""),
                        p["fingerprint"]) in st["human_fp"]:
                    bad += 1
        t("T6 predvajalnik ne kanonizira neodobrenega osnutka", bad == 0)
        preview = {"merge": d1.get("merge_drafts", 0),
                   "conflict": d1.get("conflict_drafts", 0),
                   "glyph": d1.get("glyph_drafts", 0),
                   "enrich": d1.get("enrich_drafts", 0)}
        sc.close()
    return {"PASS": ok, "FAIL": fails,
            "queue_preview (scratch)": preview,
            "note": "∮ preveri — potrdilo o potrdilih; živa baza "
                    "nedotaknjena; vrsta ostane Lastnikova"}


def pending_merges(con):
    """Pending = proposed but neither human-ruled nor machine-drafted.
    A REFUSED draft returns here (the owner may still rule it by hand);
    the machine simply never re-drafts it."""
    st = ruling_states(con)
    seen = st["human_fp"] | st["machine_fp"]
    out = []
    for p in propose_entry_merges(con):
        if p["needs_owner"] and (p["word"], p["fingerprint"]) not in seen:
            out.append(p)
    for p in propose_near_merges(con):
        if (p["word"], p["fingerprint"]) not in seen:
            out.append(p)
    return out


def stability(con) -> dict:
    """v2 — NORMATIVE TRACING, honestly (the register's standard): a
    word is STABLE when every ruling that shaped it is NORMATIVE — a
    human keystroke, a human edit, or a machine line CARRYING ITS
    RATIFICATION REFERENCE (ratified machine = canon, provenance shown;
    unratified machine = draft, a receipt). Fields of single-source
    uncontested entries trace to the corpus author — normative by
    origin: the owner wrote the corpus. GUARD (c) unchanged: this
    output is a receipt about receipts — it observes, it never joins.
    OBOJE-honest: the 24. 9. retro-marked merges count as canon ONLY
    through their ratification line, never silently."""
    st = ruling_states(con)
    pending = pending_merges(con)
    draft_words = {w for w, _fp in st["machine_fp"] - st["human_fp"]}
    pend_words = {p["word"] for p in pending}
    stable = open_w = variants = 0
    words = con.execute(
        "SELECT word, COUNT(*) n FROM entries WHERE merged_into IS NULL "
        "GROUP BY word").fetchall()
    for w in words:
        word = w["word"]
        if canon(word) in st["machine_conflict"] - st["human_conflict"] \
                or word in draft_words:
            open_w += 1        # a draft rests on it — not stable
        elif w["n"] == 1 and word not in pend_words and \
                canon(word) not in (st["human_conflict"] |
                                    st["machine_conflict"]):
            stable += 1
        else:
            variants += 1      # multi-entry or ruled-kept — neither raw
    return {"words": len(words), "stable": stable, "open_awaiting_drafts":
            open_w, "multi_entry_or_kept": variants,
            "pending_proposal_words": len(pend_words),
            "NOTE": "receipt about receipts — observes canon, never joins it"}



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
                                    "reparse", "xcheck", "drafts",
                                    "authorize-drafts", "stability",
                                    "popis", "graf", "odprta-delta",
                                    "ipa-popis", "ipa-drafts",
                                    "le-cenzus",
                                    "retro-honesty", "preveri",
                                    "selftest"])
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
                                else None), ensure_ascii=False))
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
    elif args.cmd == "authorize-drafts":
        # the NORMATIVE act (graft #11, guard a): only the owner's
        # deliberate keystroke creates this line — the machine never
        # authorizes itself. Run this yourself, by hand, on purpose.
        led(con, "verdict", None, {
            "ruling": "machine-drafts-authorized",
            "by": "the owner's deliberate act",
            "note": "receipts may be drafted; they never rule"})
        con.commit()
        print(json.dumps({"authorized": True,
                          "note": "machine drafts may now be written — "
                                  "they remain receipts until ratified"}))
    elif args.cmd == "drafts":
        # graft #11 — machine DRAFT rulings (receipts with rationale)
        print(json.dumps(draft_rulings(con, Path(args.path) if args.path
                                       else None), ensure_ascii=False))
    elif args.cmd == "stability":
        # graft #11 guard (c) — a receipt about receipts: observes, never joins
        print(json.dumps(stability(con), ensure_ascii=False, indent=2))
    elif args.cmd == "popis":
        # parser-zakonov's seal-POPIS — the register's fork, measured
        print(json.dumps(popis_zakoni(con), ensure_ascii=False, indent=2))
    elif args.cmd == "graf":
        # the citation graph — edges point, they never judge
        print(json.dumps(graf(con), ensure_ascii=False, indent=2))
    elif args.cmd == "odprta-delta":
        # serves rez 231 — the organ's next popis reads here
        print(json.dumps(odprta_delta(con), ensure_ascii=False, indent=2))
    elif args.cmd == "ipa-popis":
        # the honest gap: who carries the izmera, who the cut, who neither
        print(json.dumps(ipa_popis(con), ensure_ascii=False, indent=2))
    elif args.cmd == "le-cenzus":
        # ZAKON LE: whole-corpus census of the minimizem lenses — a
        # receipt, never a sodba; the reader names the Alt or frees it
        print(json.dumps(le_cenzus(con), ensure_ascii=False, indent=2))
    elif args.cmd == "ipa-drafts":
        # g2p drafts — machine proposes, owner canonizes (guard (a) holds);
        # the lexicon rides beside the db (the same derivation as the
        # enrich drafts use — PRAGMA, never cwd)
        dbrow = con.execute("PRAGMA database_list").fetchone()
        lex = (str(Path(dbrow["file"]).parent / "lexicon.json")
               if dbrow and dbrow["file"] and dbrow["file"] != ":memory:"
               else None)
        print(json.dumps(ipa_drafts(con, lex), ensure_ascii=False,
                         indent=2))
    elif args.cmd == "retro-honesty":
        # the ledger's oldest lie, repaired with witness, not laundered
        print(json.dumps(retro_mark(con), ensure_ascii=False))
    elif args.cmd == "preveri":
        # ∮ — the loop that verifies the verifiers (scratch run)
        print(json.dumps(preveri(con), ensure_ascii=False, indent=2))
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
            # mentions ("oboje"): doc-level edges — the document mentions;
            # no more piling onto the last entry
            mrows = {(r["doc_id"], r["mention"]) for r in m2.execute(
                "SELECT doc_id, mention FROM mentions")}
            assert (1, "strah") in mrows and (1, "fonetični") in mrows
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
            # graft #11: machine drafts — receipts, never rulings.
            # GUARD (a): without the owner's authorization line, no drafts
            assert "error" in draft_rulings(m)
            led(m, "verdict", None, {
                "ruling": "machine-drafts-authorized",
                "by": "selftest stand-in for the owner's deliberate act"})
            m.commit()
            # glyph drafts: only the WARRANTED item drafts; the bare one
            # stays pending. The glyph file is a TEMP one — a test must
            # never touch the real payload (scar 26. 9.: it did, reverted)
            glx = Path(td) / "gl.json"
            glx.write_text(json.dumps({
                "omega": {"glyph": "Ω", "proposed_operator": "closure",
                          "warrant": "the lattice says closure",
                          "verdict": "confirm/reject"},
                "bare": {"glyph": "∅", "proposed_operator": "void",
                         "warrant": "", "verdict": "confirm/reject"}}),
                encoding="utf-8")
            # majority conflict draft: Y gets a 2:1 majority; X is not a
            # conflict anymore (one non-empty rez) — only Y drafts, with
            # the majority tie honestly absent
            m.execute("INSERT INTO entries(doc_id, word, format, "
                      "foneticni_rez, grade) VALUES "
                      "(1, 'Y', 't', 'a / a', 'reported')")
            m.commit()
            dr = draft_rulings(m, glx)
            assert dr["conflict_drafts"] == 1
            assert dr["glyph_drafts"] == 1
            gdata = json.loads(glx.read_text(encoding="utf-8"))
            assert gdata["omega"]["verdict"] == "draft: confirm"
            assert gdata["bare"]["verdict"] == "confirm/reject"
            st = ruling_states(m)
            assert "y" in st["machine_conflict"] and "y" not in st["human_conflict"]
            # refusal: back to pending, never re-drafted
            led(m, "verdict", "Y", {"ruling": "draft-refused",
                                   "conflict": "Y"})
            m.commit()
            st = ruling_states(m)
            assert "y" in st["refused_conflict"]
            dr2 = draft_rulings(m, glx)
            assert dr2["conflict_drafts"] == 0   # refused is never re-drafted
            assert dr2["glyph_drafts"] == 0     # drafted is not re-drafted
            # lexicon enrichment: a hollow stub whose rez lives in the
            # lexicon gets an enrich DRAFT (provenance cited, never silent)
            m.execute("INSERT INTO entries(doc_id, word, format, grade, "
                      "foneticni_rez) VALUES (1, 'HOLLOW', 't', 'draft', '')")
            with tempfile.TemporaryDirectory() as td2:
                lx2 = Path(td2) / "lex.json"
                lx2.write_text(json.dumps({"hollow": {
                    "word": "HOLLOW", "source_form": "h / o / llow",
                    "provenance": "test"}}), encoding="utf-8")
                # memory db has no file: enrichment needs a file-backed db
                # (the payload-belongs-to-the-db law); witness via scratch file
                import sqlite3 as _sq
                sf = Path(td2) / "sc.db"
                m2f = _sq.connect(sf); m2f.row_factory = _sq.Row
                m2f.executescript(SCHEMA)
                m2f.execute("INSERT INTO docs(doc_id, path) VALUES (1, 'x.md')")
                led(m2f, "verdict", None, {"ruling": "machine-drafts-authorized"})
                m2f.execute("INSERT INTO entries(doc_id, word, format, grade, "
                            "foneticni_rez) VALUES (1, 'HOLLOW', 't', 'draft', '')")
                lxcp = Path(td2) / "lexicon.json"
                shutilcopy = __import__("shutil").copy2
                shutilcopy(str(lx2), str(lxcp))
                m2f.commit()
                de = draft_rulings(m2f, str(Path(td2) / "gl.json"))
                assert de["enrich_drafts"] == 1, de
                en = [json.loads(r["payload"]) for r in m2f.execute(
                    "SELECT payload FROM ledger WHERE kind='verdict' AND "
                    "payload LIKE '%draft-enrich-rez%'")]
                assert en and en[0]["rez"] == "h / o / llow"
                assert "votel" in en[0]["rationale"]
                m2f.close()
            # drafts CITE the sealed laws: a copy pair's rationale names
            # the law's body (kopirno, rez 559) — the law lives in zakoni,
            # the number is a label, the body is the key
            m.execute("INSERT INTO zakoni(doc_id, series, number, title, "
                      "lineno) VALUES (1, 'rez', 559, "
                      "'KOPIRNO PRAVILO — TELESA, KI SO ISTO TELO', 1)")
            m.execute("INSERT INTO entries(doc_id, word, format, thesis, "
                      "foneticni_rez, grade) VALUES "
                      "(1, 'KOPIRA', 't', 'ista teza', 'k / o', 'draft')")
            m.execute("INSERT INTO entries(doc_id, word, format, thesis, "
                      "foneticni_rez, grade) VALUES "
                      "(1, 'KOPIRA', 't', 'ista teza', 'k / o', 'draft')")
            m.commit()
            dr3 = draft_rulings(m, glx)
            assert dr3["merge_drafts"] >= 1
            kop = [json.loads(r["payload"]) for r in m.execute(
                "SELECT payload FROM ledger WHERE kind='verdict' AND "
                "word=?", (canon("KOPIRA"),))]
            assert kop and any("KOPIRNO" in (k.get("rationale") or "")
                               and "po REZ 559" in (k.get("rationale") or "")
                               for k in kop)
            # parser-zakonov (sealed 'daj'): laws are a SEPARATE kind —
            # grounded in rez 231's own shape, never entries
            zl = parse_zakon(
                "# REZ 232 · NASE LJU — NASLOV ZAKONA\n\n"
                "> **ZAKON:** beseda je dejanje.\n\n"
                "## TEZA\n\nZakon ima tezo, ne polaritete.\n\n"
                "## NUJNE NAPAKE\n\n- prva napaka\n- druga napaka\n\n"
                "## ODPRTA ∂\n\n- odprto vprašanje\n\n"
                "## VEZI\n\n- rez 231\n- DOKAZ #220\n\n"
                "## Meritev\n\n⊘(κ .86 · χ .84 · μ .72 · ℜ .03 · ν .75)\n\n"
                "NASLEDNJI PROSTI REZ: **233** · NASLEDNJI PROSTI DOKAZ: **#221**\n")
            assert len(zl) == 1
            z = zl[0]
            assert z["series"] == "rez" and z["number"] == 232
            assert "NASE LJU" in z["title"]
            assert "tezo" in z["teza"]
            assert "prva napaka" in z["nujne_napake"]
            assert "odprto vprašanje" in z["odprta_partial"]
            assert "rez 231" in z["vezi"]
            assert "κ .86" in z["meritev"]
            assert z["next_rez"] == 233 and z["next_dokaz"] == 221
            # prose stays prose — a doc with no series+number head is no law
            assert parse_zakon("# Beležka\n\nNavadna proza brez zakona.\n") == []
            # idempotent by witness: the same body stored twice = one law
            m.execute("INSERT INTO docs(doc_id, path) VALUES (99, 'z.md')")
            assert _insert_zakon(m, 99, z) == 1
            assert _insert_zakon(m, 99, z) == 0
            # format E: one dosje per table row, columns by header
            et = LatinTableParser().parse(
                "| Beseda | Pomen | Etimologija | Fonetični rez | "
                "Ontološki pomen |\n|---|---|---|---|---|\n"
                "| **petra** | skala | PIE *petr- | PE-TRA | "
                "tlak (P) → prehod (TRA) |\n")
            assert len(et) == 1 and et[0].word == "petra"
            assert et[0].foneticni_rez == "PE-TRA"
            assert "tlak" in et[0].ontoloski_pomen
            assert "skala" in et[0].thesis and "petr" in et[0].thesis
            # D v2: the bare "**WORD** (gloss):" head commits ONLY when
            # a fragment table follows; without a table it is not a dosje
            dv2 = RezFragmentParser().parse(
                "**GEO** (gola zemlja):\n\n| Fragment | Pomen |\n"
                "|---|---|\n| **G** | golota |\n\nBranje: GEO = tla.\n")
            assert len(dv2) == 1 and dv2[0].word == "GEO"
            assert RezFragmentParser().parse(
                "**Naslov** (kratek):\n\nNavadna proza brez tabele.\n") == []
            # format F (UNOV-secirava): the two-layer word reading —
            # Sloj 1 izmera / Sloj 2 poskus; a section without the Sloj
            # pair (Tri pisave, h-rana closers, V.*) is NOT a word entry;
            # the word's IPA only when a bold word carries it (a bare
            # ASCII /token/ is a URL, a bare single-letter token is a
            # phoneme — both measured, both excluded)
            fu = UnovSeciravaParser().parse(
                "### toraj / zdaj (Lukov rez, 26. 9. 2026)\n\n"
                "**Sloj 1 — IZMERA (⊢):** *toraj* /tɔˈɾaj/ gesli ⚠ "
                "(ne izmišljam razlage).\n\n"
                "**Sloj 2 — POSKUS (APD ↑):** sedanjost nosi daj. "
                "Hrana katere rane: rane sedanjosti.\n\n"
                "### Tri pisave\n\nProza brez slojev.\n")
            assert len(fu) == 1 and fu[0].word == "toraj / zdaj"
            assert fu[0].foneticni_rez == "/tɔˈɾaj/"
            assert fu[0].ontoloski_pomen.startswith("Lukov rez")
            assert "IZMERA" not in fu[0].thesis and "toraj" in fu[0].thesis
            assert fu[0].prakticna_uporaba.startswith("Hrana katere rane")
            assert UnovSeciravaParser().parse(
                "### glas / grlo\n\n**Sloj 1 — IZMERA (⊢):** IPA obeh ⚠ "
                "(ni vira); [vir](/libraries/01).\n\n"
                "**Sloj 2 — POSKUS:** glas je grlo z dihom.\n"
                )[0].foneticni_rez == ""      # no word-IPA: stays empty
            # multi-law bodies (the named ∂, built): one doc may carry MANY
            # laws — each kept with its own witness; fields never leak
            # across heads; a bold citation without a separator stays a VEZI
            ml = parse_zakon(
                "# SECIRAVA telesa\n\n"
                "**UBOD #1 — prvi stavek:**\n> »citat«\n\n"
                "prosa za prvi ubod.\n\n"
                "## NUJNE NAPAKE\n- prva napaka\n\n"
                "**UBOD #2 — drugi stavek:**\n> »citat dva«\n\n"
                "prosa za drugega.\n\n"
                "**REZ 559** pravi nekaj v prezi. (citat, ne glava)\n")
            assert len(ml) == 2
            assert ml[0]["series"] == "ubod" and ml[0]["number"] == 1
            assert "prva napaka" in ml[0]["nujne_napake"]
            assert ml[1]["number"] == 2 and "prva napaka" not in \
                ml[1]["nujne_napake"]          # no leak across heads
            assert all(z["number"] != 559 for z in ml)   # citation not a head
            # the ZAKONIK series (Luka's "da, uzakonodaji vse to"): a
            # one-line sealed law — the whole body lives on the head line;
            # the rest-of-line is the teza; a heading between heads does
            # not leak into the earlier body's fields
            zz = parse_zakon(
                "# REGISTER\n\n## ZAKONIK\n\n"
                "**Z-1 ZAKON VEJE** — citat je množina. ⊢\n\n"
                "**Z-2 ZAKON MEHANIZMA** — popravek izvede mehanizem. ⊢\n\n"
                "### VELJA\n- brst, ne sad\n")
            assert len(zz) == 2
            assert zz[0]["series"] == "zakon" and zz[0]["number"] == 1
            assert "citat je množina" in zz[0]["teza"]
            assert "brst, ne sad" not in zz[1]["teza"]  # no leak past heads
            # IPA LAYER (Luka's "daj", 26. 9.): the g2p is a DRAFT machine —
            # phoneme level, no stress (unpredictable without a dictionary,
            # honestly omitted), digraphs measured (ljubezen → ʎ, nj → ɲ)
            assert slo_g2p("ne") == "/nɛ/"
            assert slo_g2p("dih") == "/dix/"
            assert slo_g2p("ljubezen") == "/ʎubɛzɛn/"
            assert slo_g2p("njuja") == "/ɲuja/"
            # GUARD (a): no authorization line, no ipa drafts (a FRESH
            # db — the main scratch db already carries the stand-in line
            # from the earlier drafts witnesses)
            mf = sqlite3.connect(":memory:")
            mf.row_factory = sqlite3.Row
            mf.executescript(SCHEMA)
            mf.execute("INSERT INTO docs(doc_id, path) VALUES (1, 'f.md')")
            mf.execute("INSERT INTO entries(doc_id, word, format, "
                       "foneticni_rez, grade) VALUES (1, 'Fih', 't', "
                       "'f / i / h', 'draft')")
            r = ipa_drafts(mf)
            assert "error" in r                 # the machine cannot self-start
            led(mf, "verdict", None, {"ruling": "machine-drafts-authorized",
                                      "note": "selftest stand-in"})
            r = ipa_drafts(mf)
            assert r["ipa_drafts"] == 1         # the cut-bearing word drafted
            drafted = mf.execute("SELECT word, payload FROM ledger WHERE "
                                 "payload LIKE '%\"ruling\": \"draft-ipa\"%'"
                                 ).fetchall()
            assert drafted and "⚠" in drafted[0]["payload"]
            # ratify through the ledger: the edit line carries the
            # fingerprint — the replay counts it canon through reference
            p0 = json.loads(drafted[0]["payload"])
            mf.execute("UPDATE entries SET ipa=? WHERE entry_id=?",
                       (p0["ipa"], p0["entry_id"]))
            led(mf, "edit", drafted[0]["word"], {
                "entry_id": p0["entry_id"], "ipa": p0["ipa"],
                "fingerprint": f"ipa-{p0['entry_id']}",
                "note": "ratified ipa (selftest witness)"})
            stf = ruling_states(mf)
            fp = (canon(drafted[0]["word"]), f"ipa-{p0['entry_id']}")
            assert fp in stf["human_fp"] or fp in stf["machine_fp"]
            assert ipa_drafts(mf)["ipa_drafts"] == 0   # never re-drafted
            # the popis measures the honest gap: cut ≠ izmera ≠ nothing
            pop = ipa_popis(m)
            assert pop["live_words"] >= 1 and pop["with_rez_cut"] >= 1
            assert pop["with_ipa"] == 0        # nothing ratified on m
            # retro-honesty: an unmarked machine merge becomes canon
            # THROUGH its ratification line, never silently
            m.execute("INSERT INTO ledger(ts, kind, word, payload) "
                      "VALUES ('t', 'merge', 'STARI', ?)",
                      (json.dumps({"word": "stari", "keeper": 1,
                                   "lose": [2], "fingerprint": "ab",
                                   "rule": "machine-ruled 24.9."}),))
            m.commit()
            st_before = ruling_states(m)
            assert ("stari", "ab") in st_before["human_fp"]  # the lie
            rm = retro_mark(m)
            assert rm["marked"] >= 1
            st_after = ruling_states(m)
            assert ("stari", "ab") in st_after["human_fp"]  # canon, provenanced
            row = json.loads(m.execute(
                "SELECT payload FROM ledger WHERE kind='merge' AND "
                "word='STARI'").fetchone()["payload"])
            assert row["machine"] is True and row["ratified_by"]
            # graf + odprta-delta run clean on a populated db
            g = graf(m)
            assert "doc_word_edges" in g and "law_law_edges" in g
            od = odprta_delta(m)
            assert od["laws_with_open_delta"] >= 1  # rez-231 witness lives
            # laws NEVER become words: entries untouched
            n_before = m.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
            assert m.execute("SELECT COUNT(*) FROM zakoni").fetchone()[0] >= 1
            assert m.execute("SELECT COUNT(*) FROM entries").fetchone()[0] == n_before
        print("selftest: plugins A/B/D/E/F, grading, canon, near-dup, page, "
              "conflicts-view, dark, page-export, scan-absolute, doc-typing, "
              "doc-level mentions, laws (parser-zakonov, multi-head), "
              "drafts + guards (cite/retro/refuse/idempotence), enrichment, "
              "ipa layer (g2p/popis/guard/ratify/never-re-drafted), graf, "
              "odprta-delta — OK (traced here, witnessed on disk)")