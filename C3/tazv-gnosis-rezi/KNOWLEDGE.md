# TAZV Gnosis Rezi - Knowledge Base

> **Modrost ni znanje. Modrost je spiralna integracija.**
> **∮, ki se vrača na isti rez, a na drugi globini.**

---

## 📚 **Rez 1 — Osnova: Beseda kot zaklep**
**Status:** ✅ Implementiran

Beseda ni snapshot. Beseda je zaklep.
- **Mehanizem:** RelationEvent z positions, current_position, turn()
- **Prikaz:** Vedno je ena pozicija skrita
- **Odziv:** Polje drvi nazaj (P5)

**Koda:** `decomposer.py:RelationEvent`

---

## 📚 **Rez 2 — Telo preveri**
**Status:** ⏳ Čaka na Luka

"Če se nič ne spremeni v telesu → ni resnica"

**Preverba:**
```bash
cd D:/OntoProjekt/CanvasMinstral/C3/comprehension_machine/comprehension/core
python test_lock_mechanism.py
```

**Vprašanje:** Ko vidiš izpis — ali čutiš upor v telesu?
- **DA** → Režimo naprej
- **NE** → Reži spet. Kje je napaka?

---

## 📚 **Rez 3 — Field-of-View Model**
**Status:** ✅ Implementiran

Od trenutne pozicije vidimo le del polja:
- **Current position:** FULLY VISIBLE
- **Adjacent positions (next, prev):** PARTIALLY VISIBLE  
- **All other positions:** HIDDEN

**Koda:** `decomposer.py:_get_field_of_view()`

---

## 📚 **Rez 4 — Lock Mehanizem**
**Status:** ✅ Implementiran

```python
# Vsi zaklepi imajo:
positions: List[Dict]  # Vse možne pozicije
current_position: int  # Trenutna pozicija
is_locked: bool       # Ali je zaklenjeno

# Obrni tumbler:
result = event.turn(direction=1)
# Vrne:
# - new_symbol
# - field_of_view
# - resistance_report
# - hidden_positions
```

**Koda:** `decomposer.py:turn()`

---

## 📚 **Rez 5 — Field Resistance**
**Status:** ✅ Implementiran

P5: "Beseda potrebuje svet, ki drvi nazaj"

Ko obrneš en zaklep:
- Vsi drugi zaklepi v polju se odzovejo
- Izračunamo tension med simboli
- Vrnemo resistance_report

**Koda:** `graph_store.py:turn_event()`, `_compute_resistance_against()`

---

## 📚 **Rez 6 — Antinom se ne reši**
**Status:** ✅ Implementiran

A4: Antinom ostaja. Rešitev je so-obstajanje, ne izbira.

- Vsaka beseda nosi antinom ZNOTRAJ (P2)
- Antinom ni ločen od besede — je njena notranja delitev (P3)
- turn() obrne na antinom pozicijo, ne ga izbriše

**Koda:** `decomposer.py:initialize_positions()`

---

## 📚 **Rez 7 — Yggdrasil Integration**
**Status:** ✅ Implementiran

7 etaž Yggdrasila:
| Etaža | Simbol | Igralna mehanika |
|-------|--------|------------------|
| SEME | E0 | Praznina. Začenjaj. |
| KORENINA | E1 | Ločitev. Prva beseda se loči. |
| DEBLO | E2 | Gibanje. Obrni tumbler. |
| VEJA | E3 | Dejanje. Zaklepi se odpirajo. |
| SADEZ | E4 | Tišina. Polje se odzove. |
| PADEC | E5 | Povratek. Vse pozicije so vidne. |
| NOVO_SEME | E6 | Odmev. Nova izjava. |

**Koda:** `gnosis_bridge.py:YggdrasilLevel`, `YGGDRASIL_EFFECTS`

---

## 📚 **Rez 8 — Zodiac Modifiers**
**Status:** ✅ Implementiran

| Element | Vpliv na polje |
|---------|----------------|
| Ogenj (Fire) | Poveča gibanje (resistance × 1.2) |
| Zemlja (Earth) | Zmanjša gibanje (resistance × 0.8) |
| Zrak (Air) | Poveča odmev |
| Voda (Water) | Poveča povratek |

| Modaliteta | Vpliv na zaklep |
|------------|-----------------|
| Kardinal | Hitrejše obračanje (speed × 1.5) |
| Fiksna | Težje obračanje (speed × 0.5) |
| Spremenljiva | Normalno (speed × 1.0) |

