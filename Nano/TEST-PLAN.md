# VBL release acceptance test plan

A release cannot be marked `VERIFIED` until required tests pass and the evidence is reviewed by someone other than the executor. The local checker is only a first-stage gate.

| ID | Test | Pass condition | Required evidence |
|---|---|---|---|
| VBL-001 | Canonical source | Exactly one clean `LICENSE.md`; no page chrome or whole-document duplication | File bytes + SHA-256 |
| VBL-002 | Version metadata | Header and machine record both identify 2.6 / 2026-10-23; predecessor metadata agrees with verified source | Canonical file + predecessor reference |
| VBL-003 | Register presence | Both named JSONL registers exist and every non-empty line parses as JSON | Register files + validation output |
| VBL-004 | Contributor attribution | Entries distinguish name, pseudonym, unknown identity, and privacy/consent basis | Register policy + reviewed entries |
| VBL-005 | Fall/cure protocol | Notice, evidence, 30-day clock, classification, remediation, disputes, and verification are defined | Protocol + test cases |
| VBL-006 | Permission hierarchy | §7 cannot override the §9 ethical floor | Revised clauses + contradiction review |
| VBL-007 | Grant/version policy | Reproduction, redistribution, modification, commercial use, and prior grants are explicitly addressed | Grant matrix + legal review |
| VBL-008 | Scope inventory | Covered works, excluded corpus, and third-party works are distinguished | Release manifest + rights notices |
| VBL-009 | Provenance | Current source and predecessor are linked to immutable refs/commit IDs; hashes match checked-out bytes | Repository URLs, commit IDs, SHA-256 manifest |
| VBL-010 | Encoding/round trip | Defined UTF-8/line-ending policy; supported transfers round-trip byte-identically | Test script, before/after hashes, logs |
| VBL-011 | Independent review | Reviewer is distinct from release executor and signs/records result | Review record |
| VBL-012 | Legal review | Grant, termination, cure, warranty and liability terms have jurisdiction-specific review | Counsel review record |

## Suggested release gate

- Any missing canonical file or register: **FAIL / INCOMPLETE**.
- Any unresolved blocker: **REVIEW_REQUIRED**.
- A passing local script alone: **PRECHECK_PASSED**, never `VERIFIED`.
- `VERIFIED` requires all applicable evidence, independent review, and a versioned decision record.
