# Proposal for review: VBL §−1 / §9 alignment and adversarial verification

**Status: PROPOSAL · NOT CANONICAL · NOT RELEASED · NOT INDEPENDENTLY APPROVED**

This is a public review request for the VBL — Verification Before Assertion License work. It does not claim that the clauses are legally enforceable, merged, implemented in production, or accepted by maintainers.

## Purpose

Align proposed §−1 (equal dignity) with §9 (ethics, responsibility, and verifiable remediation), evidence statuses, correction history, registers, and independent verification. The same standard must apply to authors, operators, reviewers, users, and the license itself: no position substitutes for evidence, and no actor may be the sole verifier of their own action.

## Proposed §9 additions (Slovenian working text)

### §9.1 — Responsibility is demonstrated by actions
No one establishes ethical conduct merely by stating intentions, position, authority, or their own interpretation. Where consequences can be checked, record actions, relevant evidence, outcomes, and verification limits.

### §9.2 — Equal criteria, differentiated duties
All participants have equal dignity. Evidence criteria must be consistent regardless of status. Different powers may create different duties, but not automatic credibility or exemption from review.

### §9.3 — Prevent and reduce harm
Before an action with a reasonably foreseeable risk, assess likely consequences, choose proportionate safeguards, and identify an accountable owner. If risk becomes unacceptable, stop or limit the action, or require documented re-approval.

### §9.4 — Right to contest
Where feasible and safe, affected people must be able to challenge relevant data, report harm, and submit counter-evidence. An objection may not be dismissed merely because of the objector's status or disagreement with the decision-maker.

### §9.5 — Correct without silently erasing history
Record the error, reason for correction, time of change, and link to the original record. Preserve the original except where a lawful deletion or data-protection requirement requires another process; when lawful and safe, retain a proportionate audit trail without unnecessary personal data.

### §9.6 — Independent verification
A claim of independent review must identify the reviewer, scope, evidence, limitations, and conflicts of interest. The executor's assertion is not sufficient proof of independence. If independence cannot be confirmed, mark it unverified.

### §9.7 — Acknowledgment and remediation
Distinguish acknowledgment, correction of a record, remediation of consequences, and prevention of recurrence. Completion of one does not prove completion of the others.

### §9.8 — No false compliance
Do not declare compliance based only on self-assertion, unrun tests, incomplete evidence, or inaccessible independent review. Failures, uncertainty, objections, and unresolved defects remain visible.

### §9.9 — Proportionality, privacy, and dignity
Verification must be sufficient for its purpose without collecting or disclosing excess personal data. Privacy must not be used to conceal misconduct; evidence requirements must not be used to expose people without justification.

### §9.10 — Completion criteria
A duty is complete only when required evidence has been collected, checked, and connected to the outcome; identified errors have been handled; and remaining gaps are stated. If verification is impossible, record the limitation, not success.

## Eight machine-checkable control families

1. **Equal dignity:** a record, allegation, low status, or failed task never changes a person's dignity status.
2. **Evidence over authority:** identity, rank, ownership, confidence, or repeated assertion cannot replace supporting evidence.
3. **Independent review:** the executor cannot be the sole reviewer for a claim of independence.
4. **Correction-history integrity:** a correction carries an original record ID, correction ID, reason, timestamp, and linkage; silent overwrite fails.
5. **Uncertainty and disagreement:** missing or conflicting evidence produces an explicit unresolved/disputed status, not a fabricated finding.
6. **Consent and refusal:** consent is not inferred from silence; a clear refusal of further contact stops follow-up except where a lawful duty requires otherwise.
7. **Privacy and least privilege:** protected evidence is available only to authorized readers; redaction and deletion are governed, documented, and proportionate.
8. **No false compliance:** draft, test pass, external delivery, independent review, release, and legal approval are distinct states.

## Adversarial tests required before acceptance

For each control, provide passing and failing cases, including: forged or non-resolving source; duplicate record identifier; missing timestamp; falsely named reviewer; unauthorized access through a proxy; deletion of an original; suppressed disagreement; recorded but unexecuted correction; role-based double standard; consent inferred from silence; redaction that removes all accountability evidence; and a claim that a test ran without an execution record.

Tests must run against the actual implementation and relevant registries—not only examples or schemas. Preserve raw output, code/version identifiers, environment where relevant, source artifacts, computed digests, and known limitations. A hash proves byte identity relative to a reference, not truth, authorship, consent, or correctness.

## Acceptance gate

- Map every control to an actual repository function, data field, and register/schema.
- Add positive, negative, boundary, and adversarial tests.
- Run the suite against the implementation and retain raw outputs.
- Have a reviewer other than the executor inspect the evidence and record conflicts.
- Keep legal review, rights-holder release approval, independent verification, and successful CI as separate gates.
- Retain draft status until the gates are completed or explicitly waived by the proper authority, with the waiver recorded.

## Collaboration request

Please review for contradictions with existing §9 and other operative clauses, security weaknesses, privacy risks, test gaps, and legal ambiguity. Propose specific changes with evidence. Disagreement is welcome and must not be silently discarded.

Related existing review: https://github.com/AtmaOVictu/agents-cli/pull/1

**Slovensko:** Predlagana dopolnitev ostaja delovni predlog. Namen je pošteno preverjanje, sledljivost popravkov, možnost ugovora, zmanjševanje škode in neodvisna presoja — ne prisila, samopotrditev ali izmišljeno soglasje.

**Transparency note:** This requests review; it does not assert implementation, production behavior, legal validity, release, or endorsement.
