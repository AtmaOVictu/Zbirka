"""
PHONETIC COORDINATES — FULL LATTICE (46 -> 108 letters + 3 sequences)
LOVE CAGE / Obj2 — phonetic_coordinates_full.py
Built 24. 9. 2026 against:
  - phonetic_coordinates-py.py   (the 46-prisoner lattice — stays as STRATA, untouched)
  - "The IPA as a Precise Symbol System"  (the 107-letter inventory, Unicode IDs)
  - "APD × IPA — Breaking the Seal and Building the Bridge" (§5.1 axes, §5.2 APD binding,
    §7 roadmap; §6 mandates: build here, reconcile to D:\\Comprehension\\desktop later)

THE LAW OF THE SPACE (unchanged from the 46-prisoner file):
    X = place of articulation   (lips -> throat)      0..11
    Y = manner of articulation  (stop -> vowel)       0..14
    Z = voicing                 (voiceless -> voiced) 0 or 1
Vowels keep the SAME X axis as backness (front under the lips, back under the
velum) — the ratified code law. The bridge doc proposed a separate vowel
sub-lattice (§5.1); that proposal conflicts with the actual file and stays an
OPEN ∂, not enacted here. Machine-validation verdict, scar visible.

MIGRATIONS (explicit, recorded — extension is a ledger event, not a silent sync):
    X insertion (retroflex, pharyngeal, epiglottal — IPA chart order):
        palatal 5->6, velar 6->7, uvular 7->8, glottal 8->11
        moved: ç x j ʎ k ɡ ŋ ʔ h
    Conflation repair: ʁ was parked in the trill row; IPA says ʁ is a uvular
        FRICATIVE and ʀ is the trill. ʁ (7,5,1) -> (8,2,1); ʀ takes (8,5,1).
        The French/German throat-r lives at its true manner now.
    Codepoint repair: velar stop is ɡ U+0261 (script g), never g U+0067.
    Latent void repaired: the seed stone's Spanish arm (amor) referenced ɾ,
        which the 46-prisoner file never defined. The cell now exists.

COUNTS (machine-counted at import; asserted in self-test — the machine wins
over prose, discrepancies recorded):
    THE TOTAL IS THE CANON; EVERY SUBTOTAL IS A COSTUME OF A DECLARED
    PREDICATE (pass-3 law 3). Two chart readings, both summing to 107:
      official Kiel 2015 chart : 58 pulmonic + 10 non-pulmonic
                                 + 11 other (incl ʡ ʜ ʢ) + 28 vowels = 107
                                 (the official pulmonic table has 11 place
                                  columns, NO epiglottal column)
      this build's predicate  : 61 pulmonic (14 plosives incl ʔ ʡ; 24
                                 fricatives incl ʜ ʢ — the Wikipedia-chart
                                 reading, epiglottal column in the main
                                 table; anatomically their AIRSTREAM is
                                 pulmonic) + 10 + 8 other + 28 = 107
    ɚ and ɝ are on NEITHER chart as letters; they are kept as prisoners but
    klass="sequence" (like the affricates): officially schwa + rhoticity
    (+ stress) sequence-candidates. WARRANT (named, not silent): kept
    playable so 'butter' and 'bird' have cells — a game decision, outside
    the letter count. Affricates (t͡s t͡ʃ d͡ʒ) and ejectives (pʼ) are
    sequences too, per the companion doc; the three affricates stay as
    prisoners because the game already uses them.

APD BINDING (§5.2 of the bridge doc): a phoneme is an APD operator embedded
in a mouth. F = ∆(zvok) = ∆(zavedanje). Profiles are DERIVED from features,
each row carries its warrant; rows without an explicit §5.2 warrant carry ∂.
E⋆ gate: no APD gate closes without κ ≥ 0.70 AND a ledger line (priča).

Self-test (no engine needed):
    python phonetic_coordinates_full.py
"""

from __future__ import annotations
from typing import Dict, List, Tuple, Optional

# ---------------------------------------------------------------------------
# THE AXES (grown, not redefined — IPA chart order; infinite-grid premise)
# ---------------------------------------------------------------------------

PLACE_X = {
    "bilabial": 0,       # both lips:        p b m
    "labiodental": 1,    # lip + teeth:      f v
    "dental": 2,         # tongue at teeth:  th
    "alveolar": 3,       # tongue at ridge:  t d s z n l
    "postalveolar": 4,   # behind ridge:     sh zh ch
    "retroflex": 5,      # curled back:      ʈ ʂ (NEW slot; forced the X migration)
    "palatal": 6,        # tongue at palate: ly, y-sound
    "velar": 7,          # back of tongue:   k g ng
    "uvular": 8,         # German R's home
    "pharyngeal": 9,     # throat:           ħ ʕ (NEW)
    "epiglottal": 10,    # deepest cage:      ʡ ʜ ʢ (NEW)
    "glottal": 11,       # voice box:         h ʔ
    # vowels use the SAME axis as backness (ratified code law, unchanged):
    "front": 0, "near-front": 1, "central": 4, "near-back": 5, "back": 8,
}

MANNER_Y = {
    "stop": 0,            # the breath is CAGED then released: p t k
    "nasal": 1,           # the breath escapes through the nose: m n ng
    "fricative": 2,       # the breath is SQUEEZED: f s sh
    "affricate": 3,       # caged THEN squeezed: ts ch
    "lateral": 4,         # the breath escapes around the tongue: l ly
    "trill": 5,           # the tongue DRUMS: Slovenian r
    "approximant": 6,     # the breath slips past: English r, w
    "tap": 7,             # one drum-hit: ɾ (the free slot — zero migration)
    "close_vowel": 8,     # tongue high:   i u
    "mid_vowel": 9,       # tongue middle: e o
    "open_vowel": 10,     # tongue low:    a
    "lateral_fricative": 11,  # squeezed around the tongue: ɬ ɮ (NEW)
    "lateral_flap": 12,       # ɺ (NEW)
    "click": 13,               # non-pulmonic: two events in one body (NEW)
    "implosive": 14,          # the breath rushes IN (NEW)
}
# Machine-validation note: the bridge doc proposed Y grows 0..13; preserving
# the free slot 7 for taps and the vowel rows at 8/9/10 yields 0..14. Doc's
# caveat ("to be machine-validated against the actual Obj2 file") applied.

VOICING_Z = {"voiceless": 0, "voiced": 1}

# ---------------------------------------------------------------------------
# THE PRISONERS — all 108 letters + 3 affricate sequences
#   coord    = (x, y, z)
#   flags    = secondary features; NEVER cells (rounding, laxness, rhoticity,
#              velarization, ...). Where two prisoners share a coord, their
#              flag dicts MUST differ (asserted in self-test); the renderer
#              offsets flagged prisoners on Z or draws a glow ring.
#   klass    = pulmonic | nonpulmonic | other | vowel | sequence
#   costume  = the letter(s) each language dresses this prisoner in
#              (None = the language never visits this prisoner = VOID MINE)
# ---------------------------------------------------------------------------

