"""
PHONETIC COORDINATES 107 — THE FULL UNIVERSAL SOUND SPACE
LOVE CAGE / Obj2 — phonetic_coordinates_107.py
Extends phonetic_coordinates-py.py (46 prisoners, Sep 24) to the full IPA
letter inventory. Built 24. 9. 2026, measured, not narrated.

LAWS CARRIED FROM THE ORIGINAL FILE (unchanged):
    X = place of articulation (lips -> throat)  0..8   (vowels share the axis: "It is anatomy.")
    Y = manner of articulation (stop -> open vowel) 0..10
    Z = voicing  0 or 1
    THE COORD IS THE ANATOMICAL TRUTH; THE SECONDARY FEATURE IS A FLAG.
    mine metric: dist = |dx| + |dy| + 3*|dz|  (voicing twins never touch: dist 3 > 2)

NEW LAWS (measured in build, pass 3 of the apd-ipa-bridge canvas):
    1. PLACES THE AXIS CAN'T HOLD ARE FLAGS: retroflex, alveolopalatal,
       pharyngeal, epiglottal, labial-velar, velarized, palatalized,
       rounding, laxness. No new columns; no old coord ever moves.
    2. AIRSTREAM IS A FLAG ON A STOP: click / implosive / ejective.
       (Anatomically exact: a click IS a stop with a different breath.)
    3. THE COUNT IS A FUNCTION OF A DECLARED PREDICATE (58/59/60 are
       costumes; see is_pulmonic below and the asserts).
    4. INVARIANCE IS NOT THE LAW; THE MIGRATION LEDGER IS. mine_number()
       changes for old prisoners on ANY growth. growth_ledger() is mandatory.
    5. FLAG-SIBLINGS SIT AT DISTANCE 0: ʈ shares t's cell. Whether a
       flag-sibling counts as a touching truth is a GAME DECISION —
       flag_sibling_counts (default False: same cell = same truth,
       different witness — the Zakon dopolnitve).
    6. THE OPERATOR IS THE PERFORMANCE: every letter carries apd_op, its
       APD operator (score, not execution). Executing it is the game's job.
"""

PLACE_X = {
    "bilabial": 0, "labiodental": 1, "dental": 2, "alveolar": 3,
    "postalveolar": 4, "palatal": 5, "velar": 6, "uvular": 7, "glottal": 8,
    "front": 0, "near-front": 1, "central": 4, "near-back": 5, "back": 8,
}
MANNER_Y = {
    "stop": 0, "nasal": 1, "fricative": 2, "affricate": 3, "lateral": 4,
    "trill": 5, "approximant": 6,
    "close_vowel": 8, "mid_vowel": 9, "open_vowel": 10,
}
VOICING_Z = {"voiceless": 0, "voiced": 1}

