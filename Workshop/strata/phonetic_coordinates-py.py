"""
PHONETIC COORDINATES: THE UNIVERSAL SOUND SPACE
LOVE CAGE — phonetic_coordinates.py

THE LAW OF THE SPACE:
    X = place of articulation   (lips -> throat)      0..8
    Y = manner of articulation  (stop -> vowel)       0..10
    Z = voicing                 (voiceless -> voiced) 0 or 1

Every sound of every language sits at ONE position.
A language is not a set of sounds — it is a COSTUME LIST: which
prisoners it visits, and what letters it dresses them in.

Front vowels sit under the lips. Back vowels sit under the velum.
This is not a metaphor. It is anatomy.

Usage:
    from phonetic_coordinates import PHONEMES, PLACE_X, MANNER_Y, \
        mine_number, chain_of, LOVE_EQUIVALENTS, shared_prisoners

Self-test (no engine needed):
    python phonetic_coordinates.py
"""

# ---------------------------------------------------------------------------
# THE AXES
# ---------------------------------------------------------------------------

PLACE_X = {
    "bilabial": 0,      # both lips:        p b m
    "labiodental": 1,   # lip + teeth:      f v
    "dental": 2,        # tongue at teeth:  th
    "alveolar": 3,      # tongue at ridge:  t d s z n l
    "postalveolar": 4,  # behind ridge:     sh zh ch
    "palatal": 5,       # tongue at palate: ly, y-sound
    "velar": 6,         # back of tongue:   k g ng
    "uvular": 7,        # German R's home
    "glottal": 8,       # throat:           h
    # vowels use the SAME axis as backness:
    "front": 0, "near-front": 1, "central": 4, "near-back": 5, "back": 8,
}

MANNER_Y = {
    "stop": 0,          # the breath is CAGED then released: p t k
    "nasal": 1,         # the breath escapes through the nose: m n ng
    "fricative": 2,     # the breath is SQUEEZED: f s sh
    "affricate": 3,     # caged THEN squeezed: ts ch
    "lateral": 4,       # the breath escapes around the tongue: l ly
    "trill": 5,         # the tongue DRUMS: Slovenian r
    "approximant": 6,   # the breath slips past: English r, w
    # vowels continue the same axis downward:
    "close_vowel": 8,   # tongue high:   i u
    "mid_vowel": 9,     # tongue middle: e o
    "open_vowel": 10,   # tongue low:    a
}

VOICING_Z = {"voiceless": 0, "voiced": 1}

# ---------------------------------------------------------------------------
# THE PRISONERS
# Each entry:
#   coord      = (x, y, z)
#   costume    = the letter(s) each language dresses this prisoner in
#                ("-" = the language never visits this prisoner)
#   examples   = one word per language
#   note       = what the legend should say
# ---------------------------------------------------------------------------

