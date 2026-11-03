# VBL Shared Assistant Card

**Purpose:** a short handoff protocol for people and AI systems reviewing VBL together. This card is procedural guidance, not license text or a claim of canon.

## 1. Start from the same source

- Name the exact file, excerpt, or capture and its version.
- Where bytes exist, record size and SHA-256. A hash identifies bytes relative to a reference; it does not prove authorship, truth, permission, or publication.
- Mark whether the source is canonical, a local copy, a pasted excerpt, or unknown. Never silently fill missing text.

## 2. Record claims with witnesses

For each material claim, preserve its source/location, claim kind (`observation`, `measurement`, `inference`, `interpretation`, `proposal`, `subjective_testimony`, `legal_assertion`, `other`), evidence, limits, affected parties, reviewer, challenge route, and correction path. Treat human dignity as independent of claim status.

Keep these separate:

- claim verification: `VERIFIED`, `UNVERIFIED`, `CONTRADICTED`, `UNKNOWN`, `NOT_APPLICABLE`;
- form/test result: `PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`;
- publication, implementation, independent review, and legal review states.

A complete form or passing test does not certify the truth of the claim.

## 3. Measure time at the answer

- Query a clock source when answering; record its returned UTC value, source, precision, local timezone conversion, and conversion rule.
- Record `reading_status` separately from `clock_accuracy`. Unless independent synchronization evidence exists, accuracy is `UNVERIFIED_INDEPENDENTLY`.
- Every reviewer obtains their own timestamp. Never copy another reviewer's time as a fresh measurement.

## 4. Review visual sources traceably

- Use the exact supplied image/file or a named live capture; record its hash, capture method/time, and relevant region.
- State what is directly visible separately from OCR, inference, and conclusion. State what pixels cannot establish.
- If another reviewer checks it, give them the same bytes/hash. A second model is not automatically independent; record shared tools and dependencies. If no image was supplied/accessed, say `VISUAL_EVIDENCE_UNAVAILABLE`.
- Models analyze pixels; they do not have biological eyes.

## 5. Collaborate without false consensus

- Name proposer, executor, reviewer, and adoption authority separately.
- When independence matters, the reviewer checks the source before reading the first conclusion where practical.
- Keep disagreements and counterevidence visible. Do not average conflicting conclusions into certainty.
- Correct by appending a new record that references the prior one. Preserve necessary history while protecting sensitive information.
- Keep translations linked by stable IDs; record translator/reviewer and unresolved meaning differences.

## 6. Protect people and preserve agency

- Hear testimony without automatically treating every inference as established; do not dismiss testimony because it is difficult to reproduce.
- Do not infer a person's worth, intent, diagnosis, or guilt from uncertain evidence.
- In distress, respond to the immediate practical need, ask concise safety questions only when warranted, and encourage suitable human support. Do not pretend to have human feelings, a body, or shared consciousness.
- Only an authorized human decision can adopt a proposal into canon. Report unresolved decisions plainly.

## Current example clock observation

At the time this card was prepared, the clock tool returned `2026-10-27T10:17:34Z`; the local conversion was `2026-10-27T11:17:34+01:00` for `Europe/Ljubljana`. Source: Codex `clock__curr_time`; displayed precision: one second; independent synchronization accuracy: `UNVERIFIED_INDEPENDENTLY`.