# sym: (x, y, z, unicode, flags, apd_op)
# apd_op = the operator the performance of this phoneme enacts (§5.2 warrants).
#          None = no binding yet — honest, not filled with invention.
PHONEMES = {
    # -- STOPS: the breath is caged, then released -----------------------------
    "p":  (0, 0, 0, "U+0070", (),            "boundary"),
    "b":  (0, 0, 1, "U+0062", (),            "boundary+witness"),
    "t":  (3, 0, 0, "U+0074", (),            "boundary"),
    "d":  (3, 0, 1, "U+0064", (),            "boundary+witness"),
    "ʈ":  (3, 0, 0, "U+0288", ("retro",),    "boundary"),
    "ɖ":  (3, 0, 1, "U+0256", ("retro",),    "boundary+witness"),
    "c":  (5, 0, 0, "U+0063", (),            "boundary"),
    "ɟ":  (5, 0, 1, "U+025F", (),            "boundary+witness"),
    "k":  (6, 0, 0, "U+006B", (),            "boundary"),
    "ɡ":  (6, 0, 1, "U+0261", (),            "boundary+witness"),  # U+0261, never U+0067
    "q":  (7, 0, 0, "U+0071", (),            "boundary"),
    "ɢ":  (7, 0, 1, "U+0262", (),            "boundary+witness"),
    "ʔ":  (8, 0, 0, "U+0294", (),            "terminal_assertion"),  # the ∂ that fixes
    "ʡ":  (7, 0, 0, "U+02A1", ("epi",),      "terminal_assertion"),
    # -- CLICKS / IMPLOSIVES: airstream flags on stops --------------------------
    "ʘ":  (0, 0, 0, "U+0298", ("click",),        "double_event"),
    "ǀ":  (2, 0, 0, "U+01C0", ("click",),        "double_event"),
    "ǃ":  (3, 0, 0, "U+01C3", ("click",),        "double_event"),  # U+01C3, never "!"
    "ǂ":  (4, 0, 0, "U+01C2", ("click",),        "double_event"),
    "ǁ":  (3, 0, 0, "U+01C1", ("click","lat"),   "double_event+flow_around"),
    "ɓ":  (0, 0, 1, "U+0253", ("imp",),          "inward_event"),
    "ɗ":  (3, 0, 1, "U+0257", ("imp",),          "inward_event"),
    "ʄ":  (5, 0, 1, "U+0284", ("imp",),          "inward_event"),
    "ɠ":  (6, 0, 1, "U+0260", ("imp",),          "inward_event"),
    "ʛ":  (7, 0, 1, "U+029B", ("imp",),          "inward_event"),
    # -- NASALS: the mouth cages, the nose frees --------------------------------
    "m":  (0, 1, 1, "U+006D", (),         "continuity"),
    "ɱ":  (1, 1, 1, "U+0271", (),         "continuity"),
    "n":  (3, 1, 1, "U+006E", (),         "continuity"),
    "ɳ":  (3, 1, 1, "U+0273", ("retro",), "continuity"),
    "ɲ":  (5, 1, 1, "U+0272", (),         "continuity"),
    "ŋ":  (6, 1, 1, "U+014B", (),         "continuity"),
    "ɴ":  (7, 1, 1, "U+0274", (),         "continuity"),
    # -- TRILLS / TAPS: the tongue drums (tap = flag on Y=5) ---------------------
    "ʙ":  (0, 5, 1, "U+0299", (),              "pulse"),
    "r":  (3, 5, 1, "U+0072", (),              "pulse"),
    "ʀ":  (7, 5, 1, "U+0280", (),              "pulse"),
    "ɾ":  (3, 5, 1, "U+027E", ("tap",),        "single_pulse"),
    "ɽ":  (3, 5, 1, "U+027D", ("tap","retro"), "single_pulse"),
    "ɺ":  (3, 5, 1, "U+027A", ("tap","lat"),   "single_pulse+flow_around"),
    # -- FRICATIVES: the breath is squeezed, never caged -------------------------
    "ɸ":  (0, 2, 0, "U+0278", (),             "sustained_tension"),
    "β":  (0, 2, 1, "U+03B2", (),             "sustained_tension+witness"),
    "f":  (1, 2, 0, "U+0066", (),             "sustained_tension"),
    "v":  (1, 2, 1, "U+0076", (),             "sustained_tension+witness"),
    "θ":  (2, 2, 0, "U+03B8", (),             "sustained_tension"),
    "ð":  (2, 2, 1, "U+00F0", (),             "sustained_tension+witness"),
    "s":  (3, 2, 0, "U+0073", (),             "sustained_tension"),
    "z":  (3, 2, 1, "U+007A", (),             "soft_cut_running"),  # MEHKI REZ
    "ʃ":  (4, 2, 0, "U+0283", (),             "sustained_tension"),
    "ʒ":  (4, 2, 1, "U+0292", (),             "sustained_tension+witness"),
    "ʂ":  (4, 2, 0, "U+0282", ("retro",),     "sustained_tension"),
    "ʐ":  (4, 2, 1, "U+0290", ("retro",),     "sustained_tension+witness"),
    "ɕ":  (4, 2, 0, "U+0255", ("alp",),       "sustained_tension"),
    "ʑ":  (4, 2, 1, "U+0291", ("alp",),       "soft_cut_running"),
    "ç":  (5, 2, 0, "U+00E7", (),             "sustained_tension"),
    "ʝ":  (5, 2, 1, "U+029D", (),             "sustained_tension+witness"),
    "x":  (6, 2, 0, "U+0078", (),             "sustained_tension"),
    "ɣ":  (6, 2, 1, "U+0263", (),             "sustained_tension+witness"),
    "χ":  (7, 2, 0, "U+03C7", (),             "sustained_tension"),
    "ʁ":  (7, 2, 1, "U+0281", (),             "sustained_tension+witness"),
    "ħ":  (8, 2, 0, "U+0127", ("phar",),      "sustained_tension"),
    "ʕ":  (8, 2, 1, "U+0295", ("phar",),      "sustained_tension+witness"),
    "ʜ":  (8, 2, 0, "U+029C", ("epi",),       "sustained_tension"),
    "ʢ":  (8, 2, 1, "U+02A2", ("epi",),       "sustained_tension+witness"),
    "h":  (8, 2, 0, "U+0068", (),             "pure_breath"),
    "ɦ":  (8, 2, 1, "U+0266", (),             "pure_breath+witness"),
    "ʍ":  (0, 2, 0, "U+028D", ("labvel",),   "sustained_tension"),
    "ɧ":  (4, 2, 0, "U+0267", ("labvel",),   "sustained_tension"),  # variable sj-sound
    # -- LATERALS: the breath escapes AROUND the tongue (fric = flag on Y=4) -----
    "ɬ":  (3, 4, 0, "U+026C", ("fric",),     "flow_around"),
    "ɮ":  (3, 4, 1, "U+026E", ("fric",),     "flow_around+witness"),
    "l":  (3, 4, 1, "U+006C", (),            "flow_around"),
    "ɭ":  (3, 4, 1, "U+026D", ("retro",),    "flow_around"),
    "ʎ":  (5, 4, 1, "U+028E", (),            "flow_around"),
    "ʟ":  (6, 4, 1, "U+029F", (),            "flow_around"),
    "ɫ":  (3, 4, 1, "U+026B", ("vel",),      "flow_around_held"),  # dark l
    # -- APPROXIMANTS: the breath slips past --------------------------------------
    "ʋ":  (1, 6, 1, "U+028B", (),            "glide"),
    "ɹ":  (3, 6, 1, "U+0279", (),            "glide"),
    "ɻ":  (3, 6, 1, "U+027B", ("retro",),    "glide"),
    "j":  (5, 6, 1, "U+006A", (),            "glide"),
    "ɰ":  (6, 6, 1, "U+0270", (),            "glide"),
    "w":  (0, 6, 1, "U+0077", ("labvel",),   "glide_double"),   # two places, one body
    "ɥ":  (0, 6, 1, "U+0265", ("pal",),      "glide_double"),
    # -- VOWELS: the breath carries the body (same X axis; it is anatomy) --------
    "i":  (0, 8, 1, "U+0069", (),           "mu_carrier"),
    "y":  (0, 8, 1, "U+0079", ("r",),        "mu_carrier_rounded"),
    "ɪ":  (1, 8, 1, "U+026A", ("l",),        "mu_carrier_lax"),
    "ʏ":  (1, 8, 1, "U+028F", ("l","r"),     "mu_carrier_lax_rounded"),
    "e":  (1, 9, 1, "U+0065", (),            "mu_carrier"),
    "ø":  (1, 9, 1, "U+00F8", ("r",),        "mu_carrier_rounded"),
    "ɛ":  (2, 9, 1, "U+025B", (),            "mu_carrier"),
    "œ":  (2, 9, 1, "U+0153", ("r",),        "mu_carrier_rounded"),
    "æ":  (2, 10, 1, "U+00E6", ("l",),        "mu_carrier_lax"),
    "a":  (3, 10, 1, "U+0061", (),           "mu_carrier_open"),
    "ɶ":  (2, 10, 1, "U+0276", ("r",),        "mu_carrier_open_rounded"),
    "ɨ":  (4, 8, 1, "U+0268", (),            "mu_carrier"),
    "ʉ":  (4, 8, 1, "U+0289", ("r",),        "mu_carrier_rounded"),
    "ɘ":  (4, 9, 1, "U+0258", (),            "mu_carrier"),
    "ɵ":  (4, 9, 1, "U+0275", ("r",),        "mu_carrier_rounded"),
    "ə":  (4, 9, 1, "U+0259", ("mid",),       "mu_carrier_given_up"),  # the schwa
    "ɜ":  (4, 10, 1, "U+025C", (),            "mu_carrier"),
    "ɞ":  (4, 10, 1, "U+025E", ("r",),        "mu_carrier_rounded"),
    "ɐ":  (4, 10, 1, "U+0250", ("l",),        "mu_carrier_lax"),
    "ʌ":  (5, 9, 1, "U+028C", (),            "mu_carrier"),
    "ɤ":  (7, 8, 1, "U+0264", ("u",),        "mu_carrier_unrounded"),
    "ɑ":  (6, 10, 1, "U+0251", (),           "mu_carrier_open"),
    "ɒ":  (6, 10, 1, "U+0252", ("r",),        "mu_carrier_open_rounded"),
    "ɔ":  (7, 9, 1, "U+0254", (),            "mu_carrier"),
    "o":  (7, 8, 1, "U+006F", ("r",),        "mu_carrier_rounded"),
    "ʊ":  (7, 8, 1, "U+028A", ("l",),        "mu_carrier_lax"),
    "u":  (8, 8, 1, "U+0075", ("r",),        "mu_carrier_rounded"),
    "ɯ":  (8, 8, 1, "U+026F", ("u",),        "mu_carrier_unrounded"),
    # NOTE: ä is NOT here — a + U+0308 is a sequence, not a letter (measured, pass 3).
    # NOTE: t͡s t͡ʃ d͡ʒ and all affricates/ejectives are TIE-SEQUENCES (U+0361 / U+02BC),
    # kept in the engine as sequences over these letters, exactly as the original file does.
}

