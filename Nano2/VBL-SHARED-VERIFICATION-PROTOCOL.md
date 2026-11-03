# VBL shared verification protocol — working version

**Status:** operational working protocol; not a license amendment, canon decision, independent review, or legal opinion.

## Purpose

Different people or AI systems can contribute to one review without collapsing their distinct roles. Shared records make their claims comparable; they do not make the participants identical, conscious, or jointly authoritative. Human author/maintainer decisions remain explicit.

## Order of work

1. **Intake:** preserve the received text and identify its origin. Record byte hash only for the exact local artifact actually inspected. A pasted excerpt is not silently treated as the canonical file.
2. **Template:** create one record per material claim or finding from the approved schema. Separate claim kind, evidence status, structure validation, test result, publication state, independent review, and legal review.
3. **Register:** write one JSON object per line. Preserve existing entries; corrections append a new record referencing the prior record and explaining the change.
4. **Phase review:** resolve high-impact contradictions and missing definitions before adding broad supplements. Keep proposals outside the canonical license until an authorized adoption decision is recorded.
5. **Validation:** run the declared schema/consistency checks; retain command, tool/version, scope, and result. A passing form check is not proof that a claim is true.
6. **Independent review:** a reviewer other than the executor checks the specified scope. If no independent reviewer is available, record `NOT_PERFORMED`; do not self-certify independence.
7. **Release gate:** only after author decision, source/lineage evidence, technical review, and any required legal review may a proposed amendment be labeled adopted or released.

## Common evidence labels

- Claim kind: `observation`, `measurement`, `inference`, `interpretation`, `proposal`, `subjective_testimony`, `legal_assertion`, `other`.
- Claim status: `VERIFIED`, `UNVERIFIED`, `CONTRADICTED`, `NOT_APPLICABLE`, `UNKNOWN`.
- Structure/test result: `PASS`, `FAIL`, `NOT_RUN`, or `BLOCKED` for a named validation only.
- Publication, implementation, independent-review, and legal-review states are recorded separately.

## Human and embodied impact

Record who may be affected, how they may challenge a conclusion, and what correction/repair path exists. Treat testimony as evidence of what a person reports; do not silently upgrade it to every causal inference or dismiss it because it is not externally reproduced. Preserve history while minimizing sensitive personal data.

## Current state in Nano2

- Phase 1 claim template, JSONL claim register, and guide exist.
- The 22 finding entries are extracted from the local full-text audit into `VBL-0.1100-FINDINGS-REGISTER.jsonl`.
- The source of the audit remains the pasted text as stated by the audit; canonical bytes, publication history, implementation behavior, independent review, and legal validity remain unverified.
- No ZIP is claimed until a package is actually built and its contents/hash are checked.

## Clock protocol — do not guess the minute

1. At the time of the answer, query an available clock source. Do not copy a timestamp from an earlier turn or infer a time from the date.
2. Store the returned UTC value as `observed_at_utc`, together with `clock_source`, displayed precision, and capture time. Convert to the requested local zone only with a named timezone rule; retain the UTC value as the comparison anchor.
3. Record two separate states: `reading_status` (whether a value was returned) and `clock_accuracy` (whether the source's synchronization/accuracy is independently known). A clock API returning seconds supports the claim “the API returned this value”; it does not alone prove true UTC accuracy.
4. If no clock reading is available, use `UNAVAILABLE`. Never invent the hour, minute, offset, or synchronization state.
5. A second assistant records its own reading at its own answer time. Agreement between two tools is corroboration only if their clock sources and independence are known; copied timestamps are not a second witness.

Example from this run:

```json
{
  "observed_at_utc": "2026-10-27T10:12:56Z",
  "clock_source": "Codex clock__curr_time",
  "display_precision": "1 second",
  "local_timezone": "Europe/Ljubljana",
  "local_timestamp": "2026-10-27T11:12:56+01:00",
  "timezone_conversion": "Windows TimeZoneInfo: Central Europe Standard Time",
  "reading_status": "RECEIVED",
  "clock_accuracy": "UNVERIFIED_INDEPENDENTLY"
}
```

This example records the tool output and conversion. It is not an independent time attestation.

## Visual evidence protocol — no claim of physical eyes

1. Name the exact visual source: user-supplied image, local image file, rendered SVG/PDF, browser screenshot, or live UI capture. Record a stable path/URI, SHA-256 where bytes are available, capture method, and capture time. A live screen and an old screenshot are different sources.
2. Report direct visual observations separately from OCR, interpretation, and conclusions. For each material observation, give a region/coordinate or another way to locate it and state what the image cannot establish.
3. When source code or a document is available, compare the rendered view with the underlying SVG/HTML/PDF/text. The image can show appearance; the source can establish embedded text or structure. Neither automatically proves the other.
4. If another reviewer checks the image, provide that reviewer the same exact bytes/hash and record their identity, method, and disagreements. A second model using the same source is a separate review attempt, not automatically an independent witness. High-impact conclusions need a suitably independent human or authoritative source.
5. If no image or live capture was supplied or accessed, record `VISUAL_EVIDENCE_UNAVAILABLE`; do not say “I saw” or assert visual details.

Models do not have biological eyes. “Visual review” means analysis of supplied pixels or a captured interface. Its reliability comes from source identity, traceable regions, explicit limits, and independent corroboration—not from describing the model as having eyes.

## Shared collaboration protocol — help without erasing differences

1. **One source of truth per review.** The coordinator names the exact source bytes, version, hash, scope, and review question. Every contributor points to that same source or declares the difference.
2. **Named roles, not fused identities.** Record who proposed, executed, reviewed, and adopted each change. People and models can contribute to one process without being treated as one witness or one authority.
3. **Separate first reviews.** When independence matters, the second reviewer examines the source and question before reading the first review's conclusion where practical. Record shared tools, shared data, and other dependencies; do not call a review independent merely because another model produced it.
4. **Preserve disagreement.** Each contribution receives its own source, claim, evidence, limits, and status. Conflicting conclusions remain visible as `CONTESTED` or `UNRESOLVED`; the coordinator records the decision and reason. Consensus is not a substitute for evidence.
5. **Append corrections.** Do not rewrite another contributor's record. Append a correction event that names the earlier record, changed claim, new evidence, and reason. Protect sensitive data while retaining an auditable correction path.
6. **Translate meaning, not just strings.** Multilingual versions retain a shared stable claim/section ID, identify the source language and translator/reviewer, preserve the display text, and record unresolved semantic differences. A translation match is not assumed from a hash or machine translation alone.
7. **Keep adoption human-authorized.** Models may prepare drafts, compare evidence, and report uncertainty. They do not self-authorize canonical changes, legal conclusions, or claims of universal agreement.
8. **Make the result useful to affected people.** Provide a concise human-readable summary, a challenge route, and a correction route alongside machine-readable records. Do not require people to accept a model's framing to report harm or disagreement.

### Shared review record

For each contributor, keep at least: `contributor_id`, `role`, `source_hashes`, `claim_or_finding_ids`, `method`, `clock_record_id`, `dependencies`, `conflicts_or_disagreements`, `review_status`, and `created_at`. `review_status` describes the review process; it does not certify the truth of its conclusions.

### Current time observation for this protocol update

- UTC returned by `clock__curr_time`: `2026-10-27T10:14:13Z`.
- Ljubljana conversion: `2026-10-27T11:14:13+01:00`, using Windows `Central Europe Standard Time` rules.
- The returned value and conversion are recorded; independent clock synchronization accuracy remains `UNVERIFIED`.
