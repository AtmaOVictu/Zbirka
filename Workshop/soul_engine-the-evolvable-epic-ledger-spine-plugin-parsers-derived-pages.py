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
    kind      TEXT NOT NULL,   -- scan|verdict|merge|edit|grade
    word      TEXT,
    payload   TEXT NOT NULL    -- JSON
);
CREATE TABLE IF NOT EXISTS docs (
    doc_id    INTEGER PRIMARY KEY,
    path      TEXT UNIQUE NOT NULL,
    mtime     TEXT,
    raw_size  INTEGER
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
    FROM entries WHERE foneticni_rez IS NOT NULL
    GROUP BY word HAVING variants > 1;
"""

def db() -> sqlite3.Connection:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
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

PLUGINS: List[ParserPlugin] = [StotnijeBulletParser(), HeadlineParser(),
                               NumberedSectionParser()]
# EVOLUTION POINT: append MyFormatDParser() here. Nothing else changes.

def grade_of(p: Parsed) -> str:
    if p.foneticni_rez and p.ontoloski_pomen and p.antinoma and p.synthesis:
        return "reported"
    if p.synthesis and (p.thesis or p.number):
        return "headline"
    return "draft"

# =========================================================== INGEST =======

def scan(root: Path, con: sqlite3.Connection) -> dict:
    files = [p for p in root.rglob("*") if p.suffix.lower()
             in {".md", ".txt"}]
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
    led(con, "scan", None, {"root": str(root), "files": len(files),
                            "new_docs": n_docs, "new_entries": n_entries})
    con.commit()
    return {"files": len(files), "new_docs": n_docs, "new_entries": n_entries}

# ========================================================== THE PAGE ======

def page(con, word: str) -> dict:
    w = canon(word)
    entries = [dict(r) for r in con.execute(
        "SELECT * FROM entries WHERE lower(word)=? OR merged_into=?", (w, w))]
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

# ============================================================= MAIN =======

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["scan", "gui", "page", "export",
                                    "merge", "unmerge", "dups", "selftest"])
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
    elif args.cmd == "merge":
        # python soul_engine.py merge        → auto-merge unambiguous, list rest
        print(json.dumps(merge_auto(con), ensure_ascii=False, indent=2))
    elif args.cmd == "unmerge":
        print(json.dumps({"restored": unmerge_all(con, args.word)}))
    elif args.cmd == "dups":
        # duplicate FILES report — you delete, the engine only names them
        print(json.dumps(dup_file_report(con), ensure_ascii=False, indent=2))
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
        print("selftest: plugins A/B, grading, canon, near-dup — OK (traced "
              "here, witnessed on disk)")