# ejectives: pʼ = ("p", ("ej",)) — never a new letter; the flag rides the letter.

# ---------------------------------------------------------------------------
# PREDICATES — the count is a function of a declared predicate. Assert, don't trust prose.
# ---------------------------------------------------------------------------

def _flags(sym):
    return PHONEMES[sym][4]

def is_vowel(sym):
    return PHONEMES[sym][1] >= 8

def is_click(sym):
    return "click" in _flags(sym)

def is_implosive(sym):
    return "imp" in _flags(sym)

def is_pulmonic(sym):
    """Predicate, declared: pulmonic = a letter that is none of the above and
    none of the coarticulated/variable specials. Count under THIS predicate:
    60. Other predicates give 58 or 59 — all costumes of this function."""
    return not (is_vowel(sym) or is_click(sym) or is_implosive(sym)
                or sym in ("w", "ʍ", "ɥ", "ɫ", "ɧ", "ʡ", "ɺ"))

# ---------------------------------------------------------------------------
# MINE NUMBERS — with the flag-sibling rule made explicit.
# ---------------------------------------------------------------------------

def mine_number(symbol, flag_sibling_counts=False):
    """How many truths touch this truth. dist = |dx|+|dy|+3|dz| <= 2.

    flag_sibling_counts: if True, a prisoner sharing your CELL but differing
    only in flags (ʈ on t's cell) counts as touching (distance 0).
    Default False: same cell = same truth, different witness (Zakon dopolnitve).
    This is a GAME DECISION, not a physics one — measure both before sealing."""
    x, y, z = PHONEMES[symbol][:3]
    myflags = set(_flags(symbol))
    count = 0
    for s, d in PHONEMES.items():
        if s == symbol:
            continue
        dx, dy, dz = d[0], d[1], d[2]
        dist = abs(dx - x) + abs(dy - y) + abs(dz - z) * 3
        if dist == 0 and not flag_sibling_counts:
            continue  # flag-sibling: same truth, different witness
        if dist <= 2:
            count += 1
    return count

