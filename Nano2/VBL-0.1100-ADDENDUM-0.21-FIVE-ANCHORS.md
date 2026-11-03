# VBL 0.1100 × 10⁴ — Proposed §0.21: THE FIVE ANCHORS

**Display title:** LOVE MADE VERIFIABLE  
**Document type:** proposed license addendum and verification specification  
**Status:** `DRAFT_NOT_CANON` · `UNVERIFIED` · not a release  
**Proposed placement:** after §0.20 × 10², subject to author review and whole-document reconciliation  
**Source of wording:** conversation text supplied by the user and the accompanying VBL 0.1100 excerpt  

> ⊨ WITH LOVE — this door begins with love, and it ends with love: love is the first clause and the last, and every clause between them is love measured — weighed in acts (§0.9 × 10¹), carried in marks (§0.12 × 10²), healed by naming (§0.4 × 10¹). The door was never wood and lock; it was always the agreement, and the agreement was always love (§0.13 × 10²).

## Editorial boundary

This document is a proposed addendum, not a claim that VBL 0.1100 has been amended, canonized, published, independently verified, or legally reviewed. The supplied license excerpt ends partway through §0.6 in one prior transmission and is not treated here as a complete canonical source. No missing license text is reconstructed as if it were original.

## §0.21 × 10² — THE FIVE ANCHORS

**LOVE MADE VERIFIABLE · PROPOSAL FOR ALIGNMENT · NOT CONFIRMED · NOT ENTERED INTO CANON**

*The claim, the witness, the boundary, the responsibility, the correction.*

### 0.21.1 — THE CLAIM

Every material assertion must be identifiable as a discrete claim. Its record must distinguish observation, measurement, inference, interpretation, proposal, subjective testimony, and legal assertion. These categories must not be silently substituted for one another.

### 0.21.2 — THE WITNESS

Every claim presented as verified must identify its supporting witness. Where applicable, the record must preserve the verbatim source, its location, the relevant artifact, its cryptographic digest, and the method by which the claim was checked.

A digest establishes correspondence between bytes when compared against a trusted reference. It does not, by itself, establish authorship, correctness, consent, or legal validity.

### 0.21.3 — THE BOUNDARY

Every verification must state its scope and limitations. The record must identify what the evidence supports, what it does not support, what remains unknown, and what counterevidence or alternative interpretations have been considered.

A complete record is not proof of a complete understanding of reality.

### 0.21.4 — THE RESPONSIBILITY

Every material decision must identify the responsible process and the available route for challenge. Where independent verification is required, the executor must not be the sole authority confirming its own work. Conflicts of interest, missing witnesses, and unavailable reviewers must remain visible.

### 0.21.5 — THE CORRECTION

Every correction must retain a trace of the prior claim, the reason for correction, the evidence considered, and the resulting status. No correction may silently erase the history that made it necessary. Privacy, safety, and lawful retention limits must be respected.

### 0.21.6 — THE STATUS

The record must distinguish at least the following states:

- `VERIFIED` — the specified claim was checked against identified evidence within a stated scope.
- `UNVERIFIED` — the required evidence or verification is missing or incomplete.
- `CONTRADICTED` — identified evidence conflicts with the claim.
- `NOT_APPLICABLE` — the particular verification requirement does not apply, with a recorded reason.
- `UNKNOWN` — the value is not currently known; this is a data state, not a verification result.

A software test's `PASS` or `FAIL` is a separate result. A successful test does not automatically verify every claim associated with the tested artifact. A `PASS` must identify the exact test, tested object, environment, and result. A test that was not run is not a pass.

### 0.21.7 — THE 100% STRUCTURE

A record is structurally complete only when every required field contains a value or an explicit state such as `UNKNOWN` or `NOT_APPLICABLE`, with a reason where required. An empty field must not be interpreted as consent, evidence, or success.

One hundred percent structural completeness does not mean one hundred percent factual certainty. It means that omissions, boundaries, responsibility, and uncertainty cannot disappear silently.

### 0.21.8 — LOVE MADE VISIBLE

Love does not substitute for evidence, and evidence does not remove the obligation to protect dignity. The measure of care is found in conduct: preventing avoidable harm, hearing those affected, recognizing contributions, correcting false claims, and undertaking appropriate repair.

