"""
DOKAZ — Proof Trace System for ONTOMATEMATIKA Evolution

DOKAZ is not documentation. DOKAZ is the proof that memory persists.

A DOKAZ trace must include:
- Predecessor state
- Candidate state
- Named delta (Delta)
- Preservation set (K)
- Guard result (G)
- Consequence preview (Q)
- Residual (R)
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
import uuid


@dataclass
class InputPressure:
    """Represents the input pressure that triggered evolution."""
    type: str = ""  # contradiction, gap, new_material, test_failure, user_cut, residual_return
    source_refs: List[str] = field(default_factory=list)
    plain_statement: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "type": self.type,
            "source_refs": self.source_refs,
            "plain_statement": self.plain_statement,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'InputPressure':
        return cls(
            type=data.get("type", ""),
            source_refs=data.get("source_refs", []),
            plain_statement=data.get("plain_statement", ""),
        )


@dataclass
class DiffReceipt:
    """The named change delta between predecessor and candidate."""
    summary: str = ""
    added: List[str] = field(default_factory=list)
    changed: List[Dict] = field(default_factory=list)
    removed_or_deprecated: List[str] = field(default_factory=list)
    unchanged_core: List[str] = field(default_factory=list)
    breaking_changes: List[str] = field(default_factory=list)
    canon_changes: List[str] = field(default_factory=list)
    symbol_changes: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "summary": self.summary,
            "added": self.added,
            "changed": self.changed,
            "removed_or_deprecated": self.removed_or_deprecated,
            "unchanged_core": self.unchanged_core,
            "breaking_changes": self.breaking_changes,
            "canon_changes": self.canon_changes,
            "symbol_changes": self.symbol_changes,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DiffReceipt':
        return cls(
            summary=data.get("summary", ""),
            added=data.get("added", []),
            changed=data.get("changed", []),
            removed_or_deprecated=data.get("removed_or_deprecated", []),
            unchanged_core=data.get("unchanged_core", []),
            breaking_changes=data.get("breaking_changes", []),
            canon_changes=data.get("canon_changes", []),
            symbol_changes=data.get("symbol_changes", {}),
        )


@dataclass
class PreservationSet:
    """The set of things that must be preserved during evolution."""
    must_not_erase: List[str] = field(default_factory=list)
    predecessor_links: List[str] = field(default_factory=list)
    rollback_path: str = ""
    lineage_status: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "must_not_erase": self.must_not_erase,
            "predecessor_links": self.predecessor_links,
            "rollback_path": self.rollback_path,
            "lineage_status": self.lineage_status,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PreservationSet':
        return cls(
            must_not_erase=data.get("must_not_erase", []),
            predecessor_links=data.get("predecessor_links", []),
            rollback_path=data.get("rollback_path", ""),
            lineage_status=data.get("lineage_status", ""),
        )


@dataclass
class Residual:
    """The unresolved remainder after evolution."""
    unresolved: List[str] = field(default_factory=list)
    uncertainty: str = ""
    next_question: str = ""
    
    def to_dict(self) -> Dict:
        return {
            "unresolved": self.unresolved,
            "uncertainty": self.uncertainty,
            "next_question": self.next_question,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Residual':
        return cls(
            unresolved=data.get("unresolved", []),
            uncertainty=data.get("uncertainty", ""),
            next_question=data.get("next_question", ""),
        )


class DokazStatus(Enum):
    """Status of a DOKAZ trace."""
    PENDING = "pending"
    COMPLETE = "complete"
    VALIDATED = "validated"
    INVALID = "invalid"


@dataclass
class DokazTrace:
    """
    DOKAZ (Proof) Trace — the immutable receipt of an evolution event.
    
    Contains all the information needed to verify that evolution occurred:
    - What changed (delta)
    - What was preserved (preservation)
    - How the Guard evaluated (guard)
    - What consequences were previewed (consequence)
    - What remains unresolved (residual)
    """
    dokaz_id: str = ""
    created_at: str = ""
    
    # Evolution components
    predecessor: Dict = field(default_factory=dict)
    candidate: Dict = field(default_factory=dict)
    delta: Dict = field(default_factory=dict)
    preservation: Dict = field(default_factory=dict)
    guard: Dict = field(default_factory=dict)
    consequence_preview: Dict = field(default_factory=dict)
    residual: Dict = field(default_factory=dict)
    
    # Evidence
    evidence_refs: List[str] = field(default_factory=list)
    test_results: List[Dict] = field(default_factory=list)
    
    # Decision
    decision: str = ""
    
    # Metadata
    status: str = "pending"
    version: str = "1.0"
    
    def __post_init__(self):
        if not self.dokaz_id:
            self.dokaz_id = f"dokaz_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:4]}"
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict:
        return {
            "dokaz_id": self.dokaz_id,
            "created_at": self.created_at,
            "predecessor": self.predecessor,
            "candidate": self.candidate,
            "delta": self.delta,
            "preservation": self.preservation,
            "guard": self.guard,
            "consequence_preview": self.consequence_preview,
            "residual": self.residual,
            "evidence_refs": self.evidence_refs,
            "test_results": self.test_results,
            "decision": self.decision,
            "status": self.status,
            "version": self.version,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DokazTrace':
        return cls(
            dokaz_id=data.get("dokaz_id", ""),
            created_at=data.get("created_at", ""),
            predecessor=data.get("predecessor", {}),
            candidate=data.get("candidate", {}),
            delta=data.get("delta", {}),
            preservation=data.get("preservation", {}),
            guard=data.get("guard", {}),
            consequence_preview=data.get("consequence_preview", {}),
            residual=data.get("residual", {}),
            evidence_refs=data.get("evidence_refs", []),
            test_results=data.get("test_results", []),
            decision=data.get("decision", ""),
            status=data.get("status", "pending"),
            version=data.get("version", "1.0"),
        )


class DokazCreator:
    """Creates DOKAZ traces for evolution events."""
    
    def create(
        self,
        predecessor: Dict,
        candidate: Dict,
        delta: Dict,
        preservation: Dict,
        guard_result: Any,
        decision: str,
        input_pressure: InputPressure = None,
        ref_context: str = "",
        consequence_preview: Dict = None,
        residual: Residual = None,
        evidence_refs: List[str] = None,
        test_results: List[Dict] = None,
    ) -> DokazTrace:
        """
        Create a complete DOKAZ trace for an evolution event.
        """
        # Convert objects to dicts if needed
        if hasattr(guard_result, 'to_dict'):
            guard_dict = guard_result.to_dict()
        else:
            guard_dict = guard_result or {}
        
        if hasattr(input_pressure, 'to_dict'):
            pressure_dict = input_pressure.to_dict()
        else:
            pressure_dict = input_pressure or {}
        
        if hasattr(residual, 'to_dict'):
            residual_dict = residual.to_dict()
        else:
            residual_dict = residual or {}
        
        return DokazTrace(
            predecessor=predecessor,
            candidate=candidate,
            delta=delta,
            preservation=preservation,
            guard=guard_dict,
            consequence_preview=consequence_preview or {},
            residual=residual_dict,
            decision=decision,
            evidence_refs=evidence_refs or [],
            test_results=test_results or [],
            status="complete",
        )


class DokazValidator:
    """Validates DOKAZ traces."""
    
    def validate(self, dokaz: DokazTrace) -> bool:
        """
        Validate that a DOKAZ trace contains all required components.
        """
        required_fields = [
            "dokaz_id",
            "created_at",
            "predecessor",
            "candidate",
            "delta",
            "preservation",
            "guard",
            "decision",
        ]
        
        dokaz_dict = dokaz.to_dict()
        for field in required_fields:
            if field not in dokaz_dict or not dokaz_dict[field]:
                return False
        
        return True