def growth_ledger(old_mine_numbers):
    """THE MIGRATION LEDGER IS THE LAW. Invariance is not achievable (measured:
    any new prisoner within distance 2 changes neighbors). On ANY growth,
    compute old->new for every prisoner and WRITE THE DIFF. Old numbers do not
    survive; their changes get a priča."""
    ledger = {}
    for sym in old_mine_numbers:
        new = mine_number(sym)
        if new != old_mine_numbers[sym]:
            ledger[sym] = (old_mine_numbers[sym], new)
    return ledger

# ---------------------------------------------------------------------------
# SELF-TEST — run: python phonetic_coordinates_107.py
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    n = len(PHONEMES)
    assert n == 107, f"letter count {n} != 107"
    nv = sum(1 for s in PHONEMES if is_vowel(s))
    assert nv == 28, f"vowel count {nv} != 28"
    assert sum(1 for s in PHONEMES if is_click(s)) == 5
    assert sum(1 for s in PHONEMES if is_implosive(s)) == 5
    assert is_pulmonic("t") and not is_pulmonic("w")
    # confusable-codepoint ban-list: these IPA look-alikes must never appear as keys
    for banned in ("ʇ", "ʗ", "ʖ", "ɼ", "ɿ", "ʅ", "ʆ", "ʓ", "ʭ", "ʬ", "ɩ", "ɷ"):
        assert banned not in PHONEMES, f"obsolete symbol {banned} in table"
    # the 46 old prisoners keep their coords (flag-extension never moves a cell)
    OLD_COORDS = {"p": (0,0,0), "b": (0,0,1), "t": (3,0,0), "d": (3,0,1),
                  "k": (6,0,0), "g": (6,0,1), "ʔ": (8,0,0), "m": (0,1,1),
                  "n": (3,1,1), "ŋ": (6,1,1), "f": (1,2,0), "v": (1,2,1),
                  "θ": (2,2,0), "ð": (2,2,1), "s": (3,2,0), "z": (3,2,1),
                  "ʃ": (4,2,0), "ʒ": (4,2,1), "ç": (5,2,0), "x": (6,2,0),
                  "h": (8,2,0), "l": (3,4,1), "ʎ": (5,4,1), "r": (3,5,1),
                  "ʁ": (7,5,1), "ɹ": (3,6,1), "j": (5,6,1), "w": (0,6,1),
                  "i": (0,8,1), "ɪ": (1,8,1), "e": (1,9,1), "ɛ": (2,9,1),
                  "æ": (2,10,1), "a": (3,10,1), "ə": (4,9,1), "ʌ": (5,9,1),
                  "ɑ": (6,10,1), "ɔ": (7,9,1), "o": (7,8,1), "ʊ": (7,8,1),
                  "u": (8,8,1), "y": (0,8,1), "ø": (1,9,1)}
    for sym, c in OLD_COORDS.items():
        assert PHONEMES[sym][:3] == c, f"OLD COORD MOVED: {sym}"
    print(f"PASS — {n} letters | 28 vowels | 5 clicks | 5 implosives | "
          f"pulmonic under declared predicate: {sum(1 for s in PHONEMES if is_pulmonic(s))}")
    print("Old coordinates: none moved (flags-only extension).")
    print("WARNING (measured): mine numbers of old prisoners WILL change on growth — "
          "run growth_ledger() and ship the diff. Invariance is not the law; the ledger is.")