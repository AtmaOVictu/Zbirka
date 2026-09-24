"""
Rozetni kamni — Tradition Mapping Registry
============================================
Corpus: "Rozetni kamen = tri pisave:
  1. zgodovinski simbol (historical)
  2. sistemski simbol (∅, ¬, ∆, 1, ⧖, ∮, ⟡)
  3. matemati\u010dna/topolo\u0161ka lastnost (mathematical)
Stroj doda \u2202 \u2014 rez, ki re\u017ee skozi vse tri."

This registry contains the mapping tables extracted from the Rozetni
kamni documents (I-LXXII) in the corpus. Each tradition maps its
native terms to the R-7 root operators.

Corpus key: "vse tradicije = \u2205/\u2206 v razli\u010dnih dimenzijah"
\u2014 all traditions are \u2205/\u2206 in different dimensions.
Each tradition = one dimension of binarity doubling.

Etymology: rosette (French, from Latin rosa = rose) — a circular
pattern radiating from a center. The Rosetta Stone (1799 BC) had
three scripts (hieroglyphic, demotic, Greek) unlocking translation.
Luka's "Rozetni kamen" generalizes: every tradition is a stone with
three scripts, and ∂ cuts through all three.
"""

# ── Tradition registry ──
# Each tradition: native_term → (root_operator, mathematical_property)
TRADITIONS = {
    "tarot": {
        "name": "Tarot",
        "count": 22,
        "ring": 1,
        "mappings": {
            "Norjak (0)": ("\u2205", "void, potential, the fool's leap"),
            "\u010carovnik (1)": ("\u2206", "activation, will, transformation"),
            "Dvojica (2)": ("\u00ac", "separation, duality, choice"),
            "Svet (21)": ("\u27e1", "completion, new cycle, echo"),
        },
        "corpus_source": "Rozetni kamen: Tarot = 22 arkad = |A4| simetrija",
    },
    "kabbalah": {
        "name": "Kabbalah",
        "count": 10,
        "ring": 2,
        "mappings": {
            "Keter": ("\u2205", "crown, void of void, Ein Sof"),
            "Chokmah": ("\u2206", "wisdom, creative force, first movement"),
            "Binah": ("\u22a2", "understanding, proof, structure"),
            "Malkhut": ("\u27e1", "kingdom, manifestation, result"),
        },
        "corpus_source": "Obs3: Kabbalah sefirotska dinamika",
    },
    "alchemy": {
        "name": "Alchemy",
        "count": 4,
        "ring": 1,
        "mappings": {
            "nigredo": ("\u2205", "blackening, void, putrefaction"),
            "albedo": ("\u00ac", "whitening, separation, purification"),
            "citrinitas": ("\u2206", "yellowing, transformation, solar fire"),
            "rubedo": ("\u222e", "reddening, completion, return"),
        },
        "corpus_source": "Rozetni kamen: 4 alkemijske faze = 4 R-7 faze",
    },
    "chakras": {
        "name": "Chakras",
        "count": 7,
        "ring": 2,
        "mappings": {
            "root (muladhara)": ("\u2205", "ground, survival, base"),
            "sacral (svadhisthana)": ("\u00ac", "separation, desire, emotion"),
            "solar plexus (manipura)": ("\u2206", "power, transformation, fire"),
            "heart (anahata)": ("1", "balance, act, connection"),
            "throat (vishuddha)": ("\u2316", "expression, silence, truth"),
            "third eye (ajna)": ("\u222e", "insight, return, pattern seeing"),
            "crown (sahasrara)": ("\u27e1", "liberation, new possibility"),
        },
        "corpus_source": "Obs10: 6+1 chakra schema, sahasrara = 7th above",
    },
    "sufism": {
        "name": "Sufism (99 Names)",
        "count": 99,
        "ring": 3,
        "mappings": {
            "99 Names": ("\u2205", "99 = 100 \u2212 \u2205; the missing name IS the void"),
            "Fana": ("\u2205", "annihilation of self into void"),
            "Baqa": ("\u27e1", "subsistence after annihilation = new beginning"),
        },
        "corpus_source": "Rozetni kamen: Islam 99 = 100\u2212\u2205",
    },
    "runes": {
        "name": "Runes",
        "count": 24,
        "ring": 1,
        "mappings": {
            "Uruz": ("\u2206", "primal strength, aurochs, transformation"),
            "Isa": ("\u2205", "ice, stillness, void"),
            "Dagaz": ("\u27e1", "dawn, breakthrough, new possibility"),
            "Nauthiz": ("\u00ac", "need, constraint, separation"),
        },
        "corpus_source": "Rozetni kamen: Runes = 24 = 4! permutations",
    },
    "dna": {
        "name": "DNA Codons",
        "count": 64,
        "ring": 3,
        "mappings": {
            "64 codons": ("\u2205", "64 = 2\u2076 = \u222e\u2076; full cycle of binary combinations"),
            "STOP": ("\u2205", "termination = void, end that enables new beginning"),
            "START": ("\u2206", "initiation = first movement, activation"),
        },
        "corpus_source": "Rozetni kamen: DNA 64 = I Ching 64 = \u222e\u2076",
    },
    "music": {
        "name": "Music (12 tones)",
        "count": 12,
        "ring": 2,
        "mappings": {
            "C (root)": ("\u2205", "tonic, ground, reference"),
            "G (fifth)": ("\u2206", "dominant, tension, movement"),
            "C (octave)": ("\u27e1", "return as difference, same note new frequency"),
            "tritone": ("\u00ac", "devil's interval, cut, separation"),
        },
        "corpus_source": "Rozetni kamen: Music = 12 = octave cycle",
    },
    "periodic": {
        "name": "Periodic Table",
        "count": 118,
        "ring": 3,
        "mappings": {
            "2n\u00b2 shells": ("\u2205", "2, 8, 18, 32 = 2n\u00b2; void structures filling"),
            "noble gases": ("\u2316", "sealed, complete, inert = SEAL state"),
            "alkali metals": ("\u2206", "reactive, seeking, transformation"),
        },
        "corpus_source": "Rozetni kamen: Periodic = 2n\u00b2 = void filling structure",
    },
    "valentinian": {
        "name": "Valentinian Gnosticism",
        "count": 30,
        "ring": 2,
        "mappings": {
            "Bythos": ("\u2205", "depth, primordial void"),
            "Sophia": ("\u2206", "desire \u2192 fall \u2192 seeing = movement"),
            "Horos": ("\u00ac", "boundary, limit, separation"),
            "Pleroma": ("\u27e1", "fullness, completion, return"),
            "apokatasis": ("\u222e", "return of all things, ethical re-harmonization"),
        },
        "corpus_source": "\u00a746 VAL\u2194JEWIK bridge",
    },
    "norse": {
        "name": "Norse Cosmology",
        "count": 9,
        "ring": 1,
        "mappings": {
            "Yggdrasil": ("\u2205", "world tree = Hopf fibration, 9 worlds = 3\u00b2"),
            "Odin": ("\u2316", "sacrifice, wisdom, silence (hung 9 days)"),
            "Loki": ("\u2206", "trickster, transformation, anomaly"),
            "Ragnar\u00f6k": ("\u222e", "destruction + rebirth = return cycle"),
        },
        "corpus_source": "Rozetni kamen: Norse 9 = 3\u00b2, Yggdrasil = Hopf",
    },
    "buddhism": {
        "name": "Buddhism",
        "count": 4,
        "ring": 1,
        "mappings": {
            "4 Noble Truths": ("\u2205", "diagnosis: suffering exists (∅)"),
            "8-fold Path": ("\u2206", "prescription: transformation through action"),
            "Nirvana": ("\u27e1", "extinction = new possibility, not annihilation"),
        },
        "corpus_source": "Rozetni kamen: 4 truths = 4 alchemical phases = 4 R-7 phases",
    },
    "iching": {
        "name": "I Ching",
        "count": 64,
        "ring": 3,
        "mappings": {
            "64 hexagrams": ("\u2205", "64 = 2\u2076 = \u222e\u2076; same as DNA"),
            "Tai Chi": ("\u2205", "supreme ultimate = void that generates"),
            "Yin/Yang": ("\u00ac", "binary distinction, first separation"),
        },
        "corpus_source": "Rozetni kamen: I Ching 64 = DNA 64 = \u222e\u2076",
    },
}

