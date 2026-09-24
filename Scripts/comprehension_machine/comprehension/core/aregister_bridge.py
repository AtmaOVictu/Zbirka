"""
ARegister Bridge — apercepcija → operator
=========================================
Korpus: "ARegister slovar: osnovni jezik → apercepcija → operator"
         (Obs11, 00-11-resnicami-comprehension-machine.tsx)

ARegister je VHODNI slovar. Ko uporabnik izrazi stanje (besedo),
ARegister prepozna apercepcijo in vrne ustrezen R-7 glyph.

To ni iskanje pomena — je prepoznavanje operacije, ki je ze aktivna
v uporabnikovi izkusnji. ARegister ne interpretira; prepozna.

Struktura (iz korpusa):
  userExpression → perception → glyph → inquiry → etymology

Uporaba:
  from comprehension.core.aregister_bridge import ARegisterBridge
  bridge = ARegisterBridge()
  entry = bridge.recognize("prazno")
  # → {glyph: "∅", perception: "...", inquiry: "...", etymology: "..."}
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ARegisterEntry:
    """Vnos iz ARegister slovarja (iz korpusa c7638bad)."""
    user_expression: str   # npr. "empty / prazno"
    perception: str         # apercepcija: kaj telo cuti
    glyph: str              # R-7 korenski glif
    inquiry: str            # vprasanje etaže
    etymology: str          # etimologija glifa


# Korpus-validirani ARegister vnosi (iz 00-11-resnicami.tsx)
AREGISTER_DATA = [
    ARegisterEntry(
        user_expression="empty / prazno",
        perception="I feel nothing — but the nothing feels open, not absent",
        glyph="∅",
        inquiry="Kaj se odpira v praznini, ki jo cutis? Ali je praznina pogoj, ne odsotnost?",
        etymology="∅ (1939, André Weil, iz norveske crke) — v tem sistemu: pogoj, ki omogoca, ne manjkajoci",
    ),
    ARegisterEntry(
        user_expression="separated / loceno",
        perception="Something was cut — I feel the edge",
        glyph="¬",
        inquiry="Kaj je rez locil? Ali je rez odprtje ali prekinitev?",
        etymology="¬ (logika) — v tem sistemu: locitev kot odprtje, ne negacija (§54)",
    ),
    ARegisterEntry(
        user_expression="moving / gibljoco",
        perception="I feel a shift — something is becoming",
        glyph="∆",
        inquiry="Kaj se spreminja? Ali je ∆ prehod ali sila?",
        etymology="∆ (grs. delta) — sprememba, razlika, derivative",
    ),
    ARegisterEntry(
        user_expression="sealed / zapechateno",
        perception="Something completed — an act that cannot be undone",
        glyph="1",
        inquiry="Kaj je zapechateno? Ali je 1 dejanje ali potrditev?",
        etymology="1 — terminal object, SEAL, unit, dejanje",
    ),
    ARegisterEntry(
        user_expression="still / tiho",
        perception="I feel a pulse — silence after speaking",
        glyph="⧖",
        inquiry="Kaj je utrip? Ali je cas parameter ali izgovor?",
        etymology="⧖ — cas kot parameter, utrip, periodicity",
    ),
    ARegisterEntry(
        user_expression="returning / se vračajoče",
        perception="Something comes back — but different",
        glyph="∮",
        inquiry="Kaj se vraca? Ali je ∮ povratek ali integracija?",
        etymology="∮ — integral, cikel, povratna zveza, loop",
    ),
    ARegisterEntry(
        user_expression="opening / odpirajoče",
        perception="Something opened that wasn't there before — an echo, a door",
        glyph="⟡",
        inquiry="Kaj se odpira? Ali je nova moznost odmev prejsnjega cikla?",
        etymology="⟡ — resonanca, odmev; nova moznost, ki izhaja iz ∮",
    ),
    ARegisterEntry(
        user_expression="transitioning / prehajajoče",
        perception="I'm between — not here, not there, but in the passage itself",
        glyph="∂",
        inquiry="Kaj se prehaja? Med cim in cim? Ali si v rezu ali na robu reza?",
        etymology="∂ (matematika) — prehod, partialna derivative; rez, ki povezuje abstrakcijo in izvedbo",
    ),
    ARegisterEntry(
        user_expression="present / prisotno",
        perception="I feel something that stays — beneath the noise",
        glyph="∫",
        inquiry="Kaj ostane, ko sum preide? Ali je ∫ prisotnost ali molk?",
        etymology="∫ — integral kot prisotnost; kar ostane, ko prehod preide",
    ),
    ARegisterEntry(
        user_expression="related / povezano",
        perception="I feel a connection — something links to something else",
        glyph="∴",
        inquiry="Kaj povezuje? Ali je ∴ vzroc ali zaveza?",
        etymology="∴ — odnos, vzrocnost, povezava, relacija",
    ),
]


class ARegisterBridge:
    """
    ARegister most: prepozna uporabnikovo besedo in vrne aperceptivni vhod.

    Korpus: "ARegister funkcija: prepozna uporabnikovo besedo
             in vrne aperceptivni vhod" (c7638bad)
    """

    def __init__(self):
        self.entries = AREGISTER_DATA

    def recognize(self, input_text: str) -> Optional[ARegisterEntry]:
        """
        Prepozna uporabnikov izraz in vrne ustrezen ARegister vnos.
        Isce po user_expression polju (split po '/').
        """
        lower = input_text.lower().strip()
        for entry in self.entries:
            expressions = [e.strip().lower() for e in entry.user_expression.split("/")]
            if any(expr in lower for expr in expressions):
                return entry
        return None

    def glyph_for(self, input_text: str) -> str:
        """Vrne glyph za izraz, ali None."""
        entry = self.recognize(input_text)
        return entry.glyph if entry else None

    def inquiry_for(self, input_text: str) -> str:
        """Vrne vprasanje etaže za izraz."""
        entry = self.recognize(input_text)
        return entry.inquiry if entry else ""

    def all_glyphs(self) -> list:
        """Vrne vse registrirane glyphe."""
        return [e.glyph for e in self.entries]
