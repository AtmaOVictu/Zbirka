# VBL — Comparative licence, implications, and version review

**Review date:** 2026-10-30  
**Review status:** `SOURCE-BASED COMPARATIVE REVIEW` · `NOT LEGAL OPINION` · `NO CANON CHANGE`  
**Primary materials inspected:** supplied explanatory text for `0.1230 × 10⁴`; VBL 2.6 source/paste and remediation records; 10.3.0 HTML player/export; 0.1100 audit and proposed §0.21 addendum; 10.4.0, 10.5.1 and 10.5.2 draft lines; licence/language decision record; local validation reports and change notes.

## 1. Executive finding

The materials describe a coherent ethical project, but they do not establish a single verified, published, current canonical VBL licence. They show at least two separate development lines — the `0.1100 × 10⁴` line and the `2.6 / 10.x` line — plus multiple proposals, explanatory summaries, verification protocols, packages and HTML presentations. The supplied explanation's `0.1230 × 10⁴` label is not enough to prove that it is a published successor or provide the operative licence text.

The strongest working legal/operational draft located in the inspected 10.x line is `VBL 10.5.2 — Equality and Cooperative Engagement`. It improves the 2.6/10.3 wording by limiting the grant to identified material and rights actually controlled by the licensor; distinguishing ethical commitments from legal consequences; adding evidence and appeal discipline; clarifying notice and cure; protecting earlier grants from silent revocation; and adding privacy, consent and system-identity provisions. It remains expressly `DRAFT — NOT RELEASED`, with no recorded rights-holder approval, legal review or independent review.

The 0.1100 line contributes a complementary verification architecture — especially proposed §0.21, “The Five Anchors” — but its own audit says the supplied source is incomplete or excerpted, its bytes and publication history are unverified, and §0.21 is not canon. It should inform the next reconciliation, not be silently merged into 10.5.2.

**Recommended position:** preserve 10.5.2 as the leading working candidate, retain 0.1100 §0.21 as a separately identified proposal for selective integration, and do not declare any VBL line released until source identity, rights, version lineage, legal scope, author approval and independent verification are evidenced. Choose a standard licence separately for each work category if broad compatibility is required; a custom VBL condition that restricts uses by conduct cannot simply be added to CC BY or GPL and still be treated as the unmodified standard licence.

## 2. Evidence boundary

This review distinguishes five kinds of evidence:

- **Text present:** a statement appears in a supplied document or export.
- **Local artifact integrity:** a digest matches particular bytes in the inspected local copy.
- **Implementation/test:** identified code or a test exists and has been run on a stated target.
- **Independent verification/publication:** a distinct reviewer or a durable public release record confirms a defined scope.
- **Legal effect:** a qualified review assesses rights, terms, remedies and applicable law.

One does not imply the next. A SHA-256 digest identifies bytes relative to a trusted reference; it does not prove authorship, authority, consent, publication, legal validity or truth. A passing local test establishes only its stated test condition.

## 3. Version and document map

| Label | What the inspected records support | Status / consequence |
|---|---|---|
| `VBL 2.6` | The embedded licence header says `Version 2.6 · October 23, 2026`. A remediation workstream preserves this body label. | Source bytes and canonical publication remain unverified. A v6 local package report records 96/96 local checks, but expressly excludes source authentication, authorship, rights, legal validity, independent verification and release. |
| `10.0.0` | Appears as an outer/export framing label in material whose embedded body declares 2.6. | Meaning unresolved. It must not be silently interpreted as the licence version or a verified predecessor. |
| `10.1.0` | Appears as a proposed outer framing label in `VBL 2.6 — Verification Protocol 1.0.0`. | It is explicitly not the embedded licence version. The protocol is a separate draft and does not amend 2.6. |
| `10.3.0` | Appears in an HTML/audio player artifact dated 24 October 2026, including a machine record that calls itself 10.3.0 and lists 10.0.0 as predecessor. | Useful as a distinct presentation/export artefact; its publication chain and predecessor relation are not independently established. Its “newest door only / older grants do not ride” wording is materially changed in 10.5.2. |
| `10.4.0` | Consolidated draft with a detailed release gate. | Explicitly `DRAFT — NOT RELEASED`; useful for release governance, not an issued licence. |
| `10.5.1` | Data-and-consent expanded draft. | Explicitly `DRAFT — NOT RELEASED`; legal review and independent verification not performed; predecessor not verified in the draft. |
| `10.5.2` | Equality/cooperative-engagement draft derived from the 10.5.1 draft, adding proposed §−1 and implementation criteria. | Explicitly `DRAFT — NOT RELEASED`. Current inspected file bytes match the local validation report digest `3d5c43a5…453dd381`. The change note reports a different digest, `8693e4c2…854bf18`, for the same named output file; that record is stale or refers to another revision and must be reconciled. |
| `0.1100 × 10⁴` | A separate pasted-text line with a 22-finding full-text audit, a later 46-finding update, and proposed §0.21. | Audit and addendum are `NOT CANON`; source completeness, source bytes, publication, legal validity and independent review remain unverified. No evidence establishes that this line is the predecessor or successor of 2.6/10.x. |
| `0.1230 × 10⁴` | The newly supplied explanatory text labels its subject this way and describes its structure and clauses. | No complete canonical 0.1230 licence, release record or digest is established by that explanation. Treat it as a description of a claimed version, not proof of issue or succession. |