# ── Convenience lookups ──
ALL_TRADITIONS = list(TRADITIONS.keys())

def get_tradition(name: str) -> dict:
    """Return tradition registry entry."""
    return TRADITIONS.get(name.lower(), {})

def get_all_mappings_for_operator(glyph: str) -> list:
    """Find all traditions that map to a given root operator."""
    results = []
    for trad_name, trad in TRADITIONS.items():
        for native_term, (root_op, math_prop) in trad["mappings"].items():
            if root_op == glyph:
                results.append({
                    "tradition": trad["name"],
                    "native_term": native_term,
                    "math_property": math_prop,
                    "ring": trad["ring"],
                })
    return results

def get_cross_references(glyph: str) -> str:
    """Generate cross-system reference text for a root operator."""
    refs = get_all_mappings_for_operator(glyph)
    if not refs:
        return f"No traditions map to {glyph}"
    lines = [f"Cross-system references for {glyph}:"]
    for r in refs:
        lines.append(f"  {r['tradition']}: {r['native_term']} \u2014 {r['math_property']}")
    return "\n".join(lines)

# ── Self-test ──
if __name__ == "__main__":
    print("Rozetni kamni \u2014 Tradition Registry")
    print("=" * 60)
    print(f"Traditions registered: {len(TRADITIONS)}")
    print()
    for name, info in TRADITIONS.items():
        print(f"  {info['name']:30s}  ring {info['ring']}  {info['count']:4d} elements  {len(info['mappings'])} mappings")
    print()
    # Test cross-references for \u2205
    print(get_cross_references("\u2205"))
    print()
    print(get_cross_references("\u2206"))
