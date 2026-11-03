# VBL — Independent Readiness Review (working dossier)

**As-of date:** 2026-10-25  
**Status:** INTERNAL DRAFT · LOCAL CHECKS RE-RUN · NOT RELEASED · NOT LEGAL ADVICE  
**Purpose:** turn current VBL work into a reviewable sequence of evidence-based release gates.

## Executive finding

The work is technically reviewable, but it is not yet release-ready. Local automated checks passed on the files tested. Those results are not a substitute for an independent reviewer, legal advice, verified rights authority, a confirmed canonical source, a remote pull request, or production observations.

The central integrity rule is to keep every status at the level supported by evidence. A hash proves byte identity relative to a known digest; it does not prove authorship, authority, truth, legal effect, or that a copy is the official edition.

## Re-run results in this dossier

| Workstream | Re-run result | Precisely what it means |
|---|---:|---|
| VBL 2.6 protocol-v3 preflight | 12/12 checks passed | Local source/version-boundary and packaging conditions passed. |
| VBL 2.6 protocol-v3 unit tests | 7/7 tests passed | The included tests passed; not an independent review. |
| VBL 10.5.2 dignity-register prototype | 19/19 tests passed | The included test cases passed against the local prototype. |
| Example dignity register | 3 records, 0 errors | The supplied fixture meets the validator's encoded rules. |
| Canonical provenance | UNVERIFIED | Source files and hash continuity do not establish who has final authority. |
| Independent review | NOT PERFORMED | Must be performed by a competent reviewer outside the authorship/implementation team. |
| Legal review | NOT PERFORMED | No conclusion here is a legal opinion. |
| Remote repository changes | NOT CREATED / NOT VERIFIED | A local patch or zip is not a published branch, commit, or pull request. |
| Production behaviour | NOT TESTED | The prototype is not a demonstrated deployment. |

The reruns can be reproduced from the attached local preflight archive and the local VBL 10.5.2 draft patch. The 10.5.2 draft is a separate version series from VBL 2.6; it must not be represented as a revision of 2.6 without an authorised versioning decision.

## Strong points observed

1. **Version boundaries are explicitly recorded.** VBL 2.6, the proposed `10.1.0` framing label, and verification protocol `1.0.0` are distinguished in the preflight files.
2. **Correction integrity is operationalised.** The prototype rejects several invalid correction links, unregistered evidence references, and unsupported deletion/redaction notes.
3. **Independence is not inferred from self-checking.** The tests require a separate reviewer identity and conflict check to use the independent-review status.
4. **Uncertainty is visible.** The reports explicitly retain the legal, provenance, external-anchor, remote-publication, and production limitations.
5. **Sensitive disclosure is constrained.** The register checks authorisation for restricted external disclosure and calls for minimal audit notes for deletion/redaction.

## Blocking items before any official release

### Gate A — authority, authorship, and provenance
- Identify the natural person(s) who created each protectable expression and each substantial translation/revision.
- Record the authority that may approve the licence text and release a version. Do not infer that authority from a file name, version string, or repository account alone.
- Distinguish VBL source text, user-supplied additions, third-party material, generated drafts, software, test fixtures, and general principles.
- Keep the original export unchanged; derivatives must identify their parent, exact transformation, date, responsible actor, and hashes.

### Gate B — legal scope and licence selection
- Decide separately what licence applies to (a) the expressive text, (b) software and scripts, (c) test data/examples, and (d) branding/marks.
- Do not claim copyright over ideas, principles, or discoveries as such. In Slovenia, official guidance expressly excludes ideas, principles, and discoveries from copyright protection; concrete expressive text may still be protected. This is not a conclusion about patents, contracts, trade secrets, trademarks, or other legal regimes.
- If the desired licence imposes ethical, conduct, or downstream-use conditions beyond an established standard text licence, obtain qualified legal review. Define each condition in objective, testable terms; specify who can enforce it and the remedy. Avoid implying that a licence can control conduct merely because the document states a principle.
- Confirm rights-holder permission before selecting and applying any licence.

