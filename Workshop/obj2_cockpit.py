"""
OBJ2 COCKPIT — the review interface for the canon and its receipts
LOVE CAGE / Obj2 — obj2_cockpit.py. 24. 9. 2026.

PURPOSE (scoped deliberately): this is the PROCESSING/REVIEW cockpit, not the
game. SODBA #002: a self-test result written and run by the same hand that
built the file is a receipt, not canon; Luka's own review turns it. This
window makes that review one click. It is container-agnostic: it processes
canvases, receipts, ledgers and decisions — no cubes, no balls, no world
assumptions. The game view waits for the ball spec.

TABS
  CANVAS     browse + search every .md canvas/canon file in Obj2
  RECEIPTS   run each sister file's self-test, see PASS/FAIL + full output
             (each run in its own thread — the window never freezes)
  PERFORM    utter a chain live: state bars vs guard thresholds, ledger
             lines, verdict (WORD/DISCOVERY/FOREIGN + PASS/MORAVA/HOLD/FALL)
  REVIEW     graft #1+#2: the owner's queues, one toggle, two sources.
             MERGE queue — soul_engine's proposals: ambiguous exact dups
             (needs_owner) and near-dups (graft #2: one small edit apart —
             typo or refinement, the machine cannot know). [k] keep the
             proposed keeper · [m] merge with your own keeper · [c] conflict
             — not duplicates, real variants · [s] skip.
             GLYPH queue — glyph_proposals.json: [k] confirm, [c] reject the
             proposed glyph→operator mapping (verdict written to the payload).
             Every ruling is a ledger line in soul.db; the pending merge queue
             is derived by replaying the ledger — the machine proposes, you rule.
  LIBRARY    graft #3: browse the spine — every live word in soul.db with
             its sources and grades; select one and its page (entries,
             mentions, conflicts) derives by soul_engine's own page().
             "export ruled page" = graft #7: the ruled page written OUT as
             a derived dosje (canon_ruled stratum), ledger-witnessed;
             a rescan admits it back through the ordinary door.
  PARK       the decision records + inventory of the parked cube era

LAWS
  stdlib only (tkinter/ttk) — the Comprehension workbench precedent
  the sisters are loaded by path (their names carry hyphens)
  running a self-test here is STILL a receipt-by-proxy — the honest review
  is you running the same file yourself; this window just shows you what
  you should expect to see.

Run:        python obj2_cockpit.py
Smoke test: python obj2_cockpit.py --smoke   (constructs, no mainloop)
"""

from __future__ import annotations
import json
import os
import queue
import re
import subprocess
import sys
import threading
import importlib.util
import tkinter as tk
from tkinter import ttk, filedialog

_HERE = os.path.dirname(os.path.abspath(__file__))

SISTERS = [
    # (display name, filename, expected)
    ("phonetic_coordinates_full.py (the lattice)", "phonetic_coordinates_full.py",
     "ALL CHECKS PASSED"),
    ("apd_engine (the runtime)", "apd_engine-py-apd-runtime-for-love-cage-deliverable-2.py",
     "PASS — apd_engine"),
    ("wordlist_validator (the finiteness layer)", "wordlist_validator.py",
     "PASS — the finiteness layer"),
    ("pass-3 rival (KNOWN CRASH — parked strata)", "phonetic_coordinates_107-py-the-full-universe-extension-of-the-obj2-lattice.py",
     None),  # expected crash: receipts tab shows the scar, not a failure of the tab
]

DECISION_RECORDS = [
    "decision-balls-not-cubes-parking-the-cube-layer.md",
]


