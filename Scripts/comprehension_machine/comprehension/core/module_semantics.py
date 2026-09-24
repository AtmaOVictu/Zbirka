"""
Module Semantics — R-7 Core Modules
====================================
Defines the 7 root operators and their semantic properties.

Corpus: R-7 = 7 root operators that form the basis of all knowledge mapping.
Each module has:
  - symbol: the R-7 glyph
  - name: the module name
  - meaning: corpus meaning
  - agent: associated agent

Source: Obs3, Rozetni kamni I-LXXII
"""

# ── R-7 Module definitions ──
MODULE_SEMANTICS = {
    "bios": {
        "symbol": "\u2205",  # ∅
        "name": "BIOS",
        "meaning": "Praznina — potencial, odprtost, pogoj za prehod",
        "agent": "AgentLUKA",
        "color": "kem",
    },
    "state": {
        "symbol": "\u00ac",  # ¬
        "name": "STATE", 
        "meaning": "Ločitev — struktura, meritev, meja",
        "agent": "AgentRez",
        "color": "hedj",
    },
    "uaf": {
        "symbol": "\u2206",  # ∆
        "name": "UAF",
        "meaning": "Razlika — gibanje, antinomija, prehod",
        "agent": "AgentDj",
        "color": "desher",
    },
    "jewik": {
        "symbol": "1",
        "name": "JEWIK",
        "meaning": "Dejanje — emanacija, pečat, manifestacija",
        "agent": "AgentAkt",
        "color": "gold",
    },
    "apd": {
        "symbol": "\u2316",  # ⧖
        "name": "APD",
        "meaning": "Tišina — preverba, izgovor, molk",
        "agent": "Tiheon",
        "color": "khesbedj",
    },
    "micro": {
        "symbol": "\u222e",  # ∮
        "name": "MICRO",
        "meaning": "Povratek — učenje, odmev, cikel",
        "agent": "AgentReturn",
        "color": "egyptian_blue",
    },
    "visualization": {
        "symbol": "\u27e1",  # ⟡
        "name": "VISUALIZATION",
        "meaning": "Nova možnost — manifestacija, graf, projekcija",
        "agent": "AgentEcho",
        "color": "wadj",
    },
}

# ── R-7 Order (from SymbolMapper) ──
MODULE_ORDER = ["bios", "state", "uaf", "jewik", "apd", "micro", "visualization"]

# ── Convenience functions ──
def get_module(symbol):
    """Return module dict by R-7 symbol."""
    for name, mod in MODULE_SEMANTICS.items():
        if mod["symbol"] == symbol:
            return mod
    return None

def get_symbol(module_name):
    """Return R-7 symbol by module name."""
    mod = MODULE_SEMANTICS.get(module_name)
    return mod["symbol"] if mod else "?"

def get_name(symbol):
    """Return module name by R-7 symbol."""
    mod = get_module(symbol)
    return mod["name"] if mod else "?"

# ── Self-test ──
if __name__ == "__main__":
    print("Module Semantics — R-7")
    print("=" * 50)
    for name in MODULE_ORDER:
        mod = MODULE_SEMANTICS[name]
        print(f"  {mod['symbol']:3s}  {mod['name']:15s}  {mod['color']:15s}  {mod['meaning']}")
    print()
    print(f"Modules: {len(MODULE_SEMANTICS)}")
    print(f"Order: {MODULE_ORDER}")