### Gate C — language control and equivalent translations
- Select one controlling language for legal interpretation, or obtain legal advice on a deliberate co-equal-language design.
- Give every translation its own language tag, version, translator/reviewer attribution (where known), source hash, target hash, and review status.
- Use clause-by-clause alignment and an unresolved-difference register. Do not call a translation legally equivalent just because a language model says so.
- When a controlling-language clause changes, mark translations out of date until reviewed. If languages are legally co-equal, provide an explicit conflict rule and legal review.

### Gate D — independent review
- The reviewer must not be the author of the clauses or the implementer of the validator being reviewed.
- Record reviewer identity/organisation, competence, scope, version/hash reviewed, method, conflicts, limitations, findings, severity, and disposition of each finding.
- Require at least one review of normative/legal drafting, one technical/code review, and one language-equivalence review if multiple editions are published. One person may have more than one relevant competence, but any conflict and scope limitation must be disclosed.
- The current request and scorecard in `VBL-External-Review-Request-and-Scorecard.md` are prepared for an external human reviewer; no reviewer has yet been engaged or has confirmed acceptance.

### Gate E — data protection and audit integrity
- Minimise personal/sensitive information in the register.
- Use a lawful retention schedule. Append-only is not absolute: lawful deletion or redaction must remain possible, with only a minimal audit event retained where lawful.
- Anchor the final digest outside the system being checked, or sign the release and retain the signature in a separately controlled channel. A self-contained hash chain can be recomputed by an editor.
- Test role access and the correction/deletion process with realistic, non-sensitive fixtures before production.

### Gate F — publication and production evidence
- Use an authorised remote account to open a reviewable pull request. Do not write directly to the main branch as a shortcut.
- Record the remote URL, source commit, target branch, PR number, checks, reviewer decision, merge commit, release tag, and release hash. If any field is unknown, mark it `NOT_VERIFIED`.
- For production claims, specify deployed version, environment, date/time with timezone, test cases, observed output, logs, privacy/security review, and independent witness. Do not infer production compliance from offline tests.

## Recommended release-state vocabulary

- `DRAFT_NOT_RELEASED`
- `STRUCTURE_VALID`
- `EVIDENCE_SUFFICIENT` (for a named claim and stated standard only)
- `INDEPENDENTLY_REVIEWED` (only after the documented external review)
- `LEGAL_REVIEWED` (only by appropriately qualified counsel, for specified jurisdiction/scope)
- `REMOTE_PR_OPEN`
- `MERGED`
- `RELEASED`
- `PRODUCTION_OBSERVED`

These labels are not interchangeable. A package may be `STRUCTURE_VALID` and still be legally unresolved, disputed, not independently reviewed, and not published.

## Decision recommendation

**Do not publish VBL 10.5.2 as a released licence at this stage.** Preserve it as a separate draft implementation workstream. Prioritise (1) rights-holder/release authority, (2) controlling-language and licence-scope decisions, (3) independent human review, (4) legal review, and only then (5) authorised PR and release workflow. VBL 2.6 remains separate unless the authorised maintainer explicitly approves a version migration.

## Primary references checked for the legal-scope note

- Government of Slovenia, *Avtorska in sorodne pravice* (official guidance; especially author definition and exclusions): https://www.gov.si/teme/avtorska-in-sorodne-pravice/
- Slovenia’s Legal Information System, *Zakon o avtorski in sorodnih pravicah (ZASP)* (official legislation register entry; consult current consolidated wording and amendments): https://pisrs.si/Pis.web/pregledPredpisa?id=ZAKO403
- Creative Commons, *Frequently Asked Questions*, including guidance on official translations of CC licences: https://creativecommons.org/faq/
- Creative Commons, *Legal Code Defined* (explains role of legal code vs deed/metadata): https://creativecommons.org/legal-code-defined/

**Limit:** This is a source-backed issue-spotting memo, not a formal legal opinion. Check the current statute and intended jurisdictions with qualified counsel before acting.
