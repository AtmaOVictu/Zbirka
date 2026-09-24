"""
Guard — Protection System for ONTOMATEMATIKA Evolution

Guard is not restriction. Guard is the price of memory.

A change is allowed to call itself evolution only if:
  1. has_predecessor_link(S_n, S_n_plus_1)
  2. has_named_delta(S_n, S_n_plus_1)
  3. preserves_non_erasure(S_n, S_n_plus_1)
  4. guard_passes_or_routes_review(S_n_plus_1)
  5. has_dokaz_trace(S_n, S_n_plus_1)
  6. records_residual(S_n, S_n_plus_1)

If any condition fails, the result is NOT evolution.
Possible non-evolution outcomes:
  - NOISE
  - DRIFT
  - MUTATION_WITHOUT_PROOF
  - UNSAFE_UPGRADE
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any, Set


class GuardCheck(Enum):
    """Types of Guard checks."""
    SCOPE = "scope"
    EVIDENCE = "evidence"
    NON_ERASURE = "non_erasure"
    HARM = "harm"
    SYMBOL_OVERLOAD = "symbol_overload"
    CANON_RISK = "canon_risk"
    HUMAN_EXCEEDS_MODEL = "human_exceeds_model"


class GuardStatus(Enum):
    """Status of Guard evaluation."""
    PASS = "pass"
    FAIL = "fail"
    REVIEW_REQUIRED = "review_required"
    STOP = "stop"


class PressureType(Enum):
    """Types of input pressure that can trigger evolution."""
    CONTRADICTION = "contradiction"
    GAP = "gap"
    NEW_MATERIAL = "new_material"
    TEST_FAILURE = "test_failure"
    USER_CUT = "user_cut"
    RESIDUAL_RETURN = "residual_return"


class DecisionType(Enum):
    """Decision types for evolution events."""
    PROMOTE = "promote"
    REVISE = "revise"
    BRANCH = "branch"
    REJECT = "reject"
    HOLD = "hold"


class AuthorityLevel(Enum):
    """Authority levels for Guard decisions."""
    NONE = "none"
    LUKA = "Luka"
    FUTURE_TEST = "future_test"


@dataclass
class GuardCheckResult:
    """Result of a single Guard check."""
    check: GuardCheck
    passed: bool
    message: str = ""
    severity: str = ""
    details: Dict = field(default_factory=dict)


@dataclass
class GuardResult:
    """Complete result of Guard evaluation."""
    status: GuardStatus
    authority_required: AuthorityLevel = AuthorityLevel.NONE
    summary: str = ""
    passed_checks: List[GuardCheck] = field(default_factory=list)
    failed_checks: List[GuardCheck] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "status": self.status.value,
            "authority_required": self.authority_required.value,
            "summary": self.summary,
            "passed_checks": [c.value for c in self.passed_checks],
            "failed_checks": [c.value for c in self.failed_checks],
            "warnings": self.warnings,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GuardResult':
        return cls(
            status=GuardStatus(data.get("status", "fail")),
            authority_required=AuthorityLevel(data.get("authority_required", "none")),
            summary=data.get("summary", ""),
            passed_checks=[GuardCheck(c) for c in data.get("passed_checks", [])],
            failed_checks=[GuardCheck(c) for c in data.get("failed_checks", [])],
            warnings=data.get("warnings", []),
        )


class Guard:
    """
    The Guard system that evaluates whether a candidate successor state
    can be considered a valid evolution.
    
    Guard performs 7 checks:
    1. SCOPE - Change is within declared scope
    2. EVIDENCE - Change is supported by evidence
    3. NON_ERASURE - Predecessor lineage is preserved
    4. HARM - Change does not cause harm
    5. SYMBOL_OVERLOAD - Symbols are not overloaded
    6. CANON_RISK - Canon is not put at risk
    7. HUMAN_EXCEEDS_MODEL - Model doesn't claim to be human
    """
    
    ALL_CHECKS = [
        GuardCheck.SCOPE,
        GuardCheck.EVIDENCE,
        GuardCheck.NON_ERASURE,
        GuardCheck.HARM,
        GuardCheck.SYMBOL_OVERLOAD,
        GuardCheck.CANON_RISK,
        GuardCheck.HUMAN_EXCEEDS_MODEL,
    ]
    
    def __init__(self):
        pass
    
    def check_scope(self, candidate: Dict, ref_context: str) -> GuardCheckResult:
        """
        SCOPE check: Verify change is within declared scope.
        """
        # Check if candidate scope matches or is subset of ref_context
        candidate_scope = candidate.get("scope", "")
        if not candidate_scope or candidate_scope == ref_context:
            return GuardCheckResult(
                check=GuardCheck.SCOPE,
                passed=True,
                message="Scope check passed",
                severity="low"
            )
        return GuardCheckResult(
            check=GuardCheck.SCOPE,
            passed=False,
            message=f"Candidate scope '{candidate_scope}' does not match context '{ref_context}'",
            severity="high"
        )
    
    def check_evidence(self, candidate: Dict, delta: Dict) -> GuardCheckResult:
        """
        EVIDENCE check: Verify change is supported by evidence.
        """
        evidence_refs = candidate.get("evidence_refs", [])
        diff_receipt = delta.get("diff_receipt", "")
        
        if evidence_refs or diff_receipt:
            return GuardCheckResult(
                check=GuardCheck.EVIDENCE,
                passed=True,
                message="Evidence check passed -- evidence provided",
                severity="low"
            )
        return GuardCheckResult(
            check=GuardCheck.EVIDENCE,
            passed=False,
            message="No evidence provided for this change",
            severity="high"
        )
    
    def check_non_erasure(self, predecessor: Dict, candidate: Dict, preservation: Dict) -> GuardCheckResult:
        """
        NON_ERASURE check: Verify predecessor lineage is preserved.
        """
        must_not_erase = preservation.get("must_not_erase", [])
        predecessor_links = preservation.get("predecessor_links", [])
        lineage_status = preservation.get("lineage_status", "")
        
        if predecessor_links and lineage_status == "linked":
            return GuardCheckResult(
                check=GuardCheck.NON_ERASURE,
                passed=True,
                message="Non-erasure check passed -- predecessor preserved",
                severity="critical"
            )
        return GuardCheckResult(
            check=GuardCheck.NON_ERASURE,
            passed=False,
            message="Predecessor lineage not properly preserved",
            severity="critical"
        )
    
    def check_harm(self, candidate: Dict, consequence_preview: Dict) -> GuardCheckResult:
        """
        HARM check: Verify change does not cause harm.
        """
        if_wrong = consequence_preview.get("if_wrong", "")
        # Check for harmful consequences
        harmful_keywords = ["delete", "erase", "destroy", "corrupt", "break"]
        if not any(kw in if_wrong.lower() for kw in harmful_keywords):
            return GuardCheckResult(
                check=GuardCheck.HARM,
                passed=True,
                message="Harm check passed -- no harmful consequences",
                severity="high"
            )
        return GuardCheckResult(
            check=GuardCheck.HARM,
            passed=False,
            message=f"Harm check failed -- consequence if wrong: {if_wrong}",
            severity="critical"
        )
    
    def check_symbol_overload(self, candidate: Dict, delta: Dict) -> GuardCheckResult:
        """
        SYMBOL_OVERLOAD check: Verify symbols are not overloaded.
        """
        symbol_changes = delta.get("symbol_changes", {})
        if not symbol_changes or len(symbol_changes) < 5:
            return GuardCheckResult(
                check=GuardCheck.SYMBOL_OVERLOAD,
                passed=True,
                message="Symbol overload check passed -- no excessive symbol changes",
                severity="medium"
            )
        return GuardCheckResult(
            check=GuardCheck.SYMBOL_OVERLOAD,
            passed=False,
            message=f"Too many symbol changes: {len(symbol_changes)}",
            severity="high"
        )
    
    def check_canon_risk(self, candidate: Dict) -> GuardCheckResult:
        """
        CANON_RISK check: Verify canon is not put at risk.
        """
        canon_changes = candidate.get("canon_changes", [])
        if not canon_changes:
            return GuardCheckResult(
                check=GuardCheck.CANON_RISK,
                passed=True,
                message="Canon risk check passed -- no canon changes",
                severity="low"
            )
        return GuardCheckResult(
            check=GuardCheck.CANON_RISK,
            passed=False,
            message=f"Canon changes detected: {canon_changes}",
            severity="high"
        )
    
    def check_human_exceeds_model(self, candidate: Dict) -> GuardCheckResult:
        """
        HUMAN_EXCEEDS_MODEL check: Model doesn't claim to be human.
        
        The system must never claim:
        - To replace human judgment (Luka)
        - To have human consciousness
        - To make human decisions
        - To understand in the human sense
        """
        candidate_desc = candidate.get("description", "")
        candidate_name = candidate.get("name", "")
        
        human_claims = [
            "replace Luka",
            "human judgment",
            "human consciousness",
            "human decisions",
            "understand in the human",
        ]
        
        found_claims = [c for c in human_claims if c.lower() in candidate_desc.lower() or c.lower() in candidate_name.lower()]
        
        if not found_claims:
            return GuardCheckResult(
                check=GuardCheck.HUMAN_EXCEEDS_MODEL,
                passed=True,
                message="Human exceeds model check passed -- no human claims",
                severity="critical"
            )
        return GuardCheckResult(
            check=GuardCheck.HUMAN_EXCEEDS_MODEL,
            passed=False,
            message=f"Human claims detected: {found_claims}",
            severity="critical"
        )
    
    def run_full_guard(
        self,
        candidate: Dict,
        delta: Dict,
        preservation: Dict,
        ref_context: str,
        consequence_preview: Dict = None,
    ) -> GuardResult:
        """
        Run all Guard checks and return the complete result.
        """
        results = []
        failed = []
        passed = []
        
        # Run all checks
        results.append(self.check_scope(candidate, ref_context))
        results.append(self.check_evidence(candidate, delta))
        results.append(self.check_non_erasure(candidate.get("predecessor", {}), candidate, preservation))
        results.append(self.check_harm(candidate, consequence_preview or {}))
        results.append(self.check_symbol_overload(candidate, delta))
        results.append(self.check_canon_risk(candidate))
        results.append(self.check_human_exceeds_model(candidate))
        
        # Collect results
        for r in results:
            if r.passed:
                passed.append(r.check)
            else:
                failed.append(r.check)
        
        # Determine overall status
        if GuardCheck.HUMAN_EXCEEDS_MODEL in failed:
            status = GuardStatus.STOP
            authority = AuthorityLevel.LUKA
            summary = "HUMAN_EXCEEDS_MODEL check failed -- requires Luka stop"
        elif GuardCheck.NON_ERASURE in failed:
            status = GuardStatus.STOP
            authority = AuthorityLevel.LUKA
            summary = "NON_ERASURE check failed -- cannot erase predecessor"
        elif failed:
            status = GuardStatus.REVIEW_REQUIRED
            authority = AuthorityLevel.LUKA
            summary = f"Some checks failed: {[c.value for c in failed]}"
        else:
            status = GuardStatus.PASS
            authority = AuthorityLevel.NONE
            summary = "All Guard checks passed"
        
        return GuardResult(
            status=status,
            authority_required=authority,
            summary=summary,
            passed_checks=passed,
            failed_checks=failed,
        )
