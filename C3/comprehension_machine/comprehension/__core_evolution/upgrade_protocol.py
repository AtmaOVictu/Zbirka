"""
Upgrade Protocol — Self-Upgrade Loop Implementation for ONTOMATEMATIKA

Formal loop:
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

Valid evolution condition:
  EvolutionValid(S_n -> S_n_plus_1) =
    has_predecessor_link(S_n_plus_1, S_n)
    AND has_named_delta(S_n, S_n_plus_1)
    AND preserves_non_erasure(S_n, S_n_plus_1)
    AND guard_passes_or_routes_review(S_n_plus_1)
    AND has_dokaz_trace(S_n, S_n_plus_1)
    AND records_residual(S_n, S_n_plus_1)

If any condition fails, the result is NOT evolution.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Set, Tuple
from guard import Guard, GuardResult, GuardStatus, GuardCheck, DecisionType, AuthorityLevel
from dokaz import DokazTrace, DokazValidator


class ChangeType(Enum):
    """Classification of change types."""
    EVOLUTION = "evolution"
    NOISE = "noise"
    DRIFT = "drift"
    MUTATION_WITHOUT_PROOF = "mutation_without_proof"
    UNSAFE_UPGRADE = "unsafe_upgrade"
    BRANCH_ONLY = "branch_only"
    REVIEW_REQUIRED = "review_required"


@dataclass
class ConsequencePreview:
    """Preview of what happens if a candidate is accepted or wrong."""
    if_accepted: str = ""
    if_wrong: str = ""
    affected_registries: List[str] = field(default_factory=list)
    affected_runtime_objects: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "if_accepted": self.if_accepted,
            "if_wrong": self.if_wrong,
            "affected_registries": self.affected_registries,
            "affected_runtime_objects": self.affected_runtime_objects,
        }


class ConsequenceAnalyzer:
    """Analyzes consequences of accepting or rejecting a candidate."""
    
    def preview(
        self,
        predecessor: Dict,
        candidate: Dict,
        delta: Dict,
        guard_result: GuardResult,
    ) -> ConsequencePreview:
        """
        Preview what will happen if the candidate is accepted and what breaks if it's wrong.
        """
        # Build if_accepted message
        candidate_name = candidate.get("name", "candidate")
        delta_summary = delta.get("summary", "changes")
        
        if_accepted = (
            f"System will evolve to {candidate_name} with changes: {delta_summary}. "
            f"Guard status: {guard_result.status.value}"
        )
        
        # Build if_wrong message
        if guard_result.failed_checks:
            failed = [c.value for c in guard_result.failed_checks]
            if_wrong = f"Failed checks: {failed}. Revert to predecessor state."
        else:
            if_wrong = "Revert to predecessor state, residual preserved."
        
        # Identify affected registries and objects
        affected_registries = list(set(
            candidate.get("scope", "").split(",") + 
            delta.get("changed", [])
        ))
        
        affected_runtime_objects = [
            "guard.py", "dokaz.py", "evolution_ledger.py", "upgrade_protocol.py"
        ]
        
        return ConsequencePreview(
            if_accepted=if_accepted,
            if_wrong=if_wrong,
            affected_registries=affected_registries,
            affected_runtime_objects=affected_runtime_objects,
        )


class EvolutionValidator:
    """Validates that a change meets the criteria for evolution."""
    
    def evolution_valid(
        self,
        predecessor: Dict,
        successor: Dict,
        delta: Dict,
        preservation: Dict,
        guard_result: GuardResult,
        dokaz: Dict,
        residual: Dict,
    ) -> Tuple[bool, List[str]]:
        """
        Check if a change is valid evolution.
        
        Returns:
            (is_valid, [list of failed conditions])
        """
        failures = []
        
        # Check 1: has_predecessor_link
        predecessor_id = predecessor.get("state_id")
        successor_predecessor = successor.get("predecessor_state_id")
        if not predecessor_id or predecessor_id != successor_predecessor:
            failures.append("has_predecessor_link")
        
        # Check 2: has_named_delta
        if not delta or not delta.get("summary"):
            failures.append("has_named_delta")
        
        # Check 3: preserves_non_erasure
        must_not_erase = preservation.get("must_not_erase", [])
        if not must_not_erase:
            failures.append("preserves_non_erasure")
        
        # Check 4: guard_passes_or_routes_review
        if guard_result.status in [GuardStatus.FAIL, GuardStatus.STOP]:
            if guard_result.authority_required == AuthorityLevel.NONE:
                failures.append("guard_passes_or_routes_review")
        
        # Check 5: has_dokaz_trace
        if not dokaz or not dokaz.get("dokaz_id"):
            failures.append("has_dokaz_trace")
        
        # Check 6: records_residual
        if not residual or (not residual.get("unresolved") and not residual.get("next_question")):
            failures.append("records_residual")
        
        return (len(failures) == 0, failures)
    
    def classify_change(
        self,
        predecessor: Dict,
        candidate: Dict,
        delta: Dict,
        guard_result: GuardResult,
        dokaz: Dict,
    ) -> ChangeType:
        """
        Classify what type of change this is.
        """
        is_valid, failures = self.evolution_valid(
            predecessor, candidate, delta, {}, guard_result, dokaz, {}
        )
        
        if is_valid:
            return ChangeType.EVOLUTION
        
        # Check for specific failure modes
        if "has_predecessor_link" in failures:
            return ChangeType.DRIFT
        
        if "guard_passes_or_routes_review" in failures and guard_result.status == GuardStatus.STOP:
            return ChangeType.UNSAFE_UPGRADE
        
        if "has_dokaz_trace" in failures:
            return ChangeType.MUTATION_WITHOUT_PROOF
        
        if guard_result.status == GuardStatus.REVIEW_REQUIRED:
            return ChangeType.REVIEW_REQUIRED
        
        return ChangeType.NOISE


class DecisionHelper:
    """Helps make decisions about evolution candidates."""
    
    def decide(
        self,
        candidate: Dict,
        dokaz_trace: Dict,
        guard_result: GuardResult,
        residual: Dict,
    ) -> str:
        """
        Make a decision about a candidate evolution.
        
        Returns one of: promote, revise, branch, reject, hold
        """
        # PROMOTE: All conditions met
        if guard_result.status == GuardStatus.PASS:
            if dokaz_trace:
                return DecisionType.PROMOTE.value
        
        # REJECT: Critical failures
        if guard_result.status == GuardStatus.STOP:
            return DecisionType.REJECT.value
        
        if GuardCheck.HUMAN_EXCEEDS_MODEL in guard_result.failed_checks:
            return DecisionType.REJECT.value
        
        if GuardCheck.NON_ERASURE in guard_result.failed_checks:
            return DecisionType.REJECT.value
        
        # HOLD/REVIEW_REQUIRED: Needs human review
        if guard_result.status == GuardStatus.REVIEW_REQUIRED:
            if guard_result.authority_required == AuthorityLevel.LUKA:
                return DecisionType.HOLD.value
        
        # BRANCH: Useful but not universally better
        # This would need more sophisticated analysis
        return DecisionType.BRANCH.value


def evolution_valid(
    predecessor: Dict,
    successor: Dict,
    delta: Dict,
    preservation: Dict,
    guard_result: GuardResult,
    dokaz: Dict,
    residual: Dict,
) -> Tuple[bool, List[str]]:
    """
    Convenience function to check if evolution is valid.
    """
    validator = EvolutionValidator()
    return validator.evolution_valid(
        predecessor, successor, delta, preservation, guard_result, dokaz, residual
    )


def classify_change(
    predecessor: Dict,
    candidate: Dict,
    delta: Dict,
    guard_result: GuardResult,
    dokaz: Dict,
) -> ChangeType:
    """
    Convenience function to classify a change.
    """
    validator = EvolutionValidator()
    return validator.classify_change(predecessor, candidate, delta, guard_result, dokaz)