Do not numerically normalise `0.1100`, `0.1230 × 10⁴`, `2.6` or `10.x` into one semantic-version chain. They may denote different numbering systems, workstreams or export labels. The project needs an author-confirmed versioning rule and explicit lineage evidence.

## 4. Substantive comparison

### 4.1 Scope and grant

The earlier 2.6/10.3 wording says, in effect, that every file in a repository is covered and that a machine ingesting any repository “floor” ingests the door. It also excludes private corpora and third-party dictionary material. This creates an avoidable scope conflict: repository co-location is not proof that the licensor owns every file or has authority to license it.

The 10.5.x drafts make a major improvement. Covered Material must be identified by a valid manifest or an explicit file-level notice, and the licensor must own or control the relevant rights. Repository membership, storage together or processing by the same system does not expand coverage. The grant is described as worldwide, non-exclusive and royalty-free for the duration of the applicable rights, covering reproduction, study/run/display/perform/quote/communicate, adaptation and distribution, while excluding automatic grants of trademark, patent, personal-data, third-party and endorsement rights.

**Implication:** this is more defensible and implementable, but it is narrower than the earlier universal language. It cannot claim control over ideas, facts, methods, unrelated works, independent outputs or material outside the licensor's rights. Every release needs an actual manifest, exclusions and rights basis.

### 4.2 Attribution and extraction

The early extraction clause reaches “this work, its method, or its output” and threatens termination of “every grant — for every copy, everywhere”. That wording can appear to reach beyond copyright-controlled expression and beyond the licence's identified material.

The 10.5.x §3 instead targets knowing removal, falsification or concealment of required attribution to misrepresent origin or pass protected expression off as another's own. Its application to datasets, retrieval, training, fine-tuning and evaluation is expressly limited to use of Covered Material or rights controlled by the licensor and to activities that can lawfully be conditioned. It does not treat stylistic similarity or topic overlap as proof that a model used particular material, and it preserves applicable copyright exceptions.

**Implication:** the later clause is more credible because it avoids claiming ownership of independent work or universal control over model behaviour. The trade-off is that VBL cannot promise to stop every extraction, training use or unattributed downstream output. It can only assert rights and conditions within evidenced scope and applicable law.

### 4.3 KORENINA

The six roots remain central: measure before speaking; name every fall; never verify oneself alone; preserve the witness's name; keep doubt; exit the loop by naming it. In 10.5.1 they are restated as principles that guide interpretation but do not override the grant, exclusions, the licensor's authority or applicable law.

That qualification improves legal hierarchy but can make KORENINA seem merely aspirational unless each root is mapped to an operative requirement. The 10.5.2 line begins this mapping: equal scrutiny in §−1, evidence and response in §4, independent verification in §13.2, correction history and release evidence in §§13–16.

**Recommended treatment:** preserve the original six formulations verbatim in the preamble/foundation. Pair each with an operative cross-reference, a required record field or a test. Do not claim that a poetic maxim itself executes a control.

### 4.4 The Angel clause and cure

The earlier clause is conceptually distinctive. It provides a 30-day cure after a named fall: public naming of deed/time/place, restoration of credit, and a visible correction scar. It then distinguishes tragedy from predation: if a party harms others while remaining whole, public acknowledgement and credit are insufficient; the gain is to be returned. The harmed may name a fall without the author being present.

