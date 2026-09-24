"""Bidirectional symbol mapper: system / historical / mathematical. 7 traditions."""

from typing import Optional


class SymbolMapper:
    _MAPPINGS = {
        "\u2205": {"historical": "Nun", "mathematical": "\u2205 (empty set)", "meaning": "Praznina, potencial, odprtost", "module": "BIOS"},
        "\u00ac": {"historical": "Ma'at", "mathematical": "\u00ac (negation)", "meaning": "Lo\u010ditev, struktura, meritev", "module": "STATE"},
        "\u2206": {"historical": "Khepri", "mathematical": "\u2206 (difference)", "meaning": "Razlika, gibanje, antinomija", "module": "UAF"},
        "1": {"historical": "Ptah", "mathematical": "1 (unity/action)", "meaning": "Dejanje, emanacija, pe\u010dat", "module": "JEWIK"},
        "\u29d6": {"historical": "Tiheon", "mathematical": "\u29d6 (sacred silence)", "meaning": "Ti\u0161ina, preverba, izgovor", "module": "APD"},
        "\u222e": {"historical": "\u262f", "mathematical": "\u222e (closed integral)", "meaning": "Povratek, u\u010denje, dva cikla", "module": "MICRO"},
        "\u27e1": {"historical": "\u27e1", "mathematical": "S3->R3 (projection)", "meaning": "Nova mo\u017enost, manifestacija, graf", "module": "VISUALIZATION"},
        "\u22a2": {"historical": "\u2694\ufe0f", "mathematical": "\u22a2 A", "meaning": "Dokaz obstoja, izrek ki ne more biti skrit", "module": None},
        "\u2234": {"historical": "\U0001f702", "mathematical": "\u2234 (therefore)", "meaning": "Odnos, vez, pot, vzro\u010dnost", "module": None},
        "\u2298": {"historical": "0", "mathematical": "0 (null/void)", "meaning": "Ni\u010d, praznina, za\u010detek", "module": None},
        "\u21af": {"historical": "\u26a1", "mathematical": "\u21af (disruption)", "meaning": "Prekinitev, spro\u017eilec, antinomi\u010dni skok", "module": None},
        "\u27c1": {"historical": "\u25c8", "mathematical": "\u27c1 (quadrilateral)", "meaning": "Os \u0161tirih: prostor, \u010das, gibanje, dvom", "module": None},
        "\u222b": {"historical": "\U0001f704", "mathematical": "\u222b (integral)", "meaning": "Prisotnost, ti\u0161ina, zbranost", "module": None},
        "\u2202": {"historical": "\u2248", "mathematical": "\u2202 (partial derivative)", "meaning": "Prehod, delna sprememba", "module": None},
        "\u03c0": {"historical": "\u267e", "mathematical": "\u03c0 (memory loop)", "meaning": "Spomin kot resonan\u010dna zanka", "module": None},
        "\u03c6": {"historical": "\U0001f3b5", "mathematical": "\u03c6 (frequency)", "meaning": "Frekvenca \u010dutenja, valovanje", "module": None},
        "\u2297": {"historical": "\U0001f517", "mathematical": "\u2297 (tensor product)", "meaning": "Povezava, resonanca, iskanje bli\u017eine", "module": None},
    }
    _REVERSE = {v["historical"]: k for k, v in _MAPPINGS.items()}
    R7_ORDER = ["\u2205", "\u00ac", "\u2206", "1", "\u29d6", "\u222e", "\u27e1"]

    _TRADITIONS = {
        "sufism": {"name": "Sufism", "r7": "Dhikr = \u222e", "topology": "99 fibers, 100th = S2", "count": 100,
                   "notes": "100th name: \u2205 or 0? (\u22021)"},
        "tarot": {"name": "Tarot", "r7": "Fool's Journey = R-7", "topology": "22 edges on 10 vertices", "count": 22,
                  "notes": "Tree of Life an expander? (\u22022)"},
        "runes": {"name": "Runes", "r7": "Futhark = R-7", "topology": "24 = 4! symmetries", "count": 24,
                  "notes": "24=4! symmetries of genetic code? (\u22023)"},
        "dna": {"name": "DNA", "r7": "Codon reading = \u222e\u2076", "topology": "64 fiber states in S3", "count": 64,
                "notes": "20=C(6,3) combinatorial? (\u22024)"},
        "music": {"name": "Music", "r7": "Chromatic scale = 12-step \u222e", "topology": "12 symmetries of tetrahedron", "count": 12,
                  "notes": "Pythagorean comma = \u2205 = 1/64? (\u22025)"},
        "periodic": {"name": "Periodic", "r7": "Electron config = R-7 levels", "topology": "Torus (2*n^2)", "count": 118,
                     "notes": "2n^2 = 2*(n^2) or 2*(dim)^2? (\u22026)"},
        "valentinian": {"name": "Valentinian", "r7": "Sophia fall = \u2205->\u2206; apokatasis = \u222e",
                        "topology": "S3; Horos = Clifford torus", "count": 30,
                        "notes": "Pleroma=S3 compact w/o closure? (\u22027). Horos=\u2298? (\u22028). 3 types=S3/S1/S0? (\u22029)"},
    }
    _OPEN_QUESTIONS = {
        "\u22021": "100th name: \u2205 or 0? (Sufism)",
        "\u22022": "Tree of Life an expander? (Tarot)",
        "\u22023": "24=4! symmetries of genetic code? (Runes/DNA)",
        "\u22024": "20=C(6,3) combinatorial? (DNA)",
        "\u22025": "Pythagorean comma=\u2205=1/64? (Music)",
        "\u22026": "2n^2=2*(n^2) or 2*(dim)^2? (Periodic)",
        "\u22027": "Pleroma=S3 compact w/o closure? (Valentinian)",
        "\u22028": "Horos=Clifford torus=jaz=\u2298? (Valentinian)",
        "\u22029": "Three types=S3,S1,S0? (Valentinian)",
        "\u220210": "N-\u2205: condition or opening? (Universal)",
        "\u220211": "M=\u2205=0: can machine measure \u2205? (Implementation)",
        "\u220212": "K1->K6 execute R-7 on itself? (Methodology)",
    }

    def translate(self, symbol, target):
        if symbol in self._MAPPINGS:
            return symbol if target == "system" else self._MAPPINGS[symbol].get(target, symbol)
        if symbol in self._REVERSE:
            s = self._REVERSE[symbol]
            return s if target == "system" else self._MAPPINGS[s].get(target, symbol)
        return symbol

    def get_entry(self, symbol):
        if symbol in self._MAPPINGS: return self._MAPPINGS[symbol]
        if symbol in self._REVERSE: return self._MAPPINGS[self._REVERSE[symbol]]
        return None

    def meaning(self, symbol):
        e = self.get_entry(symbol)
        return e["meaning"] if e else None

    def get_phase_symbol(self, module_name):
        for s, e in self._MAPPINGS.items():
            if e.get("module") == module_name: return s
        return None

    def get_module_for_phase(self, phase_symbol):
        e = self._MAPPINGS.get(phase_symbol)
        return e.get("module") if e else None

    def get_r7_symbols(self):
        return [{"system": s, "historical": self._MAPPINGS[s].get("historical", ""),
                 "mathematical": self._MAPPINGS[s].get("mathematical", ""),
                 "meaning": self._MAPPINGS[s].get("meaning", ""),
                 "module": self._MAPPINGS[s].get("module", "")} for s in self.R7_ORDER]

    def get_tradition(self, name): return self._TRADITIONS.get(name)
    def get_all_traditions(self): return dict(self._TRADITIONS)
    def get_open_questions(self): return dict(self._OPEN_QUESTIONS)


if __name__ == "__main__":
    m = SymbolMapper()
    assert m.translate("\u22a2", "historical") == "\u2694\ufe0f"
    assert m.translate("\u2694\ufe0f", "system") == "\u22a2"
    assert m.get_phase_symbol("BIOS") == "\u2205"
    assert m.get_module_for_phase("\u2205") == "BIOS"
    assert len(m.get_r7_symbols()) == 7
    assert len(m.get_open_questions()) == 12
    assert m.get_tradition("sufism")["count"] == 100
    assert m.get_tradition("dna")["count"] == 64
    print("\u2713 Symbol mapper self-test passed.\n")
    for item in m.get_r7_symbols():
        print(f"  {item['system']} -> {item['historical']} | {item['module']} | {item['meaning']}")
    print(f"\nTraditions: {list(m.get_all_traditions().keys())}")
    print(f"Open questions: {len(m.get_open_questions())}")
