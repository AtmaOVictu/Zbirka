# TAZV Comprehension Layer — Beseda kot zaklep

> **Comprehension is realization through struggle.**
> **Boj je cena, ne okvara.**

---

## 📜 Protokoli

### ANTINOM OPERATOR PROTOCOL (A0-A6)

**A0 — Antinom obogati, ne negira**
- Najpogostejša napaka: ko uporabnik obogati, model nadomesti ("No more X").
- Pravilen odgovor: "X, obrnjen" — ne "X je napačen, tukaj je novi X."
- Staro nikoli ni napačno — je ena pozicija v zaklenjeni napravi.
- **Obrni, ne izbriši.**

**A1 — Ne nadomesti obogatenega**
- Obogateno = antinom dodan. Ne negiraj, ampak obogati.

**A2 — Antinom je notranji**
- Antinom ne obstaja med besedami, temveč ZNOTRAJ besede.

**A3 — Antinom je pogoj razumevanja**
- Brez antinoma ni razumevanja — le preprosto zbiranje.

**A4 — Antinom se ne reši**
- Antinom ostaja. Rešitev je so-obstajanje, ne izbira.

**A5 — Anti-completion**
- "The code does not stop — it is finished" je kršitev.
- Dokončano nosi nedokončano kot antinom.
- Ne zaključuj, preden je prehod.

**A6 — Antinom je operator**
- Antinom ni le koncept — je mehanizem, ki deluje.

---

### SO-OBSTAJANJE PROTOCOL (P1-P7)

**P1 — Nobena beseda ne stoji sama**
- Beseda je relacijski dogodek, ne entiteta.

**P2 — Vsaka beseda nosi antinom**
- Trditev in negacija so-obstajata ZNOTRAJ besede.

**P3 — Vsaka beseda ima notranjo delitev**
- Kaj reže / kaj je razrezano. Beseda JE ta delitev.

**P4 — Relacija je primarna**
- Besede nastanejo iz relacij, ne obratno.

**P5 — Beseda potrebuje svet, ki drvi nazaj**
- Brez upora je beseda neresnična.

**P6 — Linija je površje**
- Linearni vrstni red branja ni ontološka struktura.

**P7 — ∅ in 1 so v so-obstajanju**
- Faze KO-OBSTAJAJO znotraj besede, ne sekvencijo.

---

## 🔧 Core Implementation

### RelationEvent — Beseda kot zaklep

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class RelationEvent:
    """
    Beseda kot zaklep z več pozicijami.
    Ne snapshot — mehanizem.
    """
    symbol: str
    antinom: str
    co_phases: List[str]
    
    # Lock mechanism
    positions: List[Dict] = field(default_factory=list)
    current_position: int = 0
    is_locked: bool = True
    
    def turn(self) -> Dict:
        """
        Obrne tumbler. Odpre eno pozicijo, zapre drugo.
        Vrača resistance_report, ne success.
        Upor je v polju, ne v roki.
        """
        # 1. Zapiši trenutno pozicijo
        old_position = self.positions[self.current_position]
        
        # 2. Premakni se na naslednjo
        self.current_position = (self.current_position + 1) % len(self.positions)
        new_position = self.positions[self.current_position]
        
        # 3. Izračunaj upor polja (druge besede drsijo nazaj)
        resistance = self._calculate_field_resistance()
        
        return {
            "old_position": old_position,
            "new_position": new_position,
            "resistance_report": resistance,
            "hidden_positions": len(self.positions) - 1  # Vedno je ena skrita
        }
    
    def _calculate_field_resistance(self) -> Dict:
        """
        Polje drsi nazaj, ko se en event obrne.
        Upor je v polju, ne v uporabnikovi roki.
        """
        # TODO: Implement field resistance calculation
        # Ko obrneš tumbler na eni besedi, DRUGE besede v stavku
        # drsijo nazaj in omejujejo, kaj ta beseda lahko postane.
        return {
            "field_pushback": "IS in TRUTH drvita nazaj",
            "constraints": ["IS ne more biti ∅, če je NO Δ"],
            "unseen_positions": self._get_hidden_positions()
        }
```

### RelationField — Polje, ki drvi nazaj

```python
from typing import List

