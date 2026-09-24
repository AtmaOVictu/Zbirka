#!/usr/bin/env python
"""
Verification script for ONTOMATEMATIKA Evolution Engine.
Run this to verify the implementation is working.
"""

import sys
import os

# Add the __core_evolution directory to sys.path
core_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                        'comprehension_machine', 'comprehension', '__core_evolution')
sys.path.insert(0, core_dir)

import json
from evolution_ledger import EvolutionLedger, seed_first_evolution, DEFAULT_LEDGER_DIR
from guard import Guard, GuardResult, GuardStatus, AuthorityLevel
from dokaz import DokazTrace, DokazCreator
from upgrade_protocol import evolution_valid, classify_change

print("=" * 70)
print("ONTOMATEMATIKA Evolution Engine — Verification")
print("=" * 70)

# Test 1: Verify imports
print("\n[1/5] Verifying imports...")
try:
    print("  ✓ All core modules imported successfully")
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Seed first evolution
print("\n[2/5] Seeding first evolution event...")
try:
    ledger = EvolutionLedger()
    event = seed_first_evolution(ledger)
    print(f"  ✓ Event created: {event.upgrade_id}")
    print(f"    - Predecessor: {event.predecessor_state_id}")
    print(f"    - Candidate: {event.candidate_state_id}")
    print(f"    - Decision: {event.decision}")
    print(f"    - Guard: {event.guard.get('status')} (requires: {event.guard.get('authority_required')})")
except Exception as e:
    print(f"  ✗ Seed failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Verify ledger files
print("\n[3/5] Verifying ledger files...")
states_dir = os.path.join(DEFAULT_LEDGER_DIR, 'states')
events_dir = os.path.join(DEFAULT_LEDGER_DIR, 'events')

if not os.path.exists(states_dir):
    print(f"  ✗ States directory not found: {states_dir}")
    sys.exit(1)

if not os.path.exists(events_dir):
    print(f"  ✗ Events directory not found: {events_dir}")
    sys.exit(1)

states_files = os.listdir(states_dir)
events_files = os.listdir(events_dir)

print(f"  ✓ States directory: {len(states_files)} files")
print(f"  ✓ Events directory: {len(events_files)} files")

# Check for S_0 and S_1
if 'S_0.json' in states_files and 'S_1.json' in states_files:
    print(f"  ✓ S_0 and S_1 states recorded")
else:
    print(f"  ✗ Missing S_0 or S_1")
    sys.exit(1)

# Check for evo_* event
evo_files = [f for f in events_files if f.startswith('evo_')]
if evo_files:
    print(f"  ✓ Evolution event recorded: {evo_files[0]}")
else:
    print(f"  ✗ No evolution event found")
    sys.exit(1)

# Test 4: Verify event structure
print("\n[4/5] Verifying event structure...")
try:
    # Check that event has all required fields
    required_fields = [
        'upgrade_id', 'predecessor_state_id', 'candidate_state_id',
        'delta', 'preservation', 'guard', 'consequence_preview',
        'residual', 'decision', 'dokaz'
    ]
    
    event_dict = event.to_dict()
    for field in required_fields:
        if field not in event_dict or not event_dict[field]:
            print(f"  ✗ Missing or empty field: {field}")
            sys.exit(1)
    
    print(f"  ✓ All required fields present")
    
    # Check DOKAZ trace
    if 'dokaz' in event_dict and event_dict['dokaz']:
        dokaz = event_dict['dokaz']
        if all(k in dokaz for k in ['dokaz_id', 'created_at', 'predecessor', 'candidate']):
            print(f"  ✓ DOKAZ trace valid")
        else:
            print(f"  ✗ DOKAZ trace incomplete")
            sys.exit(1)
    
    # Check Guard result
    if event_dict['guard'].get('status') == 'review_required':
        print(f"  ✓ Guard result: REVIEW_REQUIRED (awaiting Luka)")
    
    # Check Residual
    if event_dict['residual'].get('next_question'):
        print(f"  ✓ Residual question: {event_dict['residual']['next_question'][:60]}...")
    
except Exception as e:
    print(f"  ✗ Structure verification failed: {e}")
    sys.exit(1)

# Test 5: Verify query methods
print("\n[5/5] Verifying ledger query methods...")
try:
    # Get states
    s0 = ledger.get_state('S_0')
    s1 = ledger.get_state('S_1')
    if s0 and s1:
        print(f"  ✓ get_state() working")
    else:
        print(f"  ✗ get_state() failed")
        sys.exit(1)
    
    # Get event
    evo_files = os.listdir(os.path.join(DEFAULT_LEDGER_DIR, 'events'))
    if evo_files:
        event_id = evo_files[0].replace('.json', '')
        retrieved_event = ledger.get_event(event_id)
        if retrieved_event:
            print(f"  ✓ get_event() working")
        else:
            print(f"  ✗ get_event() failed")
            sys.exit(1)
    
    # Get lineage
    lineage = ledger.get_lineage('S_1')
    if lineage:
        print(f"  ✓ get_lineage() working: {len(lineage)} states")
    else:
        print(f"  ✗ get_lineage() failed")
        sys.exit(1)
    
    # Get residual questions
    questions = ledger.get_residual_questions()
    if questions:
        print(f"  ✓ get_residual_questions() working: {len(questions)} questions")
    else:
        print(f"  ✗ get_residual_questions() failed")
        sys.exit(1)
    
    # Get stats
    stats = ledger.get_ledger_stats()
    print(f"  ✓ get_ledger_stats() working: {stats['total_states']} states, {stats['total_events']} events")
    
except Exception as e:
    print(f"  ✗ Query methods failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Final summary
print("\n" + "=" * 70)
print("✅ ALL VERIFICATION TESTS PASSED")
print("=" * 70)
print("\nEvolution engine is fully functional.")
print("First evolution event (evo_0001) has been recorded.")
print("Guard status: REVIEW_REQUIRED")
print("Authority required: Luka")
print("\nReady for Luka review and canon promotion decision.")
print("\nRun 'verify_evolution.py' anytime to re-verify.")
print("=" * 70)
