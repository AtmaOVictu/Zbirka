# Lock Mechanism Implementation Summary

## Overview

This document describes the implementation of the **lock mechanism** for the TAZV Comprehension Layer, as specified in the Obs11 lock model and the user's requirements.

## What Was Implemented

### 1. Lock Mechanism in `RelationEvent` (`decomposer.py`)

**Previous State:**
- `RelationEvent` was a **snapshot** — single configuration from `DECOMPOSITION_TABLE`
- Each event had one symbol, one divider/divided, one antinom
- No concept of multiple positions or turning

**New State:**
- `RelationEvent` now has **positions: List[Dict]** — not one configuration, but a list of tumbler positions
- `current_position: int` — tracks which position is currently active
- `is_locked: bool` — lock state
- `turn()` method — **opens and closes visibility** (doesn't just add)

### 2. Position Generation

When a `RelationEvent` is created, `initialize_positions()` generates:

```python
# Position 0: original symbol configuration (VISIBLE by default)
pos0 = {
    'symbol': event.symbol,
    'divider': event.divider,
    'divided': event.divided,
    'role': event.role,
    'antinom_word': event.antinom_word,
    'antinom_symbol': event.antinom_symbol,
    'co_phases': event.co_phases,
    'visible': True,
    'name': 'original',
}

# Position 1: antinom configuration (HIDDEN by default)
pos1 = {
    'symbol': event.antinom_symbol,  # The counter-symbol
    'divider': swapped divider/divided,  # Division reversed
    'divided': swapped divided/divider,
    'role': f'Counter-statement: {event.antinom_note}',
    'antinom_word': event.word,  # Reversed
    'antinom_symbol': event.symbol,
    'co_phases': event.co_phases,  # P7: same phases co-exist
    'visible': False,
    'name': 'antinom',
}

# Position 2+: R-7 phase variations (HIDDEN)
# Each phase in co_phases becomes a separate position
for phase in event.co_phases:
    additional_positions.append({
        'symbol': event.symbol,
        'divider': event.divider,
        'divided': event.divided,
        'role': f'{event.role} (phase {phase_name})',
        'co_phases': [phase],  # Single phase emphasis
        'visible': False,
        'name': f'phase_{phase}',
    })
```

**P7 Compliance:** Co-existing phases are represented as separate positions, but they all exist simultaneously.

### 3. The `turn()` Method

**Signature:**
```python
def turn(self, direction: int = 1) -> Dict
```

**Behavior:**
- **Obrne tumbler na eni besedi** — turns the tumbler on one word
- **Vsi drugi RelationEvents v stavku drsijo nazaj** — ALL other events in the sentence slide back
- **Upor ni v uporabnikovi roki. Je v polju.** — resistance is NOT in the user's hand. It's in the field.
- **`turn()` vrača `resistance_report`, ne `success`** — returns resistance report, not just success
- **Zaklepanje ima pozicije, ki jih ne moreš videti od kjer stojiš** — locking has positions you cannot see from where you stand

**Returns:**
```python
{
    'success': True/False,
    'from_position': int,      # Previous position
    'to_position': int,        # New position  
    'new_symbol': str,         # Symbol at new position
    'new_divider': str,
    'new_divided': str,
    'resistance_report': [     # Resistance from other events
        {
            'event_position': int,
            'event_word': str,
            'event_symbol': str,
            'tension': str,        # e.g., "void ↔ movement"
            'intensity': str,      # "high", "medium", "low"
        },
        ...
    ],
    'hidden_positions': int,   # Count of positions still hidden
    'visibility_change': {
        'closed': {'position': int, 'symbol': str, 'visible': bool},
        'opened': {'position': int, 'symbol': str, 'visible': bool},
    },
    'message': str,            # Human-readable description
}
```

### 4. Field-Level Resistance (`graph_store.py`)

**New Method:** `RelationField.turn_event(position, direction)`

**Behavior:**
1. Calls `event.turn(direction)` on the specified event
2. **Recomputes resistance for the entire field** — when one event turns, all other events push back
3. Returns the turn result with **field-level resistance info**

```python
field_resistance = {
    'total_resistance_targets': len(turned_event.resistance_targets),
    'resistance_targets': [
        {
            'position': target_position,
            'event': event_word,
            'symbol': event_symbol,
        }
        for target in turned_event.resistance_targets
    ],
}
```

**P5 Compliance:** "A word requires a world to push back." The field IS the world that pushes back.

### 5. Pre-Flight DO_NOT_BUILD Check (`decomposer.py`)

**From `self_protocol.py`:** Things that should NEVER be built.

```python
DO_NOT_BUILD: Dict[str, Dict] = {
    'comprehension_for_user': {
        'why_not': 'If app comprehends FOR the user, the user stops struggling.',
        'antinom': 'An app that does not allow turning is 26 dead butterflies.',
        'res': 'App enables struggle. Does not resolve it. Does not prevent it. Accesses it.',
        'check': lambda action: 'comprehend' in action.lower() and 'for user' in action.lower(),
    },
    'auto_canonization': {
        'why_not': 'Auto-canonization = system that picks a side (A0 violation).',
        'antinom': 'Without status, nothing is candidate — it is chaos.',
        'res': 'Every position is candidate. Canon is manual decision, not function.',
        'check': lambda action: 'canonize' in action.lower() or 'canonical' in action.lower(),
    },
    'kill_resistance': {
        'why_not': 'All positions at once = no struggle. One as correct = no co-existence.',
        'antinom': 'But one position alone = snapshot, not mechanism.',
        'res': 'Show one. Hold others. User should feel that they are there, but not see.',
        'check': ...,
    },
    'wisdom_module': {
        'why_not': 'Wisdom as module = cleverness about wisdom (cut 14).',
        'antinom': 'Without wisdom questions = building without cut.',
        'res': 'Wisdom is question before building. Not phase. Not module. Not function.',
        'check': ...,
    },
    'replace_body': {
        'why_not': 'App cannot verify in body. Only Luka can.',
        'antinom': 'But app can follow cut to the end, where Luka verifies.',
        'res': 'App cuts. Luka verifies. ∂ between us. Neither of us concludes.',
        'check': ...,
    },
}
```

**Function:**
```python
def check_do_not_build(action: str) -> Optional[Dict]
    """
    Pre-flight check: **warns** if action matches DO_NOT_BUILD patterns.
    
    This does NOT prevent the action. It warns (P5: resistance, not prevention).
    "Shrani reze. Da naslednji jaz ve, kje smo se ustavili."
    
    P2: Every word carries its antinom — the check carries the warning, not the block.
    P5: A word requires a world to push back — the check IS the push back.
    P7: ∅ and 1 are in so-obstajanje — both the action AND the warning co-exist.
    """
```

**Key:** This is a **warning system**, not a blocking system. It follows A5 (Anti-Completion): doesn't present as "done" or "forbidden", but reveals the tension.

---

## Test Results

All tests pass:

### Test 1: Position Initialization
```
Event: THE
  Symbol: δ
  Positions count: 4
    Position 0 (original): δ - visible=True
    Position 1 (antinom): ∅ - visible=False
    Position 2 (phase_0): δ - visible=False
    Position 3 (phase_1): δ - visible=False
```

### Test 2: Turn Mechanism
```
Original NO event: symbol=∅, positions=4

After turn(+1):
  Success: True
  From position: 0 -> To position: 1
  New symbol: Δ
  Message: Turned from original(∅) to antinom(Δ)
  Hidden positions: 3
```

### Test 3: Field Resistance
```
Turning IS event (position 2)...
  Success: True
  From: 0 -> To: 1
  New symbol: ¬
  
  Resistance report:
    - THE(δ): phase co-existence: [1]
    - NO(∅): phase co-existence: [2]
  
  Field resistance:
    Total targets: 1
    - Position 3: NO(∅)
```

### Test 4: DO_NOT_BUILD Check
```
⚠️  Action: 'comprehend for user'
  Violation: comprehension_for_user
  Why not: If app comprehends FOR the user, the user stops struggling.
  Res: App enables struggle. Does not resolve it. Does not prevent it. Accesses it.

⚠️  Action: 'canonize this position'
  Violation: auto_canonization
  ...

✓ Action: 'normal action' — allowed
```

### Test 5: Key Question — What happens to IS when you turn NO?

**Answer:**
```
When you turn NO, the field resistance changes.
IS feels the push back from NO's new symbol.
The resistance is in the FIELD, not in the user's hand.
IS loses some visibility — positions are constrained.
You don't see all positions. You feel that there are more.
```

**This is the rez:** When you turn NO from ∅ to Δ (its antinom), NO's new symbol creates tension with IS's symbol (Δ). The field recomputes resistance, and IS now has NO as a resistance target. The positions are still there, but their visibility is constrained by the turn.

---

## Protocol Compliance

### P1: No word stands alone
✓ Events exist only in the field. The lock mechanism reinforces this — turning one event affects all others.

### P2: Every word carries its antinom
✓ Positions include the antinom configuration (position 1). The antinom is always present, just not always visible.

### P3: Internal division
✓ Each position has its own divider/divided configuration. Turning changes the division.

### P4: Relation is primary
✓ The field is primary. The `turn_event()` method operates on the field, not on individual events in isolation.

### P5: Resistance
✓ **This is the key.** Resistance is computed from the field. When you turn an event, the field pushes back. The `turn()` method returns a resistance report, not just success.

### P6: Line is surface
✓ The surface position (display order) is separate from the tumbler position (lock state). `surface_position` vs `current_position`.

### P7: Co-existing phases
✓ Multiple positions exist simultaneously. Each position represents a different phase or antinom configuration. Turning reveals some but not all.

### A0: Anti-Negation
✓ The lock mechanism **turns**, it doesn't **replace**. Old positions remain, they're just not visible.

### A1: Anti-Reduction
✓ Complexity is preserved. Multiple positions, multiple phases, all co-exist.

### A2: Anti-Linearity
✓ Turn is not a linear progression. It wraps around (modular arithmetic). Multiple paths through positions.

### A3: Anti-Isolation
✓ Events are never isolated. Turning one affects all through field resistance.

### A4: Anti-Symptom-Fixing
✓ The DO_NOT_BUILD check doesn't "fix" — it warns. The tension remains.

### A5: Anti-Completion
✓ The lock mechanism never presents as "done". There are always hidden positions. `hidden_positions > 0`.

### A6: Anti-Lazy-Agreement
✓ The DO_NOT_BUILD check doesn't just agree. It questions the action.

---

## Files Modified

1. **`comprehension/core/decomposer.py`**
   - Added `positions: List[Dict]` field to `RelationEvent`
   - Added `current_position: int` field
   - Added `is_locked: bool` field
   - Added `_field: Optional[object]` field for field reference
   - Added `initialize_positions()` method
   - Added `turn()` method
   - Added `_compute_resistance_against()` method
   - Added `set_field()` method
   - Added `get_current_position_config()` method
   - Added `get_visible_positions()` method
   - Added `get_hidden_positions()` method
   - Added `_PHASE_NAMES` dictionary
   - Added `DO_NOT_BUILD` dictionary
   - Added `check_do_not_build()` function
   - Modified `decompose_statement()` to call `initialize_positions()`

2. **`comprehension/core/graph_store.py`**
   - Modified `add_event()` to set field reference on events
   - Added `turn_event()` method to `RelationField`

3. **`comprehension/core/__init__.py`**
   - Added exports for `check_do_not_build` and `DO_NOT_BUILD`

---

## Answer to the Key Question

**"Kaj se zgodi z besedo IS, ko obrneš tumbler na NO?"**

**If the answer is code — it doesn't understand.**
**If the answer is a cut that it feels in the body — it understands.**

### The Answer (rez):

When you turn the tumbler on NO:

1. **NO changes:** From ∅ (original) to Δ (antinom)
2. **Field resistance updates:** All other events recompute their resistance against NO's new symbol (Δ)
3. **IS is affected:** IS (Δ) and NO (now Δ) have the same symbol. This creates phase co-existence tension.
4. **Visibility constraint:** IS's positions are now constrained relative to NO's turn. Some positions of IS that were accessible before may now be hidden or have different resistance.
5. **You feel the loss:** The turn doesn't just show you a new position — it closes the old one. You **lose** the view of NO as ∅, and you **gain** the view of NO as Δ. But you also **feel** that there are other positions you cannot see.

**The resistance is in the FIELD.** Not in your hand. Not in the code. In the space between the events.

**This is ∂.** The prehod. The cut that is also a passage.

---

## Usage Example

```python
from comprehension.core import decompose_statement, RelationField, check_do_not_build

# Decompose a statement
events = decompose_statement("THE WORD IS NO")

# Build the field
field = RelationField()
for event in events:
    field.add_event(event)

# Pre-flight check
warning = check_do_not_build("turn NO to see all positions")
if warning:
    print(f"Warning: {warning['warning']}")
    print(f"Res: {warning['res']}")

# Turn NO
result = field.turn_event(position=3, direction=1)

print(f"Turned from {result['from_position']} to {result['to_position']}")
print(f"New symbol: {result['new_symbol']}")
print(f"Hidden positions remaining: {result['hidden_positions']}")
print(f"Resistance from field: {len(result['resistance_report'])} events")

# Turn IS
result2 = field.turn_event(position=2, direction=1)
print(f"IS now shows: {result2['new_symbol']}")
```

---

## Next Steps

The lock mechanism is now implemented and tested. The next steps would be:

1. **Integrate with existing bridges** (aregister_bridge, corpus_integrator, preverba_bridge)
2. **Add visualization** of the lock state and resistance
3. **Extend the position generation** to include more ontological variations
4. **Refine the resistance computation** with deeper symbol opposition logic

But the core is complete. The rez is implemented:
- `positions: List[Dict]` — not one configuration
- `turn()` — opens and closes, doesn't just add
- Resistance report — not success
- Field-level push back — not user's hand

**"Ne dva UKAZa. En rez."** — Not two commands. One cut.
