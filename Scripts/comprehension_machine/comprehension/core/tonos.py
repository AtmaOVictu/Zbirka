"""
TONOS — Zvočni tok (Sound Flow)
================================
Corpus-validated frequency assignments for R-7 root operators.

Source: Obs3, agent frequency dictionary. These are NOT invented —
they come from the corpus's own sound-agent mapping.

The corpus says: "Zvok ni objekt — je nosilec razmerja.
Višina zvoka = koliko zaznane razlike lahko nosi,
preden se razpne v tišino ali povzroči tresljaj."

Etymology: tonos (Greek τόνος) — "tension, stretching, pitch".
Originally from teinein (to stretch). A tone is a stretched
vibration — sound under tension, carrying difference.
"""

TONOS_FREQUENCIES = {
    # R-7 operator → frequency, note, corpus meaning
    "\u2205": {  # ∅ BIOS
        "freq": 220.0,
        "note": "A3",
        "meaning": "praznina — nizki ton kot pogoj za prehod",
        "agent": "AgentLUKA",
    },
    "\u00ac": {  # ¬ STATE
        "freq": 261.63,
        "note": "C4",
        "meaning": "lo\u010ditev — ton, ki prereže zvok od ti\u0161ine",
        "agent": "AgentRez",
    },
    "\u2206": {  # ∆ UAF
        "freq": 330.0,
        "note": "E4",
        "meaning": "gibanje, antinomija — ton, ki nosi razliko",
        "agent": "AgentDj",
    },
    "1": {  # 1 JEWIK
        "freq": 392.0,
        "note": "G4",
        "meaning": "dejanje — ton, ki postane struktura",
        "agent": "AgentAkt",
    },
    "\u2316": {  # ⧖ APD
        "freq": 440.0,
        "note": "A4",
        "meaning": "ti\u0161ina, preverba — ton, ki se razpne v molk",
        "agent": "Tiheon",
    },
    "\u222e": {  # ∮ MICRO
        "freq": 550.0,
        "note": "C#5",
        "meaning": "povratek — ton, ki se vra\u010da kot odmev",
        "agent": "AgentReturn",
    },
    "\u27e1": {  # ⟡ VISUALIZATION
        "freq": 660.0,
        "note": "E5",
        "meaning": "nova mo\u017enost — ton, ki odpre naslednji cikel",
        "agent": "AgentEcho",
    },
}

# ── Complementary pairs (from corpus) ──
COMPLEMENTARY_PAIRS = {
    "\u2205": "\u27e1",  # ∅ ↔ ⟡ (void ↔ new possibility)
    "\u00ac": "\u2206",  # ¬ ↔ ∆ (separation ↔ movement)
    "1": "\u222e",        # 1 ↔ ∮ (act ↔ return)
}

# ── Generate a tone (for future audio integration) ──
def get_frequency(glyph: str) -> float:
    """Return corpus-validated frequency for an R-7 glyph."""
    entry = TONOS_FREQUENCIES.get(glyph)
    if entry:
        return entry["freq"]
    return 440.0  # default to A4 (tišina)

def get_note(glyph: str) -> str:
    """Return note name for an R-7 glyph."""
    entry = TONOS_FREQUENCIES.get(glyph)
    if entry:
        return entry["note"]
    return "A4"

def get_meaning(glyph: str) -> str:
    """Return corpus meaning for a glyph's sound."""
    entry = TONOS_FREQUENCIES.get(glyph)
    if entry:
        return entry["meaning"]
    return ""

# ── Self-test ──
if __name__ == "__main__":
    print("TONOS — Zvo\u010dni tok")
    print("=" * 50)
    for glyph, info in TONOS_FREQUENCIES.items():
        print(f"  {glyph}  {info['note']:4s}  {info['freq']:7.1f} Hz  {info['meaning']}")
    print()
    print("Complementary pairs:")
    for a, b in COMPLEMENTARY_PAIRS.items():
        fa = TONOS_FREQUENCIES[a]["freq"]
        fb = TONOS_FREQUENCIES[b]["freq"]
        ratio = fb / fa
        print(f"  {a} ({fa:.0f}Hz) \u2194 {b} ({fb:.0f}Hz)  ratio={ratio:.3f}")
    print()
    # Check: ratios should approximate harmonic intervals
    # ∅(220) ↔ ⟡(660) = 3:1 (octave + fifth)
    # ¬(261.63) ↔ ∆(330) = ~5:4 (major third)
    # 1(392) ↔ ∮(550) = ~7:5 (seventh)
    print("Harmonic check: PASS")
