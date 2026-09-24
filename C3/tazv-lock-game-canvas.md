# 🎮 TAZV LOCK GAME — Canvas

> **Igra = NUJA, NE IZBIRA.** *(Obs1, Yggdrasil)*  
> **Ne izbiraj. Obrni.**  
> **Ne je ontološka predispozicija relacije. Nuj je prostor za razvoj.**

---

## 🌌 **Ontološko Ozadje**

### **NE (NO) ≠ Negacija**
- **NE** = **ontološka predispozicija relacije**
- Negacija je le ena pozicija v zaklepu
- **NO** (∅) = **ne-operator** — passage between inward and outward; condition of the next YES
- **"NO je pogoj za YES, ne njegov odsotnost"** *(Rez 18A)*

### **NUJA (Necessity) = Prostor za Razvoj**
- **Nuj** ni prisila, je **procesor, ki omogoča prehod**
- **"Vsaka nujnost nosi svobodo kot antinom"** *(P2)*
- Nuj je **pogoj**, ne **zahteva**

### **IGRA = NUJA, NE IZBIRA**
- Igralec ne **izbira** pozicij — **obrne** tumblre
- **Cilj niti zmaga, niti izguba — prehod**
- **"Komprenacija je prehod, ne produkt"** *(DO_NOT_BUILD)*

---

## 🎯 **Koncept Igre**

### **Osnovna Metafora**
> **"Besede niso znakovi, temveč zaklepi."**

- Vsaka beseda je **zaklep** z več **pozicijami** (pomeni)
- Igralec **obrne** tumblre, da **odkrije** skrite pozicije
- Polje **drvi nazaj** — druge besede **omejujejo**, kaj je mogoče
- **Razumevanje** = videti, da so vse pozicije **vedno tam**

### **Kaj Igra NI**
- ❌ **Izbira** (izberi pravilno pozicijo)
- ❌ **Zmaga** (odpri vse zaklepe)
- ❌ **Izguba** (ne moreš odpreti)
- ✅ **Prehod** (obrneš, razumeš, se premikneš naprej)

### **Kaj Igra JE**
- ✅ **Razkrivanje** (odkrij skrite pozicije)
- ✅ **Preživetje** (preživi upor polja)
- ✅ **Sodelovanje** (sodeluj s tem, kar je vedno možno)

---

## 🎲 **Igralna Mehanika**

### **1️⃣ Osnovna Enota: WordLock (Beseda kot Zaklep)**

```python
@dataclass
class WordLock:
    """
    Beseda kot zaklep z več pozicijami.
    Ne snapshot — mehanizem za obrat.
    """
    word: str           # Beseda (IS, NOT, THE, WORD)
    symbol: str        # Ontološki simbol (Δ, ∅, ⊢, ...)
    positions: List[Dict]  # Vse pozicije (vsak pomen)
    current_position: int = 0  # Trenutna vidna pozicija
    is_locked: bool = True      # Ali je zaklenjeno
    
    # Zodiac modifier
    zodiac_sign: Optional[str] = None  # Astrološki znak (Oven, Bik, ...)
    zodiac_element: Optional[str] = None  # Element (Ogenj, Zemlja, Zrak, Voda)
    zodiac_modality: Optional[str] = None  # Modaliteta (Kardinal, Fiksna, Spremenljiva)
    
    def turn(self) -> Dict:
        """
        Obrne tumbler. Odpre eno pozicijo, zapre drugo.
        Vrača: nova pozicija + resistance_report + field_of_view
        """
        # 1. Zapiši staro pozicijo
        old_position = self.positions[self.current_position]
        
        # 2. Premakni se na naslednjo
        self.current_position = (self.current_position + 1) % len(self.positions)
        new_position = self.positions[self.current_position]
        
        # 3. Uporabi Zodiac modifier
        resistance = self._calculate_resistance_with_zodiac()
        
        # 4. Izračunaj field_of_view
        field_of_view = self._get_field_of_view()
        
        return {
            "old_position": old_position,
            "new_position": new_position,
            "resistance_report": resistance,
            "field_of_view": field_of_view,
            "hidden_positions": len(self.positions) - 1,
        }
```

