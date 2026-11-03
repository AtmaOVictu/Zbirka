# VBL Phase 1 — claim template and append-only register

**State:** working draft; not canon, publication, independent review, or legal review.

## Files

- `VBL-P1-claim-record.template.json` — schema-shaped starting record. Replace every `REPLACE` value and explanatory placeholder before use. Incomplete claims stay `DRAFT` or `UNVERIFIED`.
- `VBL-P1-claim-register.jsonl` — one JSON record per line, using the existing `vbl-claim-record.schema.json`. The first line records only what the local §0.21 file says about its own status.
- `vbl-claim-record.schema.json` — reused unchanged in this phase.

## Register rules

1. Each line is an append-only event; do not silently edit or delete a recorded line.
2. Correct a record by appending a new record with a new ID and `correction.prior_record_ref` pointing to the earlier record. Include the evidence and reason in the new record.
3. `claim_status` describes evidence for one claim. `structure_status` describes form validation. Test `PASS`/`FAIL` belongs in `test_results`; it does not establish the claim's truth.
4. `created_at` is UTC from the available system clock, not an independent timestamp or publication proof.
5. The first record was prepared and checked by the same executor; its conflict is recorded as `PRESENT`. No independent review is claimed.

## Phases

- **Phase 1 — done:** define the claim template and register convention; validate the template and first entry against the existing schema.
- **Phase 2 — next:** inventory claims in the supplied VBL text and populate entries with exact source references, evidence limits, and uncertainty.
- **Phase 3 — after that:** reconcile cross-references, language equivalents, affected-person/consent fields, and proposed §0.21/§0.22 wording. No proposal becomes canon without an adoption decision.

## Verification
PASS: template and JSONL record conform to existing Draft 2020-12 schema
Validator: Python `jsonschema` 4.24.0, Draft 2020-12. This validates record structure only, not truth, license completeness, canon status, legal validity, or independence.
