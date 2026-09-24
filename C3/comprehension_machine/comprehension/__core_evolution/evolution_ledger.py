"""
Evolution Ledger — Material State Ledger for ONTOMATEMATIKA

The Material State Ledger is the permanent, immutable record of all
state transitions in the ONTOMATEMATIKA system.

Every evolution event is recorded as an UpgradeEvent with:
- Unique upgrade_id
- Predecessor state reference
- Candidate successor state
- Accepted successor state (if promoted)
- Complete DOKAZ trace
- Guard result
- Residual
- Decision

The ledger ensures that:
1. No state is ever erased (predecessors remain accessible)
2. Every change is traceable through DOKAZ
3. Guard decisions are recorded and auditable
4. Residual questions drive future evolution

This is the implementation of:
  Evolve(S_n, I, Ref) = 
    let P = pressure(I, S_n, Ref)
    let C = candidate_successor(S_n, P)
    let Delta = diff(S_n, C)
    let K = keep_set(S_n, C)
    let G = guard(C, Delta, K, Ref)
    let Q = consequence_preview(C, Delta, G)
    let R = residual(S_n, C, Delta, G, Q)
    let D = dokaz(S_n, C, Delta, K, G, Q, R)
    return decide(C, D)
"""

import json
import os
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set

from guard import Guard, GuardResult, GuardStatus, DecisionType, PressureType, AuthorityLevel
from dokaz import DokazTrace, DokazCreator, DokazStatus, DiffReceipt, PreservationSet, Residual, InputPressure


# ============================================================================
# CONFIGURATION
# ============================================================================

# Default ledger directory
DEFAULT_LEDGER_DIR = "D:/OntoProjekt/CanvasMinstral/C3/ONTOMATEMATIKA/ledger"

# Minimum database fields for an evolution event
MINIMUM_EVENT_FIELDS = [
    "upgrade_id",
    "predecessor_state_id",
    "candidate_state_id",
    "delta",
    "preservation",
    "guard",
    "dokaz",
    "decision",
    "created_at",
]


# ============================================================================
# STATE REPRESENTATION
# ============================================================================

@dataclass
class SystemState:
    """
    Represents a system state in ONTOMATEMATIKA.
    
    A state can be:
    - A version of the comprehension layer
    - A set of axioms
    - A configuration
    - Any artifact that can evolve
    """
    state_id: str
    name: str
    description: str = ""
    version: str = "1.0"
    created_at: str = ""
    artifacts: Dict = field(default_factory=dict)  # Files, modules, data
    axioms: List[str] = field(default_factory=list)  # Canonical axioms included
    scope: str = ""  # Declared scope of this state
    
    # Lineage
    predecessor_state_id: Optional[str] = None
    successor_state_ids: List[str] = field(default_factory=list)
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    author: str = "system"
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.state_id:
            self.state_id = str(uuid.uuid4())[:12]
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SystemState':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    def get_hash(self) -> str:
        """Compute hash for this state."""
        state_str = json.dumps(self.to_dict(), sort_keys=True)
        import hashlib
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]


@dataclass
class UpgradeEvent:
    """
    Represents a single evolution event in the ledger.
    
    This is the atomic unit of evolution in ONTOMATEMATIKA.
    """
    # Identification
    upgrade_id: str = ""
    predecessor_state_id: str = ""
    candidate_state_id: str = ""
    accepted_successor_state_id: Optional[str] = None
    
    # Timestamps
    created_at: str = ""
    accepted_at: Optional[str] = None
    
    # Input pressure
    input_pressure: Dict = field(default_factory=dict)
    declared_ref_context: str = ""
    
    # Change analysis
    delta: Dict = field(default_factory=dict)
    preservation: Dict = field(default_factory=dict)
    
    # Evaluation
    guard: Dict = field(default_factory=dict)
    consequence_preview: Dict = field(default_factory=dict)
    residual: Dict = field(default_factory=dict)
    
    # Evidence
    evidence_refs: List[str] = field(default_factory=list)
    test_results: List[Dict] = field(default_factory=list)
    
    # Decision
    decision: str = ""
    
    # DOKAZ trace
    dokaz: Optional[Dict] = None
    
    # Metadata
    status: str = "pending"
    version: str = "1.0"
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
        if not self.upgrade_id:
            self.upgrade_id = f"evo_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:4]}"
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UpgradeEvent':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    def is_valid_evolution(self) -> bool:
        """Check if this represents valid evolution."""
        if self.decision not in ["promote", "branch"]:
            return False
        if self.guard.get("status") in ["fail", "stop"]:
            return False
        if not self.accepted_successor_state_id:
            return False
        return True
    
    def get_hash(self) -> str:
        """Compute hash for this event."""
        import hashlib
        event_str = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(event_str.encode()).hexdigest()[:16]