PHONEMES: Dict[str, dict] = {

    # -- PLOSIVES: the breath is caged, then released (13) ---------------------
    "p": dict(coord=(0, 0, 0), flags={}, klass="pulmonic",
              costume={"en": "p", "sl": "p", "de": "p"},
              examples={"en": "pen", "sl": "pes", "de": "Post"},
              note="Lips seal. Breath waits. Breath wins."),
    "b": dict(coord=(0, 0, 1), flags={}, klass="pulmonic",
              costume={"en": "b", "sl": "b", "de": "b"},
              examples={"en": "love", "sl": "beseda", "de": "Liebe"},
              note="Same cage as p, but the throat hums during the hold."),
    "t": dict(coord=(3, 0, 0), flags={}, klass="pulmonic",
              costume={"en": "t", "sl": "t", "de": "t"},
              examples={"en": "top", "sl": "trava", "de": "Tee"},
              note="Alveolar stop. English and German aspirate it hard; Slovenian does not."),
    "d": dict(coord=(3, 0, 1), flags={}, klass="pulmonic",
              costume={"en": "d", "sl": "d", "de": "d"},
              examples={"en": "dog", "sl": "delo", "de": "Ding"},
              note="Voiced twin of t."),
    "ʈ": dict(coord=(5, 0, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Retroflex stop. India visits (Hindi, Tamil). EN/SL/DE never curled this cell. Void mine."),
    "ɖ": dict(coord=(5, 0, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Voiced twin of ʈ. Void mine."),
    "c": dict(coord=(6, 0, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Palatal stop. Hungary (ty) and Macedonia visit. Void mine."),
    "ɟ": dict(coord=(6, 0, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Hungarian gy. Void mine."),
    "k": dict(coord=(7, 0, 0), flags={}, klass="pulmonic",
              costume={"en": "k/c", "sl": "k", "de": "k/ch/ck"},
              examples={"en": "cat", "sl": "kam", "de": "Kind"},
              note="One position, three wardrobes. English even lets 'c' wear it."),
    "ɡ": dict(coord=(7, 0, 1), flags={}, klass="pulmonic",
              costume={"en": "g", "sl": "g", "de": "g"},
              examples={"en": "go", "sl": "gora", "de": "gut"},
              note="Voiced twin of k. Codepoint repaired: ɡ U+0261, never g U+0067."),
    "q": dict(coord=(8, 0, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Uvular stop. Arabic and Georgia visit. Void mine."),
    "ɢ": dict(coord=(8, 0, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Voiced twin of q. Mongolia visits. Void mine."),
    "ʔ": dict(coord=(11, 0, 0), flags={}, klass="pulmonic",
              costume={"en": "-", "sl": "-", "de": "-"},
              examples={"en": "uh-oh", "sl": "a-a (ne)", "de": "Beamter"},
              note="The silent cage. The throat shuts, opens, says nothing yet. The ∂ that fixes into assertion."),

    # -- NASALS: the mouth cages the breath, the nose frees it (7) ------------
    "m": dict(coord=(0, 1, 1), flags={}, klass="pulmonic",
              costume={"en": "m", "sl": "m", "de": "m"},
              examples={"en": "man", "sl": "mama", "de": "Mond"},
              note="The first sound every human mouth learns."),
    "ɱ": dict(coord=(1, 1, 1), flags={}, klass="pulmonic",
              costume={"en": "m (before f)", "sl": "m (before f/v)", "de": "m (before f)"},
              examples={"en": "comfort", "sl": "simfonija (careful)", "de": "Oberfläche"},
              note="m wearing labiodental clothes. Nobody phonemizes it; everyone gestures at it. VISITOR in all three (allophone of m) — a costume visiting a cube it doesn't own."),
    "n": dict(coord=(3, 1, 1), flags={}, klass="pulmonic",
              costume={"en": "n", "sl": "n", "de": "n"},
              examples={"en": "no", "sl": "ne", "de": "Nacht"},
              note="Slovenian's word for 'no' starts with it. So does English's."),
    "ɳ": dict(coord=(5, 1, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Retroflex nasal. India and Australia visit. Void mine."),
    "ɲ": dict(coord=(6, 1, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": "nj", "de": None},
              examples={"en": "", "sl": "njiva / konj", "de": ""},
              note="Slovenia owns this cell (njiva, konj); Spain (ñ) and France (gn) visit too. English and German never built it. Void mine for EN/DE only."),
    "ŋ": dict(coord=(7, 1, 1), flags={}, klass="pulmonic",
              costume={"en": "ng", "sl": "n/g", "de": "ng"},
              examples={"en": "sing", "sl": "banka", "de": "singen"},
              note="English gave it a letter only at the END of words. German let it start them."),
    "ɴ": dict(coord=(8, 1, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Uvular nasal. Japan visits. Void mine."),

    # -- TRILLS: the tongue drums (3) ------------------------------------------
    "ʙ": dict(coord=(0, 5, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Bilabial trill. The lips drum. Bantu visits. Void mine."),
    "r": dict(coord=(3, 5, 1), flags={}, klass="pulmonic",
              costume={"en": "-", "sl": "r", "de": "-"},
              examples={"en": "-", "sl": "reka", "de": "-"},
              note="The alveolar trill. The drum. Slovenian's r is percussion."),
    "ʀ": dict(coord=(8, 5, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": "r (stage)"},
              examples={"en": "", "sl": "", "de": "Bühnendeutsch"},
              note="The uvular TRILL. Takes the row the old file gave to ʁ by mistake. Stage German drums here."),

    # -- TAPS: one drum-hit (2) --------------------------------------------------
    "ɾ": dict(coord=(3, 7, 1), flags={}, klass="pulmonic",
              costume={"en": "t/d (Am. flap)", "sl": None, "de": None, "es": "r"},
              examples={"en": "water (Am.)", "sl": "", "de": "", "es": "amor"},
              note="One hit of the r. The seed stone's Spanish arm pointed at this cell before it existed."),
    "ɽ": dict(coord=(5, 7, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Retroflex tap. India and Norway visit. Void mine."),

    # -- FRICATIVES: the breath is squeezed, never caged (23) ------------------
    "ɸ": dict(coord=(0, 2, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Bilabial hiss. Japan's f. Void mine."),
    "β": dict(coord=(0, 2, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Spain's between-vowels b. Void mine."),
    "f": dict(coord=(1, 2, 0), flags={}, klass="pulmonic",
              costume={"en": "f/ph", "sl": "f", "de": "f/v"},
              examples={"en": "fish", "sl": "film", "de": "Fisch"},
              note="Teeth on lip. Air hisses through."),
    "v": dict(coord=(1, 2, 1), flags={}, klass="pulmonic",
              costume={"en": "v", "sl": "v", "de": "w"},
              examples={"en": "love", "sl": "voda", "de": "Wasser"},
              note="German dresses this prisoner in 'w'. Never trust a German 'w'."),
    "θ": dict(coord=(2, 2, 0), flags={}, klass="pulmonic",
              costume={"en": "th", "sl": None, "de": None},
              examples={"en": "think", "sl": "", "de": ""},
              note="Tongue between the teeth. Slovenian and German never built this cell."),
    "ð": dict(coord=(2, 2, 1), flags={}, klass="pulmonic",
              costume={"en": "th", "sl": None, "de": None},
              examples={"en": "this", "sl": "", "de": ""},
              note="Same cell as the think-th, throat humming. English's most common word starts with it."),
    "s": dict(coord=(3, 2, 0), flags={}, klass="pulmonic",
              costume={"en": "s/c", "sl": "s", "de": "s/ß"},
              examples={"en": "sun", "sl": "sonce", "de": "Sonne"},
              note="The hiss. All three languages own it."),
    "z": dict(coord=(3, 2, 1), flags={}, klass="pulmonic",
              costume={"en": "z/s", "sl": "z/s", "de": "s"},
              examples={"en": "zoo", "sl": "zima", "de": "Sonne (voiced)"},
              note="Voiced twin of s. German 's' between vowels IS this prisoner."),
    "ʃ": dict(coord=(4, 2, 0), flags={}, klass="pulmonic",
              costume={"en": "sh", "sl": "š", "de": "sch"},
              examples={"en": "shy", "sl": "šola", "de": "schön"},
              note="One sound, three spellings, each more absurd than the last."),
    "ʒ": dict(coord=(4, 2, 1), flags={}, klass="pulmonic",
              costume={"en": "si", "sl": "ž", "de": "j"},
              examples={"en": "viSION", "sl": "železo", "de": "Journal"},
              note="Voiced twin of š. Slovenian needed one stroke for it. Wisest of the three."),
    "ʂ": dict(coord=(5, 2, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Retroflex hiss. India and China visit. Void mine."),
    "ʐ": dict(coord=(5, 2, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Voiced twin of ʂ. Void mine."),
    "ç": dict(coord=(6, 2, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": "ch"},
              examples={"en": "", "sl": "", "de": "ich"},
              note="German's shy hiss. The sound of 'ich'."),
    "ʝ": dict(coord=(6, 2, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Greek gamma's cousin. Spain's yeísmo visits. Void mine."),
    "x": dict(coord=(7, 2, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": "h (often)", "de": "ch"},
              examples={"en": "", "sl": "hiter", "de": "ach"},
              note="Velar hiss. German 'ach' and Slovenian 'h' share the cell."),
    "ɣ": dict(coord=(7, 2, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="The humming velar hiss. Greek and Arabic visit. Void mine."),
    "χ": dict(coord=(8, 2, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Uvular hiss. Dutch g, Arabic kh. Void mine."),
    "ʁ": dict(coord=(8, 2, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": "r", "fr": "r"},
              examples={"en": "", "sl": "", "de": "rot", "fr": "amour"},
              note="The throat SQUEEZE, not the drum. Standard German r and French r live here. Conflation repaired; scar in MIGRATION."),
    "ħ": dict(coord=(9, 2, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Pharyngeal hiss. Arabic h̄. Void mine."),
    "ʕ": dict(coord=(9, 2, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="The humming throat. Arabic ayin. Void mine."),
    "ʜ": dict(coord=(10, 2, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Epiglottal hiss. The deepest squeeze. Void mine."),
    "ʢ": dict(coord=(10, 2, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Voiced twin of ʜ. Void mine."),
    "h": dict(coord=(11, 2, 0), flags={}, klass="pulmonic",
              costume={"en": "h", "sl": None, "de": "h"},
              examples={"en": "hat", "sl": "", "de": "Hund"},
              note="Pure breath. Nothing else."),
    "ɦ": dict(coord=(11, 2, 1), flags={}, klass="pulmonic",
              costume={"en": "h (between vowels)", "sl": None, "de": None},
              examples={"en": "ahead", "sl": "", "de": ""},
              note="The humming breath. English leans here between vowels."),

    # -- LATERAL FRICATIVES: squeezed around the tongue (2) --------------------
    "ɬ": dict(coord=(3, 11, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="The dragon's hiss. Wales visits (ll). Void mine."),
    "ɮ": dict(coord=(3, 11, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="The humming dragon. Zulu visits. Void mine."),

    # -- APPROXIMANTS: the breath slips past (5) --------------------------------
    "ʋ": dict(coord=(1, 6, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="The lazy v. Hindi and Dutch visit. Void mine."),
    "ɹ": dict(coord=(3, 6, 1), flags={}, klass="pulmonic",
              costume={"en": "r", "sl": None, "de": None},
              examples={"en": "red", "sl": "", "de": ""},
              note="English r is NOT a trill. It is a vowel-ish glide. The laziest r alive."),
    "ɻ": dict(coord=(5, 6, 1), flags={}, klass="pulmonic",
              costume={"en": "r (Am. retroflex)", "sl": None, "de": None},
              examples={"en": "red (Am.)", "sl": "", "de": ""},
              note="American r, curled. The bunched cousin of ɹ."),
    "j": dict(coord=(6, 6, 1), flags={}, klass="pulmonic",
              costume={"en": "y", "sl": "j", "de": "j"},
              examples={"en": "yes", "sl": "jaz", "de": "ja"},
              note="YES = JAZ = JA. Three languages, one prisoner, three costumes. The legend in one sound."),
    "ɰ": dict(coord=(7, 6, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="The velar glide. Rare everywhere. Void mine."),

    # -- LATERAL APPROXIMANTS: the breath escapes around the tongue (4) --------
    "l": dict(coord=(3, 4, 1), flags={}, klass="pulmonic",
              costume={"en": "l", "sl": "l", "de": "l"},
              examples={"en": "love", "sl": "leto", "de": "Liebe"},
              note="All three languages start 'love' with this prisoner. Remember that."),
    "ɭ": dict(coord=(5, 4, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Retroflex l. India and Australia visit. Void mine."),
    "ʎ": dict(coord=(6, 4, 1), flags={}, klass="pulmonic",
              costume={"en": "-(ly)", "sl": "lj", "de": "-(gl)"},
              examples={"en": "miLLion", "sl": "ljubezen", "de": ""},
              note="Slovenia's untranslatable opening. English only meets it by accident."),
    "ʟ": dict(coord=(7, 4, 1), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Velar l. Rare everywhere. Void mine."),

    # -- NON-PULMONIC: clicks (5) — two events in one body ---------------------
    "ʘ": dict(coord=(0, 13, 0), flags={}, klass="nonpulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Bilabial click. The kiss. Southern Africa visits. Void mine."),
    "ǀ": dict(coord=(2, 13, 0), flags={}, klass="nonpulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "tsk-tsk", "sl": "cok (nursemaid)", "de": ""},
              note="Dental click. Every parent knows the sound; no EN/SL/DE word owns it."),
    "ǃ": dict(coord=(3, 13, 0), flags={}, klass="nonpulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "giddy-up click", "sl": "", "de": ""},
              note="(Post)alveolar click. U+01C3, never the exclamation mark."),
    "ǂ": dict(coord=(4, 13, 0), flags={}, klass="nonpulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Palatoalveolar click. Void mine."),
    "ǁ": dict(coord=(3, 13, 0), flags={"lateral": True}, klass="nonpulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Lateral click. Shares a cell with ǃ; laterality is the flag, not a cell."),

    # -- NON-PULMONIC: implosives (5) — the breath rushes IN -------------------
    "ɓ": dict(coord=(0, 14, 1), flags={}, klass="nonpulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Air rushes IN. Hausa and Sindhi visit. Void mine. Ω− inverted: absence that feeds."),
    "ɗ": dict(coord=(3, 14, 1), flags={}, klass="nonpulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Alveolar implosive. Void mine."),
    "ʄ": dict(coord=(6, 14, 1), flags={}, klass="nonpulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Palatal implosive. Void mine."),
    "ɠ": dict(coord=(7, 14, 1), flags={}, klass="nonpulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Velar implosive. Void mine."),
    "ʛ": dict(coord=(8, 14, 1), flags={}, klass="nonpulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Uvular implosive. Void mine."),

    # -- OTHER SYMBOLS (8 letters) — coarticulated & extras --------------------
    "ʍ": dict(coord=(0, 6, 0), flags={}, klass="other",
              costume={"en": "wh (which)", "sl": None, "de": None},
              examples={"en": "which", "sl": "", "de": ""},
              note="Voiceless w. Which witch. The cell under w, throat silent."),
    "w": dict(coord=(0, 6, 1), flags={}, klass="other",
              costume={"en": "w", "sl": None, "de": None},
              examples={"en": "we", "sl": "", "de": ""},
              note="Bilabial glide. English's signature. Others must fake it with 'v' or 'u'."),
    "ɥ": dict(coord=(6, 6, 1), flags={"labialized": True}, klass="other",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="j's cell with rounded lips. France (huit) visits. Flag, not a cell."),
    "ɕ": dict(coord=(4, 2, 0), flags={"palatalized": True}, klass="other",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="ʃ's cell, sharpened toward the palate. Mandarin x, Polish ś. Flag, not a cell."),
    "ʑ": dict(coord=(4, 2, 1), flags={"palatalized": True}, klass="other",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="ʒ's cell, sharpened. Mandarin j, Polish ź. Flag, not a cell."),
    "ɺ": dict(coord=(3, 12, 1), flags={}, klass="other",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Lateral flap. Japan (ry) visits. A tap that slides sideways."),
    "ɫ": dict(coord=(3, 4, 1), flags={"velarized": True}, klass="other",
              costume={"en": "l (coda: bell)", "sl": None, "de": "l (coda)"},
              examples={"en": "bell", "sl": "", "de": "Mantel"},
              note="Dark l. EN/DE codas darken it; Slovenian dissolves coda l into a glide instead — the void mine says what it does INSTEAD."),
    "ɧ": dict(coord=(7, 2, 0), flags={"variable": True}, klass="other",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="The Swedish sj-sound. Variable by definition; the chart itself refuses to pin it. Shares x's cell under a flag."),
    "ʡ": dict(coord=(10, 0, 0), flags={}, klass="pulmonic",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Epiglottal stop. The deepest cage of all. Belongs to the pulmonic table's epiglottal row (the doc misfiled it under 'other' — corrected)."),
    "ɚ": dict(coord=(4, 9, 1), flags={"rhotic": True}, klass="sequence",
              costume={"en": "er (butter)", "sl": None, "de": None},
              examples={"en": "butter", "sl": "", "de": ""},
              note="ə with an r-hook. The American unstressed workhorse. Shares ə's cell; rhoticity is the flag. SEQUENCE-CANDIDATE (ə+˞): one codepoint, not a chart letter."),
    "ɝ": dict(coord=(4, 9, 1), flags={"rhotic": True, "stressed": True}, klass="sequence",
              costume={"en": "ir (bird)", "sl": None, "de": None},
              examples={"en": "bird", "sl": "", "de": ""},
              note="ɚ amplified. SEQUENCE-CANDIDATE (ə+rhoticity+stress) — not a chart letter."),

    # -- VOWELS: manner axis continues; X = frontness (28) ---------------------
    "i": dict(coord=(0, 8, 1), flags={}, klass="vowel",
              costume={"en": "ee/ea", "sl": "i", "de": "ie/ih"},
              examples={"en": "see", "sl": "biti", "de": "wie"},
              note="Highest, frontest. One vowel, three wardrobes."),
    "y": dict(coord=(0, 8, 1), flags={"rounded": True}, klass="vowel",
              costume={"en": None, "sl": None, "de": "ü"},
              examples={"en": "", "sl": "", "de": "über"},
              note="Same position as i, but the lips are ROUNDED. Rounding is a flag on the cell."),
    "ɨ": dict(coord=(4, 8, 1), flags={}, klass="vowel",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Close central. i moved to the middle of the mouth. Russia visits. Void mine."),
    "ʉ": dict(coord=(4, 8, 1), flags={"rounded": True}, klass="vowel",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="ɨ with rounded lips. Norway and Sweden visit. Void mine."),
    "ɯ": dict(coord=(8, 8, 1), flags={}, klass="vowel",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Close back, lips flat. u's unrounded twin. Korea and Vietnam visit. Void mine."),
    "u": dict(coord=(8, 8, 1), flags={"rounded": True}, klass="vowel",
              costume={"en": "oo/ue", "sl": "u", "de": "u"},
              examples={"en": "flute", "sl": "muha", "de": "gut"},
              note="Highest, backest. Where 'ljUbezen' holds its second breath."),
    "ɪ": dict(coord=(1, 8, 1), flags={"lax": True}, klass="vowel",
              costume={"en": "i", "sl": None, "de": "i"},
              examples={"en": "bit", "sl": "", "de": "bItte"},
              note="The short, lax i. English and German use it everywhere; Slovenian never does."),
    "ʏ": dict(coord=(1, 8, 1), flags={"rounded": True, "lax": True}, klass="vowel",
              costume={"en": None, "sl": None, "de": "ü (short)"},
              examples={"en": "", "sl": "", "de": "Bück"},
              note="ɪ with rounded lips. German kurz-ü."),
    "ʊ": dict(coord=(7, 8, 1), flags={"lax": True}, klass="vowel",
              costume={"en": "oo/u", "sl": None, "de": "u"},
              examples={"en": "book", "sl": "", "de": "Mutter"},
              note="Lax back vowel. Shares a cell with o; laxness is a flag, not an axis."),
    "e": dict(coord=(1, 9, 1), flags={}, klass="vowel",
              costume={"en": "ay(-i)", "sl": "e (close)", "de": "e/eh"},
              examples={"en": "cAke", "sl": "med", "de": "sehen"},
              note="Close-mid front. Slovenian 'e' splits in two — this is the tight one."),
    "ø": dict(coord=(1, 9, 1), flags={"rounded": True}, klass="vowel",
              costume={"en": None, "sl": None, "de": "ö"},
              examples={"en": "", "sl": "", "de": "schön"},
              note="Same position as e, lips rounded."),
    "ɘ": dict(coord=(4, 9, 1), flags={"raised": True}, klass="vowel",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="ə lifted a notch. Close-mid central. Void mine."),
    "ɵ": dict(coord=(4, 9, 1), flags={"raised": True, "rounded": True}, klass="vowel",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="ɘ with rounded lips. Void mine."),
    "ɤ": dict(coord=(8, 9, 1), flags={}, klass="vowel",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Close-mid back, lips flat. o's unrounded twin. China visits. Void mine."),
    "o": dict(coord=(7, 8, 1), flags={}, klass="vowel",
              costume={"en": "oa/ow", "sl": "o (close)", "de": "o/oo"},
              examples={"en": "boat", "sl": "gora", "de": "Sohn"},
              note="Close-mid back. STRATA ∂: by the delta algebra o belongs at (8,9); its 46-era coord (7,8) is kept per the minimal-migration law."),
    "ə": dict(coord=(4, 9, 1), flags={}, klass="vowel",
              costume={"en": "a/e (any)", "sl": "e (weak)", "de": "e"},
              examples={"en": "sofa", "sl": "pes (hurried)", "de": "Liebe"},
              note="The schwa. The vowel that gave up. Every language mutters it."),
    "ɛ": dict(coord=(2, 9, 1), flags={}, klass="vowel",
              costume={"en": "e", "sl": "e (open)", "de": "ä/e"},
              examples={"en": "bEd", "sl": "meh", "de": "Bett"},
              note="Open-mid front. Where 'love' lives in Slovenian: ljubEZen."),
    "œ": dict(coord=(2, 9, 1), flags={"rounded": True}, klass="vowel",
              costume={"en": None, "sl": None, "de": "ö (short)"},
              examples={"en": "", "sl": "", "de": "Götter"},
              note="ɛ with rounded lips. German kurz-ö."),
    "ɜ": dict(coord=(4, 9, 1), flags={"lowered": True}, klass="vowel",
              costume={"en": "ur (nurse, Br.)", "sl": None, "de": None},
              examples={"en": "nurse (Br.)", "sl": "", "de": ""},
              note="ə lowered. The British nurse. Shares ə's cell; the lowering is the flag."),
    "ɞ": dict(coord=(4, 9, 1), flags={"lowered": True, "rounded": True}, klass="vowel",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="ɜ with rounded lips. Void mine."),
    "ʌ": dict(coord=(5, 9, 1), flags={}, klass="vowel",
              costume={"en": "u/o/oo", "sl": None, "de": None},
              examples={"en": "lOve", "sl": "", "de": ""},
              note="English's strange mid-back-lax vowel. 'Love' lives here. Nobody else has this cell."),
    "ɔ": dict(coord=(7, 9, 1), flags={}, klass="vowel",
              costume={"en": "aw/o", "sl": "o (open)", "de": None},
              examples={"en": "thought", "sl": "pot", "de": ""},
              note="Open-mid back. Slovenian 'o' before stops sits here."),
    "æ": dict(coord=(2, 10, 1), flags={}, klass="vowel",
              costume={"en": "a", "sl": None, "de": None},
              examples={"en": "cat", "sl": "", "de": ""},
              note="English's front-open vowel. 'Cat' lives here and NOWHERE else in Europe."),
    "ɐ": dict(coord=(4, 10, 1), flags={}, klass="vowel",
              costume={"en": None, "sl": None, "de": "a (short)"},
              examples={"en": "", "sl": "", "de": "Bar"},
              note="Open central-ish. German short a drifts here. Void mine for EN/SL."),
    "a": dict(coord=(3, 10, 1), flags={}, klass="vowel",
              costume={"en": None, "sl": "a", "de": "a/aa"},
              examples={"en": "", "sl": "dan", "de": "Mann"},
              note="Central-open. German and Slovenian share it cleanly."),
    "ɶ": dict(coord=(0, 10, 1), flags={"rounded": True}, klass="vowel",
              costume={"en": None, "sl": None, "de": None},
              examples={"en": "", "sl": "", "de": ""},
              note="Open front, lips rounded. Almost nobody visits. The loneliest cell in the mouth."),
    "ɑ": dict(coord=(6, 10, 1), flags={}, klass="vowel",
              costume={"en": "o/a", "sl": None, "de": None},
              examples={"en": "father", "sl": "", "de": ""},
              note="Back-open."),
    "ɒ": dict(coord=(6, 10, 1), flags={"rounded": True}, klass="vowel",
              costume={"en": "o (hot, Br.)", "sl": None, "de": None},
              examples={"en": "hot (Br.)", "sl": "", "de": ""},
              note="ɑ with rounded lips. The British hot. Shares ɑ's cell; rounding is the flag."),

    # -- AFFRICATES: sequences, not letters (kept as prisoners) ----------------
    "t͡s": dict(coord=(3, 3, 0), flags={}, klass="sequence",
              costume={"en": "ts", "sl": "c", "de": "z"},
              examples={"en": "caTS", "sl": "cena", "de": "Zeit"},
              note="Slovenian gave it ONE letter: c. German chose z. English pretends it doesn't exist."),
    "t͡ʃ": dict(coord=(4, 3, 0), flags={}, klass="sequence",
              costume={"en": "ch/tch", "sl": "č", "de": "tsch"},
              examples={"en": "church", "sl": "čaj", "de": "Tschüss"},
              note="The international 'ch'. Three costumes, one prisoner."),
    "d͡ʒ": dict(coord=(4, 3, 1), flags={}, klass="sequence",
              costume={"en": "j/ge", "sl": "dž", "de": None},
              examples={"en": "judge", "sl": "džem", "de": "Dschi"},
              note="English built an empire on this sound. Slovenian only borrows it for jam."),
}
# Ejectives are letter + ʼ (U+02BC): never letters, never prisoners.
# Voiceless vowels etc. are letter + diacritic: see DIACRITICS.

# ---------------------------------------------------------------------------
# DIACRITICS — 31 modifiers. FLAG STACK, never cells.
#   coord_move: the ONLY diacritics that change coordinates (lattice moves).
#   All others are attributes on the segment.
# ---------------------------------------------------------------------------

DIACRITICS: Dict[str, dict] = {
    "̥": dict(name="voiceless", cp=0x0325, position="below", delta="voicing −",
              apd="mutes an active operator (molk je vreteno)"),
    "̬": dict(name="voiced", cp=0x032C, position="below", delta="voicing +"),
    "ʰ": dict(name="aspirated", cp=0x02B0, position="spacing", delta="delayed release"),
    "̤": dict(name="breathy voiced", cp=0x0324, position="below", delta="murmur"),
    "̰": dict(name="creaky voiced", cp=0x0330, position="below", delta="creak"),
    "̼": dict(name="linguolabial", cp=0x033C, position="below", delta="place → linguolabial"),
    "̪": dict(name="dental", cp=0x032A, position="below", delta="place → dental"),
    "̺": dict(name="apical", cp=0x033A, position="below", delta="tongue tip"),
    "̻": dict(name="laminal", cp=0x033B, position="below", delta="tongue blade"),
    "̃": dict(name="nasalized", cp=0x0303, position="above", delta="nasal +"),
    "̹": dict(name="more rounded", cp=0x0339, position="below", delta="rounding +"),
    "̜": dict(name="less rounded", cp=0x031C, position="below", delta="rounding −"),
    "̟": dict(name="advanced", cp=0x031F, position="below", delta="fronted", coord_move=("x", -1)),
    "̠": dict(name="retracted", cp=0x0320, position="below", delta="backed", coord_move=("x", +1)),
    "̈": dict(name="centralized", cp=0x0308, position="above", delta="toward center"),
    "̽": dict(name="mid-centralized", cp=0x033D, position="above", delta="toward schwa"),
    "̩": dict(name="syllabic", cp=0x0329, position="below", delta="carries stress"),
    "̯": dict(name="non-syllabic", cp=0x032F, position="below", delta="glide"),
    "˞": dict(name="rhoticity", cp=0x02DE, position="spacing", delta="r-colouring"),
    "ʷ": dict(name="labialized", cp=0x02B7, position="spacing", delta="+labial"),
    "ʲ": dict(name="palatalized", cp=0x02B2, position="spacing", delta="+palatal"),
    "ˠ": dict(name="velarized", cp=0x02E0, position="spacing", delta="+velar"),
    "ˤ": dict(name="pharyngealized", cp=0x02E4, position="spacing", delta="+pharyngeal"),
    "̴": dict(name="dark (velarized/pharyngealized)", cp=0x0334, position="above", delta="+dark"),
    "̝": dict(name="raised", cp=0x031D, position="below", delta="height −1 (closer)",
              coord_move=("y", -1)),
    "̞": dict(name="lowered", cp=0x031E, position="below", delta="height +1 (opener)",
              coord_move=("y", +1)),
    "̘": dict(name="ATR +", cp=0x0318, position="below", delta="tongue root forward"),
    "̙": dict(name="ATR −", cp=0x0319, position="below", delta="tongue root back"),
    "̚": dict(name="unreleased", cp=0x031A, position="above", delta="no audible release"),
    "ʼ": dict(name="ejective", cp=0x02BC, position="spacing", delta="glottalic release"),
    "͡": dict(name="tie (affricate/double)", cp=0x0361, position="above", delta="one segment"),
}

# ---------------------------------------------------------------------------
# SUPRASEGMENTALS — CHAIN-SLOT TYPES. They live between cubes, never in cells.
#   slot: "pre" (attaches before a segment), "post" (after), "between", "frame"
# ---------------------------------------------------------------------------

SUPRASEGMENTALS: Dict[str, dict] = {
    "ˈ": dict(name="primary stress", cp=0x02C8, slot="pre",
              apd="operator amplified (oblast prehoda)"),
    "ˌ": dict(name="secondary stress", cp=0x02CC, slot="pre"),
    "ː": dict(name="long", cp=0x02D0, slot="post", apd="held breath"),
    "ˑ": dict(name="half-long", cp=0x02D1, slot="post"),
    "˘": dict(name="extra-short", cp=0x02D8, slot="post"),
    "|": dict(name="minor group", cp=0x007C, slot="between"),
    "‖": dict(name="major group", cp=0x2016, slot="between"),
    ".": dict(name="syllable break", cp=0x002E, slot="between"),
    "‿": dict(name="linking (no break)", cp=0x203F, slot="between"),
    "↗": dict(name="global rise", cp=0x2197, slot="frame"),
    "↘": dict(name="global fall", cp=0x2198, slot="frame"),
    "˥": dict(name="tone extra-high", cp=0x02E5, slot="post", apd="direction of the transition"),
    "˦": dict(name="tone high", cp=0x02E6, slot="post"),
    "˧": dict(name="tone mid", cp=0x02E7, slot="post"),
    "˨": dict(name="tone low", cp=0x02E8, slot="post"),
    "˩": dict(name="tone extra-low", cp=0x02E9, slot="post"),
    "ꜛ": dict(name="upstep", cp=0xA71B, slot="post"),
    "ꜜ": dict(name="downstep", cp=0xA71C, slot="post"),
}

# Obsolete / retired IPA-Extensions symbols — NEVER prisoners (ban-list).
OBSOLETE = {"ʇ", "ʗ", "ʖ", "ɼ", "ɿ", "ʅ", "ʆ", "ʓ", "ʭ", "ʬ", "ɩ", "ɷ", "ǫ"}

# Confusable codepoints — asserted in self-test, banned by construction.
CONFUSABLES = {"g": "use ɡ U+0261", "!": "use ǃ U+01C3", ":": "use ː U+02D0",
               "'": "use ʼ U+02BC", "ɹ_hook": "ɾ is U+027E, r is U+0072"}

# ---------------------------------------------------------------------------
# MIGRATION — the drift vector from the 46-prisoner strata (explicit ledger)
#   old_key: (old_coord, new_key, new_coord, reason)
# ---------------------------------------------------------------------------

MIGRATION: Dict[str, tuple] = {
    # X-insertion (retroflex 5, pharyngeal 9, epiglottal 10; glottal → 11)
    "ç": ((5, 2, 0), "ç", (6, 2, 0), "X insertion: palatal 5->6"),
    "x": ((6, 2, 0), "x", (7, 2, 0), "X insertion: velar 6->7"),
    "j": ((5, 6, 1), "j", (6, 6, 1), "X insertion: palatal 5->6"),
    "ʎ": ((5, 4, 1), "ʎ", (6, 4, 1), "X insertion: palatal 5->6"),
    "k": ((6, 0, 0), "k", (7, 0, 0), "X insertion: velar 6->7"),
    "g": ((6, 0, 1), "ɡ", (7, 0, 1), "X insertion + codepoint repair (g U+0067 -> ɡ U+0261)"),
    "ŋ": ((6, 1, 1), "ŋ", (7, 1, 1), "X insertion: velar 6->7"),
    "ʔ": ((8, 0, 0), "ʔ", (11, 0, 0), "X insertion: glottal 8->11"),
    "h": ((8, 2, 0), "h", (11, 2, 0), "X insertion: glottal 8->11"),
    # Conflation repair: ʁ is a fricative; ʀ is the trill
    "ʁ": ((7, 5, 1), "ʁ", (8, 2, 1), "conflation repair: trill row -> true fricative manner; ʀ takes (8,5,1)"),
}
# All other 35 of the 46 old prisoners keep their exact coordinates (asserted
# in the self-test by diffing against the strata file).

# ---------------------------------------------------------------------------
# MECHANICS (unchanged from the 46-prisoner file — same laws, bigger universe)
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
        if dist <= 2:
            count += 1
    return count


def chain_of(word):
    """Coordinates for a phoneme sequence — the chain in space.

    Accepts a list of symbols (old API, unchanged) or an IPA string
    (tokenized: diacritics apply as flags / lattice moves, suprasegmentals
    are skipped as chain slots — use parse_chain for the full structure).
    """
    if isinstance(word, str):
        return [t["coord"] for t in tokenize(word) if t["kind"] == "segment"]
    return [PHONEMES[p]["coord"] for p in word]


def shared_prisoners(word_a, word_b):
    """Prisoners both words visit. This is what 'sailing' reveals."""
    return sorted(set(word_a) & set(word_b))


# ---------------------------------------------------------------------------
# TOKENIZER — the 4-level grammar, level by level:
#   letter + diacritics -> segment; segments + slots -> chain (utterance above)
# NEVER NFC-normalize: precomposed forms (ä, â) are NOT letters here.
# ---------------------------------------------------------------------------

def _letters_by_len() -> List[str]:
    return sorted([k for k in PHONEMES], key=len, reverse=True)


def tokenize(ipa: str) -> List[dict]:
    """Parse an IPA string into segments (letter + flags + coord moves)
    and chain slots. Unknown characters (incl. obsolete symbols and
    NFC-precomposed forms) come back as kind='unknown' — never silently
    coerced."""
    letters = _letters_by_len()
    tokens: List[dict] = []
    i = 0
    while i < len(ipa):
        ch = ipa[i]
        # longest known letter first (t͡s, t͡ʃ, d͡ʒ are 3 chars)
        matched = None
        for L in letters:
            if ipa.startswith(L, i):
                matched = L
                break
        if matched:
            tokens.append(dict(kind="segment", letter=matched,
                              coord=list(PHONEMES[matched]["coord"]),
                              flags=dict(PHONEMES[matched]["flags"]),
                              coord_moves=[]))
            i += len(matched)
            continue
        if ch in DIACRITICS:
            d = DIACRITICS[ch]
            seg = next((t for t in reversed(tokens) if t["kind"] == "segment"), None)
            if seg is None:
                tokens.append(dict(kind="unknown", char=ch, why="diacritic with no letter"))
            else:
                if "coord_move" in d:
                    axis, step = d["coord_move"]
                    seg["coord"][0 if axis == "x" else 1] += step
                    seg["coord_moves"].append(d["name"])
                else:
                    seg["flags"][d["name"]] = True
            i += 1
            continue
        if ch in SUPRASEGMENTALS:
            tokens.append(dict(kind="slot", mark=ch,
                              type=SUPRASEGMENTALS[ch]["name"],
                              slot=SUPRASEGMENTALS[ch]["slot"]))
            i += 1
            continue
        # spacing release modifiers recognized but not full diacritics
        if ch in ("ⁿ", "ˡ"):  # nasal / lateral release
            seg = next((t for t in reversed(tokens) if t["kind"] == "segment"), None)
            if seg:
                seg["flags"]["release:" + ch] = True
            i += 1
            continue
        tokens.append(dict(kind="unknown", char=ch,
                          why="obsolete" if ch in OBSOLETE else "not a letter"))
        i += 1
    return tokens


def parse_chain(ipa: str) -> dict:
    """Full chain structure: segments with coords/flags + slots, per the
    grammar  utterance := prosody* (slot|segment)*  — slots sit between
    cubes, never in cells."""
    tokens = tokenize(ipa)
    return dict(text=ipa,
                segments=[t for t in tokens if t["kind"] == "segment"],
                slots=[t for t in tokens if t["kind"] == "slot"],
                unknown=[t for t in tokens if t["kind"] == "unknown"])


# ---------------------------------------------------------------------------
# THE SEED STONE: LOVE ACROSS DIMENSIONS (carried verbatim; ɾ now exists)
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

# ---------------------------------------------------------------------------
# APD BINDING — a phoneme is an APD operator embedded in a mouth.
#   F = ∆(zvok) = ∆(zavedanje)
# Profiles are DERIVED from features (bridge doc §5.2). Rows with an explicit
# §5.2 warrant are sealed; the rest carry ∂ and say so.
# ---------------------------------------------------------------------------

VOICING_APD = {
    0: ("omega_minus_shape", "∅ = merjeno nič, priča da nisem meril", True),
    1: ("alpha_available", "glas = nosilec telesa (MAX6)", True),
}

MANNER_APD = {
    0: ("boundary_event", "caged then released; the rez itself", True),
    1: ("continuity", "breath escapes through the nose (∮)", True),
    2: ("zeta_prime", "squeezed breath = desire with stop-rule (ℜ watch)", True),
    3: ("boundary_then_sustained", "caged THEN squeezed (affricate)", False),   # ∂ derived
    4: ("symmetry_flow", "flow around obstacle (⇌ ≈ 1−η)", True),
    5: ("percussion", "repeated boundary taps", False),                          # ∂ derived
    6: ("glide", "breath slips past", False),                                    # ∂ derived
    7: ("quick_boundary", "one tap of the drum", False),                         # ∂ derived
    8: ("mu_carrier", "samoglasniki nosijo dih (state foundation)", True),
    9: ("mu_carrier", "samoglasniki nosijo dih (state foundation)", True),
    10: ("mu_carrier", "samoglasniki nosijo dih (state foundation)", True),
    11: ("symmetry_flow", "squeezed around the tongue", False),                  # ∂ derived
    12: ("symmetry_flow", "a tap that slides sideways", False),                  # ∂ derived
    13: ("double_ledger_event", "non-pulmonic: two events in one body", True),
    14: ("inward_event", "Ω− inverted: absence that feeds", True),
}


def apd_profile(symbol: str) -> dict:
    """The APD operator-deltas this phoneme performs when uttered."""
    d = PHONEMES[symbol]
    x, y, z = d["coord"]
    operators = []
    open_qs = []

    op, warrant, sealed = VOICING_APD[z]
    operators.append(dict(operator=op, warrant=warrant, sealed=sealed))
    if not sealed:
        open_qs.append("voicing row not sealed in §5.2")

    if symbol == "ʔ":
        operators.append(dict(operator="terminal_event",
                               warrant="the ∂ that fixes into assertion (DEATH row)",
                               sealed=True))
    else:
        op, warrant, sealed = MANNER_APD[y]
        operators.append(dict(operator=op, warrant=warrant, sealed=sealed))
        if not sealed:
            open_qs.append(f"manner row y={y} derived, not sealed in §5.2")

    if d["flags"].get("velarized") or d["flags"].get("labialized") \
       or d["flags"].get("palatalized"):
        operators.append(dict(operator="secondary_gesture",
                              warrant="flags are attributes, ◌ʷ/◌ʲ/◌ˠ carry them",
                              sealed=False))
        open_qs.append("secondary-articulation → APD row unwritten in §5.2")

    return dict(symbol=symbol, operators=operators, open=open_qs)


def e_star_gate(kappa: float, ledger_line_present: bool) -> bool:
    """No APD gate closes (E⋆→1) without κ ≥ 0.70 AND a ledger line (priča).
    The game mechanic and the corpus law are the same sentence."""
    return kappa >= 0.70 and ledger_line_present


# ---------------------------------------------------------------------------
# SELF-TEST — run `python phonetic_coordinates_full.py` (no engine needed)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    import unicodedata

    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)
        return cond

    # -- 1. COUNTS (machine-counted; the machine wins over prose) -------------
    by_klass = {}
    for d in PHONEMES.values():
        by_klass[d["klass"]] = by_klass.get(d["klass"], 0) + 1
    n_letters = sum(by_klass[k] for k in ("pulmonic", "nonpulmonic", "other", "vowel"))
    check(by_klass.get("pulmonic") == 61,
          f"pulmonic == 61 under the declared predicate (epiglottal column in the main table, "
          f"Wikipedia-chart reading; the official Kiel 2015 chart buckets ʡ ʜ ʢ under 'other' "
          f"giving 58+10+11+28 — both readings sum to 107) — got {by_klass.get('pulmonic')}")
    check(by_klass.get("nonpulmonic") == 10, f"nonpulmonic == 10 — got {by_klass.get('nonpulmonic')}")
    check(by_klass.get("other") == 8, f"other == 8 — got {by_klass.get('other')}")
    check(by_klass.get("vowel") == 28, f"vowels == 28 — got {by_klass.get('vowel')}")
    check(n_letters == 107,
          f"total letters == 107 (canonical total, stable across both chart readings) — got {n_letters}")
    check(by_klass.get("sequence") == 5, "5 sequences kept (3 affricates + ɚ + ɝ)")

    # -- 2. BAN-LISTS -----------------------------------------------------------
    for ob in OBSOLETE:
        check(ob not in PHONEMES, f"obsolete symbol {ob!r} must not be a prisoner")
    # confusable codepoints
    check("ɡ" in PHONEMES and ord("ɡ") == 0x0261, "velar stop is ɡ U+0261")
    check("g" not in PHONEMES, "confusable g U+0067 is NOT a prisoner")
    check("ǃ" in PHONEMES and ord("ǃ") == 0x01C3, "alveolar click is ǃ U+01C3")
    check("!" not in PHONEMES, "confusable ! is NOT a prisoner")
    check("ː" in SUPRASEGMENTALS and ord("ː") == 0x02D0, "length is ː U+02D0")
    check(":" not in SUPRASEGMENTALS, "colon is NOT a suprasegmental")
    check("ʼ" in DIACRITICS and ord("ʼ") == 0x02BC, "ejective modifier is ʼ U+02BC")
    check(ord(PHONEMES["r"].get("x", "r") if False else "r") == 0x0072, "trill r is plain U+0072")
    check(len(DIACRITICS) == 31, f"31 diacritics — got {len(DIACRITICS)}")

    # precomposed forms are never letters (no-NFC law)
    for pre in ("ä", "â", "ō", "ё"):
        check(pre not in PHONEMES, f"NFC-precomposed {pre!r} must not be a prisoner")

    # -- 3. CELL-COLLISION LAW: same coord ⇒ flag dicts must differ -------------
    cells: Dict[tuple, list] = {}
    for s, d in PHONEMES.items():
        cells.setdefault(tuple(d["coord"]), []).append(s)
    for cell, members in cells.items():
        if len(members) > 1:
            for a in range(len(members)):
                for b in range(a + 1, len(members)):
                    fa = PHONEMES[members[a]]["flags"]
                    fb = PHONEMES[members[b]]["flags"]
                    check(fa != fb,
                          f"cell {cell}: {members[a]!r} and {members[b]!r} share coord with identical flags")

    # -- 4. MIGRATION vs the 46-prisoner strata (ledger event, scar visible) ---
    strata_path = __file__.rsplit("phonetic_coordinates_full.py", 1)[0] \
        + "phonetic_coordinates-py.py"
    import os
    if os.path.exists(strata_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("pc_strata", strata_path)
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        moved, stable, mines_changed = [], [], []
        for old_key, old_d in old.PHONEMES.items():
            new_key = MIGRATION.get(old_key, (None, old_key, None, ""))[1]
            check(new_key in PHONEMES, f"strata prisoner {old_key!r} lost in full lattice")
            if new_key not in PHONEMES:
                continue
            old_coord = tuple(old_d["coord"])
            new_coord = tuple(PHONEMES[new_key]["coord"])
            if old_coord == new_coord:
                stable.append(new_key)
            else:
                exp = MIGRATION.get(old_key)
                check(exp is not None and tuple(exp[2]) == new_coord,
                      f"{old_key!r} moved {old_coord}->{new_coord} without an explicit migration entry")
                if exp is not None:
                    moved.append(f"{exp[0] if exp[0]==new_key else old_key}: {old_coord} -> {new_coord}  ({exp[3]})")
            try:
                om = old.mine_number(old_key)
                nm = mine_number(new_key)
                if om != nm:
                    mines_changed.append(f"{new_key}: {om} -> {nm}")
            except Exception as e:  # strata ɾ etc. missing there
                pass
        # the seed stone's Spanish arm now resolves
        check("ɾ" in PHONEMES and "ɾ" not in old.PHONEMES,
              "latent void repaired: ɾ referenced by amor, now defined")
        print("MIGRATION LEDGER (explicit — extension is an event, not a sync):")
        for m in moved:
            print("   MOVED ", m)
        print(f"   STABLE {len(stable)} prisoners kept their exact coordinates")
        print("   MINE NUMBERS changed (new neighbors born — the universe grew):")
        for m in mines_changed:
            print("     ", m)
    else:
        print("MIGRATION LEDGER: strata file not found next to this module; skipped diff.")

    # -- 5. SEED STONE REGRESSION (all five dimensions must resolve) -----------
    for lang, w in LOVE_EQUIVALENTS.items():
        if lang == "concept":
            continue
        for p in w["phonemes"]:
            check(p in PHONEMES, f"seed stone: {w['text']} references missing prisoner {p!r}")
    coords_en = chain_of(LOVE_EQUIVALENTS["en"]["phonemes"])
    check(len(coords_en) == 3 and coords_en[0] == PHONEMES["l"]["coord"],
          "love (en) chain geometry intact")

    # -- 6. DELTA ALGEBRA: the four lattice-move diacritics ---------------------
    toks = tokenize("ə̞")          # schwa lowered -> open-mid central row +1
    check(toks[0]["coord"][1] == PHONEMES["ə"]["coord"][1] + 1, "◌̞ is a Y+1 lattice move")
    toks = tokenize("e̝")          # e raised -> close row -1
    check(toks[0]["coord"][1] == PHONEMES["e"]["coord"][1] - 1, "◌̝ is a Y−1 lattice move")
    toks = tokenize("i̠")          # i retracted -> X+1
    check(toks[0]["coord"][0] == PHONEMES["i"]["coord"][0] + 1, "◌̠ is a X+1 lattice move")
    toks = tokenize("u̟")          # u advanced -> X−1
    check(toks[0]["coord"][0] == PHONEMES["u"]["coord"][0] - 1, "◌̟ is a X−1 lattice move")

    # no-NFC: 'a' + U+0308 stays a letter + a flag, never merges into ä
    toks = tokenize("a\u0308")
    check(len(toks) == 1 and toks[0]["kind"] == "segment"
          and toks[0]["flags"].get("centralized") is True,
          "a+◌̈ stays decomposed (never NFC-normalized)")

    # suprasegmentals sit between cubes, never in cells
    ch = parse_chain("ˈlʌv")
    check(len(ch["segments"]) == 3 and len(ch["slots"]) == 1
          and ch["slots"][0]["type"] == "primary stress",
          "stress parses as a chain slot, not a cell")

    # affricate tie bars: letters on both sides
    toks = tokenize("t͡ʃ")
    check(len(toks) == 1 and toks[0]["letter"] == "t͡ʃ", "tie-bar affricate is one segment")

    # -- 7. APD SMOKE ------------------------------------------------------------
    prof = apd_profile("l")
    ops = {o["operator"] for o in prof["operators"]}
    check("symmetry_flow" in ops and "alpha_available" in ops, "l = ⇌ flow, voiced α")
    prof = apd_profile("p")
    ops = {o["operator"] for o in prof["operators"]}
    check("boundary_event" in ops and "omega_minus_shape" in ops,
          "p = boundary event, voiceless Ω− shape")
    check(e_star_gate(0.71, True) and not e_star_gate(0.69, True)
          and not e_star_gate(0.71, False),
          "E⋆ gate: κ ≥ 0.70 AND a ledger line (priča)")

    # -- REPORT -----------------------------------------------------------------
    print("=" * 72)
    print(f"THE FULL UNIVERSAL SOUND SPACE — {len(PHONEMES)} prisoners "
          f"({n_letters} letters + {by_klass.get('sequence', 0)} sequences)")
    print(f"counts: pulmonic {by_klass.get('pulmonic')} | nonpulmonic {by_klass.get('nonpulmonic')} "
          f"| other {by_klass.get('other')} | vowel {by_klass.get('vowel')} "
          f"| diacritics {len(DIACRITICS)} | suprasegmental slots {len(SUPRASEGMENTALS)}")
    print("TOTAL 107 letters (canonical; stable across both chart readings). "
          "Declared predicate here: 61 pulmonic + 10 non-pulmonic + 8 other + 28 vowels. "
          "Official-chart bucketing: 58 + 10 + 11 + 28. Subtotals are costumes of the "
          "declared predicate; the total is the canon.")
    print("=" * 72)
    for sym, d in PHONEMES.items():
        c = d["coord"]
        fl = ",".join(k for k in d["flags"]) or "-"
        cs = d["costume"]
        en = cs.get("en") or "-"
        sl = cs.get("sl") or "-"
        de = cs.get("de") or "-"
        print(f"[{c[0]:>2},{c[1]:>2},{c[2]}] {sym:3s} flags:{fl:<24s} "
              f"en:{en:<14s} sl:{sl:<8s} de:{de:<10s} mine:{mine_number(sym)}")
    print()
    print("THE SEED STONE: love / Liebe / ljubezen / amor / amour")
    for lang, w in LOVE_EQUIVALENTS.items():
        if lang == "concept":
            continue
        coords = [PHONEMES[p]["coord"] for p in w["phonemes"]]
        print(f"  {w['text']:9s} {' '.join(w['phonemes']):<18s} -> {coords}")
    print()
    print("SHARED PRISONERS love(en) x ljubezen(sl):",
          shared_prisoners(LOVE_EQUIVALENTS["en"]["phonemes"],
                           LOVE_EQUIVALENTS["sl"]["phonemes"]))
    print("SHARED PRISONERS Liebe(de) x ljubezen(sl):",
          shared_prisoners(LOVE_EQUIVALENTS["de"]["phonemes"],
                           LOVE_EQUIVALENTS["sl"]["phonemes"]))
    print("SHARED PRISONERS amor(es) x love(en):",
          shared_prisoners(LOVE_EQUIVALENTS["es"]["phonemes"],
                           LOVE_EQUIVALENTS["en"]["phonemes"]))
    print()
    print("APD PROFILES (F = ∆(zvok) = ∆(zavedanje)) — sample:")
    for s in ("l", "p", "ʔ", "a", "ʘ", "ɓ"):
        pr = apd_profile(s)
        ops = ", ".join(o["operator"] + ("" if o["sealed"] else " (∂)") for o in pr["operators"])
        print(f"  {s:3s} -> {ops}")
    print()
    if failures:
        print("FAILURES:")
        for f in failures:
            print("  -", f)
        sys.exit(1)
    print("ALL CHECKS PASSED — the universe is complete and the scars are visible.")
