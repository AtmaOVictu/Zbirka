"""Reference validator for the proposed VBL 10.5.2 implementation profile.

This module validates records and workflow claims. It does NOT enforce a license
on people or services and does not prove legal validity or release authority.
"""
from __future__ import annotations

from datetime import datetime
import re
from typing import Any

CLAIM_STATUSES = {
    "UNVERIFIED", "VERIFIED", "REFUTED", "PARTIALLY_VERIFIED",
    "DISPUTED", "INCONCLUSIVE",
}
MESSAGE_STATES = {"DRAFTED", "SENT", "RECEIVED", "CONSENTED"}
RECORD_TYPES = {"OBSERVATION", "CLAIM", "CORRECTION", "DISPUTE", "REDACTION", "REVIEW"}
HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _valid_timestamp(value: Any) -> bool:
    if not _nonempty(value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except (ValueError, AttributeError):
        return False


def validate_claim(claim: dict[str, Any]) -> tuple[bool, list[str]]:
    """Check claim provenance. Authority alone can never satisfy the evidence fields."""
    errors: list[str] = []
    for key in ("claim_id", "subject", "claim", "scope", "method", "status"):
        if not _nonempty(claim.get(key)):
            errors.append(f"missing:{key}")
    status = claim.get("status")
    if status not in CLAIM_STATUSES:
        errors.append("invalid:status")
    sources = claim.get("source_ids")
    if not isinstance(sources, list):
        errors.append("missing_or_invalid:source_ids")
        sources = []
    if status == "VERIFIED":
        if not sources or not all(_nonempty(x) for x in sources):
            errors.append("verified_requires_source_ids")
        if not _valid_timestamp(claim.get("verification_date")):
            errors.append("verified_requires_verification_date")
        if not _nonempty(claim.get("method")) or not _nonempty(claim.get("scope")):
            errors.append("verified_requires_method_and_scope")
    return not errors, errors


def validate_independent_review(review: dict[str, Any]) -> tuple[bool, list[str]]:
    """Prevent an executor from being the sole verifier of their own work."""
    errors: list[str] = []
    required = ("task_id", "executor_id", "reviewer_id", "method", "scope", "review_date")
    for key in required:
        if not _nonempty(review.get(key)):
            errors.append(f"missing:{key}")
    evidence_ids = review.get("evidence_ids")
    if not isinstance(evidence_ids, list) or not evidence_ids or not all(_nonempty(x) for x in evidence_ids):
        errors.append("review_requires_evidence_ids")
    if _nonempty(review.get("executor_id")) and review.get("executor_id") == review.get("reviewer_id"):
        errors.append("executor_cannot_be_sole_independent_reviewer")
    if review.get("conflict_of_interest") is None:
        errors.append("conflict_of_interest_must_be_declared")
    elif review.get("conflict_of_interest") is True:
        errors.append("conflict_of_interest_requires_mitigation_or_non_independent_status")
    if not _valid_timestamp(review.get("review_date")):
        errors.append("invalid:review_date")
    return not errors, errors


def validate_event_stream(records: list[dict[str, Any]]) -> tuple[bool, list[str]]:
    """Validate an append-only event list; corrections refer back rather than replacing."""
    errors: list[str] = []
    seen: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        record_id = record.get("record_id")
        if not _nonempty(record_id):
            errors.append(f"record[{index}]:missing_record_id")
            continue
        if record_id in seen:
            errors.append(f"duplicate_record_id:{record_id}")
            continue
        event_type = record.get("event_type")
        if event_type not in RECORD_TYPES:
            errors.append(f"record[{index}]:invalid_event_type")
        if not _valid_timestamp(record.get("timestamp")):
            errors.append(f"record[{index}]:invalid_timestamp")
        if event_type == "CORRECTION":
            target = record.get("corrects_record_id")
            if not _nonempty(target) or target not in seen:
                errors.append(f"record[{index}]:correction_target_must_preexist")
            if not _nonempty(record.get("reason")):
                errors.append(f"record[{index}]:correction_requires_reason")
            if not _nonempty(record.get("actor_id")):
                errors.append(f"record[{index}]:correction_requires_actor")
        if event_type == "REDACTION":
            target = record.get("redacts_record_id")
            if not _nonempty(target) or target not in seen:
                errors.append(f"record[{index}]:redaction_target_must_preexist")
            if not _nonempty(record.get("basis_or_reason")):
                errors.append(f"record[{index}]:redaction_requires_basis_or_reason")
        seen[record_id] = record
    return not errors, errors


def classify_evidence(*, source_ids: list[str], method: str, scope: str,
                      conflict: bool = False, assessment_result: str | None = None,
                      assessment_ref: str | None = None, assessed_by: str | None = None) -> str:
    """Record a reviewed outcome; mere presence of source identifiers is not verification.

    The assessment reference should point to the actual review evidence. This helper
    classifies a supplied assessment; it cannot independently establish truth.
    """
    if conflict or assessment_result == "CONFLICT":
        return "DISPUTED"
    if not source_ids:
        return "UNVERIFIED"
    if not _nonempty(method) or not _nonempty(scope) or not _nonempty(assessment_ref) or not _nonempty(assessed_by):
        return "INCONCLUSIVE"
    mapping = {
        "SUPPORTS": "VERIFIED",
        "REFUTES": "REFUTED",
        "PARTIAL": "PARTIALLY_VERIFIED",
        "INDETERMINATE": "INCONCLUSIVE",
    }
    return mapping.get(str(assessment_result), "INCONCLUSIVE")


def can_contact(recipient_state: dict[str, Any]) -> tuple[bool, str]:
    """Decide if one appropriate invitation is permitted under the draft profile."""
    if recipient_state.get("no_contact_requested") is True:
        return False, "explicit_no_contact_request"
    if recipient_state.get("declined") is True or recipient_state.get("persuasion_unwelcome") is True:
        return False, "recipient_declined_or_persuasion_unwelcome"
    if recipient_state.get("recipient_initiated") is True or recipient_state.get("consented_to_contact") is True:
        return True, "recipient_initiated_or_consented"
    if recipient_state.get("lawful_and_appropriate") is not True:
        return False, "lawfulness_and_appropriateness_not_established"
    if recipient_state.get("invitation_attempts", 0) != 0:
        return False, "single_invitation_already_used"
    if recipient_state.get("clear_purpose") is not True:
        return False, "purpose_not_clear"
    return True, "one_good_faith_invitation_only"


def validate_message_state(event: dict[str, Any]) -> tuple[bool, list[str]]:
    """Prevent drafted/sent/received/consented from being treated as synonyms."""
    errors: list[str] = []
    if event.get("state") not in MESSAGE_STATES:
        errors.append("invalid:state")
    if not _nonempty(event.get("message_id")):
        errors.append("missing:message_id")
    if event.get("state") in {"SENT", "RECEIVED", "CONSENTED"}:
        if not _valid_timestamp(event.get("timestamp")):
            errors.append("state_requires_timestamp")
        if not _nonempty(event.get("evidence_ref")):
            errors.append("state_requires_evidence_ref")
    if event.get("state") == "CONSENTED" and not _nonempty(event.get("consent_scope")):
        errors.append("consent_requires_explicit_scope")
    return not errors, errors


def validate_privacy_record(record: dict[str, Any]) -> tuple[bool, list[str]]:
    """Require purpose, necessity, access, retention, and review of public disclosure."""
    errors: list[str] = []
    for key in ("purpose", "necessity", "access_rule", "retention_rule", "basis_or_reason"):
        if not _nonempty(record.get(key)):
            errors.append(f"missing:{key}")
    if record.get("publicly_disclosed") is True and record.get("contains_personal_data") is True:
        if record.get("redacted_or_authorized") is not True:
            errors.append("personal_data_publication_requires_redaction_or_authorization")
    if record.get("retention_rule") == "FOREVER" and record.get("necessity_reviewed") is not True:
        errors.append("indefinite_retention_requires_documented_necessity_review")
    return not errors, errors


def validate_release_record(record: dict[str, Any]) -> tuple[bool, list[str]]:
    """Allow drafts; require evidence and an approved gate decision to claim RELEASED."""
    errors: list[str] = []
    status = record.get("status")
    if status not in {"DRAFT", "RELEASED", "WITHDRAWN", "SUPERSEDED"}:
        return False, ["invalid:status"]
    if status != "RELEASED":
        return True, []
    for key in ("rights_holder_approval_ref", "canonical_uri", "publication_date", "test_report_ref"):
        if not _nonempty(record.get(key)):
            errors.append(f"released_requires:{key}")
    if not _valid_timestamp(record.get("publication_date")):
        errors.append("released_requires_valid_publication_date")
    if not _nonempty(record.get("canonical_sha256")) or not HEX64.fullmatch(str(record.get("canonical_sha256", ""))):
        errors.append("released_requires_valid_sha256")
    gates = record.get("release_gates")
    if not isinstance(gates, list) or not gates:
        errors.append("released_requires_gate_decisions")
    else:
        for idx, gate in enumerate(gates):
            if gate.get("status") == "WAIVED":
                if not _nonempty(gate.get("waiver_reason")) or not _nonempty(gate.get("authorized_by")):
                    errors.append(f"gate[{idx}]:waiver_requires_reason_and_authority")
            elif gate.get("status") == "COMPLETED":
                if not _nonempty(gate.get("evidence_ref")):
                    errors.append(f"gate[{idx}]:completion_requires_evidence")
            else:
                errors.append(f"gate[{idx}]:must_be_completed_or_explicitly_waived")
    return not errors, errors
