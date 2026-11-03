# VBL registry schema and implementation test plan

**Status:** proposed engineering requirements; not yet part of the VBL license and not yet independently reviewed.

## Minimum record invariants

1. **Record type and schema version:** every row has a defined `record_type`, `schema_version`, and an explicitly permitted `status`. Reject unknown required fields only if versioning rules say to reject them; otherwise preserve them for forward compatibility.
2. **Unique immutable identifier:** every non-template record has a stable `record_id` unique across all merged registers within a declared namespace. Template rows are not live data, must never be counted, and must never be merged into a live register.
3. **Evidence provenance:** verified claims require a source URI or stable source identifier, an exact quote or content reference where appropriate, retrieval/occurrence timestamps with timezone, evidence digest, and the identity or protected identifier of the verifier. Missing fields result in `INCOMPLETE` or `UNVERIFIED`, never `VERIFIED`.
4. **Append-only correction:** do not overwrite a prior incident/contributor/permission entry. A correction is a new record with `supersedes_record_id` or `corrects_record_id`, timestamp, rationale, and retained prior evidence.
5. **Status transition rules:** define an explicit transition table (for example `PROPOSED -> IN_REVIEW -> VERIFIED | REJECTED | UNVERIFIED`). Record actor, timestamp, reason, and evidence for every change. Status may not be self-approved by the executor when independent verification is required.
6. **Permissions:** distinguish request, pending, granted, denied, withdrawn, expired, and unknown. A request or silence is never treated as a grant. Capture exact scope, material, action, destination/context, decision-maker, timestamp, written reference, and conditions.
7. **Privacy and minimization:** never require public disclosure of sensitive personal details when a protected reference will do. Redact secrets from public evidence while retaining an auditable private locator where lawful and appropriate.
8. **Manifest safety:** reject absolute paths and parent traversal; verify raw file bytes, byte size, and SHA-256; report any missing file or mismatch explicitly. A generated report must distinguish `PASS`, `WARN`, `BLOCKED`, `REVIEW`, and `FAIL`.

## Required automated tests before production use

- Valid and invalid UTF-8, JSONL parsing, blank lines, and non-object rows.
- Missing, malformed, empty, or wrong-shaped manifest.
- Exact size/hash match, size-only mismatch, digest-only mismatch, missing file, absolute path, `..` traversal, and symlink escape.
- Template rows excluded from the live-record count and rejected from live merges.
- Header count equals the number of actual rows; any declared/observed mismatch fails.
- Duplicate IDs within one register and across all merged registers fail.
- Missing evidence source/hash/timestamp prevents verified status.
- Timestamp format and timezone validation.
- Only allowed status transitions; unauthorized or self-approved transitions fail.
- Append-only corrections preserve the original row and point back to it.
- Permission requests, grants, withdrawals, expired grants, and ambiguous/silent responses remain distinct.
- A `BLOCKED` required check returns a nonzero process exit code and is never presented as a clean pass.
- Independent reproduction against an immutable commit and a clean environment; preserve commands, versions, raw output, and the resulting artifact hashes.

## Current implementation coverage

The supplied lightweight checker covers JSONL object parsing, basic header counts, Todo App manifest sizes/digests, exclusion of Cookbook template rows, duplicate IDs among actual rows, detection of `UNVERIFIED` checksum placeholders, manifest path traversal, and a nonzero blocked exit code. Eight unit tests pass for those behaviors.

Not implemented yet: a full versioned schema validator, full status-transition authorization model, evidence completeness gates, timestamp semantics, permissions lifecycle validation, whole-repository manifest inventory, robust symlink audit, or an isolated ZPV test. Do not treat this checker as sufficient for production certification.