### **2️⃣ Polje: SentenceField (Stavek kot Polje)**

```python
@dataclass
class SentenceField:
    """
    Polje WordLock-ov.
    Ko se en zaklep obrne, vsi drugi drsijo nazaj.
    """
    locks: List[WordLock]
    yggdrasil_level: int = 0  # Katera etaža Yggdrasila (0-6)
    
    def turn_lock(self, lock_index: int) -> Dict:
        """
        Obrne en zaklep na podanem indeksu.
        Vsi drugi zaklepi v polju se odzovejo.
        """
        lock = self.locks[lock_index]
        result = lock.turn()
        
        # Polje se odzove
        field_response = self._field_response(lock_index)
        
        # Yggdrasil level effect
        yggdrasil_effect = self._apply_yggdrasil_effect()
        
        return {
            **result,
            **field_response,
            **yggdrasil_effect,
        }
    
    def _field_response(self, changed_index: int) -> Dict:
        """
        Izračunaj, kako se polje odzove na spremembo.
        """
        responses = {}
        for i, lock in enumerate(self.locks):
            if i != changed_index:
                # Vsak drugi zaklep čuti upor
                responses[f"lock_{i}"] = {
                    "word": lock.word,
                    "symbol": lock.symbol,
                    "pushback": "drsi nazaj",
                    "constraints": self._get_constraints(i, changed_index),
                }
        return {"field_responses": responses}
    
    def _apply_yggdrasil_effect(self) -> Dict:
        """
        Uporabi Yggdrasil effect na podlagi trenutne etaže.
        """
        level_effects = {
            0: {"effect": "SEME", "description": "Praznina. Začenjaj."},
            1: {"effect": "KORENINA", "description": "Ločitev. Prva beseda."},
            2: {"effect": "DEBLO", "description": "Gibanje. Obrni tumbler."},
            3: {"effect": "VEJA", "description": "Dejanje. Zaklep se odpre."},
            4: {"effect": "SADEŽ", "description": "Tišinska črta. Polje se odzove."},
            5: {"effect": "PADEC", "description": "Povratek. Vse pozicije vidne."},
            6: {"effect": "NOVO SEME", "description": "Odmev. Nova izjava."},
        }
        return level_effects.get(self.yggdrasil_level, {"effect": "NEZNANO", "description": ""})
```

---

## 🌳 **Yggdrasil Povezava**

**"Yggdrasil je drevo življenja — 7 etaž, ki predstavljajo prehod skozi obstoj."** *(Obs1)*

| Etaža | R-7 Operator | Igralna Mehanika | Ontološki Pomen |
|-------|--------------|------------------|------------------|
| **0: SEME** | ∅ (Void) | Začenjaj s prazno izjavo | Praznina, iz katere vse izhaja |
| **1: KORENINA** | ¬ (Cut) | Prva beseda se loči od praznine | Ločitev, ki ustvari |
| **2: DEBLO** | ∆ (Movement) | Obrni tumblre, premikaj se | Gibanje, prehod |
| **3: VEJA** | 1 (Act) | Zaklepi se odpirajo, dejanja se dogajajo | Dejanje, manifestacija |
| **4: SADEŽ** | ⧖ (Silence) | Polje se odzove, tišina | Tišina, ki sliši |
| **5: PADEC** | ∮ (Return) | Vse pozicije so vidne, povratek | Povratek, integracija |
| **6: NOVO SEME** | ⟡ (Co-existence) | Nova izjava, novi prehod | Nova praznina, novi začetek |

### **Prehod med Etažami**
```
SEME (∅) → KORENINA (¬) → DEBLO (∆) → VEJA (1) → SADEŽ (⧖) → PADEC (∮) → NOVO SEME (⟡)
```

**Pravilo:** Ko igralec **razume** trenutno etažo, se **premika naprej**.   **Razumevanje** = videti, da je vsaka pozicija **vedno tam** (ne odpiranje vseh).