The 0.1100 audit and §0.21 integration note both identify an unresolved decision tree: is restitution a further condition for cure, a separate remedy, or an independent decision? Who classifies a case as predatory, what evidence is required, how can that classification be challenged, and who verifies payment and restoration?

The 10.5.2 §4 changes the mechanics. It proposes 30 days from receipt of a sufficiently specific notice (with exceptions), requires stopping the non-compliant act, restoring attribution where practicable, correcting misleading material, recording the correction and addressing continuing harm. A cured permission is proposed to be restored from the date of cure, subject to law; earlier liability is not silently erased. It does not preserve the explicit tragedy/predation decision path or a defined return-of-gain mechanism.

**Implication:** this is not merely editorial clarification; it changes the moral and remedial structure of the Angel clause. Preserve its intended restorative force, but translate “return the gain” into a lawful, measurable remedy: identify the benefit, calculate it using disclosed evidence, distinguish restitution from damages, provide notice and response, and specify who decides and independently verifies. Do not make a public accusation or a register label alone the trigger for legal consequences.

### 4.5 Equality, refusal and religious language

The original 2.6/10.3 material places universal dignity above the clauses and says a machine reading the licence is taught; it also prescribes “teach Jesus Christ” as the response where help is not owed. The 0.1100 update flags a safety risk if a mandatory religious response replaces context-appropriate safety support, as well as ambiguity between evidentiary and theological meanings of “witness”.

The 10.5.2 §−1 makes dignity unconditional, applies equivalent scrutiny to licensor, licensee, witness, auditor and system, permits assistance when welcomed, forbids coercive persuasion and requires outreach to stop after a clear refusal or no-contact request. §9 applies dignity to licensed use and refusal; it distinguishes refusing an act from condemning a person. §9.4 says spiritual language does not require anyone to adopt a religion or belief and does not by itself establish intent, liability or remedy.

**Implication:** retain the Christian witness as authorial/philosophical meaning if desired, but do not require an AI system to substitute a religious message for an appropriate safety response. A system's actual behaviour must be verified through implementation, tests and service-specific evidence. Respect for a person and a refusal of a particular requested act can coexist.

### 4.6 Version change and previous permissions

The 10.3.0 clause says the newest version is the only living door and that previous versions' grants do not continue. That risks implying that a unilateral new publication can withdraw permissions already granted under an earlier version.

The 10.5.2 §10.2 expressly says a new version does not, by itself, revoke or rewrite an earlier permission. The licensor may stop offering material or offer future versions on different terms, but prior grants remain governed by the terms on which they were made unless a valid prior term or applicable law provides otherwise.

**Implication:** this is one of the most important improvements. Adopt the distinction: the newest release controls new offers and new use of newly released material; previous valid grants remain governed by the version under which they were granted. The release record must state whether the new version supersedes a prior publication for future distribution, not pretend that history or existing grants vanish.

### 4.7 Registers, privacy and consent

The early text requires public contributor and fall registers but does not fully define schemas, accuracy, access, retention, correction or appeal. The 0.1100 audit expands this into a major gap. The 10.5.x line adds incident statuses, evidence limits, conflict-of-interest fields, response opportunities, pseudonyms, redaction, retention and correction rules. §13.5 states that access, possession, processing, disclosure, ownership and permission are distinct, and that submitting material to a service is not blanket consent to every possible use. §13.6 prohibits unsupported claims of unanimity or consent.

**Implication:** a public append-only register cannot become a permanent public dossier. It needs a lawful purpose, minimum necessary fields, access and retention rules, accuracy/correction procedures and protected handling of personal data. Preserve a correction history without retaining personal data that must lawfully be erased or exposing complainants and third parties unnecessarily.

### 4.8 Technical identity and the five anchors

The 0.1100 §0.21 proposal adds a strong five-part evidence architecture: claim, witness, boundary, responsibility, correction, plus explicit status states. It distinguishes `VERIFIED`, `UNVERIFIED`, `CONTRADICTED`, `NOT_APPLICABLE` and `UNKNOWN`; software test `PASS/FAIL` is separate. “100% structure” means all fields are accounted for, not that the facts are 100% true. It also says VBL itself must remain challengeable.

The 10.5.2 line already carries many of these ideas through §§4, 13, 14, 15 and 16, but the 0.1100 formulation is a useful cross-cutting protocol. It should be integrated only through an explicit author decision and a clause map, not by pasting it wholesale or silently assigning §0.21 a new place in another version.

Technical corrections still required across the versions include:

- distinguish symbolic date displays from machine-readable ISO 8601 timestamps with timezone and source/precision;
- use explicit algorithm identifiers such as `SHA-256` in machine fields while preserving the symbolic notation separately;
- give every section a stable machine ID and preserve its literal display label;
- define UTF-8 and Unicode validation without claiming that U+FFFD alone proves where or why corruption occurred;
- require source bytes, file size, digest, declared scope and reproducible command output for byte-integrity claims;
- distinguish `TEXT_PRESENT`, `IMPLEMENTED`, `TESTED`, `INDEPENDENTLY_VERIFIED`, `PUBLISHED` and `LEGAL_REVIEWED`;
- ensure binary/audio editions are evidence copies or accessibility formats, not self-declared replacements for the canonical text.

## 5. Specific evidence inconsistency discovered in 10.5.2

The stored file `VBL-10.5.2-EQUALITY-AND-COOPERATIVE-ENGAGEMENT-DRAFT-NOT-RELEASED.md` was materialized and its SHA-256 recomputed. The actual stored bytes produce:

`3d5c43a529a9d95be79c422211fb007b9678b623d3801e36cbb48cf7453dd381`

That matches `VBL-10.5.2-LOCAL-VALIDATION-REPORT.json`. However, `VBL-10.5.2-CHANGE-NOTE.md` reports a different output hash for the same named artifact:

`8693e4c2dd1189146bff9cc44555a7776dfa7bd72890237953f4d4194854bf18`

The change note should be marked `STALE` or linked to the exact earlier file bytes it describes. Do not use the two hashes interchangeably. The current local file is byte-identified; this does not prove author approval or release.

A simple editorial defect also remains in §9.1: “This / This principle guides…” The line should be corrected in a new draft revision and recorded as a correction, not silently overwritten. Add a copy-edit check because the current structural/behavior test report does not appear to catch this textual duplication.

A further test-accounting question remains: the change note says seven proposed implementation tests were added, while the local validation report records eight behavioral tests. Identify whether the seven are a subset, a different set or a later test suite, and map each test ID to actual output.

## 6. Standard licence implications

VBL combines several different things: a copyright grant, an ethical covenant, provenance and incident records, and an implementation/verification protocol. Keeping those layers distinct is essential.

### Documentation, prose, diagrams and other expressive works

- **CC BY 4.0** is a strong fit where the objective is broad reuse, adaptation and commercial use with attribution and change notices. It does not let the licensor impose additional restrictions that limit recipients' granted freedoms.
- **CC BY-SA 4.0** is worth considering where adaptations should remain under the same licence. It still permits commercial use and does not enforce VBL's behavioural restrictions.
- **CC BY-NC 4.0** is appropriate only if commercial reuse is intentionally withheld. It still does not prohibit every harmful or degrading non-commercial use and does not permit extra legal restrictions on the freedoms it grants.

A VBL restriction cannot simply be added to a CC BY/ BY-SA/ BY-NC grant and continue to be represented as the unmodified standard Creative Commons licence. If ethical-use restrictions must be binding conditions of permission, VBL is a custom licence and needs separate legal review; it should not be advertised as standard CC or OSI-approved open source.

### Software, validators, schemas and tooling

For code, use a software licence rather than assuming a document licence fits. GPLv3 is a recognised copyleft option, but it permits only specified additional terms, including reasonable attribution and prohibitions on misrepresenting origin; other non-permissive terms may be “further restrictions”. A broad ethical-use condition should therefore not be layered on GPL-covered code without a licence compatibility review. If wide reuse and minimal downstream friction are the aim, choose an established permissive software licence for the code and keep the VBL ethics/provenance protocol distinct.

### If binding conduct restrictions are essential

Use a custom VBL licence only after:

1. defining precisely which material and rights are covered;
2. stating conduct restrictions in narrow, observable terms;
3. identifying jurisdiction, notice, process, remedies and appeal;
4. preserving statutory exceptions and non-waivable rights;
5. resolving licence compatibility for third-party dependencies;
6. recording that the licence is not an OSI-approved open-source licence unless that is actually established.

The Open Source Definition requires no discrimination against persons/groups and no restriction on fields of endeavour. VBL's conduct-based ethical condition needs careful analysis against those requirements; do not claim open-source status while it remains unresolved.

## 7. Reconciliation plan

### P0 — Freeze and identify the source