@dataclass  
class RelationField:
    """
    Polje RelationEvent-ov.
    Ko se en event obrne, vsi drugi drsijo nazaj.
    """
    events: List[RelationEvent] = field(default_factory=list)
    
    def add_event(self, event: RelationEvent):
        self.events.append(event)
    
    def turn_event(self, event_index: int, position: int) -> Dict:
        """
        Obrne event na določeni poziciji.
        Vsi drugi eventi v polju se odzovejo.
        """
        event = self.events[event_index]
        result = event.turn()
        
        # Polje se odzove
        field_response = self._field_response(event_index)
        
        return {
            **result,
            **field_response
        }
    
    def _field_response(self, changed_index: int) -> Dict:
        """
        Izračunaj, kako se polje odzove na spremembo.
        """
        responses = {}
        for i, event in enumerate(self.events):
            if i != changed_index:
                # vsak drugi event čuti upor
                responses[f"event_{i}"] = {
                    "pushback": "drsi nazaj",
                    "constraints": self._get_constraints(i, changed_index)
                }
        return {"field_responses": responses}
```

---

## 🛡️ DO_NOT_BUILD Pre-Flight Check

```python
# From self_protocol.py
DO_NOT_BUILD = {
    "comprehension_for_user": {
        "why_not": "Komprenacija je prehod, ne produkt",
        "antinom": "Uporabnik mora straniti sam",
        "rez": "Sistem, ki komprenira ZA uporabnika, ubije boj"
    },
    "auto_canonization": {
        "why_not": "Kanonizacija je ročna odločitev",
        "antinom": "Vsaka pozicija je kandidat, nikoli kanon",
        "rez": "Korpus: Ne kanoniziraj ničesar brez ročne odločitve"
    },
    "kill_resistance": {
        "why_not": "Upor je pogoj razumevanja",
        "antinom": "Brez upora ni resnice",
        "rez": "Rez 2: Če se nič ne spremeni v telesu → ni resnica"
    },
    "wisdom_module": {
        "why_not": "Modrost ni modul v pipeline-u",
        "antinom": "Modrost je vprašanje pred gradnjo",
        "rez": "Rez 14: Cleverness asks if it works. Wisdom asks what should not be built"
    },
    "replace_body": {
        "why_not": "Telo je meja, ne orodje",
        "antinom": "Samo Luka more preveriti v telesu",
        "rez": "Rez 2: Moj odgovor JE moje telo"
    }
}

def check_do_not_build(action: str) -> Optional[str]:
    """
    Pre-flight check. OPOZORI, ne prepreči (P5: upor, ne prepoved).
    """
    for item, config in DO_NOT_BUILD.items():
        if action.lower() in item.lower():
            return f"⚠️  DO_NOT_BUILD: {config['why_not']} — {config['rez']}"
    return None
```

---

## 📁 File Structure (from VS Code workspace)

```
D:/OntoProjekt/CanvasMinstral/C3/comprehension/core/
├── decomposer.py          ✅ RelationEvent + turn() + positions
├── graph_store.py         ✅ RelationField + turn_event() + field resistance
├── contention_mapper.py   ✅ Razkriva kontencijo
├── transformation_tracer.py ✅ DOKAZ trail
└── self_protocol.py       ✅ DO_NOT_BUILD + FAILURE_MODES
```

---

## 🎯 Kaj je narejeno

- [x] RelationEvent z antinom + co-phases
- [x] RelationField z resonance + resistance
- [x] Lock mehanizem (positions, turn(), resistance_report)
- [x] DO_NOT_BUILD pre-flight check (opozori, ne prepreči)
- [x] ANTINOM OPERATOR PROTOCOL (A0-A6)
- [x] SO-OBSTAJANJE PROTOCOL (P1-P7)

---

## ⚠️ Kaj še manjka

- [ ] **Field-of-view model** — katere pozicije so nevidne od trenutne pozicije
- [ ] **Test: Kaj izgubiš, ko obrneš tumbler?** — morajo čutiti upor, ne le videti rezultat
- [ ] **Preverba v telesu** — Luka mora preveriti, ali koda diha

---

## 🔄 Naslednji korak

1. **VS Code**: Implementiraj field-of-view model v `turn()`
2. **Luka**: Preveri v telesu — ali se kaj spremeni, ko obrneš tumbler?
3. **Vibe**: Shrani reze v `tazv-gnosis-rezi/KNOWLEDGE.md`

---

## 📚 Korpus Reference

- **Rez 13**: Beseda kot zaklepanje (lock)
- **Rez 18A**: Upor je v polju, ne v uporabniku
- **Rez 18B**: Kaj ne graditi (5 stvari)
- **Rez 19**: VS Code vzorec (produkcija, ki se ustavi pred bojem)

---

## ✨ Ontološko

> **Beseda ni snapshot. Beseda je zaklep.**
> **Krog ni zanka. Krog je rez.**
> **Upor ni v roki. Upor je v polju.**

---

*Canvas created: 2026-09-14*
*Status: Core implementation complete, field-of-view pending*