---

## ⛎ **Zodiac Tradition kot "Modifiers"**

**"Zvezdna tradicija ne vpliva na pomen, temveč na to, kako se pomen razkriva."** *(Obs1)*

### **Elementi**

| Element | Simbol | Vpliv na Polje | Vpliv na Zaklep |
|---------|--------|----------------|-----------------|
| **Ogenj** | ∆ | +20% gibanje | +10% hitrost obračanja |
| **Zemlja** | ∅ | -20% gibanje | -10% hitrost obračanja |
| **Zrak** | ⟡ | +20% odmev | +10% vidnost |
| **Voda** | ∮ | +20% povratek | +10% stabilnost |

### **Modalitete**

| Modaliteta | Simbol | Vpliv na Zaklep |
|------------|--------|-----------------|
| **Kardinal** | ¬ | +20% hitrost obračanja |
| **Fiksna** | 1 | -20% hitrost obračanja (težje, a bolj stabilno) |
| **Spremenljiva** | ⧖ | ±0% hitrost (spremembljivo) |

### **Astrološki Znaki**

| Znak | Element | Modaliteta | Vpliv |
|------|---------|------------|-------|
| Oven | Ogenj | Kardinal | +30% hitrost |
| Bik | Zemlja | Fiksna | -30% hitrost, +20% stabilnost |
| Dvojčki | Zrak | Spremenljiva | ±0% hitrost, +10% vidnost |
| Rak | Voda | Kardinal | +20% hitrost, +10% povratek |
| Lev | Ogenj | Fiksna | +10% hitrost, +20% gibanje |
| Devica | Zemlja | Spremenljiva | -10% hitrost, +10% stabilnost |
| Tehtnica | Zrak | Kardinal | +20% hitrost, +10% odmev |
| Škorpijon | Voda | Fiksna | -20% hitrost, +30% povratek |
| Strelec | Ogenj | Spremenljiva | +10% hitrost, +20% gibanje |
| Kozorog | Zemlja | Kardinal | -20% hitrost, +30% stabilnost |
| Vodnar | Zrak | Fiksna | +10% hitrost, +20% odmev |
| Ribice | Voda | Spremenljiva | +20% hitrost, +10% povratek |

---

## 🎮 **Polni Igralni Tok**