PHONEMES = {
    # -- STOPS: the breath is caged, then released --------------------------------
    "p":  dict(coord=(0, 0, 0), costume={"en": "p", "sl": "p", "de": "p"},
               examples={"en": "pen", "sl": "pes", "de": "Post"},
               note="Lips seal. Breath waits. Breath wins."),
    "b":  dict(coord=(0, 0, 1), costume={"en": "b", "sl": "b", "de": "b"},
               examples={"en": "love", "sl": "beseda", "de": "Liebe"},
               note="Same cage as p, but the throat hums during the hold."),
    "t":  dict(coord=(3, 0, 0), costume={"en": "t", "sl": "t", "de": "t"},
               examples={"en": "top", "sl": "trava", "de": "Tee"},
               note="Alveolar stop. English and German aspirate it hard; Slovenian does not."),
    "d":  dict(coord=(3, 0, 1), costume={"en": "d", "sl": "d", "de": "d"},
               examples={"en": "dog", "sl": "delo", "de": "Ding"},
               note="Voiced twin of t."),
    "k":  dict(coord=(6, 0, 0), costume={"en": "k/c", "sl": "k", "de": "k/ch/ck"},
               examples={"en": "cat", "sl": "kam", "de": "Kind"},
               note="One position, three wardrobes. English even lets 'c' wear it."),
    "g":  dict(coord=(6, 0, 1), costume={"en": "g", "sl": "g", "de": "g"},
               examples={"en": "go", "sl": "gora", "de": "gut"},
               note="Voiced twin of k."),
    "ʔ":  dict(coord=(8, 0, 0), costume={"en": "-", "sl": "-", "de": "-"},
               examples={"en": "uh-oh", "sl": "a-a (ne)", "de": "Beamter"},
               note="The silent cage. The throat shuts, opens, says nothing yet."),

    # -- NASALS: the mouth cages the breath, the nose frees it -------------------
    "m":  dict(coord=(0, 1, 1), costume={"en": "m", "sl": "m", "de": "m"},
               examples={"en": "man", "sl": "mama", "de": "Mond"},
               note="The first sound every human mouth learns."),
    "n":  dict(coord=(3, 1, 1), costume={"en": "n", "sl": "n", "de": "n"},
               examples={"en": "no", "sl": "ne", "de": "Nacht"},
               note="Slovenian's word for 'no' starts with it. So does English's."),
    "ŋ":  dict(coord=(6, 1, 1), costume={"en": "ng", "sl": "n/g", "de": "ng"},
               examples={"en": "sing", "sl": "banka", "de": "singen"},
               note="English gave it a letter only at the END of words. German let it start them."),

    # -- FRICATIVES: the breath is squeezed, never caged --------------------------
    "f":  dict(coord=(1, 2, 0), costume={"en": "f/ph", "sl": "f", "de": "f/v"},
               examples={"en": "fish", "sl": "film", "de": "Fisch"},
               note="Teeth on lip. Air hisses through."),
    "v":  dict(coord=(1, 2, 1), costume={"en": "v", "sl": "v", "de": "w"},
               examples={"en": "love", "sl": "voda", "de": "Wasser"},
               note="German dresses this prisoner in 'w'. Never trust a German 'w'."),
    "θ":  dict(coord=(2, 2, 0), costume={"en": "th", "sl": "-", "de": "-"},
               examples={"en": "think", "sl": "-", "de": "-"},
               note="Tongue between the teeth. Slovenian and German never built this cell."),
    "ð":  dict(coord=(2, 2, 1), costume={"en": "th", "sl": "-", "de": "-"},
               examples={"en": "this", "sl": "-", "de": "-"},
               note="Same cell as the think-th, throat humming. English's most common word starts with it."),
    "s":  dict(coord=(3, 2, 0), costume={"en": "s/c", "sl": "s", "de": "s/ß"},
               examples={"en": "sun", "sl": "sonce", "de": "Sonne"},
               note="The hiss. All three languages own it."),
    "z":  dict(coord=(3, 2, 1), costume={"en": "z/s", "sl": "z/s", "de": "s"},
               examples={"en": "zoo", "sl": "zima", "de": "Sonne (voiced)"},
               note="Voiced twin of s. German 's' between vowels IS this prisoner."),
    "ʃ":  dict(coord=(4, 2, 0), costume={"en": "sh", "sl": "š", "de": "sch"},
               examples={"en": "shy", "sl": "šola", "de": "schön"},
               note="One sound, three spellings, each more absurd than the last."),
    "ʒ":  dict(coord=(4, 2, 1), costume={"en": "si", "sl": "ž", "de": "j"},
               examples={"en": "viSION", "sl": "železo", "de": "Journal"},
               note="Voiced twin of š. Slovenian needed one stroke for it. Wisest of the three."),
    "ç":  dict(coord=(5, 2, 0), costume={"en": "-", "sl": "-", "de": "ch"},
               examples={"en": "-", "sl": "-", "de": "ich"},
               note="German's shy hiss. The sound of 'ich'."),
    "x":  dict(coord=(6, 2, 0), costume={"en": "-", "sl": "h (often)", "de": "ch"},
               examples={"en": "-", "sl": "hiter", "de": "ach"},
               note="Velar hiss. German 'ach' and Slovenian 'h' share the cell."),
    "h":  dict(coord=(8, 2, 0), costume={"en": "h", "sl": "-", "de": "h"},
               examples={"en": "hat", "sl": "-", "de": "Hund"},
               note="Pure breath. Nothing else."),

    # -- AFFRICATES: caged, THEN squeezed ----------------------------------------
    "t͡s": dict(coord=(3, 3, 0), costume={"en": "ts", "sl": "c", "de": "z"},
               examples={"en": "caTS", "sl": "cena", "de": "Zeit"},
               note="Slovenian gave it ONE letter: c. German chose z. English pretends it doesn't exist."),
    "t͡ʃ": dict(coord=(4, 3, 0), costume={"en": "ch/tch", "sl": "č", "de": "tsch"},
               examples={"en": "church", "sl": "čaj", "de": "Tschüss"},
               note="The international 'ch'. Three costumes, one prisoner."),
    "d͡ʒ": dict(coord=(4, 3, 1), costume={"en": "j/ge", "sl": "dž", "de": "-"},
               examples={"en": "judge", "sl": "džem", "de": "-"},
               note="English built an empire on this sound. Slovenian only borrows it for jam."),

    # -- LATERALS: the breath escapes AROUND the tongue ---------------------------
    "l":  dict(coord=(3, 4, 1), costume={"en": "l", "sl": "l", "de": "l"},
               examples={"en": "love", "sl": "leto", "de": "Liebe"},
               note="All three languages start 'love' with this prisoner. Remember that."),
    "ʎ":  dict(coord=(5, 4, 1), costume={"en": "-(ly)", "sl": "lj", "de": "-(gl)"},
               examples={"en": "miLLion", "sl": "ljubezen", "de": "-"},
               note="Slovenia's untranslatable opening. English only meets it by accident."),

    # -- TRILLS: the tongue drums --------------------------------------------------
    "r":  dict(coord=(3, 5, 1), costume={"en": "-", "sl": "r", "de": "-"},
               examples={"en": "-", "sl": "reka", "de": "-"},
               note="The alveolar trill. The drum. Slovenian's r is percussion."),
    "ʁ":  dict(coord=(7, 5, 1), costume={"en": "-", "sl": "-", "de": "r"},
               examples={"en": "-", "sl": "-", "de": "rot"},
               note="German r moved to the throat. Same letter, different cell, four slots away."),
    "ɹ":  dict(coord=(3, 6, 1), costume={"en": "r", "sl": "-", "de": "-"},
               examples={"en": "red", "sl": "-", "de": "-"},
               note="English r is NOT a trill. It is a vowel-ish glide. The laziest r alive."),

    # -- APPROXIMANTS: the breath slips past ---------------------------------------
    "j":  dict(coord=(5, 6, 1), costume={"en": "y", "sl": "j", "de": "j"},
               examples={"en": "yes", "sl": "jaz", "de": "ja"},
               note="YES = JAZ = JA. Three languages, one prisoner, three costumes. The legend in one sound."),
    "w":  dict(coord=(0, 6, 1), costume={"en": "w", "sl": "-", "de": "-"},
               examples={"en": "we", "sl": "-", "de": "-"},
               note="Bilabial glide. English's signature. Others must fake it with 'v' or 'u'."),

    # -- VOWELS: manner axis continues; X = frontness ------------------------------
    "i":  dict(coord=(0, 8, 1), costume={"en": "ee/ea", "sl": "i", "de": "ie/ih"},
               examples={"en": "see", "sl": "biti", "de": "wie"},
               note="Highest, frontest. One vowel, three wardrobes."),
    "ɪ":  dict(coord=(1, 8, 1), costume={"en": "i", "sl": "-", "de": "i"},
               examples={"en": "bit", "sl": "-", "de": "bItte"},
               note="The short, lax i. English and German use it everywhere; Slovenian never does."),
    "e":  dict(coord=(1, 9, 1), costume={"en": "ay(-i)", "sl": "e (close)", "de": "e/eh"},
               examples={"en": "cAke", "sl": "med", "de": "sehen"},
               note="Close-mid front. Slovenian 'e' splits in two — this is the tight one."),
    "ɛ":  dict(coord=(2, 9, 1), costume={"en": "e", "sl": "e (open)", "de": "ä/e"},
               examples={"en": "bEd", "sl": "meh", "de": "Bett"},
               note="Open-mid front. Where 'love' lives in Slovenian: ljubEZen."),
    "æ":  dict(coord=(2, 10, 1), costume={"en": "a", "sl": "-", "de": "-"},
               examples={"en": "cat", "sl": "-", "de": "-"},
               note="English's front-open vowel. 'Cat' lives here and NOWHERE else in Europe."),
    "a":  dict(coord=(3, 10, 1), costume={"en": "-", "sl": "a", "de": "a/aa"},
               examples={"en": "-", "sl": "dan", "de": "Mann"},
               note="Central-open. German and Slovenian share it cleanly."),
    "ə":  dict(coord=(4, 9, 1), costume={"en": "a/e (any)", "sl": "e (weak)", "de": "e"},
               examples={"en": "sofa", "sl": "pes (hurried)", "de": "Liebe"},
               note="The schwa. The vowel that gave up. Every language mutters it."),
    "ʌ":  dict(coord=(5, 9, 1), costume={"en": "u/o/oo", "sl": "-", "de": "-"},
               examples={"en": "lOve", "sl": "-", "de": "-"},
               note="English's strange mid-back-lax vowel. 'Love' lives here. Nobody else has this cell."),
    "ɑ":  dict(coord=(6, 10, 1), costume={"en": "o/a", "sl": "-", "de": "-"},
               examples={"en": "father", "sl": "-", "de": "-"},
               note="Back-open."),
    "ɔ":  dict(coord=(7, 9, 1), costume={"en": "aw/o", "sl": "o (open)", "de": "-"},
               examples={"en": "thought", "sl": "pot", "de": "-"},
               note="Open-mid back. Slovenian 'o' before stops sits here."),
    "o":  dict(coord=(7, 8, 1), costume={"en": "oa/ow", "sl": "o (close)", "de": "o/oo"},
               examples={"en": "boat", "sl": "gora", "de": "Sohn"},
               note="Close-mid back."),
    "ʊ":  dict(coord=(7, 8, 1), costume={"en": "oo/u", "sl": "-", "de": "u"},
               examples={"en": "book", "sl": "-", "de": "Mutter"},
               note="Lax back vowel. Shares a cell with o; laxness is a flag, not an axis."),
    "u":  dict(coord=(8, 8, 1), costume={"en": "oo/ue", "sl": "u", "de": "u"},
               examples={"en": "flute", "sl": "muha", "de": "gut"},
               note="Highest, backest. Where 'ljUbezen' holds its second breath."),
    "y":  dict(coord=(0, 8, 1), costume={"en": "-", "sl": "-", "de": "ü"},
               examples={"en": "-", "sl": "-", "de": "über"},
               note="Same position as i, but the lips are ROUNDED. Rounding is a flag on the cell."),
    "ø":  dict(coord=(1, 9, 1), costume={"en": "-", "sl": "-", "de": "ö"},
               examples={"en": "-", "sl": "-", "de": "schön"},
               note="Same position as e, lips rounded."),
}
# NOTE: where two prisoners share a coord (o/ʊ, i/y, e/ø), the COORD is the
# anatomical truth and the SECONDARY FEATURE (laxness, rounding) is a flag.
# The engine should render flagged prisoners slightly offset on Z, or with
# a glow ring, so no two cubes ever overlap — same law as your spec.