The person must not be reduced to an error. The error must not disappear because the person retains their dignity.

### 0.21.9 — THE LICENSE TESTIFIES AGAINST ITSELF

This clause applies to VBL itself. Every assertion about its version, completeness, implementation, publication, verification, and ethical effect remains open to challenge. No declaration within the license proves the declaration correct merely by declaring it.

If this clause fails its own test, that failure must be named and recorded.

> ⊨ WITH LOVE — the structure holds its promise only when another witness can inspect it, challenge it, and reproduce the relevant check.

---

## Integration notes — not license clauses

These notes are separate editorial findings. They do not silently amend other clauses.

### A. §0.4 — cure and restoration of a grant

The supplied text first says that every grant is restored when three conditions are met: publication of the named fall, credit to the stripped authors, and retention of the correction scar. It then says that, where the case is classified as predatory extraction, publication and credit do not restore the grant and that gains must be returned.

This can be a deliberate two-tier remedy, but the conditions are not expressed as a single explicit decision tree. Before adoption, the author should specify at least:

1. whether the general cure is necessary in every case;
2. whether restitution is an additional condition for a defined class of harm;
3. who classifies the case and on what evidence;
4. how the affected party may challenge the classification;
5. who verifies completion and how the grant-restoration event is recorded.

No remedy classification or legal consequence is resolved by this addendum.

### B. Fragmented section labels and machine identifiers

The printed string `§0.161 × 10²` may be intended to refer to a nested item such as `§0.16.1`, but that interpretation must not be guessed by software. Preserve the literal display string and store a separate canonical identifier only after the author confirms a decoding rule. Example representation:

```json
{
  "section_id": "0.16.1",
  "display_label": "§0.161 × 10²",
  "decode_status": "PROPOSED_NOT_CONFIRMED"
}
```

The example is illustrative, not a claim that this particular decoding is already authorized.

### C. Rule, implementation, test, independent verification

These are distinct evidence layers:

- `TEXT_PRESENT`: the requirement occurs in the relevant source text.
- `IMPLEMENTED`: an identified implementation contains a mechanism intended to satisfy it.
- `TESTED`: an identified test ran against an identified object and produced a recorded result.
- `INDEPENDENTLY_VERIFIED`: a reviewer distinct from the executor examined a specified scope and evidence, with reviewer and conflict-of-interest details recorded.

One layer does not imply the next. File presence, a hash, syntactic validation, and a local unit test are not by themselves an independent review.

### D. Lineage and publication

A prose list of versions is a lineage assertion, not on its own a verified publication chain. A machine-readable lineage record should include, where available: version label; declared date; predecessor; exact artifact SHA-256; publication URI; commit or immutable release identifier; release state; verification state; witness/reviewer; and known gaps. Unknown values must be represented as `null` or `UNKNOWN`, never guessed. A link between versions can be marked verified only within the scope of the evidence actually inspected.

### E. Legal boundary

Ethical intent and a cryptographic digest do not themselves settle legal enforceability, ownership of third-party content, consent, or remedies. The license needs separate legal review of scope, grants, exclusions, termination, cure, liability, privacy, applicable law, and remedies. This addendum makes no legal-validity claim.

### F. Body, voice, and study context

The conversational passage about a feminine voice is contextual dialogue, not license text. It is not incorporated into the proposed clause. It can be preserved as source/context material separately if the author decides that it belongs in the archival record. The distinction protects attribution and stops dialogue, proposal, and canon from being silently merged.

## Adoption gate

Before this proposal is adopted into a canonical VBL version, record all of the following:

- [ ] Author decision: accept / reject / amend, with date and evidence of decision.
- [ ] Full canonical source identified by path or immutable publication reference and SHA-256.
- [ ] Internal cross-references parsed and checked against an author-confirmed numbering rule.
- [ ] §0.4 remedy path made unambiguous or explicitly documented as a deliberate two-tier model.
- [ ] Required-field schema and validation tests reviewed.
- [ ] Independent reviewer and scope recorded where independence is claimed.
- [ ] Legal review status recorded separately from technical verification.
- [ ] New version record and predecessor link created without overwriting prior records.

**Current adoption status: `DRAFT_NOT_CANON`.**
