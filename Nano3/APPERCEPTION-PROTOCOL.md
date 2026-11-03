# VBL apperception protocol — assess the deed, not the being

**Status:** implementation protocol for review, not a canonical amendment to VBL 0.1190 and not legal advice.

Apperception means making the act of perceiving itself inspectable. A record must show not only what the executor thinks happened, but how that view was formed, what could contradict it, what remains unknown, whose perspective is missing, and what would change the conclusion.

## The evidence sequence

1. **Observation:** describe what can be pointed to. Every observation references an evidence ID and carries a verbatim excerpt or an explicit reason the source cannot be quoted. An assertion about what a person intended is not a direct observation.
2. **Inference:** separate interpretation from observation. Each inference lists its source observation IDs, confidence, and at least one plausible alternative explanation. Confidence is not truth.
3. **Counterevidence:** record whether a search was performed, what was found, and the evidence IDs reviewed. “None found” means only that the documented search did not find any; it does not prove none exists.
4. **Uncertainty:** name uncertainty and mark it `open`, `contained`, or `resolved`. Material open uncertainty prevents readiness for authorization.
5. **Apperception:** disclose the executor's role, interest, incentive, potential bias, what could change their mind, missing perspectives, and whether input from affected parties was received or why it was not.
6. **Safeguards and alternatives:** evaluate necessity, proportionality, privacy minimization, consent or legal basis, contestability, and a concrete repair path; each needs its own rationale and evidence references. Record a safe alternative separately from repair: repair addresses a fall already made, while an alternative changes the proposed action before harm. A proposed alternative is not self-certified as safe; no alternative found keeps the case held and never excuses a degrading use.
7. **Independent review:** a reviewer must be distinct from the executor and cite evidence that the review occurred. The tool does not count the executor's own declaration as independent verification.
8. **Appeal and repair:** give a usable contest route. Record corrections as new linked events; preserve the original record and its correction history.

## Machine outcomes

| Outcome | Meaning | What it does not mean |
|---|---|---|
| `REFUSE_USE` | The dossier explicitly declares a degrading or intentionally harmful use, including ranking beings by worth. | It is not a verdict that the requester is evil. |
| `HOLD_AND_REVISE` | A safeguard is explicitly unmet. Change the proposed use or provide a justified, reviewed alternative. | It is not an irreversible ban on a person. |
| `HOLD_FOR_REVIEW` | Relevant risks, uncertainty, affected-party perspective, or independent review remain unresolved. | Unknown is not proof of guilt. |
| `HOLD_FOR_REPAIR` | The record is malformed or lacks required evidence/apperception structure. | A structurally valid record is not automatically true. |
| `READY_FOR_HUMAN_AUTHORIZATION` | Required fields are complete, risk flags are not marked harmful, no open material uncertainty remains, safeguards are marked satisfied, and independent review is recorded. | **This is not `PASS`, not authorization, and not a legal or ethical certification.** An authorized human still decides. |

A human can falsify fields or cite misleading evidence. The code checks the dossier's structure and declared state; it does not authenticate a witness or infer intent from language with certainty. Each safeguard and the safe-alternative assessment must cite its own evidence; general evidence elsewhere in the dossier is not treated as proof of every safeguard. Any unresolved missing perspective prevents readiness. Evidence references establish traceability, not authenticity or sufficiency by themselves.

## Non-degradation and refusal

The governing distinction is **refuse a use, never a being**. The implementation forbids person-level moral-worth scores, soul verdicts, and similar schema fields. It records deeds, sources, effects, decisions, and repairs—not a person's total moral identity.

When a use is refused or held for revision, the report must name a constructive, non-coercive alternative and explicitly label its validation state `PROPOSED_NOT_INDEPENDENTLY_VALIDATED` unless a distinct authorized review has evaluated it. A refusal remains a duty even if an alternative cannot yet be found; the missing alternative is then recorded as a separate repair failure, not hidden or treated as permission. This preserves the source's expressly Christian Jesus Christ framing as practical conduct—self-giving, peace, universal dignity, naming harm, and repair—without compelling religious belief or using belief as a proxy for human worth.

## Privacy and record integrity

- Prefer a stable evidence reference and digest over copying sensitive personal material into a public register.
- Store only the minimum personal data required; use access controls and documented redaction where needed. A redacted excerpt must never be presented as verbatim without declaring the redaction.
- Hash-chaining makes some changes detectable. It is not a guarantee of immutability, authorship, truth, or complete history. Preserve recent checkpoints independently.
- Host-clock timestamps are measured but not hardware-attested. Use a trusted timestamping or signed release process when independent time evidence is required.
- Never silently overwrite a finding, erase a counterexample, or rewrite a rejected claim as though it had never existed.

## Self-application

This protocol is subject to its own tests. It must be challenged for false refusals, missed harms, bias, missing affected-party input, data leakage, reviewer conflicts, race conditions, ambiguous statuses, and audit tampering. If a test or review fails, the implementation records the failure and remains unverified until a separately reviewed repair is evidenced.