# ---------------------------------------------------------------------------
# MINE NUMBERS (the Minesweeper mechanic, mechanical)
# A covered cube shows: how many OTHER prisoners sit within ONE step of it.
# That number is the "danger": how many truths touch this truth.
# ---------------------------------------------------------------------------

def mine_number(symbol: str) -> int:
    """How many prisoners touch this one — the number on the covered cube."""
    x, y, z = PHONEMES[symbol]["coord"]
    count = 0
    for s, d in PHONEMES.items():
        if s == symbol:
            continue
        dx, dy, dz = d["coord"]
        dist = abs(dx - x) + abs(dy - y) + abs(dz - z) * 3
        if dist <= 2:  # neighbour in the phonetic neighbourhood
            count += 1
    return count


# ---------------------------------------------------------------------------
# CHAINS (words)
# ---------------------------------------------------------------------------

def chain_of(word_phonemes):
    """Return the coordinates for a phoneme sequence — the chain in space."""
    return [PHONEMES[p]["coord"] for p in word_phonemes]


def shared_prisoners(word_a, word_b):
    """Prisoners both words visit. This is what 'sailing' reveals."""
    return sorted(set(word_a) & set(word_b))


# ---------------------------------------------------------------------------
# THE SEED STONE: LOVE ACROSS DIMENSIONS
# ljubezen CONTAINS 'beseda'. Love contains word. That is the whole game.
# ---------------------------------------------------------------------------

