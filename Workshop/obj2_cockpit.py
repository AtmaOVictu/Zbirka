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
            if p.get("fingerprint"):
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
    """The library: every live word in soul.db with its sources, and the
    word page beside it. Read-only toward the TRUTH: no ruling happens
    here (REVIEW rules), no entry is edited here. The one write is graft
    #7's "export ruled page" — the selected page written OUT as a derived
    dosje into the canon_ruled stratum (originals untouched, ledger
    witnesses the export). The list = live entries (merged_into IS NULL)
    grouped by word; the losers live inside their keeper's page, which
    derives by the spine's own page(). Nothing here re-derives or
    re-parses anything."""

    COLS = ("word", "sources", "formats", "reported", "headline")
    W = (420, 70, 130, 90, 90)

    def __init__(self, parent):
        super().__init__(parent, padding=8)
        self.alive = False
        self.rows = []
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
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

        bar = ttk.Frame(self)
        bar.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(bar, text="filter:").pack(side="left")
        self.filter_var = tk.StringVar()
        ent = ttk.Entry(bar, textvariable=self.filter_var)
        ent.pack(side="left", fill="x", expand=True, padx=4)
        ent.bind("<KeyRelease>", lambda _e: self.fill())
        ttk.Button(bar, text="export ruled page",
                   command=self.export_page).pack(side="left", padx=(6, 0))
        ttk.Button(bar, text="edit entry", command=self.edit_entry).pack(
            side="left", padx=(6, 0))
        ttk.Button(bar, text="add entry", command=self.add_entry).pack(
            side="left", padx=(6, 0))
        self.count_var = tk.StringVar(value="—")
        ttk.Label(bar, textvariable=self.count_var).pack(side="left", padx=8)

        self.tree = ttk.Treeview(self, columns=self.COLS, show="headings")
        for c, w in zip(self.COLS, self.W):
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w, anchor="w" if c == "word" else "center")
        self.tree.grid(row=1, column=0, sticky="nsew", pady=(4, 0))
        self.text = tk.Text(self, wrap="word", state="disabled", width=58)
        self.text.grid(row=1, column=1, sticky="nsew", pady=(4, 0), padx=(6, 0))
        self.tree.bind("<<TreeviewSelect>>", self.open_page)
        self.load()

    def load(self):
        self.rows = [dict(r) for r in self.con.execute(
            "SELECT word, COUNT(*) AS sources, "
            "GROUP_CONCAT(DISTINCT format) AS formats, "
            "SUM(grade='reported') AS reported, SUM(grade='headline') AS headline "
            "FROM entries WHERE merged_into IS NULL GROUP BY word "
            "ORDER BY word COLLATE NOCASE")]
        self.fill()

    def fill(self):
        needle = self.filter_var.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        shown = 0
        for r in self.rows:
            if needle and needle not in r["word"].lower():
                continue
            self.tree.insert("", "end", iid=r["word"], values=(
                r["word"], r["sources"], r["formats"], r["reported"], r["headline"]))
            shown += 1
        self.count_var.set(f"{shown} / {len(self.rows)} words")

    def export_page(self):
        """Graft #7 — the canon feeding itself: write the selected word's
        RULED page as a derived dosje into the canon_ruled stratum (a
        sibling of the corpus dirs). The export is a ledger line; a rescan
        then admits the file through the ordinary door — parse, dup-detect
        against its own ancestors, REVIEW again."""
        sel = self.tree.selection()
        if not sel:
            self.count_var.set("select a word first — export needs a page")
            return
        word = sel[0]
        out_dir = os.path.normpath(os.path.join(_HERE, "..", "canon_ruled"))
        r = SOUL.export_page(self.con, word, out_dir)
        if "error" in r:
            self.count_var.set(r["error"])
        else:
            self.count_var.set(f"exported → {r['file']} "
                               f"({r['entries']} entries, "
                               f"{r['mentions']} mentions, ledger: export) — "
                               f"rescan admits it")

    # ------------------------------------------- graft #12: the editor --
    # The owner's hand INSIDE the canon: edits are canon DIRECTLY (a
    # normative act), and the old values survive in the ledger 'edit'
    # line — normative acts also leave causal receipts. Added entries
    # live under the doc 'cockpit://owner-added' — provenance by name.

    FIELDS = (("word", "beseda"), ("foneticni_rez", "fonetični rez"),
              ("glyph", "glyph"), ("thesis", "teza"),
              ("antithesis", "antiteza"), ("synthesis", "sinteza"),
              ("ontoloski_pomen", "ontološki pomen"),
              ("antinoma", "antinoma"),
              ("prakticna_uporaba", "praktična uporaba"))
    SHORT = {"word", "foneticni_rez", "glyph"}

    def edit_entry(self):
        sel = self.tree.selection()
        if not sel:
            self.count_var.set("select a word first — the editor needs a page")
            return
        live = [dict(r) for r in self.con.execute(
            "SELECT * FROM entries WHERE word=? AND merged_into IS NULL",
            (sel[0],))]
        if not live:
            self.count_var.set("no live entry for this word")
            return
        win = tk.Toplevel(self)
        win.title(f"edit an entry of '{sel[0]}' — your edit is canon; "
                  "the old value survives in the ledger")
        lb = tk.Listbox(win, width=104, height=min(len(live), 10))
        for e in live:
            lb.insert("end", f"{e['entry_id']} [{e['grade']}/{e['format']}] "
                             f"{e['word']} — "
                             f"{(e['thesis'] or e['synthesis'] or e['foneticni_rez'] or '—')[:60]}")
        lb.pack(padx=8, pady=8)
        lb.selection_set(0)

        def open_form(_e=None):
            s = lb.curselection()
            if not s:
                return
            win.destroy()
            self._entry_form(live[s[0]])

        lb.bind("<Double-Button-1>", open_form)
        lb.bind("<Return>", open_form)
        lb.focus_set()

    def add_entry(self):
        sel = self.tree.selection()
        self._entry_form(None, pre_word=sel[0] if sel else "")

    def _entry_form(self, entry, pre_word=""):
        win = tk.Toplevel(self)
        win.title("edit entry" if entry else "add entry — canon by your hand")
        widgets = {}
        for i, (key, label) in enumerate(self.FIELDS):
            ttk.Label(win, text=label + ":").grid(
                row=i, column=0, sticky="nw", padx=4, pady=2)
            if key in self.SHORT:
                var = tk.StringVar(value=(entry or {}).get(key)
                                   or (pre_word if key == "word" else ""))
                w = ttk.Entry(win, textvariable=var, width=90)
                widgets[key] = var
            else:
                w = tk.Text(win, width=90, height=2, wrap="word")
                w.insert("1.0", (entry or {}).get(key) or "")
                widgets[key] = w
            w.grid(row=i, column=1, sticky="ew", padx=4, pady=2)

        def save():
            vals = {k: (widgets[k].get().strip() if k in self.SHORT
                        else widgets[k].get("1.0", "end").strip())
                    for k, _l in self.FIELDS}
            if entry:
                old = {k: (entry.get(k) or "")
                       for k, _l in self.FIELDS
                       if (entry.get(k) or "") != vals[k]}
                new = {k: vals[k] for k in old}
                if not old:
                    win.destroy()
                    return
                self.con.execute(
                    "UPDATE entries SET " +
                    ", ".join(f"{k}=?" for k in new) +
                    " WHERE entry_id=?",
                    list(new.values()) + [entry["entry_id"]])
                SOUL.led(self.con, "edit", vals["word"] or entry["word"],
                         {"entry_id": entry["entry_id"], "old": old,
                          "new": new})
                self.con.commit()
                self.count_var.set(f"EDITED entry {entry['entry_id']} — "
                                  f"{len(new)} field(s) changed, old values "
                                  f"witnessed in the ledger (kind edit)")
            else:
                if not vals["word"]:
                    self.count_var.set("an added entry needs a word")
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
                    (doc_id, vals["word"], "owner", None, vals["thesis"],
                     vals["antithesis"], vals["synthesis"],
                     vals["foneticni_rez"], vals["ontoloski_pomen"],
                     vals["antinoma"], vals["glyph"],
                     vals["prakticna_uporaba"]))
                SOUL.led(self.con, "edit", vals["word"],
                         {"entry_id": cur.lastrowid, "old": None, "new": vals,
                          "note": "owner-added entry"})
                self.con.commit()
                self.count_var.set(f"ADDED entry {cur.lastrowid} for "
                                    f"'{vals['word']}' (ledger: edit)")
            win.destroy()
            self.load()
            self.fill()
            self.tree.selection_set(vals["word"] if vals["word"] in
                                   self.tree.get_children() else "")
            if self.tree.selection():
                self.open_page()

        ttk.Button(win, text="save (ledger: edit)", command=save).grid(
            row=len(self.FIELDS), column=0, columnspan=2, pady=8)

    def open_page(self, _e=None):
        sel = self.tree.selection()
        if not sel:
            return
        p = SOUL.page(self.con, sel[0])
        out = [f"=== {p['word']} — the page (derived by the spine) ===",
               f"entries: {len(p['entries'])}   omenjeno v {p['mentions']} dokumentih",
               ""]
        if p["conflicts"]:
            out.append(f"CONFLICT: {p['conflicts'][0]['variants']} fonetični rez "
                       "variants — real difference, stays yours to rule")
            out.append("")
        for e in p["entries"]:
            # graft #8: what the source text IS and where it OCCUPIES —
            # stratum · kind before the bare doc:line
            if e.get("doc_stratum"):
                doc = (f"{e['doc_stratum']} · {e['doc_kind']} · "
                       f"doc {e['doc_id']}:{e['lineno']}")
            else:
                doc = f"doc {e['doc_id']}:{e['lineno']}"
            if e.get("merged_into"):
                out.append(f"— merged into '{e['merged_into']}'  "
                           f"[{e['grade']}/{e['format']}]  {doc}")
                continue
            out.append(f"[{e['grade']}/{e['format']}]  {doc}  entry {e['entry_id']}"
                       + (f"  #{e['number']}" if e.get("number") else ""))
            for key in ("thesis", "antithesis", "synthesis", "foneticni_rez",
                        "ontoloski_pomen", "antinoma", "glyph", "prakticna_uporaba"):
                v = (e.get(key) or "").strip()
                if v:
                    out.append(f"    {key}: {v}")
            out.append("")
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("1.0", "\n".join(out))
        self.text.configure(state="disabled")


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
        nb.add(self.review, text="⊘ REVIEW")
        self.library = LibraryTab(nb)
        nb.add(self.library, text="∮ LIBRARY")
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
