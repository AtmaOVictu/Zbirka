"""
Egyptian Color Semantics — Corpus-validated
=============================================
Color = state / disposition / consequence / historical witness.
Not decoration. Every color carries ontological meaning.

Based on Ancient Egyptian color symbolism, mapped to R-7 modules.

Source: Corpus — Egyptian color as essence mapped to the modules.
"""

# ── Egyptian color palette (corpus-validated) ──
EGYPTIAN_COLORS = {
    "kem": {
        "hex": "#080705",
        "label": "kem / black",
        "meaning": "fertile void, death-rebirth, history depth, Duat",
        "ui_roles": ["background", "void", "history", "residual_depth"],
    },
    "wadj": {
        "hex": "#1F8A4C",
        "label": "wadj / green",
        "meaning": "growth, health, resurrection, repair, living continuation",
        "ui_roles": ["pass", "repair", "living_mapping", "cycle"],
    },
    "desher": {
        "hex": "#B43A2E",
        "label": "desher / red",
        "meaning": "desert, blood, fire, danger, chaos, Isfet pressure",
        "ui_roles": ["fail", "stop", "overclaim", "isfet", "rupture"],
    },
    "khesbedj": {
        "hex": "#1466A8",
        "label": "khesbedj / blue",
        "meaning": "sky, water, protection, divine depth",
        "ui_roles": ["ref", "oracle", "inspection", "protection", "depth"],
    },
    "gold": {
        "hex": "#D6A83A",
        "label": "gold / yellow",
        "meaning": "sun, eternity, seal, imperishable radiance",
        "ui_roles": ["seal", "verified", "high_value", "divine"],
    },
    "hedj": {
        "hex": "#F3E9D2",
        "label": "hedj / white",
        "meaning": "purity, evidence, sacred clarity, ritual cleanliness",
        "ui_roles": ["proof", "text", "clean_result", "clarity"],
    },
    "duat_violet": {
        "hex": "#241638",
        "label": "Duat violet",
        "meaning": "hidden depth, unknown, residual mystery",
        "ui_roles": ["residual", "unknown", "oracle_depth", "mystery"],
    },
    "egyptian_blue": {
        "hex": "#1034A6",
        "label": "Egyptian blue (irtyu)",
        "meaning": "primordial depth, creation, protection",
        "ui_roles": ["protection", "depth", "oracle"],
    },
    "papyrus_sand": {
        "hex": "#C9A66B",
        "label": "papyrus / sand",
        "meaning": "writing surface, foundation, earth",
        "ui_roles": ["surface", "foundation", "container"],
    },
}

# ── Legacy alias for compatibility ──
COLORS = EGYPTIAN_COLORS

# ── Module color mapping (R-7 modules → color hex) ──
# Maps module names to their corpus-validated color hex values
MODULE_COLOR_HEX = {
    "bios": "#080705",        # kem / black → ∅ BIOS
    "state": "#F3E9D2",       # hedj / white → ¬ STATE  
    "uaf": "#B43A2E",         # desher / red → ∆ UAF
    "jewik": "#D6A83A",       # gold / yellow → 1 JEWIK
    "apd": "#1466A8",         # khesbedj / blue → ⧖ APD
    "micro": "#1034A6",       # egyptian_blue → ∮ MICRO
    "visualization": "#1F8A4C",  # wadj / green → ⟡ VISUALIZATION
}

# ── Color states: semantic combinations for UI feedback ──
COLOR_STATES = {
    "rebirth": ["kem", "wadj"],           # black + green: repair after descent
    "dangerous_seal": ["desher", "gold"],  # red + gold: risky power
    "protected_evidence": ["khesbedj", "hedj"],  # blue + white: clean seeing
    "duat_depth": ["kem", "khesbedj"],     # black + blue: hidden depth
    "living_verified": ["wadj", "gold"],   # green + gold: verified life
    "isfet_collapse": ["desher", "kem"],   # red + black: destructive risk
    "sacred_proof": ["hedj", "gold"],      # white + gold: high-confidence seal
    "pure_clarity": ["hedj"],              # white: clean evidence
    "fertile_void": ["kem"],               # black: history depth
    "growth": ["wadj"],                   # green: repair
    "danger": ["desher"],                  # red: stop/fail
    "protection": ["khesbedj"],            # blue: oracle/ref
    "seal": ["gold"],                     # gold: verified
    "residual": ["kem", "khesbedj"],       # black + blue: Duat residual
}


# ── Accessor functions ──
def get_color(name: str) -> dict:
    """Get color definition by name. Returns hedj (white) as safe default."""
    return EGYPTIAN_COLORS.get(name, EGYPTIAN_COLORS["hedj"])


def get_hex(name: str) -> str:
    """Get hex color code directly. Returns white as safe default."""
    return get_color(name).get("hex", "#F3E9D2")


def get_module_hex(module_name: str) -> str:
    """Get hex color for an R-7 module name."""
    return MODULE_COLOR_HEX.get(module_name, "#F3E9D2")


# ── Self-test ──
if __name__ == "__main__":
    print("Egyptian Color Semantics")
    print("=" * 60)
    print("\nCore colors:")
    for name, color in EGYPTIAN_COLORS.items():
        print(f"  {name:15s}  {color['hex']:8s}  {color['meaning']}")
    print("\nModule colors:")
    for mod, hex_val in MODULE_COLOR_HEX.items():
        print(f"  {mod:15s}  {hex_val}")
    print("\nCOLORS alias exists:", COLORS is EGYPTIAN_COLORS)