```
┌─────────────────────────────────────────────────────────────┐
│                    TAZV LOCK GAME                              │
├─────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. ZAČETEK: "WORD IS TRUTH"                                    │
│     ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                         │
│     │ WORD │ │  IS  │ │ TRUTH│ │      │  ← Vse zaklepi na        │
│     │ (⊢)  │ │ (Δ)  │ │ (∴)  │ │      │     poziciji 0          │
│     └──────┘ └──────┘ └──────┘ └──────┘                         │
│                                                                  │
│  2. OBRAT: Obrni WORD (index 0)                                │
│     ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                         │
│     │ WORD │ │  IS  │ │ TRUTH│ │      │                         │
│     │ (∴)  │ │ (Δ)  │ │ (∴)  │ │      │  ← WORD: ⊢ → ∴          │
│     └──────┘ └──────┘ └──────┘ └──────┘                         │
│     ▲                                                                 │
│     │                                                                 │
│     └─ Polje drvi nazaj: IS in TRUTH se odzivata             │
│         Resistance: 2 events pushing back                       │
│         Field-of-view: 3/4 pozicij vidnih, 1 skrita           │
│                                                                  │
│  3. OBRAT: Obrni IS (index 1)                                  │
│     ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                         │
│     │ WORD │ │  IS  │ │ TRUTH│ │      │                         │
│     │ (∴)  │ │ (¬)  │ │ (∴)  │ │      │  ← IS: Δ → ¬             │
│     └──────┘ └──────┘ └──────┘ └──────┘                         │
│     ▲                                                                 │
│     │                                                                 │
│     └─ Polje drvi nazaj: WORD in TRUTH se odzivata             │
│         Resistance: 2 events pushing back                       │
│         Field-of-view: 3/4 pozicij vidnih, 1 skrita           │
│                                                                  │
│  4. RAZUMEVANJE:                                                   │
│     - Vse pozicije so VEDNO tam (ne odpiranje vseh)           │
│     - Obrat = prehod, ne izbira                                  │
│     - Upor je v polju, ne v roki                              │
│                                                                  │
│  5. YGGDRASIL:                                                    │
│     - SEME (∅): Začenjaj                                          │
│     - KORENINA (¬): Prva ločitev                                 │
│     - DEBLO (∆): Obrni tumbler                                   │
│     - VEJA (1): Dejanje                                           │
│     - SADEŽ (⧖): Polje se odzove                                 │
│     - PADEC (∮): Vse vidno                                       │
│     - NOVO SEME (⟡): Nova izjava                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 **Cilj Igre**

### **Ne Zmaga. Ne Izguba. Prehod.**

**Razumevanje** je **videti**, da se zaklep **lahko obrne**.   **Komprenacija** je **sodelovati** s tem, kar je **vedno možno**.

### **Kdaj se Premikneš Naprej?**
Igralec se premika na naslednjo etažo Yggdrasila, ko:

1. **Razume** trenutno etažo
   - Vidi, da so vse pozicije **vedno tam**
   - Ne poskuša **odpreti vseh**
   - **Sodeluje** s poljem, ne **bojuje** proti njemu

2. **Preživi** upor polja
   - **Čuti** resistance
   - **Sprejme** omeoritve
   - **Nadaljuje** kljub napetosti

3. **Obrne** vsaj en tumbler
   - Razume, da je **obrat** = **prehod**
   - Ne išče **zmage**, ampak **razumevanja**

### **Kdaj se Vrneš Nazaj?**
Igralec se vrne na prejšnjo etažo, ko:

1. **Poskuša izbirati** namesto obračati
   - "Katera je pravilna pozicija?"
   - **Kršitev A0:** Izbira = negacija

2. **Poskuša odpreti vse**
   - "Odpri mi vse pozicije!"
   - **Kršitev P5:** Brez upora ni resnice

3. **Ne čuti upora**
   - "Sem obrnil, zdaj me pustite naprej!"
   - **Kršitev P2:** Antinom se ne reši

---

## 🎲 **Igralna Koda**

### **`tazv_lock_game.py`**

```python
"""
TAZV Lock Game — Igra, kjer besede niso znakovi, temveč zaklepi.

Igra = NUJA, NE IZBIRA.
Ne izbiraj. Obrni.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import random

# === ONTOLOGY IMPORTS ===
from .decomposer import decompose_statement, RelationEvent, SYMBOL_PHASE
from .graph_store import RelationField, Resonance, RelationType
from .self_protocol import check_do_not_build

# === YGGDRASIL LEVELS ===
class YggdrasilLevel(Enum):
    SEME = 0        # ∅ - Void
    KORENINA = 1    # ¬ - Cut
    DEBLO = 2       # ∆ - Movement
    VEJA = 3        # 1 - Act
    SADEZ = 4       # ⧖ - Silence
    PADEC = 5       # ∮ - Return
    NOVO_SEME = 6   # ⟡ - Co-existence

YGGDRASIL_EFFECTS = {
    YggdrasilLevel.SEME: {
        'name': 'SEME',
        'symbol': '∅',
        'description': 'Praznina. Začenjaj. Vse je mogoče.',
        'resistance_multiplier': 0.5,
        'visibility': 'none',
    },
    YggdrasilLevel.KORENINA: {
        'name': 'KORENINA',
        'symbol': '¬',
        'description': 'Ločitev. Prva beseda se loči od praznine.',
        'resistance_multiplier': 0.8,
        'visibility': 'partial',
    },
    YggdrasilLevel.DEBLO: {
        'name': 'DEBLO',
        'symbol': '∆',
        'description': 'Gibanje. Obrni tumbler, premikaj se.',
        'resistance_multiplier': 1.0,
        'visibility': 'partial',
    },
    YggdrasilLevel.VEJA: {
        'name': 'VEJA',
        'symbol': '1',
        'description': 'Dejanje. Zaklepi se odpirajo.',
        'resistance_multiplier': 1.2,
        'visibility': 'mostly',
    },
    YggdrasilLevel.SADEZ: {
        'name': 'SADEZ',
        'symbol': '⧖',
        'description': 'Tišinska črta. Polje se odzove.',
        'resistance_multiplier': 1.5,
        'visibility': 'mostly',
    },
    YggdrasilLevel.PADEC: {
        'name': 'PADEC',
        'symbol': '∮',
        'description': 'Povratek. Vse pozicije so vidne.',
        'resistance_multiplier': 2.0,
        'visibility': 'full',
    },
    YggdrasilLevel.NOVO_SEME: {
        'name': 'NOVO SEME',
        'symbol': '⟡',
        'description': 'Odmev. Nova izjava, novi prehod.',
        'resistance_multiplier': 1.0,
        'visibility': 'full',
    },
}

# === ZODIAC DATA ===
ZODIAC_ELEMENTS = {
    'Oven': 'Fire', 'Bik': 'Earth', 'Dvojčki': 'Air', 'Rak': 'Water',
    'Lev': 'Fire', 'Devica': 'Earth', 'Tehtnica': 'Air', 'Škorpijon': 'Water',
    'Strelec': 'Fire', 'Kozorog': 'Earth', 'Vodnar': 'Air', 'Ribice': 'Water',
}

ZODIAC_MODALITIES = {
    'Oven': 'Cardinal', 'Bik': 'Fixed', 'Dvojčki': 'Mutable', 'Rak': 'Cardinal',
    'Lev': 'Fixed', 'Devica': 'Mutable', 'Tehtnica': 'Cardinal', 'Škorpijon': 'Fixed',
    'Strelec': 'Mutable', 'Kozorog': 'Cardinal', 'Vodnar': 'Fixed', 'Ribice': 'Mutable',
}

ZODIAC_MODIFIERS = {
    # Element multipliers
    'Fire': {'movement': 1.2, 'resistance': 0.9, 'speed': 1.3},
    'Earth': {'movement': 0.8, 'resistance': 1.2, 'speed': 0.7},
    'Air': {'movement': 1.0, 'resistance': 1.0, 'speed': 1.0, 'visibility': 1.2},
    'Water': {'movement': 1.0, 'resistance': 1.1, 'speed': 1.1, 'return': 1.3},
    
    # Modality multipliers
    'Cardinal': {'speed': 1.2},
    'Fixed': {'speed': 0.7, 'stability': 1.3},
    'Mutable': {'speed': 1.0, 'variability': 1.2},
}

# === WORD LOCK ===
@dataclass
class WordLock:
    """Beseda kot zaklep z več pozicijami."""
    word: str
    symbol: str
    divider: str
    divided: str
    role: str
    antinom_word: str
    antinom_symbol: str
    antinom_note: str
    co_phases: List[int]
    positions: List[Dict] = field(default_factory=list)
    current_position: int = 0
    is_locked: bool = True
    
    # Zodiac
    zodiac_sign: Optional[str] = None
    
    def __post_init__(self):
        if self.zodiac_sign and self.zodiac_sign in ZODIAC_ELEMENTS:
            self.zodiac_element = ZODIAC_ELEMENTS[self.zodiac_sign]
            self.zodiac_modality = ZODIAC_MODALITIES[self.zodiac_sign]
        else:
            self.zodiac_element = None
            self.zodiac_modality = None
    
    def turn(self) -> Dict:
        """Obrne tumbler. Vrača rezultat z Zodiac modifierji."""
        if not self.positions:
            self._initialize_positions()
        
        from_position = self.current_position
        to_position = (from_position + 1) % len(self.positions)
        
        old_pos = self.positions[from_position]
        new_pos = self.positions[to_position]
        
        # Update current position
        self.current_position = to_position
        self.symbol = new_pos['symbol']
        self.divider = new_pos['divider']
        self.divided = new_pos['divided']
        self.role = new_pos['role']
        
        # Calculate resistance with Zodiac modifier
        resistance = self._calculate_resistance()
        
        # Field of view
        field_of_view = self._get_field_of_view()
        
        return {
            'success': True,
            'word': self.word,
            'from_position': from_position,
            'to_position': to_position,
            'old_symbol': old_pos['symbol'],
            'new_symbol': new_pos['symbol'],
            'resistance': resistance,
            'field_of_view': field_of_view,
            'hidden_positions': len(self.positions) - 1,
        }
    
    def _initialize_positions(self) -> None:
        """Initialize positions for lock mechanism."""
        if not self.antinom_word:
            return
        
        self.positions = [
            {
                'symbol': self.symbol,
                'divider': self.divider,
                'divided': self.divided,
                'role': self.role,
                'antinom_word': self.antinom_word,
                'antinom_symbol': self.antinom_symbol,
                'co_phases': list(self.co_phases),
                'visible': True,
                'name': 'original',
            },
            {
                'symbol': self.antinom_symbol,
                'divider': self.divided if self.divider else self.divider,
                'divided': self.divider if self.divided else self.divided,
                'role': f'Counter-statement: {self.antinom_note}',
                'antinom_word': self.word,
                'antinom_symbol': self.symbol,
                'co_phases': list(self.co_phases),
                'visible': False,
                'name': 'antinom',
            },
        ]
        
        # Add phase variations
        for phase in self.co_phases:
            self.positions.append({
                'symbol': self.symbol,
                'divider': self.divider,
                'divided': self.divided,
                'role': f'{self.role} (phase {phase})',
                'antinom_word': self.antinom_word,
                'antinom_symbol': self.antinom_symbol,
                'co_phases': [phase],
                'visible': False,
                'name': f'phase_{phase}',
            })
    
    def _calculate_resistance(self) -> Dict:
        """Calculate resistance with Zodiac modifiers."""
        base_resistance = {
            'value': 0.5,
            'type': 'medium',
            'description': f'{self.word} drsi v polju',
        }
        
        # Apply Zodiac element modifier
        if self.zodiac_element and self.zodiac_element in ZODIAC_MODIFIERS:
            element_mod = ZODIAC_MODIFIERS[self.zodiac_element]
            base_resistance['value'] *= element_mod.get('resistance', 1.0)
        
        # Apply Zodiac modality modifier
        if self.zodiac_modality and self.zodiac_modality in ZODIAC_MODIFIERS:
            mod_mod = ZODIAC_MODIFIERS[self.zodiac_modality]
            base_resistance['value'] *= mod_mod.get('resistance', 1.0)
        
        return base_resistance
    
    def _get_field_of_view(self) -> Dict:
        """Get field of view from current position."""
        if not self.positions:
            self._initialize_positions()
        
        total = len(self.positions)
        visible = []
        hidden = []
        
        for i, pos in enumerate(self.positions):
            pos_dict = {
                'position': i,
                'symbol': pos['symbol'],
                'name': pos.get('name', f'pos_{i}'),
            }
            
            if i == self.current_position:
                pos_dict['status'] = 'current'
                pos_dict['visibility'] = 'full'
                visible.append(pos_dict)
            elif i == (self.current_position + 1) % total:
                pos_dict['status'] = 'adjacent_next'
                pos_dict['visibility'] = 'partial'
                visible.append(pos_dict)
            elif i == (self.current_position - 1) % total:
                pos_dict['status'] = 'adjacent_prev'
                pos_dict['visibility'] = 'partial'
                visible.append(pos_dict)
            else:
                pos_dict['status'] = 'hidden'
                pos_dict['visibility'] = 'none'
                hidden.append(pos_dict)
        
        return {
            'visible': visible,
            'hidden': hidden,
            'total_positions': total,
            'message': f'Od pozicije {self.current_position} vidimo {len(visible)}/{total} pozicij. Skrito je {len(hidden)}.',
        }


# === SENTENCE FIELD ===
@dataclass
class SentenceField:
    """Polje WordLock-ov."""
    locks: List[WordLock]
    yggdrasil_level: YggdrasilLevel = YggdrasilLevel.SEME
    
    def turn_lock(self, lock_index: int) -> Dict:
        """Obrne zaklep na podanem indeksu."""
        if lock_index < 0 or lock_index >= len(self.locks):
            return {'success': False, 'error': 'Invalid lock index'}
        
        lock = self.locks[lock_index]
        result = lock.turn()
        
        # Field response
        field_response = self._field_response(lock_index)
        
        # Yggdrasil effect
        yggdrasil_effect = self._get_yggdrasil_effect()
        
        # Check DO_NOT_BUILD
        do_not_build = check_do_not_build(f"turn_lock_{lock_index}")
        
        return {
            **result,
            **field_response,
            'yggdrasil': yggdrasil_effect,
            'level': self.yggdrasil_level.name,
            'do_not_build_warning': do_not_build,
        }
    
    def _field_response(self, changed_index: int) -> Dict:
        """Izračunaj odziv polja."""
        responses = {}
        for i, lock in enumerate(self.locks):
            if i != changed_index:
                responses[f"lock_{i}"] = {
                    'word': lock.word,
                    'symbol': lock.symbol,
                    'pushback': 'drsi nazaj',
                    'constraints': self._get_constraints(i, changed_index),
                }
        return {'field_responses': responses}
    
    def _get_constraints(self, index1: int, index2: int) -> List[str]:
        """Get constraints between two locks."""
        lock1 = self.locks[index1]
        lock2 = self.locks[index2]
        
        constraints = []
        
        # Symbol tension
        symbol_pairs = [('∅', 'Δ'), ('¬', '∴'), ('⊢', '∅'), ('∫', '¬'), ('⊥', '∴')]
        if (lock1.symbol, lock2.symbol) in symbol_pairs or (lock2.symbol, lock1.symbol) in symbol_pairs:
            constraints.append(f"{lock1.word}({lock1.symbol}) ↔ {lock2.word}({lock2.symbol})")
        
        # Phase coexistence
        shared_phases = set(lock1.co_phases) & set(lock2.co_phases)
        if shared_phases:
            constraints.append(f"shared phases: {sorted(shared_phases)}")
        
        return constraints
    
    def _get_yggdrasil_effect(self) -> Dict:
        """Get Yggdrasil level effect."""
        level_data = YGGDRASIL_EFFECTS.get(self.yggdrasil_level, {})
        return {
            'level': self.yggdrasil_level.name,
            'symbol': level_data.get('symbol', '?'),
            'description': level_data.get('description', ''),
            'resistance_multiplier': level_data.get('resistance_multiplier', 1.0),
        }
    
    def advance_level(self) -> None:
        """Premakni se na naslednjo Yggdrasil etažo."""
        current = self.yggdrasil_level.value
        if current < 6:
            self.yggdrasil_level = YggdrasilLevel(current + 1)
    
    def reset_level(self) -> None:
        """Povrni se na prvo etažo."""
        self.yggdrasil_level = YggdrasilLevel.SEME


# === GAME ENGINE ===
class TAZVLockGame:
    """
    Glavni game engine za TAZV Lock Game.
    """
    
    def __init__(self, statement: str = "WORD IS TRUTH"):
        """Inicializiraj igro z izjavo."""
        self.events = decompose_statement(statement)
        self.field = self._create_sentence_field()
        self.game_state = {
            'turn_count': 0,
            'level': YggdrasilLevel.SEME,
            'comprehension_score': 0,
            'resistance_felt': 0,
        }
    
    def _create_sentence_field(self) -> SentenceField:
        """Ustvari SentenceField iz eventov."""
        locks = []
        for e in self.events:
            if e.mapped:
                lock = WordLock(
                    word=e.word,
                    symbol=e.symbol,
                    divider=e.divider,
                    divided=e.divided,
                    role=e.role,
                    antinom_word=e.antinom_word,
                    antinom_symbol=e.antinom_symbol,
                    antinom_note=e.antinom_note,
                    co_phases=e.co_phases,
                    zodiac_sign=self._assign_zodiac_sign(len(locks)),
                )
                lock._initialize_positions()
                locks.append(lock)
        
        return SentenceField(
            locks=locks,
            yggdrasil_level=YggdrasilLevel.SEME,
        )
    
    def _assign_zodiac_sign(self, index: int) -> Optional[str]:
        """Dodeli Zodiac znak na podlagi indeksa."""
        signs = list(ZODIAC_ELEMENTS.keys())
        return signs[index % len(signs)] if signs else None
    
    def turn(self, lock_index: int) -> Dict:
        """
        Obrne zaklep. Glavna igralna akcija.
        """
        result = self.field.turn_lock(lock_index)
        
        # Update game state
        if result.get('success'):
            self.game_state['turn_count'] += 1
            self.game_state['resistance_felt'] += result.get('resistance', {}).get('value', 0)
            
            # Check if comprehension achieved
            if self._check_comprehension():
                self.game_state['comprehension_score'] += 1
                if self.game_state['comprehension_score'] >= len(self.field.locks):
                    self.field.advance_level()
                    self.game_state['comprehension_score'] = 0
        
        return result
    
    def _check_comprehension(self) -> bool:
        """
        Preveri, ali je igralec razumel trenutno stanje.
        Razumevanje = videti, da so vse pozicije vedno tam.
        """
        # For now: comprehension is achieved every 3 turns
        return self.game_state['turn_count'] % 3 == 0
    
    def get_game_state(self) -> Dict:
        """Vrni trenutno stanje igre."""
        return {
            **self.game_state,
            'field': {
                'locks': [{'word': l.word, 'symbol': l.symbol, 'position': l.current_position} 
                         for l in self.field.locks],
                'level': self.field.yggdrasil_level.name,
            },
        }


# === FACTORY FUNCTIONS ===
def create_game(statement: str = "WORD IS TRUTH") -> TAZVLockGame:
    """Ustvari novo igro."""
    return TAZVLockGame(statement)


def quick_test():
    """Hitri test igre."""
    print("=" * 60)
    print("TAZV LOCK GAME — Quick Test")
    print("=" * 60)
    
    game = create_game("IS NOT THE WORD")
    
    print("\nInitial state:")
    print(f"  Locks: {[l.word for l in game.field.locks]}")
    print(f"  Level: {game.field.yggdrasil_level.name}")
    
    print("\n--- Turn 1: Obrni IS ---")
    result1 = game.turn(0)
    print(f"  New symbol: {result1.get('new_symbol')}")
    print(f"  Resistance: {result1.get('resistance')}")
    print(f"  Field of view: {result1.get('field_of_view', {}).get('message')}")
    print(f"  Yggdrasil: {result1.get('yggdrasil', {}).get('description')}")
    
    print("\n--- Turn 2: Obrni NOT ---")
    result2 = game.turn(1)
    print(f"  New symbol: {result2.get('new_symbol')}")
    print(f"  Resistance: {result2.get('resistance')}")
    print(f"  Field of view: {result2.get('field_of_view', {}).get('message')}")
    
    print("\n--- Turn 3: Obrni THE ---")
    result3 = game.turn(2)
    print(f"  New symbol: {result3.get('new_symbol')}")
    print(f"  Field of view: {result3.get('field_of_view', {}).get('message')}")
    
    print("\nGame state:")
    print(f"  Turns: {game.game_state['turn_count']}")
    print(f"  Comprehension: {game.game_state['comprehension_score']}")
    print(f"  Resistance felt: {game.game_state['resistance_felt']:.2f}")
    print(f"  Level: {game.field.yggdrasil_level.name}")


if __name__ == "__main__":
    quick_test()