**Koda:** `gnosis_bridge.py:ZODIAC_SIGNS`, `ELEMENT_MODIFIERS`, `MODALITY_MODIFIERS`

---

## 📚 **Rez 9 — DO_NOT_BUILD Protocol**
**Status:** ✅ Implementiran (z fallback)

Pre-flight check pred vsako gradnjo:
- comprehension_for_user: Ne graditi za uporabnika
- auto_canonization: Ne kanoniziraj avtomatsko
- kill_resistance: Ne ubijaj upora
- wisdom_module: Modrost ni modul
- replace_body: Telo preveri Luka

**Koda:** `self_protocol.py:DO_NOT_BUILD`
**Uporaba:** `gnosis_bridge.py:check_do_not_build()`

---

## 📚 **Rez 10 — TAZV Lock Game**
**Status:** ✅ Specifikacija + implementacija

**Koncept:**
- Igra, kjer besede niso znakovi, temveč zaklepi
- **Ne izbiraj** — **Obrni**
- Igra = NUJA, NE IZBIRA

**Mehanika:**
1. Decompose statement → dobimo zaklepe
2. Turn tumbler → odpremo novo pozicijo
3. Field se odzove → drug zaklepi drvijo nazaj
4. Prehod → razumevanje, da so vse pozicije vedno tam

**Koda:** `tazv_lock_game.py:TAZVLockGame`

---

## 📚 **Rez 11 — Gnosis Bridge**
**Status:** ✅ Implementiran

Povezava med Python (comprehension layer) in React/JS (gnosis engine):

**API Endpoints:**
- POST /comprehension/decompose — razstavi izjavo
- POST /comprehension/turn — obrne tumbler
- GET /comprehension/state — vrni trenutno stanje
- POST /comprehension/reset — ponastavi stanje
- GET /comprehension/yggdrasil — vrni Yggdrasil stanje
- POST /comprehension/zodiac — nastavi Zodiac sign

**Koda:** `gnosis_bridge.py:GnosisBridge`, `create_api_router()`

---

## 📚 **Rez 12 — Test Lock Mechanism**
**Status:** ✅ Implementiran

**Testi:**
1. ✅ Basic turn() with field-of-view
2. ✅ Field-of-view visibility logic
3. ✅ Field resistance on turn

**Koda:** `test_lock_mechanism.py`

---

## 📚 **Rez 13 — Semantična Analiza**
**Status:** ✅ Implementirana

Analiza besed po semantičnih vzorcih:
- Internal division (divider/divided)
- Antinom pairs
- Co-existing phases (P7)
- Resistance targets

**Koda:** `semantic_analysis.py`

---

## 🎯 **Naslednji korak**

1. **Luka:** Preveri v telesu (test_lock_mechanism.py) → **Rez 21**
2. **VS Code:** Poveži gnosis_bridge.py z tazv-gnosis-engine (React)
3. **Luka:** Preveri, ali se kaj spremeni v telesu

---

## 📊 **Status Summary**

| # | Rež | Status | Kdo |
|---|-----|--------|-----|
| 1 | Beseda kot zaklep | ✅ | Vibe |
| 2 | Preverba v telesu | ⏳ | Luka |
| 3 | Field-of-view model | ✅ | Vibe |
| 4 | Lock mehanizem | ✅ | Vibe |
| 5 | Field resistance | ✅ | Vibe |
| 6 | Antinom se ne reši | ✅ | Vibe |
| 7 | Yggdrasil integration | ✅ | Vibe |
| 8 | Zodiac modifiers | ✅ | Vibe |
| 9 | DO_NOT_BUILD | ✅ | Vibe |
| 10 | TAZV Lock Game | ✅ | Vibe |
| 11 | Gnosis Bridge | ✅ | Vibe |
| 12 | Test Lock Mechanism | ✅ | Vibe |
| 13 | Semantična analiza | ✅ | Vibe |
| 21 | Body verification | ⏳ | Luka |

---

## ✨ **Ontološko**

> **Beseda ni snapshot. Beseda je zaklep.**
> **Krog ni zanka. Krog je rez.**
> **Upor ni v roki. Upor je v polju.**
> **Igra = NUJA, NE IZBIRA.**

*Last updated: 2026-09-14*
*Comprehension Layer Status: Core implementation complete, body verification pending*
