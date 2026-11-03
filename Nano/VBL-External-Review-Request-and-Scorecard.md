# External Independent Review — Request and Scorecard

**Status:** ready to send to a suitable human reviewer; NOT SENT; no reviewer appointed.  
**Requested review target:** VBL 2.6 verification protocol v1.0.0 / preflight v3, plus the separately labelled VBL 10.5.2 draft implementation. The reviewer may narrow the scope but must name the version/hash reviewed.

## Independence requirement

The reviewer should not be the author of the clauses or the implementer of the code being reviewed. They should disclose prior involvement, financial or organisational interests, relationships with the author/maintainer, and any other conflicts that could affect the review. If independence cannot reasonably be established, record the review as `PEER_REVIEW` or `CONFLICTED_REVIEW`, not `INDEPENDENTLY_REVIEWED`.

## Requested scope

Please assess, within your competence:

1. Version boundaries and source provenance: does the package distinguish original source, excerpts, derivatives, and unverified claims clearly?
2. Normative clarity: are obligations, actors, evidence thresholds, time limits, exceptions, and outcomes objective enough to apply consistently?
3. Equal treatment and evidence asymmetry: does the standard require comparable cases to use the same criteria, and explain justified differences?
4. Correction and privacy: does it preserve a reliable correction history without retaining unlawfully excessive personal/sensitive information?
5. Independence and challenge routes: are conflict checks, appeals, and reviewer scope operationally adequate?
6. Technical verifier: examine implementation and tests independently; report the commands/commit/hash used and identify untested attack paths.
7. License/language structure: separate protectable text from general principles; assess language control, translation drift, rights-holder authority, and any custom conditions. Refer legal questions to qualified counsel rather than treating a technical pass as a legal opinion.
8. Release readiness: state what is required before a public release or production claim can be made.

## Review response template

- **Reviewer name / organisation:**
- **Relevant competence:**
- **Review date and timezone:**
- **Exact package version, source hash(es), and files reviewed:**
- **Prior involvement / conflicts:**
- **Review method and tools:**
- **Scope excluded or not tested:**
- **Overall assessment:** `PASS` / `PASS_WITH_CONDITIONS` / `REVISE` / `REJECT` / `UNABLE_TO_ASSESS`
- **Findings:** for each, include ID, severity (`BLOCKER`/`HIGH`/`MEDIUM`/`LOW`), evidence, impact, proposed correction, owner, and retest criterion.
- **Normative/legal language review:** (state jurisdiction and competence; legal conclusion only if qualified to give one)
- **Code/test review:** commands run, observed outputs, tests added, failures or limitations
- **Translation review:** languages and clauses compared; equivalence gaps
- **Release blockers:**
- **Residual risks accepted by whom and on what authority:**
- **Signature or verifiable approval reference (if available):**

## Scorecard

| Area | Required evidence | Status choices |
|---|---|---|
| Source/authority | Source ID, hash, rights-holder and release authority | PASS / GAP / N/A |
| Version boundary | Licence version distinct from framework/protocol/build version | PASS / GAP / N/A |
| Claim/evidence link | Each material assertion tied to evidence and standard | PASS / GAP / N/A |
| Comparable treatment | Method and reasons for material differences | PASS / GAP / N/A |
| Evidence access | Record controller, information gap, safeguard | PASS / GAP / N/A |
| Independent review | Distinct reviewer, competence, scope, conflict check | PASS / GAP / N/A |
| Correction integrity | Linked correction, reason, prior version preserved lawfully | PASS / GAP / N/A |
| Privacy/deletion | Minimisation, retention basis, redaction/deletion process | PASS / GAP / N/A |
| Appeal/contest | Practical route or reason unavailable | PASS / GAP / N/A |
| Language/version | Controlling-language decision and translation variance log | PASS / GAP / N/A |
| Licence scope | Text/principle/software/data/marks separated | PASS / GAP / N/A |
| Test quality | Independent tests, negative cases, reproducibility | PASS / GAP / N/A |
| External anchor | Independently retained/signed digest | PASS / GAP / N/A |
| Production evidence | Named deployment, role/access tests, observed results | PASS / GAP / N/A |

**Important:** completing a scorecard is not automatically a pass. Findings and evidence must support the selected outcome. This document has not been submitted to or completed by an external reviewer.