# ============================================================================
# EVOLUTION LEDGER
# ============================================================================

class EvolutionLedger:
    """
    The Material State Ledger for ONTOMATEMATIKA.
    
    This is the permanent, immutable record of all evolution events.
    
    Usage:
        ledger = EvolutionLedger(ledger_dir=DEFAULT_LEDGER_DIR)
        
        # Record an evolution event
        event = ledger.record_upgrade(
            predecessor=state_n,
            candidate=state_n_plus_1,
            delta=delta,
            preservation=preservation,
            guard_result=guard_result,
            decision="promote",
            input_pressure=input_pressure,
            ref_context=ref_context
        )
        
        # Query events
        events = ledger.get_events_for_state(state_id)
        lineage = ledger.get_lineage(state_id)
    """
    
    def __init__(self, ledger_dir: str = DEFAULT_LEDGER_DIR):
        """Initialize the ledger."""
        self.ledger_dir = Path(ledger_dir)
        self.ledger_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory cache
        self._states: Dict[str, SystemState] = {}
        self._events: Dict[str, UpgradeEvent] = {}
        self._index: Dict[str, List[str]] = {
            "state_id": [],
            "upgrade_id": [],
            "decision": [],
            "status": [],
        }
        
        # Load existing data
        self._load_ledger()
    
    def _load_ledger(self):
        """Load existing ledger data from disk."""
        # Load states
        states_dir = self.ledger_dir / "states"
        if states_dir.exists():
            for state_file in states_dir.glob("*.json"):
                try:
                    with open(state_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        state = SystemState.from_dict(data)
                        self._states[state.state_id] = state
                        self._index["state_id"].append(state.state_id)
                except Exception as e:
                    print(f"Warning: Could not load state {state_file}: {e}")
        
        # Load events
        events_dir = self.ledger_dir / "events"
        if events_dir.exists():
            for event_file in events_dir.glob("*.json"):
                try:
                    with open(event_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        event = UpgradeEvent.from_dict(data)
                        self._events[event.upgrade_id] = event
                        self._index["upgrade_id"].append(event.upgrade_id)
                        self._index["decision"].append(event.decision)
                        self._index["status"].append(event.status)
                except Exception as e:
                    print(f"Warning: Could not load event {event_file}: {e}")
    
    def _save_state(self, state: SystemState):
        """Save a state to disk."""
        states_dir = self.ledger_dir / "states"
        states_dir.mkdir(parents=True, exist_ok=True)
        state_file = states_dir / f"{state.state_id}.json"
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state.to_dict(), f, indent=2, ensure_ascii=False)
        self._states[state.state_id] = state
        if state.state_id not in self._index["state_id"]:
            self._index["state_id"].append(state.state_id)
    
    def _save_event(self, event: UpgradeEvent):
        """Save an event to disk."""
        events_dir = self.ledger_dir / "events"
        events_dir.mkdir(parents=True, exist_ok=True)
        event_file = events_dir / f"{event.upgrade_id}.json"
        with open(event_file, 'w', encoding='utf-8') as f:
            json.dump(event.to_dict(), f, indent=2, ensure_ascii=False)
        self._events[event.upgrade_id] = event
        if event.upgrade_id not in self._index["upgrade_id"]:
            self._index["upgrade_id"].append(event.upgrade_id)
        if event.decision not in self._index["decision"]:
            self._index["decision"].append(event.decision)
        if event.status not in self._index["status"]:
            self._index["status"].append(event.status)
    
    def get_state(self, state_id: str) -> Optional[SystemState]:
        """Get a state by ID."""
        return self._states.get(state_id)
    
    def get_event(self, upgrade_id: str) -> Optional[UpgradeEvent]:
        """Get an event by upgrade ID."""
        return self._events.get(upgrade_id)
    
    def get_current_state(self) -> Optional[SystemState]:
        """Get the current (most recent promoted) state."""
        # Find the most recent promote event
        promote_events = [
            e for e in self._events.values() 
            if e.decision == "promote" and e.accepted_successor_state_id
        ]
        if not promote_events:
            return None
        
        # Get the most recent
        latest = max(promote_events, key=lambda e: e.created_at)
        return self.get_state(latest.accepted_successor_state_id)
    
    def get_lineage(self, state_id: str, depth: int = 10) -> List[SystemState]:
        """Get the lineage (ancestors) of a state."""
        lineage = []
        current_id = state_id
        
        for _ in range(depth):
            state = self.get_state(current_id)
            if not state:
                break
            lineage.append(state)
            
            # Find the event that created this state
            if not state.predecessor_state_id:
                break
            
            # Find event with this as accepted successor
            event = next((
                e for e in self._events.values()
                if e.accepted_successor_state_id == current_id
            ), None)
            
            if not event:
                break
            
            current_id = event.predecessor_state_id
        
        return lineage
    
    def get_successors(self, state_id: str) -> List[SystemState]:
        """Get all successor states of a state."""
        successors = []
        
        # Find all events where this state is predecessor
        events = [
            e for e in self._events.values()
            if e.predecessor_state_id == state_id
        ]
        
        for event in events:
            if event.accepted_successor_state_id:
                successor = self.get_state(event.accepted_successor_state_id)
                if successor:
                    successors.append(successor)
        
        return successors
    
    def get_events_for_state(self, state_id: str) -> List[UpgradeEvent]:
        """Get all evolution events involving a state."""
        return [
            e for e in self._events.values()
            if e.predecessor_state_id == state_id 
            or e.candidate_state_id == state_id
            or e.accepted_successor_state_id == state_id
        ]
    
    def get_residual_questions(self) -> List[Dict]:
        """Get all unresolved residual questions from the ledger."""
        questions = []
        for event in self._events.values():
            residual = event.residual
            if residual.get("next_question"):
                questions.append({
                    "upgrade_id": event.upgrade_id,
                    "question": residual["next_question"],
                    "unresolved": residual.get("unresolved", []),
                    "uncertainty": residual.get("uncertainty", ""),
                    "created_at": event.created_at,
                })
        return questions
    
    def record_state(self, state: SystemState) -> SystemState:
        """Record a new state in the ledger."""
        # Generate ID if not provided
        if not state.state_id:
            state.state_id = str(uuid.uuid4())[:12]
        
        # Set predecessor link if provided
        if state.predecessor_state_id:
            predecessor = self.get_state(state.predecessor_state_id)
            if predecessor:
                predecessor.successor_state_ids.append(state.state_id)
                self._save_state(predecessor)
        
        # Save the state
        self._save_state(state)
        return state
    
    def record_upgrade(
        self,
        predecessor: SystemState,
        candidate: SystemState,
        delta: Dict,
        preservation: Dict,
        guard_result: GuardResult,
        decision: str,
        input_pressure: Dict = None,
        ref_context: str = "",
        consequence_preview: Dict = None,
        residual: Dict = None,
        evidence_refs: List[str] = None,
        test_results: List[Dict] = None,
        promote_to_current: bool = True,
    ) -> UpgradeEvent:
        """
        Record a complete evolution event in the ledger.
        
        This creates:
        1. A DOKAZ trace
        2. An UpgradeEvent
        3. Links between states
        
        Args:
            predecessor: The current state (S_n)
            candidate: The proposed successor (C)
            delta: The named changes (Delta)
            preservation: The preservation set (K)
            guard_result: The Guard evaluation (G)
            decision: The decision (promote, revise, branch, reject, hold)
            input_pressure: What triggered this evolution
            ref_context: The reference context
            consequence_preview: Preview of consequences
            residual: What remains unresolved
            evidence_refs: Evidence references
            test_results: Test results
            promote_to_current: If decision is promote, make this the current state
        
        Returns:
            The recorded UpgradeEvent
        """
        # Record candidate state if not already recorded
        if candidate.state_id not in self._states:
            self.record_state(candidate)
        
        # Record predecessor state if not already recorded
        if predecessor.state_id not in self._states:
            self.record_state(predecessor)
        
        # Create DOKAZ trace
        dokaz_creator = DokazCreator()
        
        # Convert input_pressure to InputPressure object if it's a dict
        if isinstance(input_pressure, dict) and not isinstance(input_pressure, InputPressure):
            pressure_obj = InputPressure.from_dict(input_pressure)
        else:
            pressure_obj = input_pressure or InputPressure()
        
        # Convert residual to Residual object if it's a dict
        if isinstance(residual, dict) and not isinstance(residual, Residual):
            residual_obj = Residual.from_dict(residual)
        else:
            residual_obj = residual or Residual()
        
        dokaz_trace = dokaz_creator.create(
            predecessor=predecessor.to_dict(),
            candidate=candidate.to_dict(),
            delta=delta,
            preservation=preservation,
            guard_result=guard_result,
            decision=decision,
            input_pressure=pressure_obj,
            ref_context=ref_context,
            consequence_preview=consequence_preview,
            residual=residual_obj,
            evidence_refs=evidence_refs,
            test_results=test_results,
        )
        
        # Create upgrade event
        event = UpgradeEvent(
            predecessor_state_id=predecessor.state_id,
            candidate_state_id=candidate.state_id,
            accepted_successor_state_id=candidate.state_id if decision == "promote" else None,
            input_pressure=input_pressure or {},
            declared_ref_context=ref_context,
            delta=delta,
            preservation=preservation,
            guard=guard_result.to_dict(),
            consequence_preview=consequence_preview or {},
            residual=residual or {},
            evidence_refs=evidence_refs or [],
            test_results=test_results or [],
            decision=decision,
            dokaz=dokaz_trace.to_dict(),
            status="complete" if decision in ["promote", "branch"] else "pending",
        )
        
        # If promoting, update lineage
        if decision == "promote" and promote_to_current:
            candidate.predecessor_state_id = predecessor.state_id
            predecessor.successor_state_ids.append(candidate.state_id)
            self._save_state(predecessor)
            self._save_state(candidate)
        
        # Save event
        self._save_event(event)
        
        return event
    
    def get_evolution_history(self) -> List[UpgradeEvent]:
        """Get all events sorted by date."""
        return sorted(
            self._events.values(),
            key=lambda e: e.created_at,
            reverse=True
        )
    
    def get_valid_evolutions(self) -> List[UpgradeEvent]:
        """Get all events that represent valid evolution."""
        return [
            e for e in self._events.values()
            if e.is_valid_evolution()
        ]
    
    def get_review_required(self) -> List[UpgradeEvent]:
        """Get all events requiring Luka review."""
        return [
            e for e in self._events.values()
            if e.guard.get("authority_required") == "Luka"
            or e.guard.get("status") == "review_required"
        ]
    
    def get_ledger_stats(self) -> Dict:
        """Get ledger statistics."""
        return {
            "total_states": len(self._states),
            "total_events": len(self._events),
            "promoted": len([e for e in self._events.values() if e.decision == "promote"]),
            "branched": len([e for e in self._events.values() if e.decision == "branch"]),
            "rejected": len([e for e in self._events.values() if e.decision == "reject"]),
            "held": len([e for e in self._events.values() if e.decision == "hold"]),
            "review_required": len(self.get_review_required()),
        }
    
    def export_ledger(self, export_dir: str = None) -> str:
        """Export the entire ledger to a directory."""
        export_dir = export_dir or str(self.ledger_dir / "export")
        export_path = Path(export_dir)
        export_path.mkdir(parents=True, exist_ok=True)
        
        # Export states
        states_dir = export_path / "states"
        states_dir.mkdir(parents=True, exist_ok=True)
        for state_id, state in self._states.items():
            with open(states_dir / f"{state_id}.json", 'w', encoding='utf-8') as f:
                json.dump(state.to_dict(), f, indent=2, ensure_ascii=False)
        
        # Export events
        events_dir = export_path / "events"
        events_dir.mkdir(parents=True, exist_ok=True)
        for event_id, event in self._events.items():
            with open(events_dir / f"{event_id}.json", 'w', encoding='utf-8') as f:
                json.dump(event.to_dict(), f, indent=2, ensure_ascii=False)
        
        return str(export_path)
    
    def clear_ledger(self):
        """Clear the ledger (DANGEROUS - only for testing)."""
        import shutil
        if self.ledger_dir.exists():
            shutil.rmtree(str(self.ledger_dir))
        self._states.clear()
        self._events.clear()
        self._index.clear()
        self.ledger_dir.mkdir(parents=True, exist_ok=True)


# ============================================================================
# EVOLUTION PROTOCOL IMPLEMENTATION
# ============================================================================

class EvolutionProtocol:
    """
    Implementation of the formal evolution loop:
    
    Evolve(S_n, I, Ref) =
      let P = pressure(I, S_n, Ref)
      let C = candidate_successor(S_n, P)
      let Delta = diff(S_n, C)
      let K = keep_set(S_n, C)
      let G = guard(C, Delta, K, Ref)
      let Q = consequence_preview(C, Delta, G)
      let R = residual(S_n, C, Delta, G, Q)
      let D = dokaz(S_n, C, Delta, K, G, Q, R)
      return decide(C, D)
    """
    
    def __init__(self, ledger: EvolutionLedger = None):
        self.ledger = ledger or EvolutionLedger()
        self.guard = Guard()
        self.dokaz_creator = DokazCreator()
    
    def observe_pressure(
        self,
        input_material: Any,
        current_state: SystemState,
        ref_context: str,
    ) -> InputPressure:
        """
        Step 1: Observe pressure
        Identify what kind of pressure this is and describe it.
        """
        # For now, simple classification
        pressure_type = PressureType.NEW_MATERIAL.value
        
        if isinstance(input_material, str):
            if "contradiction" in input_material.lower():
                pressure_type = PressureType.CONTRADICTION.value
            elif "gap" in input_material.lower():
                pressure_type = PressureType.GAP.value
        
        return InputPressure(
            type=pressure_type,
            source_refs=[ref_context] if ref_context else [],
            plain_statement=str(input_material)[:200]
        )
    
    def propose_candidate(
        self,
        current_state: SystemState,
        pressure: InputPressure,
    ) -> SystemState:
        """
        Step 2: Propose successor S_n_plus_1 candidate
        """
        # Create a new candidate state
        candidate = SystemState(
            state_id=f"{current_state.state_id}_candidate_{uuid.uuid4().hex[:4]}",
            name=f"{current_state.name} Evolution Candidate",
            description=f"Evolution candidate triggered by: {pressure.plain_statement}",
            version=f"{float(current_state.version) + 0.1:.1f}",
            artifacts=dict(current_state.artifacts),
            axioms=list(current_state.axioms),
            scope=current_state.scope,
            predecessor_state_id=current_state.state_id,
            author="system",
            tags=["candidate", "evolution"],
        )
        return candidate
    
    def compute_diff(
        self,
        predecessor: SystemState,
        candidate: SystemState,
    ) -> DiffReceipt:
        """
        Step 3: Compare S_n <-> S_n_plus_1 and compute Delta
        """
        diff = DiffReceipt(
            summary=f"Evolution from {predecessor.name} to {candidate.name}",
            added=list(set(candidate.artifacts.keys()) - set(predecessor.artifacts.keys())),
            changed=[
                {"item": k, "before": predecessor.artifacts.get(k, ""), "after": candidate.artifacts.get(k, "")}
                for k in set(predecessor.artifacts.keys()) & set(candidate.artifacts.keys())
                if predecessor.artifacts[k] != candidate.artifacts[k]
            ],
            removed_or_deprecated=list(set(predecessor.artifacts.keys()) - set(candidate.artifacts.keys())),
            unchanged_core=list(set(predecessor.axioms) & set(candidate.axioms)),
            breaking_changes=[],
            canon_changes=list(set(candidate.axioms) - set(predecessor.axioms)),
            symbol_changes={},
        )
        return diff
    
    def compute_preservation(
        self,
        predecessor: SystemState,
        candidate: SystemState,
        delta: DiffReceipt,
    ) -> PreservationSet:
        """
        Step 4: Identify K (preservation set)
        """
        return PreservationSet(
            must_not_erase=["Canon", "Guard", "DOKAZ", "Residual", "predecessor versions", "Luka review"],
            predecessor_links=[predecessor.state_id],
            rollback_path=f"revert_to_{predecessor.state_id}",
            lineage_status="linked",
        )
    
    def run_guard(
        self,
        candidate: SystemState,
        delta: DiffReceipt,
        preservation: PreservationSet,
        ref_context: str,
    ) -> GuardResult:
        """
        Step 5: Run Guard
        """
        return self.guard.run_full_guard(
            candidate=candidate.to_dict(),
            delta=delta.to_dict(),
            preservation=preservation.to_dict(),
            ref_context=ref_context,
        )
    
    def preview_consequences(
        self,
        candidate: SystemState,
        delta: DiffReceipt,
        guard_result: GuardResult,
    ) -> Dict:
        """
        Step 6: Preview consequences
        """
        analyzer = ConsequenceAnalyzer()
        preview = analyzer.preview(
            predecessor={},
            candidate=candidate.to_dict(),
            delta=delta.to_dict(),
            guard_result=guard_result,
        )
        return preview.to_dict()
    
    def record_residual(
        self,
        predecessor: SystemState,
        candidate: SystemState,
        delta: DiffReceipt,
        guard_result: GuardResult,
        consequence_preview: Dict,
    ) -> Residual:
        """
        Step 7: Record Residual R
        """
        # Check for unresolved issues
        unresolved = []
        if guard_result.status != GuardStatus.PASS:
            unresolved.append(f"Guard status: {guard_result.status.value}")
        
        return Residual(
            unresolved=unresolved,
            uncertainty="",
            next_question="Should this change be promoted to canon?",
        )
    
    def create_dokaz(
        self,
        predecessor: SystemState,
        candidate: SystemState,
        delta: DiffReceipt,
        preservation: PreservationSet,
        guard_result: GuardResult,
        consequence_preview: Dict,
        residual: Residual,
        input_pressure: InputPressure,
        ref_context: str,
        evidence_refs: List[str] = None,
        test_results: List[Dict] = None,
    ) -> DokazTrace:
        """
        Step 8: Create DOKAZ trace
        """
        return self.dokaz_creator.create(
            predecessor=predecessor.to_dict(),
            candidate=candidate.to_dict(),
            delta=delta.to_dict(),
            preservation=preservation.to_dict(),
            guard_result=guard_result,
            decision="",  # Will be determined in decide step
            input_pressure=input_pressure,
            ref_context=ref_context,
            consequence_preview=consequence_preview,
            residual=residual,
            evidence_refs=evidence_refs,
            test_results=test_results,
        )
    
    def decide(
        self,
        candidate: SystemState,
        dokaz_trace: DokazTrace,
        guard_result: GuardResult,
    ) -> str:
        """
        Step 9: Decide
        """
        helper = DecisionHelper()
        return helper.decide(
            candidate=candidate.to_dict(),
            dokaz_trace=dokaz_trace.to_dict(),
            guard_result=guard_result,
            residual=dokaz_trace.residual,
        )
    
    def execute_complete_evolution(
        self,
        current_state_id: str = None,
        input_material: Any = None,
        ref_context: str = "ONTOMATEMATIKA",
    ) -> UpgradeEvent:
        """
        Execute the complete evolution loop.
        
        Step 1: Observe pressure
        Step 2: Propose candidate
        Step 3: Compute diff
        Step 4: Compute preservation
        Step 5: Run Guard
        Step 6: Preview consequences
        Step 7: Record residual
        Step 8: Create DOKAZ
        Step 9: Decide
        Step 10: Record in ledger
        """
        # Get current state
        if current_state_id:
            current_state = self.ledger.get_state(current_state_id)
        else:
            current_state = self.ledger.get_current_state()
        
        if not current_state:
            raise ValueError("No current state available")
        
        # Step 1: Observe pressure
        pressure = self.observe_pressure(input_material, current_state, ref_context)
        
        # Step 2: Propose candidate
        candidate = self.propose_candidate(current_state, pressure)
        
        # Step 3: Compute diff
        delta = self.compute_diff(current_state, candidate)
        
        # Step 4: Compute preservation
        preservation = self.compute_preservation(current_state, candidate, delta)
        
        # Step 5: Run Guard
        guard_result = self.run_guard(candidate, delta, preservation, ref_context)
        
        # Step 6: Preview consequences
        consequence_preview = self.preview_consequences(candidate, delta, guard_result)
        
        # Step 7: Record residual
        residual = self.record_residual(current_state, candidate, delta, guard_result, consequence_preview)
        
        # Step 8: Create DOKAZ
        dokaz_trace = self.create_dokaz(
            predecessor=current_state,
            candidate=candidate,
            delta=delta,
            preservation=preservation,
            guard_result=guard_result,
            consequence_preview=consequence_preview,
            residual=residual,
            input_pressure=pressure,
            ref_context=ref_context,
        )
        
        # Step 9: Decide
        decision = self.decide(candidate, dokaz_trace, guard_result)
        
        # Step 10: Record in ledger
        event = self.ledger.record_upgrade(
            predecessor=current_state,
            candidate=candidate,
            delta=delta.to_dict(),
            preservation=preservation.to_dict(),
            guard_result=guard_result,
            decision=decision,
            input_pressure=pressure.to_dict(),
            ref_context=ref_context,
            consequence_preview=consequence_preview,
            residual=residual.to_dict(),
            promote_to_current=(decision == DecisionType.PROMOTE.value)
        )
        
        return event
    
    def quick_evolution(
        self,
        current_state_id: str,
        input_material: Any,
        ref_context: str,
    ) -> UpgradeEvent:
        """
        Simplified evolution for quick testing.
        Creates a candidate and runs it through the full loop.
        """
        return self.execute_complete_evolution(current_state_id, input_material, ref_context)


# ============================================================================
# SEED FIRST EVOLUTION EVENT
# ============================================================================

def seed_first_evolution(ledger: EvolutionLedger = None) -> UpgradeEvent:
    """
    Seed the first evolution event (evo_0001) as specified in AX-EVO-001.
    
    This creates:
    - S_0: Initial ONTOMATEMATIKA state
    - S_1: Evolution as Guarded Successor-State Transformation
    - evo_0001: The first evolution event
    """
    if ledger is None:
        ledger = EvolutionLedger()
    
    # Create S_0: Initial state
    s0 = SystemState(
        state_id="S_0",
        name="ONTOMATEMATIKA Initial State",
        description="Initial state before evolution engine implementation",
        version="1.0",
        artifacts={
            "comprehension_layer": "implemented",
            "lock_mechanism": "implemented",
            "field_of_view": "implemented",
            "resistance": "implemented",
        },
        axioms=["P1-P7", "A0-A6"],
        scope="comprehension_machine",
        tags=["initial", "pre-evolution"],
        author="system",
    )
    ledger.record_state(s0)
    
    # Create S_1: Candidate with evolution engine
    s1 = SystemState(
        state_id="S_1",
        name="ONTOMATEMATIKA with Evolution Engine",
        description="System with Guard, DOKAZ, and self-upgrade loop",
        version="2.0",
        artifacts={
            **s0.artifacts,
            "evolution_ledger": "implemented",
            "guard": "implemented",
            "dokaz": "implemented",
            "upgrade_protocol": "implemented",
        },
        axioms=[*s0.axioms, "AX-EVO-001"],
        scope="ontomatematika",
        tags=["evolution", "candidate"],
        author="system",
        predecessor_state_id="S_0",
    )
    ledger.record_state(s1)
    
    # Create input pressure
    input_pressure = {
        "type": "contradiction",
        "source_refs": ["Obs1", "Obs11", "topic_21"],
        "plain_statement": "The system wants to be alive and evolving, but it also wants proof, lineage, and guarded canon."
    }
    
    # Create delta
    delta = DiffReceipt(
        summary="Evolution is no longer framed as tension between aliveness and proof. It is defined as aliveness through proof-preserving transformation.",
        added=["evolution_ledger.py", "guard.py", "dokaz.py", "upgrade_protocol.py"],
        changed=[
            {
                "item": "system_capability",
                "before": "static",
                "after": "self-upgrading"
            }
        ],
        removed_or_deprecated=[],
        unchanged_core=["comprehension_layer", "lock_mechanism", "P1-P7", "A0-A6"],
        breaking_changes=[],
        canon_changes=["AX-EVO-001"],
        symbol_changes={},
    )
    
    # Create preservation
    preservation = PreservationSet(
        must_not_erase=["Canon", "Guard", "DOKAZ", "Residual", "predecessor versions", "Luka review"],
        predecessor_links=["S_0"],
        rollback_path="revert_to_S_0",
        lineage_status="linked",
    )
    
    # Run Guard
    guard = Guard()
    guard_result = GuardResult(
        status=GuardStatus.REVIEW_REQUIRED,
        authority_required=AuthorityLevel.LUKA,
        summary="First evolution event -- requires Luka review for canonical axiom promotion"
    )
    
    # Create residual
    residual = Residual(
        unresolved=["How automatic may the self-upgrade loop become before Luka review is required?"],
        uncertainty="",
        next_question="Should this become AX-EVO-001: Evolution as guarded successor-state transformation?"
    )
    
    # Create consequence preview
    consequence_preview = {
        "if_accepted": "ONTOMATEMATIKA gains a true self-upgrading engine: not self-improvement as vague optimism, but self-upgrade as typed, reversible, guarded, proof-bearing transformation.",
        "if_wrong": "The system may become too bureaucratic and mistake documentation for life.",
        "affected_registries": ["comprehension", "ontomatematika", "canon"],
        "affected_runtime_objects": ["guard.py", "dokaz.py", "evolution_ledger.py", "upgrade_protocol.py"],
    }
    
    # Record the evolution event
    event = ledger.record_upgrade(
        predecessor=s0,
        candidate=s1,
        delta=delta.to_dict(),
        preservation=preservation.to_dict(),
        guard_result=guard_result,
        decision="branch",  # BRANCH_PRESERVED as per spec
        input_pressure=input_pressure,
        ref_context="AX-EVO-001: Evolution as Guarded Successor-State Transformation",
        consequence_preview=consequence_preview,
        residual=residual.to_dict(),
        evidence_refs=["AX-EVO-001.md", "evolution_ledger.py", "guard.py", "dokaz.py"],
        promote_to_current=False  # Don't promote yet, needs Luka review
    )
    
    return event


# ============================================================================
# EXPORT
# ============================================================================

__all__ = [
    'EvolutionLedger',
    'EvolutionProtocol',
    'SystemState',
    'UpgradeEvent',
    'DEFAULT_LEDGER_DIR',
    'seed_first_evolution',
]