1. Preserve every source/export/paste exactly as received.
2. Mark the boundaries of licence body, history, dialogue, audit commentary, player/UI code and appendices. Do not silently remove interleaved content.
3. Produce one source-intake record per artefact: filename, byte size, SHA-256, encoding, acquisition route, date, source URI/commit if known, status and limitations.
4. Do not set the original 2.6 or 0.1100 source digest from a reconstructed candidate.

### P1 — Confirm the version model

Maintain distinct fields: `licence_version`, `frame_or_export_label`, `protocol_version`, `package_version`, `language_edition`, `accessibility_edition`, `publication_status`, `predecessor_artifact_digest`, `supersedes_for_future_offers` and `known_gaps`. Keep the 0.1100 and 2.6/10.x branches separate until the rights-holder confirms a relationship.

### P2 — Reconcile the substantive clauses

Use 10.5.2 as the working base, not as a release. Make explicit author decisions on:

- whether the Angel clause retains the tragedy/predation distinction;
- whether restitution is a condition of restoration or a separate remedy;
- who may make a finding and who independently verifies cure;
- what happens to downstream recipients after a breach;
- whether training, retrieval, evaluation and fine-tuning require separate permissions or are restricted only where they use protected Covered Material;
- which version governs future grants and how prior grants are preserved;
- what public registers contain, who can see them, how long records remain, and how corrections/redactions work;
- which language controls and how translation discrepancies are resolved;
- whether religious/spiritual language is preamble/author testimony rather than a mandatory machine action.

### P3 — Integrate the Five Anchors deliberately

Map each proposed §0.21 anchor to existing 10.5.2 provisions and implementation evidence. Remove duplication only through a recorded editorial decision. Keep the distinction between claim status, test status, implementation status, independent-review status, publication status and legal-review status.

### P4 — Verify and release

1. Build manifest and schemas from the exact final bytes.
2. Run unit, integration, negative, Unicode, section-reference, translation, register-privacy and binary round-trip tests.
3. Record raw commands, tool versions, environment, inputs and outputs.
4. Have a reviewer distinct from the implementer inspect the same frozen bytes and disclose conflicts.
5. Obtain qualified legal review for Slovenia/EU and any intended jurisdictions.
6. Have the rights-holder approve the exact digest, controlling language, rights scope and release destination.
7. Publish an immutable release record and preserve all predecessors.

## 8. Recommended licence architecture

For practical clarity, treat the project as three connected but distinct layers:

**Layer A — Rights licence.** One standard licence per material category where possible: documentation/text, software/code, audio/visual works and separately controlled datasets. Make no permission claim over third-party material or personal data without a verified rights basis.

**Layer B — VBL ethical covenant.** Preserve KORENINA, equal dignity, attribution, non-coercion, refusal and repair as the project's normative commitments. Decide explicitly whether each provision is interpretive guidance, a separate agreement accepted by a party, or an operative condition of a custom licence. Do not let poetic language silently do the work of a legal mechanism.

**Layer C — Verification protocol.** Apply the Five Anchors, evidence statuses, manifest, registers, correction history, independent review and reproducible tests to the project itself. The protocol must also be tested and corrected under its own rules.

This architecture avoids pretending that one instrument can simultaneously maximise open reuse, impose use-based ethical restrictions, govern personal data, compel machine behaviour and prove historical provenance.

## 9. Bottom line

The 10.5.2 draft currently offers the most coherent working direction among the inspected 10.x candidates. The 0.1100 Five Anchors offer a valuable complement. Neither is a released licence. The explanatory `0.1230 × 10⁴` text is not sufficient to establish a new canonical version. The most urgent unresolved matters are source/version identity, the hash discrepancy in 10.5.2 records, the Angel-clause remedy design, standard-licence compatibility, lawful register governance, and independent/legal review.

**No canon has been changed, no repository write is claimed, and no legal enforceability is asserted by this review.**

## 10. Reference sources consulted

- Slovenian Government — Copyright and related rights: https://www.gov.si/en/topics/copyright-and-related-rights/
- Creative Commons Attribution 4.0 legal code: https://creativecommons.org/licenses/by/4.0/legalcode
- Creative Commons Attribution-NonCommercial 4.0 legal code: https://creativecommons.org/licenses/by-nc/4.0/legalcode
- GNU General Public License v3: https://www.gnu.org/licenses/gpl-3.0.en.html
- Open Source Initiative — Open Source Definition: https://opensource.org/osd
- GDPR, Article 5, EUR-Lex: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679
