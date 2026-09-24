"""
WORDLIST VALIDATOR — THE FINITENESS LAYER (deliverable 3)
LOVE CAGE / Obj2 — wordlist_validator.py. 24. 9. 2026.
Sister of phonetic_coordinates_full.py (lattice truth) and apd_engine
(performance). Built against the finiteness reading:

    Level 1: 107 cubes — fixed forever (IPA closed the inventory, 2005)
    Level 2: one language lights ~30–40 of them (costume masks = the preset)
    Level 3: valid words — a finite, machine-checkable list (the wordlist)
    Level 4: possible chains — the combinatorial wilderness where the game lives

This file makes all four levels machine-checkable:
    - LANGUAGE PRESETS derived from the lattice costume masks (single source
      of truth — the WORLD amendment's requirement, not prose)
    - SEED WORDLIST: schema + a small honest seed set (the full wordlist is an
      import problem with a defined schema: CMUdict for EN is the obvious
      machine source; a Slovenian source is an open ∂ — SSKJ is not freely
      machine-readable)
    - CHAIN CLASSIFIER: WORD | DISCOVERY | FOREIGN
        WORD       chain in the wordlist (stamped by the language)
        DISCOVERY  utterable (every cube lit for this language) but unstamped
        FOREIGN    the chain leaves the language's lit cubes — the foreign
                   moment; every unlit cube it touches is flagged CURIOUS
    - FINITENESS MEASUREMENT: possible chains per language, computed, not
      narrated (measured finding: the reading's "millions" understates the
      wilderness by ~5 orders of magnitude — 30 cubes, length 3–8 is ~6.6e11)
    - run_chain(): the FIRST CONSUMER of apd_engine.perform() — uttering a
      chain is a sequence of performances, every one ledgered; the guard
      verdicts accrue. MORAVA or FALL, both valid outcomes (rez 386).

Unification note (working, pending the formal merge seal): the engine's
op_map binds pass-3's apd_op vocabulary; this file reads apd_op strings from
the pass-3 table (its real contribution) while the lattice (coords, costumes,
presets, flags) remains phonetic_coordinates_full.py. One lattice truth, one
score sheet, one runtime.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import importlib.util
import os
import math

_HERE = os.path.dirname(os.path.abspath(__file__))


def _load(fname):
    spec = importlib.util.spec_from_file_location(fname.replace("-", "_").split(".")[0],
                                                  os.path.join(_HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


LATTICE = _load("phonetic_coordinates_full.py")        # the 107 (coords, costumes, flags)
ENGINE = _load("apd_engine-py-apd-runtime-for-love-cage-deliverable-2.py")  # perform/guard/ledger
PASS3 = _load("phonetic_coordinates_107-py-the-full-universe-extension-of-the-obj2-lattice.py")  # apd_op score sheet

PHONEMES = LATTICE.PHONEMES

# ---------------------------------------------------------------------------
# LEVEL 2 — LANGUAGE PRESETS (derived from costume masks; "-" = never visits)
# ---------------------------------------------------------------------------

def lit(lang: str):
    """Letters this language lights (owners + visitors; tri-state split is a
    pending seal — the mask carries the fact of the visit, the note carries
    the visitor status)."""
    return sorted(s for s, d in PHONEMES.items()
                  if d["costume"].get(lang) not in (None, "-"))

PRESETS = {lang: lit(lang) for lang in ("en", "sl", "de")}

def is_vowel(sym: str) -> bool:
    return PHONEMES[sym]["coord"][1] >= 8

# ---------------------------------------------------------------------------
# LEVEL 3 — THE WORDLIST (finite, known, checkable). Seed set, hand-verified.
# Full wordlists are imports: CMUdict (EN) is machine-ready; SL source is ∂.
# ---------------------------------------------------------------------------

WORDLIST = {
    "en": {
        "love":   ["l", "ʌ", "v"],
        "cat":    ["k", "æ", "t"],
        "dog":    ["d", "ɔ", "ɡ"],
        "think":  ["θ", "ɪ", "ŋ", "k"],
        "this":   ["ð", "ɪ", "s"],
        "sing":   ["s", "ɪ", "ŋ"],
        "we":     ["w", "i"],
        "red":    ["ɹ", "ɛ", "d"],
        "book":   ["b", "ʊ", "k"],
        "yes":    ["j", "ɛ", "s"],
        "flute":  ["f", "l", "u", "t"],
        "judge":  ["d͡ʒ", "ʌ", "d͡ʒ"],
        "church": ["t͡ʃ", "ɝ", "t͡ʃ"],
    },
    "sl": {
        "ljubezen": ["ʎ", "u", "b", "e", "z", "ɛ", "n"],
        "beseda":   ["b", "ɛ", "s", "ɛ", "d", "a"],
        "pes":      ["p", "ɛ", "s"],
        "voda":     ["v", "ɔ", "d", "a"],
        "reka":     ["r", "ɛ", "k", "a"],
        "gora":     ["ɡ", "ɔ", "r", "a"],
        "dan":      ["d", "a", "n"],
        "med":      ["m", "ɛ", "d"],
        "zima":     ["z", "i", "m", "a"],
        "sonce":    ["s", "ɔ", "n", "t͡s", "ɛ"],
        "hiter":    ["x", "i", "t", "ɛ", "r"],
        "njiva":    ["ɲ", "i", "v", "a"],
        "kam":      ["k", "a", "m"],
        "cena":     ["t͡s", "ɛ", "n", "a"],
        "čaj":      ["t͡ʃ", "a", "j"],
        "muha":     ["m", "u", "x", "a"],
    },
    "de": {
        "Liebe":  ["l", "i", "b", "ə"],
        "ich":    ["ɪ", "ç"],
        "schön":  ["ʃ", "ø", "n"],
        "über":   ["y", "b", "ʁ"],
        "rot":    ["ʁ", "o", "t"],   # phonemic /roːt/; [ɔ] is an allophone — the lattice correctly refuses de ownership of ɔ
        "Mann":   ["m", "a", "n"],
        "Bett":   ["b", "ɛ", "t"],
        "Weg":    ["v", "ɛ", "k"],
        "singen": ["z", "ɪ", "ŋ", "ə", "n"],
        "Hut":    ["h", "u", "t"],
    },
}

# chain lookup: normalized (grapheme-independent) by tuple
_CHAINS = {lang: {tuple(c): w for w, c in words.items()}
           for lang, words in WORDLIST.items()}

# Sequences (affricates, r-colored) decompose for performance: the engine
# executes letters; a sequence is its parts in order (per the lattice law:
# t͡s etc. are tie-sequences, never letters).
SEQUENCE_DECOMP = {"t͡s": ["t", "s"], "t͡ʃ": ["t", "ʃ"], "d͡ʒ": ["d", "ʒ"],
                   "ɚ": ["ə"], "ɝ": ["ə"]}


def is_word(chain, lang) -> bool:
    return tuple(chain) in _CHAINS.get(lang, {})

def is_utterable(chain, lang) -> bool:
    """Every cube in the chain is lit for this language. (Chain-level
    phonotactics — connection rules, can_connect_to — remains ∂: the grammar
    decision is not sealed; this validator checks LIT-ness and membership only.)"""
    return all(s in PRESETS[lang] for s in chain)

def has_vowel(chain) -> bool:
    """The one sealed grammar rule: a chain must carry at least one vowel."""
    return any(is_vowel(s) for s in chain)


@dataclass
class ChainVerdict:
    classification: str      # WORD | DISCOVERY | FOREIGN
    word: str = ""            # matching wordlist entry, if WORD
    curious: list = field(default_factory=list)  # unlit cubes touched (FOREIGN)
    note: str = ""


def classify(chain, lang) -> ChainVerdict:
    chain = list(chain)
    for s in chain:
        if s not in PHONEMES:
            return ChainVerdict("FOREIGN", curious=[s],
                                note=f"{s!r} is not a prisoner at all")
    if is_word(chain, lang):
        return ChainVerdict("WORD", word=_CHAINS[lang][tuple(chain)],
                            note="stamped by the language")
    if is_utterable(chain, lang):
        v = "with a vowel" if has_vowel(chain) else "NO VOWEL (grammar ∂)"
        return ChainVerdict("DISCOVERY",
                            note=f"utterable, unstamped — the wilderness. {v}")
    curious = [s for s in chain if s not in PRESETS[lang]]
    return ChainVerdict("FOREIGN", curious=curious,
                        note="the chain leaves your lit cubes — the foreign moment; "
                             "each unlit cube touched is CURIOUS")


# ---------------------------------------------------------------------------
# LEVEL 4 — THE FINITENESS MEASUREMENT (computed, not narrated)
# ---------------------------------------------------------------------------

def possible_chains(lang, k_min=1, k_max=8, require_vowel=True) -> int:
    """Chains over the lit cubes, repetition allowed (a word may reuse a sound).
    With the sealed vowel rule: subtract the vowel-less chains."""
    L = len(PRESETS[lang])
    C = sum(1 for s in PRESETS[lang] if not is_vowel(s))
    total = sum(L ** k for k in range(k_min, k_max + 1))
    if require_vowel:
        total -= sum(C ** k for k in range(k_min, k_max + 1))
    return total


# ---------------------------------------------------------------------------
# THE CONSUMER — uttering a chain is a sequence of performances.
# The first live caller of apd_engine.perform().
# ---------------------------------------------------------------------------

def run_chain(chain, lang, state=None, ledger=None, seed=0):
    """Utter a chain: perform every letter (sequences decomposed), every
    utterance writes its ledger line, the guard verdicts accrue. Returns the
    ChainVerdict, the final gate, and the number of ledger lines written.
    MORAVA or FALL — both valid outcomes (rez 386). The priča is the ledger."""
    if state is None:
        state = ENGINE.State()
    if ledger is None:
        ledger = ENGINE.Ledger()
    verdict = classify(chain, lang)
    n0 = len(ledger.rows)
    for sym in chain:
        parts = SEQUENCE_DECOMP.get(sym, [sym])
        for part in parts:
            voiced = bool(PHONEMES[part]["coord"][2])
            apd_op = PASS3.PHONEMES.get(part, (None,)*6)[5]
            if apd_op is None:
                apd_op = "boundary"  # honest fallback; engine ledger-only
            ENGINE.perform(part, apd_op, state, ledger, voiced, seed=seed)
    return verdict, ENGINE.guard(state), len(ledger.rows) - n0


# ---------------------------------------------------------------------------
# SELF-TEST — python wordlist_validator.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)
        return cond

    # -- Level 2: presets derived from the lattice, cross-checked against the
    #    WORLD reading's enumerated lists (machine-check of the amendment) --
    SL_READING = set("pbtdkfvszʃʒxmnɲlrjieɛaəɔou") | {"ɡ", "t͡s", "t͡ʃ", "d͡ʒ"}
    EN_READING = set("pbtdkfvszʃʒhmnŋlɹjwθðɪeɛæɑɔoʊuʌəɚi") | {"ɡ", "t͡ʃ", "d͡ʒ"}
    check(SL_READING <= set(PRESETS["sl"]),
          "WORLD reading's SL letters must all be lit (some are not)")
    check(EN_READING <= set(PRESETS["en"]),
          "WORLD reading's EN letters must all be lit (some are not)")

    # -- Level 3: every wordlist chain must be utterable and vowel-bearing --
    for lang, words in WORDLIST.items():
        for w, c in words.items():
            check(all(s in PHONEMES for s in c), f"{lang}:{w} references a non-prisoner")
            check(is_utterable(c, lang), f"{lang}:{w} chain leaves the lit cubes")
            check(has_vowel(c), f"{lang}:{w} has no vowel (sealed grammar rule)")

    # -- the seed stone: WORD in all five dimensions it names --
    check(classify(["l", "ʌ", "v"], "en").classification == "WORD", "love must be a WORD")
    check(classify(["ʎ", "u", "b", "e", "z", "ɛ", "n"], "sl").classification == "WORD",
          "ljubezen must be a WORD")
    check(classify(["l", "i", "b", "ə"], "de").classification == "WORD",
          "Liebe must be a WORD")

    # -- the foreign moment: θ is lit for EN but not for SL --
    v = classify(["l", "ʌ", "v", "θ"], "sl")
    check(v.classification == "FOREIGN" and "θ" in v.curious,
          "SL chain touching θ must be FOREIGN with θ curious")

    # -- the wilderness: utterable, unstamped --
    v = classify(["k", "ɔ", "z", "a"], "sl")
    check(v.classification == "DISCOVERY", "k-ɔ-z-a must be utterable+unstamped")

    # -- Level 4: the finiteness measurement --
    for lang in ("sl", "en", "de"):
        L = len(PRESETS[lang])
        k38 = possible_chains(lang, 3, 8)
        print(f"FINITENESS {lang}: {L} lit cubes | chains len 3-8 "
              f"(vowel rule): {k38:.3e}")
    check(possible_chains("sl", 3, 8) > 1e11,
          "measured wilderness must exceed the reading's 'millions' claim")

    # -- the consumer: run a real chain end-to-end through the engine --
    s = ENGINE.State(); L = ENGINE.Ledger()
    verdict, gate, lines = run_chain(["l", "ʌ", "v"], "en", s, L)
    check(lines == 3 and len(L.rows) == 3, "love must write 3 ledger lines")
    check(all(r["witnessed"] == 1 for r in L.rows),
          "l-ʌ-v are all voiced: every line witnessed (Zakon dopolnitve)")
    # a discovery chain performs too — the ledger does not care about stamps
    s2 = ENGINE.State(); L2 = ENGINE.Ledger()
    v2, gate2, lines2 = run_chain(["k", "ɔ", "z", "a"], "sl", s2, L2)
    check(v2.classification == "DISCOVERY" and lines2 == 4,
          "a discovery chain performs fully — 4 lines")
    # a foreign chain STILL performs: the curious cube gets its ledger line
    s3 = ENGINE.State(); L3 = ENGINE.Ledger()
    v3, gate3, lines3 = run_chain(["l", "ʌ", "v", "θ"], "sl", s3, L3)
    check(lines3 == 4 and v3.classification == "FOREIGN",
          "the foreign moment performs too — the curiosity is recorded")

    print("PRESETS: " + " | ".join(f"{k}: {len(v)} lit" for k, v in PRESETS.items()))
    print("SEED WORDLIST: " + ", ".join(f"{k}:{len(WORDLIST[k])}" for k in WORDLIST))
    print("SAMPLE RUNS:")
    print(f"  love (en):     verdict={verdict.classification}, lines={lines}, "
          f"gate={gate}, mu={s.mu:.3f}, alpha={s.alpha:.3f}")
    print(f"  k-ɔ-z-a (sl):  verdict={v2.classification}, lines={lines2}, gate={gate2}")
    print(f"  l-ʌ-v-θ (sl):  verdict={v3.classification}, curious={v3.curious}, "
          f"lines={lines3}, gate={gate3}")
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("PASS — the finiteness layer is machine-checkable: presets derived, "
          "wordlist sealed, wilderness measured, chains perform.")