def _load(fname):
    spec = importlib.util.spec_from_file_location(fname.replace("-", "_").split(".")[0],
                                                  os.path.join(_HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod   # required: dataclasses resolve annotations via sys.modules
    spec.loader.exec_module(mod)
    return mod


try:
    VALIDATOR = _load("wordlist_validator.py")   # pulls lattice+engine+pass3 transitively
    ENGINE = VALIDATOR.ENGINE
except Exception as e:
    VALIDATOR = None
    _LOAD_ERROR = str(e)

SOUL_FILE = "soul_engine-the-evolvable-epic-ledger-spine-plugin-parsers-derived-pages.py"
try:
    SOUL = _load(SOUL_FILE)                     # the spine: soul.db, ledger, merge queue
    SOUL.DB_PATH = os.path.join(_HERE, "soul.db")   # the .bat runs from _HERE; be explicit
except Exception as e:
    SOUL = None
    _SOUL_LOAD_ERROR = str(e)


# =============================================================================
# CANVAS TAB — browse and search every .md in Obj2
# =============================================================================

class CanvasTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=8)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        bar = ttk.Frame(self)
        bar.grid(row=0, column=0, sticky="ew")
        ttk.Label(bar, text="search:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(bar, textvariable=self.search_var)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=4)
        self.search_entry.bind("<Return>", self.search)
        ttk.Button(bar, text="find", command=self.search).pack(side="left")
        self.files_var = tk.StringVar(value=f"{len(self._files())} files")
        ttk.Label(bar, textvariable=self.files_var).pack(side="left", padx=8)

        self.listbox = tk.Listbox(self, width=44)
        self.listbox.grid(row=1, column=0, sticky="ew", pady=(6, 2))
        self.text = tk.Text(self, wrap="word", state="disabled", width=80)
        self.text.grid(row=2, column=0, sticky="nsew", pady=2)
        self.results = tk.Text(self, height=6, wrap="none", state="disabled")
        self.results.grid(row=3, column=0, sticky="ew", pady=2)
        self.results.tag_configure("hit", foreground="#6cf")
        self.results.bind("<Double-Button-1>", self._open_hit)
        self.results.bind("<Return>", self._open_hit)
        self.text.tag_configure("hitline", background="#3a4a2a")
        self._fill_list()
        self.listbox.bind("<Double-Button-1>", self._open)
        self.listbox.bind("<Return>", self._open)

    def _files(self):
        return sorted(
            (f for f in os.listdir(_HERE) if f.lower().endswith((".md", ".txt"))),
            key=lambda f: -os.path.getmtime(os.path.join(_HERE, f)))

    def _fill_list(self):
        self.listbox.delete(0, "end")
        for f in self._files():
            self.listbox.insert("end", f)
        self.files_var.set(f"{len(self._files())} files")

    def _open(self, _event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        fname = self.listbox.get(sel[0])
        try:
            with open(os.path.join(_HERE, fname), encoding="utf-8", errors="replace") as fh:
                content = fh.read()
        except OSError as e:
            content = f"[cannot read: {e}]"
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
        self.text.configure(state="disabled")

    def _open_hit(self, event=None):
        """Double-click (or Return on) a search hit: open that file at that
        line. Hit lines read `file:lineno: text` — filenames carry no ':'."""
        pos = self.results.index(f"@{event.x},{event.y}") if hasattr(event, "x") else "insert"
        line_no = int(pos.split(".")[0])
        text = self.results.get(f"{line_no}.0", f"{line_no}.end")
        m = re.match(r"^(.+?):(\d+):", text)
        if not m:
            return
        fname, lineno = m.group(1), int(m.group(2))
        if fname not in self._files():
            return
        for i, f in enumerate(self.listbox.get(0, "end")):
            if f == fname:
                self.listbox.selection_clear(0, "end")
                self.listbox.selection_set(i)
                self.listbox.see(i)
                break
        self._open(fname)
        self.text.configure(state="normal")
        self.text.tag_remove("hitline", "1.0", "end")
        self.text.tag_add("hitline", f"{lineno}.0", f"{lineno}.end")
        self.text.see(f"{lineno}.0")
        self.text.configure(state="disabled")

    def search(self):
        needle = self.search_var.get().strip()
        self.results.configure(state="normal")
        self.results.delete("1.0", "end")
        if not needle:
            self.results.insert("end", "[empty query]")
        hits = 0
        for f in self._files():
            try:
                with open(os.path.join(_HERE, f), encoding="utf-8", errors="replace") as fh:
                    for i, line in enumerate(fh, 1):
                        if needle.lower() in line.lower():
                            self.results.insert("end", f"{f}:{i}: {line.strip()[:120]}\n", ("hit",))
                            hits += 1
                            if hits >= 200:
                                self.results.insert("end", "[...truncated at 200 hits]\n")
                                break
            except OSError:
                continue
            if hits >= 200:
                break
        if hits == 0:
            self.results.insert("end", f"[no hits for {needle!r}]")
        self.results.configure(state="disabled")


# =============================================================================
# RECEIPTS TAB — run the sisters' self-tests, show the receipt
# =============================================================================

class ReceiptsTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=8)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        ttk.Label(self, text="SODBA #002: these runs are receipts shown by proxy — "
                             "canon is YOUR run of the same file.").grid(row=0, column=0, sticky="w")
        box = ttk.Frame(self)
        box.grid(row=1, column=0, sticky="nsew", pady=4)
        box.columnconfigure(0, weight=1)
        box.rowconfigure(1, weight=1)
        self.tree = ttk.Treeview(box, columns=("status",), show="tree headings", height=6)
        self.tree.heading("#0", text="file")
        self.tree.heading("status", text="self-test status")
        self.tree.column("#0", width=420)
        self.tree.column("status", width=160)
        self.tree.grid(row=0, column=0, sticky="ew")
        self.out = tk.Text(box, wrap="word", state="disabled")
        self.out.grid(row=1, column=0, sticky="nsew", pady=4)
        btns = ttk.Frame(box)
        btns.grid(row=2, column=0, sticky="w")
        ttk.Button(btns, text="run all", command=self.run_all).pack(side="left")
        ttk.Label(btns, text="  double-click a row to run one").pack(side="left")
        for name, fname, expected in SISTERS:
            self.tree.insert("", "end", iid=fname, text=name,
                             values=("not run",), tags=(fname,))
        self.tree.bind("<Double-Button-1>", lambda e: self.run_one(self.tree.selection()[0])
                       if self.tree.selection() else None)
        self._running = set()
        self._done = queue.Queue()
        self.after(200, self._poll)

    def _worker(self, fname):
        """Runs in its own thread — subprocess blocks there, never the UI."""
        try:
            proc = subprocess.run([sys.executable, os.path.join(_HERE, fname)],
                                  capture_output=True, text=True, timeout=120,
                                  encoding="utf-8", errors="replace", cwd=_HERE)
            blob = (proc.stdout or "") + (proc.stderr or "")
            ok = proc.returncode == 0
        except Exception as e:
            ok, blob = False, f"[run error: {e}]"
        self._done.put((fname, ok, blob))

    def _poll(self):
        try:
            while True:
                fname, ok, blob = self._done.get_nowait()
                self._running.discard(fname)
                self._show(fname, ok, blob)
        except queue.Empty:
            pass
        self.after(200, self._poll)

    def _show(self, fname, ok, blob):
        expected = next(exp for n, f, exp in SISTERS if f == fname)
        status = "PASS (receipt)" if ok else "FAIL (see scar)"
        self.tree.item(fname, values=(status,))
        self.out.configure(state="normal")
        self.out.delete("1.0", "end")
        head = f"=== {os.path.basename(fname)} — {status} ===\n"
        if expected is None and not ok:
            head += ("(parked strata: this file's self-test is known to crash — "
                     "see the park record; the crash is the scar, not a surprise)\n")
        self.out.insert("1.0", head + blob[-6000:])
        self.out.configure(state="disabled")

    def run_one(self, fname):
        if fname not in dict((f, 1) for _n, f, _e in SISTERS) or fname in self._running:
            return
        self._running.add(fname)
        self.tree.item(fname, values=("running…",))
        threading.Thread(target=self._worker, args=(fname,), daemon=True).start()

    def run_all(self):
        for _n, fname, _e in SISTERS:
            self.run_one(fname)


# =============================================================================
# PERFORM TAB — utter a chain, watch the guard
# =============================================================================

PARAMS = [
    # (attribute, label, threshold kind, good direction)
    ("alpha", "α namera", None, "high"),
    ("kappa", "κ konsistentnost", (">=", 0.70), "high"),
    ("chi", "χ klariteta", (">=", 0.40), "high"),
    ("mu", "μ povezanost", ("band", (0.50, 0.80)), "band"),
    ("rho", "ρ resonanca", None, "high"),
    ("Re", "ℜ odstopek", ("<=", 0.03), "low"),
    ("ora", "λ+ ORA", None, "mid"),
    ("lab", "λ− LAB", None, "mid"),
]


class PerformTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=8)
        if VALIDATOR is None:
            ttk.Label(self, text=f"cannot load sisters: {_LOAD_ERROR}").grid(row=0, column=0)
            return
        self.state = ENGINE.State()
        self.ledger = ENGINE.Ledger()

        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew")
        ttk.Label(top, text="chain:").pack(side="left")
        self.chain_var = tk.StringVar(value="l ʌ v")
        ttk.Entry(top, textvariable=self.chain_var, width=24).pack(side="left", padx=4)
        ttk.Label(top, text="language:").pack(side="left")
        self.lang_var = tk.StringVar(value="en")
        ttk.Combobox(top, textvariable=self.lang_var, values=("en", "sl", "de"),
                     width=4, state="readonly").pack(side="left", padx=4)
        ttk.Button(top, text="PERFORM", command=self.perform).pack(side="left", padx=6)

        def preset(chain, lang):
            self.chain_var.set(chain)
            self.lang_var.set(lang)
            self.perform()
        ttk.Label(top, text="  presets:").pack(side="left")
        for label, chain, lang in (("love", "l ʌ v", "en"),
                                   ("ljubezen", "ʎ u b e z ɛ n", "sl"),
                                   ("cat", "k æ t", "en"),
                                   ("zima", "z i m a", "sl")):
            ttk.Button(top, text=label, command=lambda c=chain, l=lang: preset(c, l)
                       ).pack(side="left", padx=1)
        ttk.Button(top, text="reset state", command=self.reset).pack(side="left")
        ttk.Button(top, text="export ledger CSV", command=self.export_csv).pack(side="left", padx=6)

        self.verdict_var = tk.StringVar(value="— nothing uttered yet —")
        self.verdict_lbl = ttk.Label(self, textvariable=self.verdict_var,
                                     font=("TkDefaultFont", 11, "bold"))
        self.verdict_lbl.grid(row=1, column=0, sticky="w", pady=4)

        self.bars = tk.Canvas(self, height=190, bg="#111")
        self.bars.grid(row=2, column=0, sticky="ew", pady=4)

        cols = ("ts", "event", "witnessed", "Δα", "Δκ", "Δχ", "Δμ", "Δρ", "Δℜ", "gate", "note")
        self.ledger_tree = ttk.Treeview(self, columns=cols, show="headings", height=10)
        for c, w in zip(cols, (36, 80, 64, 52, 52, 52, 52, 52, 52, 100, 140)):
            self.ledger_tree.heading(c, text=c)
            self.ledger_tree.column(c, width=w, anchor="center")
        self.ledger_tree.grid(row=3, column=0, sticky="ew", pady=4)
        self.columnconfigure(0, weight=1)

    def reset(self):
        self.state = ENGINE.State()
        self.ledger = ENGINE.Ledger()
        self.ledger_tree.delete(*self.ledger_tree.get_children())
        self.verdict_var.set("— state reset —")
        self.bars.delete("all")

    def perform(self):
        chain = [tok for tok in self.chain_var.get().split() if tok]
        lang = self.lang_var.get()
        try:
            verdict, gate, lines = VALIDATOR.run_chain(chain, lang, self.state, self.ledger)
        except Exception as e:
            self.verdict_var.set(f"ERROR: {e}")
            return
        cur = self.verdict.classification if hasattr(self, "verdict") else ""
        extra = ""
        if verdict.classification == "WORD":
            extra = f"WORD: {verdict.word}"
        elif verdict.classification == "DISCOVERY":
            extra = f"DISCOVERY: {verdict.note}"
        else:
            extra = f"FOREIGN: curious = {verdict.curious}"
        self.verdict = verdict
        self.verdict_var.set(f"{verdict.classification} | {extra} | guard: {gate} | {lines} lines")
        color = {"PASS/MORAVA": "#2a2", "HOLD": "#a80", "FALL": "#c22"}.get(gate, "#ccc")
        self.verdict_lbl.configure(foreground=color)
        for row in self.ledger.rows[-lines:]:
            d = row
            self.ledger_tree.insert("", "end", values=(
                d["ts"], d["event"], d["witnessed"],
                d["delta_alpha"], d["delta_kappa"], d["delta_chi"], d["delta_mu"],
                d["delta_rho"], d["delta_Re"], d["gate"], d["note"]))
        self.draw_bars()

    def draw_bars(self):
        c = self.bars
        c.delete("all")
        w = int(c.winfo_width()) or 600
        h = 190
        n = len(PARAMS)
        bw = max(28, (w - 40) // n - 12)
        for i, (attr, label, thr, good) in enumerate(PARAMS):
            x = 20 + i * (bw + 12)
            v = max(0.0, min(1.0, getattr(self.state, attr)))
            # param bar
            c.create_rectangle(x, 20, x + bw, 20 + 120, outline="#444")
            fill_h = int(120 * v)
            color = "#48c"
            if thr:
                kind = thr[0]
                if kind == ">=" and v >= thr[1]:
                    color = "#2a2"
                elif kind == "<=" and v <= thr[1]:
                    color = "#2a2"
                elif kind == "band" and thr[1][0] <= v <= thr[1][1]:
                    color = "#2a2"
                else:
                    color = "#c66"
            c.create_rectangle(x, 20 + 120 - fill_h, x + bw, 140, fill=color, outline="")
            # threshold marks
            if thr:
                if thr[0] == ">=":
                    ty = 20 + 120 - int(120 * thr[1])
                    c.create_line(x - 4, ty, x + bw + 4, ty, fill="#ff4", dash=(3, 2))
                elif thr[0] == "<=":
                    ty = 20 + 120 - int(120 * thr[1])
                    c.create_line(x - 4, ty, x + bw + 4, ty, fill="#ff4", dash=(3, 2))
                elif thr[0] == "band":
                    lo, hi = thr[1]
                    ylo = 20 + 120 - int(120 * lo)
                    yhi = 20 + 120 - int(120 * hi)
                    c.create_rectangle(x - 4, yhi, x + bw + 4, ylo, outline="#ff4", dash=(3, 2))
            c.create_text(x + bw // 2, 8, text=label, fill="#ddd", font=("TkDefaultFont", 8))
            c.create_text(x + bw // 2, 152, text=f"{v:.3f}", fill="#fff",
                          font=("TkDefaultFont", 9, "bold"))
            c.create_text(x + bw // 2, 168, text=attr, fill="#888",
                          font=("TkDefaultFont", 7))
        gate = ENGINE.guard(self.state)
        star = ENGINE.e_star(self.state, ledger_has_line=len(self.ledger.rows) > 0)
        c.create_text(w - 60, 182, text=f"guard: {gate}   E⋆: {star}",
                      fill="#2f2" if gate == "PASS/MORAVA" else "#fa3",
                      font=("TkDefaultFont", 9, "bold"), anchor="e")

    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            initialfile="ledger.csv",
                                            initialdir=_HERE)
        if path:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(self.ledger.csv())
            self.verdict_var.set(f"ledger exported: {os.path.basename(path)}")


# =============================================================================
# REVIEW TAB — graft #1: the owner's queue, ruled by keypress (k/c/m/s)
# =============================================================================

REVIEW_RULES = [
    ("k", "keep", "accept the proposed keeper, losers merge into it"),
    ("m", "merge", "overrule the tie — a chooser opens, you pick the keeper"),
    ("c", "conflict", "not duplicates: real variants, no merge"),
    ("s", "skip", "stays in the queue, next item"),
]

GLYPH_FILE = "glyph_proposals.json"

GLYPH_RULES = [
    ("k", "confirm", "accept the proposed glyph→operator mapping"),
    ("c", "reject", "keep the glyph, refuse the proposed operator"),
    ("s", "skip", "stays in the queue, next item"),
]

CONFLICT_RULES = [
    ("k", "true rez", "pick which fonetični rez is the true one — a chooser opens"),
    ("c", "variants", "both are real variants — no single truth, they stay"),
    ("s", "skip", "stays in the queue, next item"),
]

RATIFY_RULES = [
    ("k", "ratify", "accept the DRAFT — its receipt becomes canon"),
    ("c", "refuse", "reject the draft — back to pending, never re-drafted"),
    ("m", "amend", "rule it your way — a chooser opens"),
    ("s", "skip", "stays in the queue, next item"),
]


class ReviewTab(ttk.Frame):
    """The owner's queues, ruled by keypress. Two queues, one tab:
      MERGE  soul_engine's proposals — ambiguous exact duplicates (the
             machine could not pick a strictly richest keeper) AND near-dups
             (graft #2: same word, near-identical fields, one small edit —
             the difference is either a typo or a refinement, always yours)
      GLYPH  glyph_proposals.json — proposed glyph→operator mappings,
             payload fields "verdict": "confirm/reject" await your ruling.
      CONFLICT words whose LIVE entries carry more than one fonetični rez
             (graft #5; the ghosts — empty rez, merged losers — are
             filtered out by the repaired v_conflicts). [k] a chooser
             opens, you pick the TRUE rez, it is written onto the other
             entries, the old values survive in the ledger · [c] both
             are real variants, they stay · [s] skip.
    LAWS (both queues):
      - every ruling is a LEDGER LINE in soul.db (kind merge or verdict);
        nothing is deleted, ever. Glyph verdicts are ALSO written back into
        the payload — the ledger witnesses, the payload records.
      - the merge queue is DERIVED by replaying the ledger (a proposal
        leaves only when the ledger carries a ruling for its
        (word, fingerprint)) — the spine's own architecture, not a new table
      - skip writes nothing: deferred means it stays, honestly"""

    MERGE_COLS = ("id", "role", "word", "format", "grade", "thesis/synthesis",
                  "fonetični rez", "ontološki pomen", "antinoma", "glyph", "doc:line")
    MERGE_W = (50, 90, 130, 70, 70, 230, 130, 160, 110, 60, 80)
    GLYPH_COLS = ("word", "glyph", "proposed operator", "warrant", "verdict", "unmapped")
    GLYPH_W = (110, 230, 250, 250, 110, 80)
    CONFLICT_COLS = ("word", "fonetični rez", "grade", "format", "doc:line",
                     "thesis/synthesis")
    CONFLICT_W = (130, 230, 70, 90, 80, 260)
    RATIFY_COLS = ("queue", "word", "draft decision", "rationale (read before [k])")
    RATIFY_W = (80, 130, 260, 520)
    MODE_CYCLE = {"merge": "glyph", "glyph": "conflict", "conflict": "ratify",
                  "ratify": "merge"}

    def __init__(self, parent):
        super().__init__(parent, padding=8)
        self.alive = False
        self.btns = {}
        self.merge_queue = []
        self.glyph_queue = []
        self.conflict_queue = []
        self.ratify_queue = []
        self._k_streak = 0     # guard (b): ratifications without amendment
        self.mode = "merge"
        self.i = 0
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        if SOUL is None:
            ttk.Label(self, text=f"cannot load the spine (soul_engine): "
                                f"{_SOUL_LOAD_ERROR}").grid(row=0, column=0, sticky="w")
            return
        if not os.path.exists(SOUL.DB_PATH):
            ttk.Label(self, text=f"the spine's db is missing: {SOUL.DB_PATH} — "
                                "run soul_engine scan first").grid(row=0, column=0, sticky="w")
            return
        self.con = SOUL.db()
        self.alive = True

        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew")
        self.status_var = tk.StringVar(value="— loading the queue —")
        ttk.Label(top, textvariable=self.status_var,
                  font=("TkDefaultFont", 10, "bold")).pack(side="left")
        self.mode_btn = ttk.Button(top, text="…", command=self.switch_mode)
        self.mode_btn.pack(side="right", padx=(6, 0))
        ttk.Button(top, text="reload queue", command=self.load).pack(side="right")

        self.rules_var = tk.StringVar()
        ttk.Label(self, textvariable=self.rules_var).grid(row=1, column=0, sticky="w")

        self._build_tree()

        bar = ttk.Frame(self)
        bar.grid(row=3, column=0, sticky="ew")
        for key, short in (("k", "keep"), ("m", "merge"),
                           ("c", "conflict"), ("s", "skip")):
            b = ttk.Button(bar, text=f"[{key}] {short}",
                           command=lambda k=key: self._rule(k))
            b.pack(side="left", padx=(0, 6))
            self.btns[key] = b
        self.load()

    def _build_tree(self):
        if hasattr(self, "tree"):
            self.tree.destroy()
        if self.mode == "merge":
            cols, widths = self.MERGE_COLS, self.MERGE_W
        elif self.mode == "conflict":
            cols, widths = self.CONFLICT_COLS, self.CONFLICT_W
        elif self.mode == "ratify":
            cols, widths = self.RATIFY_COLS, self.RATIFY_W
        else:
            cols, widths = self.GLYPH_COLS, self.GLYPH_W
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c, w in zip(cols, widths):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="w")
        self.tree.grid(row=2, column=0, sticky="nsew", pady=4)
        self.tree.tag_configure("keeper", background="#2b3a2b")

    def queue(self):
        return getattr(self, f"{self.mode}_queue")

    def switch_mode(self):
        self.mode = self.MODE_CYCLE[self.mode]
        self.i = 0
        self._build_tree()
        self._update_chrome()
        self._show()

    # ------------------------------------------------------------ queue ----

    def _conflict_pending(self, st):
        """Words whose live entries carry more than one fonetični rez,
        minus human-ruled, minus machine-drafted (those are in RATIFY).
        Mirrors the repaired v_conflicts: empty rez and losers are ghosts."""
        ruled = st["human_conflict"] | st["machine_conflict"]
        return [{"word": r["word"]} for r in self.con.execute(
            "SELECT word, COUNT(DISTINCT foneticni_rez) AS v FROM entries "
            "WHERE merged_into IS NULL AND foneticni_rez IS NOT NULL "
            "AND TRIM(foneticni_rez) != '' GROUP BY word HAVING v > 1")
            if SOUL.canon(r["word"]) not in ruled]

    def _ratify_pending(self, st):
        """The machine's DRAFTS awaiting the owner's keystroke — derived
        by replaying machine:true ledger lines (merge, conflict) and the
        glyph payload's draft: verdicts. Guard (b): each carries its
        rationale; the ratify display READS it before [k] can mean
        anything."""
        out = []
        for r in self.con.execute("SELECT word, payload FROM ledger "
                                  "WHERE kind='verdict' AND payload "
                                  "LIKE '%\"machine\": true%'"):
            try:
                p = json.loads(r["payload"])
            except (ValueError, TypeError):
                continue
            if not isinstance(p, dict) or not p.get("machine"):
                continue
            w = SOUL.canon(r["word"] or "")
            ruling = str(p.get("ruling", ""))
            # routing by RULING, not by fingerprint-presence (scar found
            # 26. 9. while grafting the ipa layer: enrich drafts carry
            # fingerprints too — the fingerprint catch-all would display
            # them as MERGE drafts and [k] would fire the merge handler
            # on an enrichment; now every draft kind reaches its own apply)
            if ruling == "draft-enrich-rez":
                if (w, p.get("fingerprint")) in st["human_fp"] \
                        or (w, p.get("fingerprint")) in st["refused_fp"]:
                    continue
                out.append({"kind": "enrich", "word": r["word"],
                            "entry_id": p.get("entry_id"),
                            "rez": p.get("rez"),
                            "rationale": p.get("rationale", "")})
            elif ruling == "draft-sinteza":
                if (w, p.get("fingerprint")) in st["human_fp"] \
                        or (w, p.get("fingerprint")) in st["refused_fp"]:
                    continue
                out.append({"kind": "sinteza", "word": r["word"],
                            "body_md": p.get("body_md"),
                            "provenance_md": p.get("provenance_md"),
                            "fingerprint": p.get("fingerprint"),
                            "rationale": p.get("rationale", "")})
            elif ruling == "draft-sklepaj":
                if (w, p.get("fingerprint")) in st["human_fp"] \
                        or (w, p.get("fingerprint")) in st["refused_fp"]:
                    continue
                out.append({"kind": "sklepaj", "word": r["word"],
                            "claim": p.get("claim"),
                            "verdict": p.get("verdict"),
                            "verdict_class": p.get("verdict_class"),
                            "trace": p.get("trace", []),
                            "gaps": p.get("gaps", {}),
                            "fingerprint": p.get("fingerprint"),
                            "rationale": p.get("rationale", "")})
            elif ruling == "draft-ipa":
                if (w, p.get("fingerprint")) in st["human_fp"] \
                        or (w, p.get("fingerprint")) in st["refused_fp"]:
                    continue
                out.append({"kind": "ipa", "word": r["word"],
                            "entry_id": p.get("entry_id"),
                            "ipa": p.get("ipa"),
                            "rationale": p.get("rationale", "")})
            elif p.get("fingerprint"):
                if (w, p["fingerprint"]) in st["human_fp"] \
                        or (w, p["fingerprint"]) in st["refused_fp"]:
                    continue
                out.append({"kind": "merge", "word": r["word"],
                            "fingerprint": p["fingerprint"],
                            "keeper": p.get("keeper"),
                            "lose": list(p.get("lose") or []),
                            "rationale": p.get("rationale", ""),
                            "near": "near-dup" in (p.get("rationale") or "")})
            elif ruling.startswith("conflict") or ruling.startswith("draft-conflict"):
                if w in st["human_conflict"] or w in st["refused_conflict"]:
                    continue
                out.append({"kind": "conflict", "word": r["word"],
                            "true_rez": p.get("true_rez"),
                            "rationale": p.get("rationale", ""),
                            "counts": p.get("counts", {})})
        for w, p in sorted(self._glyph_all().items()):
            if isinstance(p, dict) and str(p.get("verdict", "")).startswith("draft:"):
                out.append({"kind": "glyph", "word": w,
                            "rationale": f"warrant: {p.get('warrant', '')}",
                            "proposed_operator": p.get("proposed_operator"),
                            "glyph": p.get("glyph")})
        return out

    def _glyph_all(self):
        path = os.path.join(_HERE, GLYPH_FILE)
        try:
            with open(path, encoding="utf-8") as fh:
                return json.load(fh)
        except (OSError, ValueError):
            return {}

    def load(self):
        st = SOUL.ruling_states(self.con)      # THE replay — spine-owned
        seen = st["human_fp"] | st["machine_fp"]
        exact = [p for p in SOUL.propose_entry_merges(self.con)
                 if p["needs_owner"] and
                 (p["word"], p["fingerprint"]) not in seen]
        near = [p for p in SOUL.propose_near_merges(self.con)
                if (p["word"], p["fingerprint"]) not in seen]
        self.merge_queue = exact + near        # refused drafts stay pending
        self.glyph_queue = self._glyph_pending()
        self.conflict_queue = self._conflict_pending(st)
        self.ratify_queue = self._ratify_pending(st)
        self.i = 0
        self._update_chrome()
        self._show()

    def _glyph_pending(self):
        path = os.path.join(_HERE, GLYPH_FILE)
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            return []
        return [(w, p) for w, p in sorted(data.items())
                if isinstance(p, dict) and p.get("verdict") == "confirm/reject"]

    def _update_chrome(self):
        nxt = self.MODE_CYCLE[self.mode]
        self.mode_btn.config(text=f"show {nxt} queue "
                                  f"({len(getattr(self, nxt + '_queue'))} pending)")
        rules = {"merge": REVIEW_RULES, "glyph": GLYPH_RULES,
                 "conflict": CONFLICT_RULES,
                 "ratify": RATIFY_RULES}[self.mode]
        self.rules_var.set("   ·   ".join(f"[{k}] {short}"
                          for k, short, _long in rules))

    def _show(self):
        self.tree.delete(*self.tree.get_children())
        for b in self.btns.values():
            b.state(["disabled"])
        if self.mode == "glyph":
            self._show_glyph()
            return
        if self.mode == "conflict":
            self._show_conflict()
            return
        if self.mode == "ratify":
            self._show_ratify()
            return
        if not self.merge_queue:
            self.status_var.set("merge queue empty — no duplicate or "
                                "near-duplicate proposals awaiting your ruling")
            return
        p = self.merge_queue[self.i]
        ids = [p["keeper"]] + list(p["lose"])
        marks = ",".join("?" * len(ids))
        rows = {r["entry_id"]: r for r in self.con.execute(
            f"SELECT e.entry_id, e.word, e.format, e.thesis, e.synthesis, "
            f"e.foneticni_rez, e.ontoloski_pomen, e.antinoma, e.glyph, "
            f"e.grade, e.doc_id, e.lineno, d.kind AS doc_kind, "
            f"d.stratum AS doc_stratum FROM entries e "
            f"JOIN docs d ON d.doc_id = e.doc_id "
            f"WHERE e.entry_id IN ({marks})", ids)}
        for eid, role in ([(p["keeper"], "PROPOSED KEEPER")] +
                          [(l, "loser") for l in p["lose"]]):
            r = rows.get(eid)
            if r is None:
                continue
            where = (f"{r['doc_id']}:{r['lineno']}"
                      + (f" · {r['doc_stratum']}/{r['doc_kind']}"
                         if r["doc_stratum"] else ""))
            self.tree.insert("", "end",
                             tags=("keeper",) if eid == p["keeper"] else (),
                             values=(eid, role, r["word"], r["format"], r["grade"],
                                     (r["thesis"] or r["synthesis"] or "—")[:64],
                                     r["foneticni_rez"] or "—",
                                     r["ontoloski_pomen"] or "—",
                                     r["antinoma"] or "—", r["glyph"] or "—",
                                     where))
        tail = (f"near-dup, similarity {p['similarity']}" if p.get("near")
                else "richest is a tie")
        self.status_var.set(f"ruling {self.i + 1} / {len(self.merge_queue)} — "
                            f"'{p['word']}' · {len(ids)} entries · {tail}")
        for b in self.btns.values():
            b.state(["!disabled"])

    def _show_glyph(self):
        if not self.glyph_queue:
            self.status_var.set(f"glyph queue empty — no {GLYPH_FILE} "
                                "verdicts awaiting your ruling")
            return
        w, p = self.glyph_queue[self.i]
        self.tree.insert("", "end", values=(w, p.get("glyph", "—"),
            p.get("proposed_operator", "—"), p.get("warrant", "—"),
            p.get("verdict", "—"), str(p.get("unmapped", "—"))))
        self.status_var.set(f"ruling {self.i + 1} / {len(self.glyph_queue)} — "
                            f"'{w}' · [k] confirm or [c] reject the mapping")
        for k, b in self.btns.items():
            if k != "m":
                b.state(["!disabled"])

    def _show_conflict(self):
        if not self.conflict_queue:
            self.status_var.set("conflict queue empty — no live word carries "
                                "two fonetični rez variants awaiting your ruling")
            return
        w = self.conflict_queue[self.i]["word"]
        rows = list(self.con.execute(
            "SELECT e.entry_id, e.word, e.foneticni_rez, e.grade, e.format, "
            "e.doc_id, e.lineno, e.thesis, e.synthesis, "
            "d.kind AS doc_kind, d.stratum AS doc_stratum "
            "FROM entries e JOIN docs d ON d.doc_id = e.doc_id "
            "WHERE e.word=? AND e.merged_into IS NULL "
            "AND TRIM(e.foneticni_rez) != ''", (w,)))
        for r in rows:
            where = (f"{r['doc_id']}:{r['lineno']}"
                     + (f" · {r['doc_stratum']}/{r['doc_kind']}"
                        if r["doc_stratum"] else ""))
            self.tree.insert("", "end", values=(
                r["word"], r["foneticni_rez"], r["grade"], r["format"],
                where,
                (r["thesis"] or r["synthesis"] or "—")[:64]))
        self.status_var.set(f"ruling {self.i + 1} / {len(self.conflict_queue)} — "
                            f"'{w}' · {len(rows)} live entries · "
                            f"[k] pick the true rez, [c] both are real variants")
        for k, b in self.btns.items():
            if k != "m":
                b.state(["!disabled"])

    def _show_ratify(self):
        """GUARD (b): the rationale is DISPLAYED — a receipt must be read
        before it is ruled. [k] ratifies the displayed draft; [c] refuses
        it back to pending; [m] rules your own way."""
        if not self.ratify_queue:
            self.status_var.set("ratify queue empty — no machine drafts "
                               "awaiting your keystroke (run `drafts` "
                               "after `authorize-drafts` to make some)")
            return
        d = self.ratify_queue[self.i]
        if d["kind"] == "merge":
            decision = f"merge {len(d['lose'])} loser(s) into keeper " \
                      f"{d['keeper']}"
        elif d["kind"] == "conflict":
            decision = f"true rez = {d['true_rez']!r}"
        elif d["kind"] == "enrich":
            decision = f"napolni votel rez = {d['rez']!r} (vnos {d['entry_id']})"
        elif d["kind"] == "sinteza":
            # scar repair (1. 10., sklepaj sitting): the canon file was
            # written by the DISPLAY (canon by looking, not by
            # keystroke) and [k] fell into the glyph handler — now
            # [k] is the only writer, in ratify_accept, exactly as
            # the receipt claims
            decision = ("KANON PRIMER - sestavljena sinteza (vsaka "
                        "vrstica sledi bazi; [k] zapece v canon_ruled/)")
        elif d["kind"] == "ipa":
            decision = f"izmera IPO = {d['ipa']!r} (vnos {d['entry_id']}) — ⚠ g2p"
        elif d["kind"] == "sklepaj":
            decision = (f"PRESOJA {d.get('verdict_class')}: "
                        + (d.get("verdict") or "")[:100])
        else:
            decision = f"confirm glyph→{d.get('proposed_operator')}"
        self.tree.insert("", "end", values=(
            d["kind"], d["word"], decision, d.get("rationale", "")))
        drift = ""
        if self._k_streak >= 10:
            drift = (f"  |  DRIFT WARN: {self._k_streak} drafts ratified "
                     f"with no refusal or amendment — read the rationales; "
                     f"a ruler who never amends is a rubber stamp wearing "
                     f"a crown")
        self.status_var.set(f"ratifying {self.i + 1} / {len(self.ratify_queue)} "
                            f"— '{d['word']}' · a DRAFT (receipt, not canon) "
                            f"· read the rationale, then [k]/[c]/[m]{drift}")
        for b in self.btns.values():
            b.state(["!disabled"])

    # ---------------------------------------------------------- rulings ----

    def _rule(self, key):
        if not (self.alive and self.queue()):
            return
        if self.mode == "glyph":
            {"k": self.rule_glyph_confirm, "c": self.rule_glyph_reject,
             "s": self.rule_skip}.get(key, lambda: None)()
        elif self.mode == "conflict":
            {"k": self.rule_conflict_true, "c": self.rule_conflict_variants,
             "s": self.rule_skip}.get(key, lambda: None)()
        elif self.mode == "ratify":
            {"k": self.ratify_accept, "c": self.ratify_refuse,
             "m": self.ratify_amend,
             "s": self.rule_skip}.get(key, lambda: None)()
        else:
            {"k": self.rule_keep, "m": self.rule_merge,
             "c": self.rule_conflict, "s": self.rule_skip}.get(key, lambda: None)()

    def rule_keep(self):
        p = self.merge_queue[self.i]
        SOUL.apply_merge(self.con, p)
        self.load()
        self.status_var.set(f"KEPT — {len(p['lose'])} loser(s) merged into "
                            f"'{p['word']}' (ledger: merge)  |  "
                            f"{len(self.merge_queue)} left in the queue")

    def rule_merge(self):
        self._choose_keeper(self.merge_queue[self.i])

    def _choose_keeper(self, p):
        ids = [p["keeper"]] + list(p["lose"])
        marks = ",".join("?" * len(ids))
        rows = [dict(r) for r in self.con.execute(
            f"SELECT entry_id, word, format, grade, thesis, synthesis, "
            f"foneticni_rez FROM entries WHERE entry_id IN ({marks})", ids)]
        win = tk.Toplevel(self)
        win.title("pick the keeper — you overrule the tie")
        win.transient(self.winfo_toplevel())
        lb = tk.Listbox(win, width=110, height=min(len(rows), 12))
        for r in rows:
            lb.insert("end", f"{r['entry_id']}  [{r['grade']}/{r['format']}]  "
                             f"{r['word']} — "
                             f"{(r['thesis'] or r['synthesis'] or r['foneticni_rez'] or '—')[:70]}")
        lb.pack(padx=8, pady=8)
        lb.selection_set(0)

        def pick(_e=None):
            sel = lb.curselection()
            if not sel:
                return
            chosen = rows[sel[0]]["entry_id"]
            win.destroy()
            prop = dict(p)
            prop["keeper"] = chosen
            prop["lose"] = [e for e in ids if e != chosen]
            SOUL.apply_merge(self.con, prop)
            self.load()
            self.status_var.set(f"MERGED — your keeper {chosen} won; "
                                f"{len(prop['lose'])} loser(s) merged into "
                                f"'{p['word']}' (ledger: merge)  |  "
                                f"{len(self.queue)} left in the queue")

        lb.bind("<Double-Button-1>", pick)
        lb.bind("<Return>", pick)
        ttk.Button(win, text="pick as keeper", command=pick).pack(pady=(0, 8))
        lb.focus_set()
        win.grab_set()

    def rule_conflict(self):
        p = self.merge_queue[self.i]
        SOUL.led(self.con, "verdict", p["word"], {
            "ruling": "conflict", "fingerprint": p["fingerprint"],
            "members": [p["keeper"]] + list(p["lose"]),
            "note": "not duplicates: real variants — kept separate"})
        self.con.commit()
        self.load()
        self.status_var.set(f"CONFLICT — '{p['word']}' entries stay separate "
                            f"(ledger: verdict)  |  "
                            f"{len(self.merge_queue)} left in the queue")

    # --------------------------------------------------- glyph rulings ----

    def _rule_glyph(self, ruling, word=None):
        """Confirm/reject the glyph→operator mapping: verdict written back
        into the payload, ledger line witnesses the ruling in soul.db.
        word given = the ratify queue's draft; none = the glyph queue."""
        w = word or self.glyph_queue[self.i][0]
        p = self._glyph_all().get(w) or {}
        path = os.path.join(_HERE, GLYPH_FILE)
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        data[w]["verdict"] = ruling
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        SOUL.led(self.con, "verdict", w, {
            "ruling": f"glyph-{ruling}", "glyph": p.get("glyph"),
            "proposed_operator": p.get("proposed_operator"),
            "warrant": p.get("warrant")})
        self.con.commit()
        self.load()
        self.status_var.set(f"GLYPH {ruling.upper()} — '{w}' recorded in the "
                            f"payload, witnessed (ledger: verdict)  |  "
                            f"{len(self.glyph_queue)} left in the queue")

    def rule_glyph_confirm(self):
        self._rule_glyph("confirm")

    def rule_glyph_reject(self):
        self._rule_glyph("reject")

    # ------------------------------------------------- conflict rulings ----

    def rule_conflict_true(self):
        """[k] pick the TRUE fonetični rez: a chooser opens, the true rez is
        written onto the other live entries, and the old values survive in
        the ledger — nothing is lost, the conflict is resolved by the
        owner's ruling, not by the machine."""
        self._conflict_chooser(self.conflict_queue[self.i]["word"])

    def _conflict_chooser(self, w):
        rows = [dict(r) for r in self.con.execute(
            "SELECT foneticni_rez, COUNT(*) AS n FROM entries "
            "WHERE word=? AND merged_into IS NULL AND TRIM(foneticni_rez) != '' "
            "GROUP BY foneticni_rez", (w,))]
        win = tk.Toplevel(self)
        win.title(f"pick the TRUE fonetični rez for '{w}'")
        win.transient(self.winfo_toplevel())
        lb = tk.Listbox(win, width=90, height=min(len(rows), 12))
        for r in rows:
            lb.insert("end", f"{r['foneticni_rez']}   ({r['n']} "
                             f"entr{'y' if r['n'] == 1 else 'ies'})")
        lb.pack(padx=8, pady=8)
        lb.selection_set(0)

        def pick(_e=None):
            sel = lb.curselection()
            if not sel:
                return
            true_rez = rows[sel[0]]["foneticni_rez"]
            win.destroy()
            losers = [dict(r) for r in self.con.execute(
                "SELECT entry_id, foneticni_rez FROM entries "
                "WHERE word=? AND merged_into IS NULL AND foneticni_rez IS NOT NULL "
                "AND TRIM(foneticni_rez) != '' AND foneticni_rez != ?",
                (w, true_rez))]
            for l in losers:
                self.con.execute("UPDATE entries SET foneticni_rez=? "
                                 "WHERE entry_id=?", (true_rez, l["entry_id"]))
            SOUL.led(self.con, "verdict", w, {
                "ruling": "conflict-true-rez", "true_rez": true_rez,
                "replaced": [{"entry_id": l["entry_id"],
                              "old_rez": l["foneticni_rez"]} for l in losers]})
            self.con.commit()
            self.load()
            self.status_var.set(f"CONFLICT RULED — '{w}': true rez '{true_rez}' "
                                f"written onto {len(losers)} entr"
                                f"{'y' if len(losers) == 1 else 'ies'}; old values "
                                f"witnessed in the ledger  |  "
                                f"{len(self.conflict_queue)} left in the queue")

        lb.bind("<Double-Button-1>", pick)
        lb.bind("<Return>", pick)
        ttk.Button(win, text="rule this the true rez", command=pick).pack(
            pady=(0, 8))
        lb.focus_set()
        win.grab_set()

    def rule_conflict_variants(self):
        """[c] both rezs are real variants — no single truth, both stay."""
        w = self.conflict_queue[self.i]["word"]
        variants = [r[0] for r in self.con.execute(
            "SELECT DISTINCT foneticni_rez FROM entries "
            "WHERE word=? AND merged_into IS NULL AND TRIM(foneticni_rez) != ''",
            (w,))]
        SOUL.led(self.con, "verdict", w, {
            "ruling": "conflict-variants-kept", "variants": variants,
            "note": "real variants: no single truth, both stay"})
        self.con.commit()
        self.load()
        self.status_var.set(f"CONFLICT KEPT — '{w}' has {len(variants)} real "
                            f"variants; both stay (ledger: verdict)  |  "
                            f"{len(self.conflict_queue)} left in the queue")

    # ------------------------------------------------- ratify actions ----
    # Graft #11 — the draft→canon keystrokes. The DRAFT is a receipt; these
    # are the NORMATIVE acts. GUARD (b): the drift counter resets on every
    # refusal or amendment — a ruler who never amends is a rubber stamp
    # wearing a crown.

    def ratify_accept(self):
        d = self.ratify_queue[self.i]
        if d["kind"] == "merge":
            SOUL.apply_merge(self.con, {
                "word": d["word"], "keeper": d["keeper"], "lose": d["lose"],
                "fingerprint": d["fingerprint"], "near": d.get("near", False),
                "ratified_from_draft": True})
        elif d["kind"] == "conflict":
            losers = [dict(r) for r in self.con.execute(
                "SELECT entry_id, foneticni_rez FROM entries "
                "WHERE word=? AND merged_into IS NULL AND foneticni_rez "
                "IS NOT NULL AND TRIM(foneticni_rez) != '' "
                "AND foneticni_rez != ?", (d["word"], d["true_rez"]))]
            for l in losers:
                self.con.execute("UPDATE entries SET foneticni_rez=? "
                                 "WHERE entry_id=?",
                                 (d["true_rez"], l["entry_id"]))
            SOUL.led(self.con, "verdict", d["word"], {
                "ruling": "conflict-true-rez", "true_rez": d["true_rez"],
                "replaced": [{"entry_id": l["entry_id"],
                              "old_rez": l["foneticni_rez"]}
                             for l in losers],
                "ratified_from_draft": True})
            self.con.commit()
        elif d["kind"] == "enrich":
            self.con.execute(
                "UPDATE entries SET foneticni_rez=? WHERE entry_id=?",
                (d["rez"], d["entry_id"]))
            SOUL.led(self.con, "edit", d["word"], {
                "entry_id": d["entry_id"],
                "old": {"foneticni_rez": ""},
                "new": {"foneticni_rez": d["rez"]},
                "fingerprint": f"enrich-{d['entry_id']}",
                "note": "ratified enrich: rez napolnjen iz leksikona"})
            self.con.commit()
        elif d["kind"] == "ipa":
            self.con.execute(
                "UPDATE entries SET ipa=? WHERE entry_id=?",
                (d["ipa"], d["entry_id"]))
            SOUL.led(self.con, "edit", d["word"], {
                "entry_id": d["entry_id"],
                "old": {"ipa": ""},
                "new": {"ipa": d["ipa"]},
                "fingerprint": f"ipa-{d['entry_id']}",
                "note": "ratified ipa: g2p osnutek postal izmera s tvojim "
                        "žigom — preverba proti viru je tvoje dejanje "
                        "(ZAKON IPA)"})
            self.con.commit()
        elif d["kind"] == "sinteza":
            # scar repair (1. 10., sklepaj sitting): the canon file
            # was written by the DISPLAY; [k] fell into the glyph
            # handler — the keystroke is now the only writer
            # (rez 562: korpus se hrani sam, zapece Lastnikova roka)
            canon_name = SOUL.canon(d["word"]) or "beseda"
            out_dir = os.path.join(_HERE, os.pardir, "canon_ruled")
            os.makedirs(out_dir, exist_ok=True)
            fpath = os.path.join(out_dir, canon_name + "-sinteza.md")
            NL = chr(10)
            header = NL.join([
                "# Sinteza: " + d["word"] + " - kanon primer", "",
                "> IZVOR: sestavljeno iz izmerjenih plasti (osnutek",
                "> " + d.get("rationale", "")[:120],
                "> ZAPESCENO z lastnikovim [k] v RATIFY.",
                "", ""])
            with open(fpath, "w", encoding="utf-8") as fh:
                fh.write(header + d["body_md"] + NL + NL + "---"
                         + NL + NL + d.get("provenance_md", "") + NL)
            SOUL.led(self.con, "verdict", d["word"], {
                "ruling": "sinteza-canonized",
                "fingerprint": d.get("fingerprint") or ("sint2-" + canon_name),
                "file": fpath,
                "note": "ratified sinteza: kanon primer v canon_ruled/ - korpus se hrani sam (rez 562)"})
            self.con.commit()
        elif d["kind"] == "sklepaj":
            # [k] on a PRESOJA: the counted trace becomes a derived
            # body in canon_ruled/ (the corpus feeding itself, rez
            # 562) — the canon act is the keystroke, never display
            canon_name = SOUL.canon(d["word"]) or "sklep"
            out_dir = os.path.join(_HERE, os.pardir, "canon_ruled")
            os.makedirs(out_dir, exist_ok=True)
            fpath = os.path.join(out_dir, canon_name + "-sklep.md")
            NL = chr(10)
            lines = ["# Sklep: " + (d.get("claim") or d["word"]), "",
                     "> IZVOR: PRESOJA po izmerjenih plasteh (organ",
                     "> sklepaj; REZ #31: presteje, ne presodi).",
                     "> ZAPESCENO z lastnikovim [k] v RATIFY.", ""]
            for s in d.get("trace") or []:
                lines.append(f"- **{s['step']}:** {s['meritev']}")
            lines += ["", "---", "",
                      "SODBA (presteta): " + (d.get("verdict") or ""), "",
                      "∂: " + json.dumps(d.get("gaps") or {}, ensure_ascii=False), ""]
            with open(fpath, "w", encoding="utf-8") as fh:
                fh.write(NL.join(lines) + NL)
            SOUL.led(self.con, "verdict", d["word"], {
                "ruling": "sklep-canonized",
                "fingerprint": d.get("fingerprint"),
                "file": fpath,
                "note": "ratified presoja: sled presteta, zapecena z [k]"})
            self.con.commit()
        else:
            self._rule_glyph("confirm", word=d["word"])
        self._k_streak += 1
        self.load()
        self.status_var.set(f"RATIFIED — '{d['word']}' {d['kind']} draft "
                            f"became canon by your keystroke  |  "
                            f"{len(self.ratify_queue)} drafts left")

    def ratify_refuse(self):
        """[c] — the draft is refused: its item returns to PENDING and the
        machine never re-drafts it. The receipt stays in the ledger."""
        d = self.ratify_queue[self.i]
        self._k_streak = 0
        if d["kind"] == "merge":
            SOUL.led(self.con, "verdict", d["word"], {
                "ruling": "draft-refused", "fingerprint": d["fingerprint"]})
        elif d["kind"] == "conflict":
            SOUL.led(self.con, "verdict", d["word"], {
                "ruling": "draft-refused", "conflict": d["word"]})
        elif d["kind"] in ("enrich", "ipa"):
            # the same refusal channel as merges: the fingerprint is the
            # thing the replay never re-drafts (scar: these kinds used to
            # fall into the glyph branch and rewrite the glyph payload)
            SOUL.led(self.con, "verdict", d["word"], {
                "ruling": "draft-refused",
                "fingerprint": f"{d['kind']}-{d['entry_id']}"})
        elif d["kind"] in ("sinteza", "sklepaj"):
            # scar repair (1. 10.): these drafts carry no entry_id —
            # the old channel refused them by fingerprint
            # "sinteza-None", which never matched the draft; the
            # draft's OWN fingerprint is what the replay must never
            # re-draft
            SOUL.led(self.con, "verdict", d["word"], {
                "ruling": "draft-refused",
                "fingerprint": d.get("fingerprint")})
        else:
            data = self._glyph_all()
            data[d["word"]]["verdict"] = "confirm/reject"
            with open(os.path.join(_HERE, GLYPH_FILE), "w",
                      encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
            SOUL.led(self.con, "verdict", d["word"], {
                "ruling": "draft-refused", "glyph": d["word"]})
        self.con.commit()
        self.load()
        self.status_var.set(f"REFUSED — '{d['word']}' draft rejected; the "
                            f"item returns to pending, never re-drafted  |  "
                            f"{len(self.ratify_queue)} drafts left")

    def ratify_amend(self):
        """[m] — rule it your way: the chooser opens (merge/conflict); the
        draft's rationale informed you, your ruling canonizes."""
        d = self.ratify_queue[self.i]
        if d["kind"] == "merge":
            self._k_streak = 0
            self._choose_keeper({"word": d["word"], "keeper": d["keeper"],
                                 "lose": d["lose"],
                                 "fingerprint": d["fingerprint"]})
        elif d["kind"] == "conflict":
            self._k_streak = 0
            self._conflict_chooser(d["word"])
        # glyph drafts have nothing to amend — [k] or [c] only

    def rule_skip(self):
        self.i += 1
        if self.i >= len(self.queue()):
            self.load()
        else:
            self._show()
            self.status_var.set(self.status_var.get() + "  |  skipped stays in the queue")


# =============================================================================
# LIBRARY TAB — graft #3: browse the spine's words, read their pages
# =============================================================================

class LibraryTab(ttk.Frame):
    """The library, v2 (Luka's ask, 26. 9. — "prikazno okno rubrik in
    editivni prostor"): every live word with its sources, the page as
    RUBRIKS in a display window (click an entry to load it), and a
    PERSISTENT EDITABLE SPACE beneath — not a popup form: a place to
    write. Edits are canon DIRECTLY (the ruler's touch is a normative
    act); old values survive in the ledger 'edit' line. The page
    derives by the spine's own page(); the popup editor is SUBSUMED
    by the edit space — the same line, now somewhere to write."""

    RUBRIKE = (("word", "BESEDA"), ("foneticni_rez", "FONETIČNI REZ"),
               ("glyph", "GLYPH"), ("thesis", "TEZA"),
               ("antithesis", "ANTITEZA"), ("synthesis", "SINTEZA"),
               ("ontoloski_pomen", "ONTOLOŠKI POMEN"),
               ("antinoma", "ANTINOMA"),
               ("prakticna_uporaba", "PRAKTIČNA UPORABA"))

    def __init__(self, parent):
        super().__init__(parent, padding=8)
        self.alive = False
        self.rows = []
        self._editing_id = None
        self._view_entries = {}
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)
        if SOUL is None:
            ttk.Label(self, text=f"cannot load the spine (soul_engine): "
                                f"{_SOUL_LOAD_ERROR}").grid(row=0, column=0,
                                                            sticky="w")
            return
        if not os.path.exists(SOUL.DB_PATH):
            ttk.Label(self, text=f"the spine's db is missing: "
                                f"{SOUL.DB_PATH} — run soul_engine scan "
                                "first").grid(row=0, column=0, sticky="w")
            return
        self.con = SOUL.db()
        self.alive = True

        bar = ttk.Frame(self)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(bar, text="filter:").pack(side="left")
        self.filter_var = tk.StringVar()
        ent = ttk.Entry(bar, textvariable=self.filter_var)
        ent.pack(side="left", fill="x", expand=True, padx=4)
        ent.bind("<KeyRelease>", lambda _e: self.fill())
        ttk.Button(bar, text="export ruled page",
                   command=self.export_page).pack(side="left", padx=(6, 0))
        ttk.Button(bar, text="uredi vnos",
                   command=self.edit_entry).pack(side="left", padx=(6, 0))
        ttk.Button(bar, text="dodaj vnos",
                   command=self.add_entry).pack(side="left", padx=(6, 0))
        self.count_var = tk.StringVar(value="—")
        ttk.Label(bar, textvariable=self.count_var).pack(side="left", padx=8)

        self.listbox = tk.Listbox(self, width=30)
        self.listbox.grid(row=1, column=0, sticky="nsw", pady=(4, 0))
        self.listbox.bind("<Double-Button-1>", self.open_page)
        self.listbox.bind("<Return>", self.open_page)

        pane = ttk.PanedWindow(self, orient="vertical")
        pane.grid(row=1, column=1, sticky="nsew", pady=(4, 0), padx=(6, 0))

        # ---- prikazno okno rubrik ------------------------------------
        self.view = tk.Text(pane, wrap="word", state="disabled",
                            bg="#101014", fg="#cfd3dc",
                            insertbackground="#ffffff")
        for tag, cfg in {
                "title": dict(font=("TkDefaultFont", 13, "bold"),
                              foreground="#e8c76a"),
                "meta": dict(foreground="#7788aa"),
                "ent": dict(font=("TkDefaultFont", 10, "bold"),
                            foreground="#4aa88f"),
                "rub": dict(foreground="#c98f3d"),
                "val": dict(foreground="#cfd3dc"),
                "conf": dict(foreground="#d05a5a")}.items():
            self.view.tag_configure(tag, **cfg)
        pane.add(self.view, weight=3)

        # ---- editivni prostor ----------------------------------------
        box = ttk.Frame(pane, padding=4)
        self.edit_lbl = tk.StringVar(
            value="EDITIVNI PROSTOR — klikni vnos v oknu rubrik, piši, "
                  "shrani; tvoja roka je kanon, stare vrednosti pričajo "
                  "(ledger: edit)")
        ttk.Label(box, textvariable=self.edit_lbl,
                  foreground="#c98f3d").pack(anchor="w")
        self.edit = tk.Text(box, wrap="word", height=8, bg="#14141a",
                            fg="#e8e8ec", insertbackground="#ffffff")
        self.edit.pack(fill="both", expand=True, pady=(4, 4))
        btns = ttk.Frame(box)
        btns.pack(fill="x")
        ttk.Button(btns, text="shrani (ledger: edit)",
                   command=self.save_edit).pack(side="left")
        ttk.Button(btns, text="prekliči",
                   command=self._clear_edit).pack(side="left", padx=6)
        pane.add(box, weight=2)

        self.load()

    def load(self):
        self.rows = [dict(r) for r in self.con.execute(
            "SELECT word, COUNT(*) AS sources, "
            "GROUP_CONCAT(DISTINCT format) AS formats, "
            "SUM(grade='reported') AS reported, "
            "SUM(grade='headline') AS headline "
            "FROM entries WHERE merged_into IS NULL GROUP BY word "
            "ORDER BY word COLLATE NOCASE")]
        self.fill()

    def fill(self):
        needle = self.filter_var.get().strip().lower()
        self.listbox.delete(0, "end")
        shown = 0
        for r in self.rows:
            if needle and needle not in r["word"].lower():
                continue
            self.listbox.insert("end", r["word"])
            shown += 1
        self.count_var.set(f"{shown} / {len(self.rows)} words")

    def open_page(self, _e=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        word = self.listbox.get(sel[0])
        p = SOUL.page(self.con, word)
        v = self.view
        v.configure(state="normal")
        v.delete("1.0", "end")
        self._view_entries = {}
        v.insert("end", word + "\n", ("title",))
        v.insert("end", f"{len(p['entries'])} vnosov · omenjeno v "
                  f"{p['mentions']} dokumentih\n\n", ("meta",))
        for e in p["entries"]:
            eid = e["entry_id"]
            self._view_entries[eid] = dict(e)
            tag = f"e{eid}"
            v.tag_configure(tag, background="#181820")
            head = (f"[{e['grade']}/{e['format']}] "
                    + (e.get("doc_stratum") or "?") + " · doc "
                    + f"{e['doc_id']}:{e['lineno']} · vnos {eid}"
                    + (f"  ← zlivljen v '{e['merged_into']}'"
                       if e.get("merged_into") else "") + "\n")
            v.insert("end", head, ("ent", tag))
            for key, label in self.RUBRIKE:
                if key == "word":
                    continue
                val = (e.get(key) or "").strip()
                if val:
                    v.insert("end", f"  {label}: ", ("rub", tag))
                    v.insert("end", val + "\n", ("val", tag))
            if not e.get("merged_into"):
                v.tag_bind(tag, "<Button-1>",
                           lambda ev, i=eid: self._pick_entry(i))
            v.insert("end", "\n", (tag,))
        if p["conflicts"]:
            v.insert("end", "KONFLIKT: fonetični rez ima več različic — "
                      "razsodba je v REVIEW\n", ("conf",))
        v.configure(state="disabled")

    # ------------------------------------------- editivni prostor ----

    def _pick_entry(self, eid):
        e = self._view_entries.get(eid)
        if not e:
            return
        self._editing_id = eid
        self.edit.delete("1.0", "end")
        for key, label in self.RUBRIKE:
            val = (e.get(key) or "").strip()
            self.edit.insert("end", f"{label}: {val}\n")
        self.edit_lbl.set(f"UREJAŠ vnos {eid} ('{e['word']}') — shrani: "
                          "staro priča, novo je kanon (ledger: edit)")

    def edit_entry(self):
        """loads the FIRST live entry of the selected word into the edit
        space — or the word's page is one click away in the view"""
        sel = self.listbox.curselection()
        if not sel:
            self.count_var.set("izberi besedo — urejevalni prostor čaka")
            return
        word = self.listbox.get(sel[0])
        p = SOUL.page(self.con, word)
        live = [e for e in p["entries"] if not e.get("merged_into")]
        if live:
            self._pick_entry(live[0]["entry_id"])
        else:
            self.count_var.set(f"'{word}': ni živih vnosov")

    def add_entry(self):
        sel = self.listbox.curselection()
        word = self.listbox.get(sel[0]) if sel else ""
        self._editing_id = None
        self.edit.delete("1.0", "end")
        for _key, label in self.RUBRIKE:
            self.edit.insert("end", f"{label}: "
                             + (word if label == "BESEDA" else "") + "\n")
        self.edit_lbl.set("DODAJAŠ nov vnos — shranjena vrstica postane "
                          "kanon (ledger: edit, provenance cockpit)")

    def _parse_edit(self):
        vals, cur = {}, None
        for line in self.edit.get("1.0", "end").splitlines():
            for key, label in self.RUBRIKE:
                if line.startswith(label + ":"):
                    cur = key
                    vals[cur] = line[len(label) + 1:].strip()
                    break
            else:
                if cur:
                    vals[cur] = (vals[cur] + " " + line.strip()).strip()
        return vals

    def save_edit(self):
        vals = self._parse_edit()
        if self._editing_id:
            entry = self._view_entries.get(self._editing_id, {})
            old = {k: (entry.get(k) or "") for k, _l in self.RUBRIKE
                   if (entry.get(k) or "") != (vals.get(k) or "")}
            new = {k: (vals.get(k) or "") for k in old}
            if not old:
                self.edit_lbl.set("ni sprememb — prostor ostaja odprt")
                return
            self.con.execute(
                "UPDATE entries SET " +
                ", ".join(f"{k}=?" for k in new) + " WHERE entry_id=?",
                list(new.values()) + [self._editing_id])
            SOUL.led(self.con, "edit",
                     vals.get("word") or entry.get("word", ""),
                     {"entry_id": self._editing_id, "old": old, "new": new})
            self.con.commit()
            self.edit_lbl.set(f"UREJENO vnos {self._editing_id} — "
                              f"{len(new)} rubrik spremenjenih; stare "
                              "vrednosti pričajo v glavni knjigi")
        else:
            if not (vals.get("word") or "").strip():
                self.edit_lbl.set("vnos potrebuje BESEDA")
                return
            row = self.con.execute(
                "SELECT doc_id FROM docs WHERE path=?",
                ("cockpit://owner-added",)).fetchone()
            doc_id = (row[0] if row else self.con.execute(
                "INSERT INTO docs(path, stratum, kind) VALUES "
                "('cockpit://owner-added', 'cockpit', 'owner-added')"
                ).lastrowid)
            cur = self.con.execute(
                """INSERT INTO entries(doc_id, word, format, number,
                   thesis, antithesis, synthesis, foneticni_rez,
                   ontoloski_pomen, antinoma, glyph,
                   prakticna_uporaba, lineno, grade)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,NULL,'reported')""",
                (doc_id, vals["word"], "owner", None,
                 vals.get("thesis"), vals.get("antithesis"),
                 vals.get("synthesis"), vals.get("foneticni_rez"),
                 vals.get("ontoloski_pomen"), vals.get("antinoma"),
                 vals.get("glyph"), vals.get("prakticna_uporaba")))
            SOUL.led(self.con, "edit", vals["word"],
                     {"entry_id": cur.lastrowid, "old": None, "new": vals,
                      "note": "owner-added entry"})
            self.con.commit()
            self.edit_lbl.set(f"DODAN vnos {cur.lastrowid} za "
                              f"'{vals['word']}' (ledger: edit)")
        self.load()
        sel_word = vals.get("word") or self.listbox.get(0)
        for i in range(self.listbox.size()):
            if self.listbox.get(i) == sel_word:
                self.listbox.selection_clear(0, "end")
                self.listbox.selection_set(i)
                self.listbox.see(i)
                self.open_page()
                break

    def _clear_edit(self):
        self._editing_id = None
        self.edit.delete("1.0", "end")
        self.edit_lbl.set("EDITIVNI PROSTOR prazen — klikni vnos v oknu "
                          "rubrik ali 'uredi vnos'")

    def export_page(self):
        """Graft 7 — the canon feeding itself: write the selected word's
        RULED page as a derived dosje into the canon_ruled stratum."""
        sel = self.listbox.curselection()
        if not sel:
            self.count_var.set("izberi besedo — izvoz potrebuje stran")
            return
        word = sel[0]
        out_dir = os.path.normpath(os.path.join(_HERE, "..", "canon_ruled"))
        r = SOUL.export_page(self.con, word, out_dir)
        if "error" in r:
            self.count_var.set(r["error"])
        else:
            self.count_var.set(f"izvoz -> {r['file']} ({r['entries']} "
                               f"vnosov, ledger: export) — rescan sprejme")

# =============================================================================
# TEORIJE TAB — ⨿ the theory register and the fold (Luka's "daj", 4. 10. 2026)
# G3 register + G4 stran teorije + G5 izvoz, one surface. Read-only by law:
# rulings happen in REVIEW; this tab only reads. The list derives by the
# spine's own teorije(); the fold by teorija_page(); the export follows
# LIBRARY's export line (derived body into canon_ruled, ledger-witnessed).
# Solo bodies without laws are counted, not listed (they live in LIBRARY).
# =============================================================================

class TeorijeTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent, padding=8)
        self.alive = False
        self.rows = []
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(1, weight=1)
        if SOUL is None:
            ttk.Label(self, text=f"cannot load the spine (soul_engine): "
                                f"{_SOUL_LOAD_ERROR}").grid(row=0, column=0,
                                                            sticky="w")
            return
        if not os.path.exists(SOUL.DB_PATH):
            ttk.Label(self, text=f"the spine's db is missing: "
                                f"{SOUL.DB_PATH} — run soul_engine scan "
                                "first").grid(row=0, column=0, sticky="w")
            return
        self.con = SOUL.db()
        self.alive = True

        bar = ttk.Frame(self)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(bar, text="filter:").pack(side="left")
        self.filter_var = tk.StringVar()
        ent = ttk.Entry(bar, textvariable=self.filter_var)
        ent.pack(side="left", fill="x", expand=True, padx=4)
        ent.bind("<KeyRelease>", lambda _e: self.fill())
        ttk.Button(bar, text="izvozi stran teorije",
                   command=self.export_teorija).pack(side="left", padx=(6, 0))
        self.count_var = tk.StringVar(value="—")
        ttk.Label(bar, textvariable=self.count_var).pack(side="left", padx=8)

        self.listbox = tk.Listbox(self, width=44)
        self.listbox.grid(row=1, column=0, sticky="nsw", pady=(4, 0))
        self.listbox.bind("<Double-Button-1>", self.open_page)
        self.listbox.bind("<Return>", self.open_page)

        self.view = tk.Text(self, wrap="word", state="disabled",
                            bg="#101014", fg="#cfd3dc",
                            insertbackground="#ffffff")
        self.view.grid(row=1, column=1, sticky="nsew", pady=(4, 0), padx=(6, 0))
        for tag, cfg in {
                "title": dict(font=("TkDefaultFont", 13, "bold"),
                              foreground="#e8c76a"),
                "meta": dict(foreground="#7788aa"),
                "ent": dict(font=("TkDefaultFont", 10, "bold"),
                            foreground="#4aa88f"),
                "rub": dict(foreground="#c98f3d"),
                "val": dict(foreground="#cfd3dc"),
                "delta": dict(foreground="#d0a05a")}.items():
            self.view.tag_configure(tag, **cfg)
        self.fill()

    def fill(self):
        reg = SOUL.teorije(self.con)
        q = (self.filter_var.get() or "").strip().lower()
        self.rows = [t for t in reg["register"] if q in t["teorija"]]
        self.listbox.delete(0, "end")
        for t in self.rows:
            self.listbox.insert(
                "end", f"{t['teorija'][:40]}  β{t['beta']:<5} "
                       f"{t['telesa']}t {len(t['zakoni'])}z")
        self.count_var.set(f"{len(self.rows)} / {reg['v_registru']} "
                           f"družin · solo štet: {reg['solo_brez_zakonov']}")

    def open_page(self, _e=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        t = self.rows[sel[0]]
        pg = SOUL.teorija_page(self.con, t["teorija"])
        self.view.config(state="normal")
        self.view.delete("1.0", "end")
        def w(tag, s):
            self.view.insert("end", s + "\n", tag)
        if "napaka" in pg:
            w("meta", pg["napaka"])
            if "izbira" in pg:
                for c in pg["izbira"]:
                    w("val", f"  {c['teorija']}  β{c['beta']}  {c['telesa']}t")
        else:
            w("title", pg["teorija"])
            w("meta", f"β {pg['beta']} · {pg['tip']} · telesa {pg['telesa']}")
            w("rub", "RODOVNIK")
            for b in pg["rodovnik"]:
                flags = [b["stratum"] or "?", b["kind"], f"vnosi {b['vnosi']}"]
                if b["verzija"]:
                    flags.append(b["verzija"])
                if b["kiralna_kopija"]:
                    flags.append("kiralna")
                if b["kandidat_∧_žig_čaka"]:
                    flags.append("kandidat — ∧ žig čaka")
                w("val", f"  {b['telo'][:68]} [{', '.join(flags)}]")
            w("rub", f"ZAKONI ({len(pg['zakoni'])})")
            for z in pg["zakoni"]:
                w("ent", f"  {z['serija']} {z['st']} — {z['naslov']}"
                     + ("  ∧ pečat" if z["pecat"] else ""))
            w("rub", f"ANTINOME ({len(pg['antinome'])})")
            for a in pg["antinome"][:20]:
                w("val", f"  {a['beseda']}: {a['antinoma']}")
            w("rub", "∂ ODPRTA (imena, ne sodbe)")
            for d in pg["∂_odprto"]["iz_zakonov"]:
                w("delta", f"  {d['serija']} {d['st']}: {d['∂'][:110]}")
            for t2 in pg["∂_odprto"]["temna_telesa"]:
                w("delta", f"  temno telo: {t2}")
            w("rub", "VEZI PO UBODIH")
            for v in pg["vezi_po_ubodih"][:12]:
                w("val", f"  {v['beseda']} — {v['tujih_telem']} tujih teles "
                         f"(delež {v['delez_korpusa']})")
            w("rub", "PREIZKUS NA TUJCU (T1/AX-16)")
            w("val", f"  soul_engine {pg['preizkus']['zahtevek']}")
            w("meta", pg["preizkus"]["sodba"])
        self.view.config(state="disabled")

    def export_teorija(self):
        """G5 — the fold written as a derived body into canon_ruled
        (LIBRARY's export line, theory half; rez 562: corpus feeds itself)."""
        sel = self.listbox.curselection()
        if not sel:
            self.count_var.set("izberi teorijo — izvoz potrebuje izbiro")
            return
        t = self.rows[sel[0]]
        out_dir = os.path.normpath(os.path.join(_HERE, "..", "canon_ruled"))
        r = SOUL.export_teorija(self.con, t["teorija"], out_dir)
        if "error" in r or "napaka" in r:
            self.count_var.set(str(r.get("error") or r.get("napaka")))
        else:
            self.count_var.set(f"izvoz -> {r['file']} ({r['telesa']} teles, "
                               f"{r['zakoni']} zakonov, ledger: export) — "
                               "rescan sprejme")


# =============================================================================
# SLIKA TAB — ⧖ the corpus as one clear apparition (Luka's ask, 26. 9.)
# =============================================================================

SLIKA_COLORS = {
    "zakon": "#d4a017", "dosje-A": "#4aa88f", "dosje-A+B+C": "#4aa88f",
    "dosje-B+C": "#4aa88f", "dosje-D": "#c97a33", "notes": "#7788aa",
    "prose": "#445566", "derived": "#00ccff", "empty": "#333333",
}


class SlikaTab(ttk.Frame):
    """The corpus as ONE PICTURE — a POPIS rendered visually (ISKANO,
    a receipt about receipts; truth stays in REVIEW, this only SHOWS
    the measured). LAWS OF THE VIEW: every dot is a body (hover: its
    name) · every color a kind · every sector a stratum ordered by
    MEASURED TIME (mean mtime, ascending clockwise — the visual IS the
    stratum-order proposal, seen before it is ruled) · time flows
    OUTWARD (inner = old, outer = new) · gold = sealed law bodies ·
    orange = parser targets still dark · cyan = derived (the loop) ·
    lines = law→law citations (VEZI edges — they point, never judge)."""

    def __init__(self, parent):
        super().__init__(parent, padding=4)
        if SOUL is None:
            ttk.Label(self, text=f"cannot load the spine: "
                                f"{_SOUL_LOAD_ERROR}").grid(row=0, column=0)
            return
        self.con = SOUL.db()
        bar = ttk.Frame(self)
        bar.grid(row=0, column=0, sticky="ew")
        ttk.Button(bar, text="⊕ ponari", command=self.draw).pack(side="left")
        self.info = tk.StringVar(value="hover a dot — every dot is a body")
        ttk.Label(bar, textvariable=self.info).pack(side="left", padx=10)
        self.canvas = tk.Canvas(self, bg="#0d0d12", highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.pos = {}
        self.draw()

    def draw(self):
        c = self.canvas
        c.delete("all")
        w = int(c.winfo_width()) or 980
        h = int(c.winfo_height()) or 920
        cx, cy = w // 2, h // 2
        R = min(w, h) // 2 - 70
        c.create_text(cx, 18, fill="#d4a017", font=("TkDefaultFont", 12, "bold"),
                      text="⧖ POJAVNA SLIKA KORPUSA — pika = telo · barva = "
                           "vrsta · sektor = stratuma (merjen čas, ura) · "
                           "čas teče navzven · črte = VEZI")
        # strata ordered by measured time (mean mtime)
        stats = [(r["s"] or "(root)", r["m"] or 0, r["n"])
                 for r in self.con.execute(
                 "SELECT d.stratum s, AVG(d.mtime) m, COUNT(*) n FROM docs d "
                 "GROUP BY d.stratum ORDER BY m")]
        total = sum(s[2] for s in stats) or 1
        mtimes = [float(r["mtime"]) for r in self.con.execute(
            "SELECT mtime FROM docs WHERE mtime IS NOT NULL")]
        lo, hi = (min(mtimes), max(mtimes)) if mtimes else (0, 1)
        import math
        angle = -90.0
        for s, m, n in stats:
            span = 360.0 * n / total
            for i in range(len(stats)):   # sector label
                pass
            c.create_arc(cx - R - 8, cy - R - 8, cx + R + 8, cy + R + 8,
                         start=angle, extent=span, outline="#1c2333",
                         style="arc", width=22)
            mid = angle + span / 2
            lx, ly = cx + (R + 34) * math.cos(math.radians(mid)), \
                     cy + (R + 34) * math.sin(math.radians(mid))
            c.create_text(lx, ly, fill="#5a6a8a",
                          font=("TkDefaultFont", 8),
                          text=f"{s[:14]} ({n})")
            # docs in this stratum: time flows outward
            rows = self.con.execute(
                "SELECT doc_id, path, kind, mtime FROM docs WHERE stratum=? "
                "ORDER BY mtime", (s,)).fetchall()
            for j, d in enumerate(rows):
                a = math.radians(angle + span * (j + 0.5) / max(n, 1))
                t = 0.0 if hi == lo else \
                    (float(d["mtime"] or lo) - lo) / (hi - lo)
                r = 60 + (R - 90) * t
                x, y = cx + r * math.cos(a), cy + r * math.sin(a)
                col = SLIKA_COLORS.get(d["kind"] or "empty", "#333333")
                dot = c.create_oval(x - 2.2, y - 2.2, x + 2.2, y + 2.2,
                                    fill=col, outline="", tags=("dot",))
                name = os.path.basename(d["path"])[:44]
                c.tag_bind(dot, "<Enter>", lambda e, nm=name, dk=d["kind"]:
                    self.info.set(f"{nm} · {dk}"))
                self.pos[(s, j)] = (x, y, d["doc_id"])
            angle += span
        # law→law citation edges (they point, they never judge)
        law_pos = {}
        for z in self.con.execute(
                "SELECT z.series, z.number, z.doc_id FROM zakoni z "
                "JOIN docs d ON d.doc_id = z.doc_id"):
            for (s, j), (x, y, did) in self.pos.items():
                if did == z["doc_id"]:
                    law_pos[(z["series"], z["number"])] = (x, y)
                    break
        import re as _re
        edges = 0
        for z in self.con.execute(
                "SELECT series, number, vezi FROM zakoni "
                "WHERE TRIM(vezi) != ''"):
            src = law_pos.get((z["series"], z["number"]))
            if not src:
                continue
            for mm in _re.finditer(r"(?:rez|dokaz)\s*[#·]?\s*(\d+)",
                                   z["vezi"], _re.IGNORECASE):
                tgt = law_pos.get(("rez", int(mm.group(1)))) or \
                      law_pos.get(("dokaz", int(mm.group(1))))
                if tgt:
                    c.create_line(src[0], src[1], tgt[0], tgt[1],
                                  fill="#2a3a55", width=1)
                    edges += 1
        # legend + center
        lx = 14
        ly = h - 20 - 12 * len(SLIKA_COLORS)
        for kind, col in SLIKA_COLORS.items():
            c.create_oval(lx, ly, lx + 8, ly + 8, fill=col, outline="")
            c.create_text(lx + 14, ly + 4, anchor="w", fill="#889",
                          font=("TkDefaultFont", 8), text=kind)
            ly += 12
        c.create_text(cx, cy, fill="#d4a017",
                       font=("TkDefaultFont", 16), text="⧖")
        self.info.set(f"1,194 teles · {edges} VEZI črt · ISKANO — slika "
                      f"potrdila, ne resnica; resnica je v ⊘ REVIEW")


# =============================================================================
# PARK TAB — decision records + inventory
# =============================================================================

class ParkTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=8)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.tree = ttk.Treeview(self, show="tree", height=5)
        self.tree.grid(row=0, column=0, sticky="ew")
        self.text = tk.Text(self, wrap="word", state="disabled")
        self.text.grid(row=1, column=0, sticky="nsew", pady=4)
        dec = self.tree.insert("", "end", text="DECISION RECORDS", open=True)
        for f in DECISION_RECORDS:
            self.tree.insert(dec, "end", text=f, iid=f)
        pys = self.tree.insert("", "end", text="PYTHON FILES", open=True)
        for f in sorted(f for f in os.listdir(_HERE)
                        if f.lower().endswith(".py")):
            self.tree.insert(pys, "end", text=f, iid=f)
        self.tree.bind("<Double-Button-1>", self.open_file)
        self.tree.bind("<Return>", self.open_file)

    def open_file(self, _event=None):
        sel = self.tree.selection()
        if not sel:
            return
        fname = sel[0]
        try:
            with open(os.path.join(_HERE, fname), encoding="utf-8", errors="replace") as fh:
                content = fh.read(200000)
        except OSError as e:
            content = f"[cannot read: {e}]"
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
        self.text.configure(state="disabled")


# =============================================================================
# SKLEPAJ TAB — the reasoning executor: a claim in, a counted trace out
# =============================================================================

class SklepajTab(ttk.Frame):
    """The PRESOJA surface (organ sklepaj, REZ #31: prešteje, ne presodi —
    kdor presodi preden prešteje, izreče parasodbo): pose a claim, the
    machine executes the corpus's protocol over its measured layers and
    shows the TRACE — every step a receipt. The DRAFT lands in RATIFY;
    the canon acts ([k]/[c]) happen THERE, never here."""

    def __init__(self, parent):
        super().__init__(parent, padding=8)
        self.columnconfigure(0, weight=1)
        if SOUL is None:
            ttk.Label(self, text=f"cannot load the spine (soul_engine): "
                                f"{_SOUL_LOAD_ERROR}").grid(row=0, column=0)
            return
        self.con = SOUL.db()

        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew")
        ttk.Label(top, text="trditev:").pack(side="left")
        self.claim_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.claim_var, width=52).pack(
            side="left", padx=4)
        ttk.Button(top, text="SKLEPAJ", command=self.run).pack(side="left")
        ttk.Label(top, text="  predloge:").pack(side="left")
        for label, claim in (
                ("ljubezen je dejanje", "ljubezen je dejanje"),
                ("kakor in kot", "kakor in kot sta dve telesi z eno mero"),
                ("dih", "dih")):
            ttk.Button(top, text=label,
                       command=lambda c=claim: self.preset(c)).pack(
                           side="left", padx=1)

        self.verdict_var = tk.StringVar(
            value="— napiši trditev; stroj prešteje, ne presodi (REZ #31) —")
        ttk.Label(self, textvariable=self.verdict_var,
                  font=("TkDefaultFont", 11, "bold")).grid(
                      row=1, column=0, sticky="w", pady=4)

        cols = ("step", "meritev")
        self.tree = ttk.Treeview(self, columns=cols, show="headings",
                                 height=6)
        self.tree.heading("step", text="korak")
        self.tree.column("step", width=150, anchor="w")
        self.tree.heading("meritev", text="meritev (priča)")
        self.tree.column("meritev", width=850, anchor="w")
        self.tree.grid(row=2, column=0, sticky="ew", pady=4)

        wcols = ("beseda", "stanje", "vnosi", "keeper", "rez", "izmera",
                 "telesa", "vezi", "sosede")
        self.wtree = ttk.Treeview(self, columns=wcols, show="headings",
                                  height=6)
        for c, w in zip(wcols, (110, 150, 60, 130, 140, 110, 60, 140, 170)):
            self.wtree.heading(c, text=c)
            self.wtree.column(c, width=w, anchor="w")
        self.wtree.grid(row=3, column=0, sticky="ew", pady=4)

        self.delta_var = tk.StringVar(value="∂: —")
        ttk.Label(self, textvariable=self.delta_var,
                  foreground="#a80").grid(row=4, column=0, sticky="w")

    def preset(self, claim):
        self.claim_var.set(claim)
        self.run()

    def run(self):
        claim = self.claim_var.get().strip()
        if not claim:
            return
        r = SOUL.sklepaj(self.con, claim=claim)
        if "error" in r:
            self.verdict_var.set(f"ERROR: {r['error']}")
            return
        for t in (self.tree, self.wtree):
            t.delete(*t.get_children())
        for s in r["trace"]:
            self.tree.insert("", "end", values=(s["step"], s["meritev"]))
        for wd in r["words"]:
            self.wtree.insert("", "end", values=(
                wd["word"], wd["status"], wd.get("entries", ""),
                wd.get("keeper", ""),
                "; ".join(wd.get("rez", [])) or "—",
                "; ".join(wd.get("izmera", [])) or "—",
                wd.get("telesa_omemb", ""),
                "; ".join(wd.get("vezi_zakoni", [])) or "—",
                "; ".join(wd.get("sosede", [])) or "—"))
        gaps = r.get("∂", {})
        self.delta_var.set("∂: " + json.dumps(gaps, ensure_ascii=False))
        note = r.get("note") or r.get("already") or ""
        self.verdict_var.set(
            f"{r['verdict_class']} — {r['verdict'][:150]}  |  {note}")


# MAIN
# =============================================================================

class Cockpit(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OBJ2 COCKPIT — review, not rule")
        self.geometry("1100x760")
        nb = ttk.Notebook(self)
        self.nb = nb
        self.review = ReviewTab(nb)
        nb.add(CanvasTab(nb), text="⟡ CANVAS")
        nb.add(ReceiptsTab(nb), text="⊢ RECEIPTS")
        nb.add(PerformTab(nb), text="∂ PERFORM")
        self.sklepaj = SklepajTab(nb)
        nb.add(self.sklepaj, text="⊢ SKLEPAJ")
        nb.add(self.review, text="⊘ REVIEW")
        self.library = LibraryTab(nb)
        nb.add(self.library, text="∮ LIBRARY")
        self.teorije = TeorijeTab(nb)
        nb.add(self.teorije, text="⨿ TEORIJE")
        self.slika = SlikaTab(nb)
        nb.add(self.slika, text="⧖ SLIKA")
        nb.add(ParkTab(nb), text="∅ PARK + FILES")
        nb.pack(fill="both", expand=True)
        # k/c/m/s arrive here from anywhere; they rule ONLY when the REVIEW
        # tab is up and the keyboard focus is not inside an input widget
        self.bind("<Key>", self._route_key)
        nb.bind("<<NotebookTabChanged>>", self._on_tab)

    def _on_tab(self, _e=None):
        if self.nb.select() == str(self.review) and self.review.btns:
            self.review.btns["k"].focus_set()

    def _route_key(self, event):
        if self.nb.select() != str(self.review):
            return
        w = self.focus_get()
        if isinstance(w, (tk.Entry, tk.Text)):   # covers ttk.Entry/Combobox too
            return
        key = (event.keysym or "").lower()
        if key in ("k", "m", "c", "s"):
            self.review._rule(key)


def _smoke_test():
    """Headless-ish construction test: build the window, load the data layer,
    perform a chain, then destroy — no mainloop. SODBA #002 applies: this is
    a receipt; your run of `python obj2_cockpit.py` is the review."""
    ok = []
    app = Cockpit()
    app.update_idletasks()
    ok.append(("window constructs", True))
    if VALIDATOR is not None:
        st = ENGINE.State()
        lg = ENGINE.Ledger()
        verdict, gate, lines = VALIDATOR.run_chain(["l", "ʌ", "v"], "en", st, lg)
        ok.append(("love performs: WORD/3 lines", verdict.classification == "WORD" and lines == 3))
        ok.append(("guard is a valid verdict", gate in ("PASS/MORAVA", "HOLD", "FALL")))
        ok.append(("E⋆ refuses without review-run witness",
                   ENGINE.e_star(ENGINE.State(), ledger_has_line=False) == 0))
    else:
        ok.append(("sisters load", False))
    ok.append(("REVIEW room constructs (spine + db)",
               app.review.alive if SOUL is not None else False))
    if app.review.alive:
        ok.append((f"review queues derive from the ledger "
                   f"(merge {len(app.review.merge_queue)}, "
                   f"glyph {len(app.review.glyph_queue)}, "
                   f"conflict {len(app.review.conflict_queue)}, "
                   f"ratify {len(app.review.ratify_queue)})",
                   isinstance(app.review.merge_queue, list) and
                   isinstance(app.review.glyph_queue, list) and
                   isinstance(app.review.conflict_queue, list) and
                   isinstance(app.review.ratify_queue, list)))
    ok.append(("LIBRARY constructs (spine + db, words listed)",
               app.library.alive and len(app.library.rows) > 0))
    if app.library.alive:
        w0 = app.library.rows[0]["word"]
        p0 = SOUL.page(app.library.con, w0)
        ok.append((f"library page derives by the spine "
                   f"(page for '{w0[:24]}': {len(p0['entries'])} entries)",
                   len(p0["entries"]) > 0))
    # TEORIJE (4. 10.): the register + the fold — one surface reads
    # the spine's own G3/G4; the export stays a button (rez 562 line).
    teo = getattr(app, "teorije", None)
    if teo is not None and teo.alive:
        ok.append((f"TEORIJE constructs (register {len(teo.rows)} families)",
                   len(teo.rows) > 0))
        pg0 = SOUL.teorija_page(teo.con, teo.rows[0]["teorija"])
        ok.append((f"theory page folds by the spine "
                   f"({teo.rows[0]['teorija'][:20]}...: "
                   f"{pg0.get('telesa', 0)} teles, preizkus travels)",
                   pg0.get("telesa", 0) > 0 and "preizkus" in pg0))
    else:
        ok.append(("TEORIJE constructs (spine + db)", False))
    # SKLEPAJ (1. 10.): the reasoning executor's surface — a claim in,
    # a counted trace out. The smoke claim is ALREADY drafted on the
    # live db (witnessed 1. 10.), so the run exercises the idempotent
    # path and writes nothing.
    sk = getattr(app, "sklepaj", None)
    if sk is not None and hasattr(sk, "con"):
        sk.claim_var.set("ljubezen je dejanje")
        sk.run()
        ok.append((f"SKLEPAJ runs (claim -> trace: "
                   f"{len(sk.tree.get_children())} korakov, "
                   f"{len(sk.wtree.get_children())} besed)",
                   len(sk.tree.get_children()) > 0 and
                   len(sk.wtree.get_children()) > 0))
    else:
        ok.append(("SKLEPAJ constructs (spine + db)", False))
    app.destroy()
    all_ok = all(c for _n, c in ok)
    for name, cond in ok:
        print(("PASS  " if cond else "FAIL  ") + name)
    print("SMOKE " + ("PASS" if all_ok else "FAIL") + " — obj2_cockpit constructs and the data layer performs")
    return 0 if all_ok else 1


if __name__ == "__main__":
    if "--smoke" in sys.argv:
        sys.exit(_smoke_test())
    Cockpit().mainloop()
