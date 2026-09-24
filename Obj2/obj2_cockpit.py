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
  PERFORM    utter a chain live: state bars vs guard thresholds, ledger
             lines, verdict (WORD/DISCOVERY/FOREIGN + PASS/MORAVA/HOLD/FALL)
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
import os
import sys
import subprocess
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
        ttk.Entry(bar, textvariable=self.search_var).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(bar, text="find", command=self.search).pack(side="left")
        self.files_var = tk.StringVar(value=f"{len(self._files())} files")
        ttk.Label(bar, textvariable=self.files_var).pack(side="left", padx=8)

        self.listbox = tk.Listbox(self, width=44)
        self.listbox.grid(row=1, column=0, sticky="ew", pady=(6, 2))
        self.text = tk.Text(self, wrap="word", state="disabled", width=80)
        self.text.grid(row=2, column=0, sticky="nsew", pady=2)
        self.results = tk.Text(self, height=6, wrap="none", state="disabled")
        self.results.grid(row=3, column=0, sticky="ew", pady=2)
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
                            self.results.insert("end", f"{f}:{i}: {line.strip()[:120]}\n")
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
        self.tree.bind("<Double-Button-1>", lambda e: self.run_one(self.tree.selection()[0]))

    def _run(self, fname):
        proc = subprocess.run([sys.executable, os.path.join(_HERE, fname)],
                              capture_output=True, text=True, timeout=120,
                              encoding="utf-8", errors="replace", cwd=_HERE)
        blob = (proc.stdout or "") + (proc.stderr or "")
        ok = proc.returncode == 0
        return ok, blob

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
        if fname not in dict((f, 1) for _n, f, _e in SISTERS):
            return
        self._show(fname, *self._run(fname))

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
        for f in DECISION_RECORDS + [f for f in os.listdir(_HERE)
                                     if f.lower().endswith(".py")]:
            self.tree.insert("", "end", text=f, iid=f)
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
        nb.add(CanvasTab(nb), text="CANVAS")
        nb.add(ReceiptsTab(nb), text="RECEIPTS")
        nb.add(PerformTab(nb), text="PERFORM")
        nb.add(ParkTab(nb), text="PARK + FILES")
        nb.pack(fill="both", expand=True)


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