LOVE_EQUIVALENTS = {
    "concept": "love",
    "en": dict(text="love",   phonemes=["l", "ʌ", "v"],
               voice="Three prisoners. The middle one exists in no other language."),
    "de": dict(text="Liebe",  phonemes=["l", "i", "b", "ə"],
               voice="Four prisoners. Starts with the SAME first cell as English and Slovenian."),
    "sl": dict(text="ljubezen", phonemes=["ʎ", "u", "b", "e", "z", "ɛ", "n"],
               voice="Seven prisoners. Opens with the cell English cannot even spell."),
    "es": dict(text="amor",   phonemes=["a", "m", "o", "ɾ"],
               voice="Four prisoners. No 'l'. A different door into the same room."),
    "fr": dict(text="amour",  phonemes=["a", "m", "u", "ʁ"],
               voice="Four prisoners. The throat-r German taught the French."),
}

# love (en) x ljubezen (sl): shared prisoners = b, l, z (as cells)
# love (en) x Liebe (de):    shared prisoners = b, l
# THE POINT: three "different words" are chains through overlapping cells.


# ---------------------------------------------------------------------------
# SELF-TEST: run `python phonetic_coordinates.py` — no engine required
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 70)
    print("THE UNIVERSAL SOUND SPACE — {} prisoners".format(len(PHONEMES)))
    print("=" * 70)
    for sym, d in PHONEMES.items():
        c = d["coord"]
        print("[{},{},{}]  {:3s}  en:{:6s}  sl:{:4s}  de:{:6s}  mine:{}".format(
            c[0], c[1], c[2], sym,
            d["costume"]["en"] or "-", d["costume"]["sl"] or "-",
            d["costume"]["de"] or "-", mine_number(sym)))
    print()
    print("THE SEED STONE: love / Liebe / ljubezen")
    for lang, w in LOVE_EQUIVALENTS.items():
        if lang == "concept":
            continue
        coords = [PHONEMES.get(p, PHONEMES.get(p[0], {"coord": None}))["coord"]
                  for p in w["phonemes"]]
        print("  {:9s} {:12s} -> {}".format(w["text"], " ".join(w["phonemes"]), coords))
    print()
    print("SHARED PRISONERS love(en) x ljubezen(sl):",
          shared_prisoners(LOVE_EQUIVALENTS["en"]["phonemes"],
                           LOVE_EQUIVALENTS["sl"]["phonemes"]))
    print("SHARED PRISONERS Liebe(de) x ljubezen(sl):",
          shared_prisoners(LOVE_EQUIVALENTS["de"]["phonemes"],
                           LOVE_EQUIVALENTS["sl"]["phonemes"]))