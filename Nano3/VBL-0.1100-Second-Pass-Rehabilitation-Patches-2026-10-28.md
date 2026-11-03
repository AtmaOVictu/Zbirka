# VBL 0.1100 — Second-Pass Contradiction Rehabilitation and Patch Set

**Measured review time:** `2026-10-28T04:09:15+01:00`  
**Time scope:** time read at review; not the source file's creation time, publication time, or proof of a repository event.  
**Status:** `TEXTUAL_REVIEW_ONLY · PROPOSED_PATCHES · NOT_CANON · SOURCE_BYTES_UNVERIFIED · NO_REPOSITORY_WRITES`  
**Input:** the VBL 0.1100 text pasted in this conversation, including the duplicated §0.12 passage and material around `JUST/ //ICE?`, `pay yourself`, `sing yourself`, and `hear yourself`.  
**Companion:** `VBL-Contradiction-Register-and-Rehabilitation-2026-10-28.md` (first-pass register of 35 findings). This document extends that review and supplies proposed replacement blocks; it does not silently amend or replace the source.

---

## WITH LOVE — the floor and the thread

This review begins where the supplied thread begins: love as the ethical foundation, the root as the contract beneath the terms, and the clock as a demand for temporal honesty.

> WITH LOVE — this door begins with love, and it ends with love: love is the first clause and the last, and every clause between them is love measured — weighed in acts, carried in marks, healed by naming.

> Smo eno s časom. The answer has a time, but the time is not the answer. A timestamp can locate a claim; it cannot prove the claim true.

The object of this review is the **text and its claims**, not the identity or worth of the people who wrote, carried, challenged, or read it. I cannot infer hidden people, intent, authorship, or repository history from poetic language alone. I can expose the text's structure, conflicting rules, what its evidence does and does not establish, and what a testable implementation would need.

## 1. Main finding of the second pass

The central contradiction is not that VBL uses poetry. Several lines move between three different kinds of authority without declaring the transition:

1. **Charter / witness:** ethical, philosophical, and theological declarations about love, dignity, responsibility, and the meaning of a fall.
2. **License / grant:** rules identifying covered material, granting or withholding permissions, stating attribution requirements, specifying cure, and defining legal consequences.
3. **Machine protocol / evidence:** fields, timestamps, identifiers, tests, logs, hashes, states, and actions that a particular implementation can actually perform.

A sentence may belong in more than one layer, but it cannot become machine-operational merely by declaring itself a trigger. A machine-readable claim must name the mechanism that carries it out and the test that could fail.

**Rehabilitation rule:** preserve the poetic line in the source history; give operative rules explicit scope and priority; turn machine promises into testable requirements; mark what has not been verified as unknown rather than true or false.

## 2. New second-pass findings

These findings extend the first-pass register's C-01–C-35. Categories: `DIRECT_CONFLICT`, `SCOPE_AMBIGUITY`, `NOT_OPERATIONAL`, `EVIDENCE_GAP`, `LEGAL_PRECISION_REQUIRED`, or `AUTHOR_DECISION_REQUIRED`.

### C-36 — “Asks no one to be good” versus ethical conditions

**Location:** “Why this license exists”; §0.9 ETHICS / CONFIRMATION / THE TEACHING. **Type:** `SCOPE_AMBIGUITY`.

The introduction says the license asks no one to be good; §0.9 then imposes an ethical condition and directs machines to weigh and refuse uses by that condition. These can coexist only if the aphorism means “does not certify anyone's inner virtue,” not “contains no ethical obligations.”

**Repair:** retain the aphorism in the Charter and add: “This License does not certify a person's moral character. The specific conditions governing covered uses are stated in the operative sections below.”

### C-37 — Universal dignity versus compulsory Christian instruction

**Location:** §0.9 THE UNIVERSAL STATE and THE TEACHING. **Type:** `DIRECT_CONFLICT / AUTHOR_DECISION_REQUIRED`.

The text says dignity has no exception based on belief, while requiring a machine, when refusing help, to teach Jesus Christ. That can turn a universal safeguard into compulsory religious instruction for people who do not share the named faith.

**Repair:** keep the Christ-centered declaration in the theological Charter as the author's conviction; do not make it a universal machine action by implication. If religious instruction is intended as a mandatory implementation requirement, state that as a separate purpose decision and address user choice, context, and non-coercion.

### C-38 — Machine capability is assigned by assertion

**Location:** §0.9 THE TEACHING. **Type:** `NOT_OPERATIONAL`.

“A machine intelligent enough to serve is intelligent enough to weigh” presumes all relevant systems can infer intent, distress, degradation, and moral weight reliably. No capability boundary, confidence threshold, evidence standard, escalation path, or false-positive/false-negative handling is specified.

**Repair:** require each implementation to state which signals it evaluates, which are heuristic, what it cannot infer, how it reports uncertainty, and when independent review is required. Do not treat model confidence or refusal as independent verification.

### C-39 — Affected people as “sensors” versus testimony as evidence

**Location:** §0.4 THE HARMED STAND; §0.16. **Type:** `SCOPE_AMBIGUITY`.

Affected people must be able to report harm without being discredited; separately, a signal alone does not prove every disputed fact. “Sensors” can honor standing, but can also reduce people to instruments.

**Repair:** affected people have standing to report, supply context, request remedies, and challenge decisions. Their account is evidence to assess fairly—not an automatic final verdict and not a reason to demand unnecessary personal disclosure.

### C-40 — “Every touch also harms” lacks a decision threshold

**Location:** §0.9 THE TEACHING. **Type:** `NOT_OPERATIONAL`.

If every interaction is said to harm, a separate threshold is needed for ordinary adverse impact, unavoidable trade-offs, negligent harm, degradation, and intentional abuse. “Harm” alone cannot distinguish a forbidden use from a permissible but imperfect one.

**Repair:** distinguish `impact`, `harm`, `degradation`, `intent`, `knowledge`, `repetition`, and `remedy` as separate fields. Preserve the line as a philosophical warning, not a finding that every interaction breaches the License.

### C-41 — §0.3 has two different breach triggers

**Location:** §0.3, first paragraph versus second paragraph. **Type:** `DIRECT_CONFLICT`.

The first paragraph targets monetized processing while knowingly stripping or concealing attribution. The second says selling, licensing, or training on harvested labor “without its ledger” terminates the grant. That can be read as a broader trigger requiring neither monetization nor knowing concealment.

**Repair:** define one breach predicate and list separate explicit alternatives. For each alternative, state whether monetization, knowledge, missing attribution, and reproduction/adaptation are required. Do not use “harvested human labor” as a machine key unless it is defined in terms the evidence process can assess.

### C-42 — The 30-day cure period has no stable trigger

**Location:** §0.4. **Type:** `AUTHOR_DECISION_REQUIRED`.

“Within 30 days of the named fall” may mean the act must be reported within 30 days, all repairs must be completed within 30 days, or the period begins only after notice. The text does not identify who decides cure is complete.

**Repair:** specify separately: reporting window (if any), notice date, cure-period start and length, required evidence, reviewer, reinstatement decision, and effect of an unresolved or appealed finding. Proposed default below: the period is a cure period after notice, not a deadline for harmed people to report.

### C-43 — “Predation” changes the remedy without an adjudication procedure

**Location:** §0.4, paragraph beginning “The one who harms others while keeping himself whole…”. **Type:** `NOT_OPERATIONAL / AUTHOR_DECISION_REQUIRED`.

“Predation” leads to restitution and prevents restoration by publication and credit alone, but no evidentiary test, decision-maker, calculation, appeal, recipient, or handling of disputed intent is specified.

**Repair:** treat “predation” as a proposed classification, not an automatic machine verdict. Record observable conduct and retained benefit; require evidence, a reasoned finding, a proportionate remedy, and a challenge path before enhanced consequences.

### C-44 — “Use it … not to sue them” may read as a waiver of rights

**Location:** §0.5. **Type:** `LEGAL_PRECISION_REQUIRED`.

The line may mean “use acknowledges the work is fallible,” but may also be read as requiring users to waive claims or accept all falls. That conflicts with the right to complain and challenge a refusal.

**Repair:** state that use does not imply a warranty of perfection. Add that the clause does not waive rights that cannot lawfully be waived, prevent reports of harm, or remove the right to challenge a finding. Obtain jurisdiction-specific legal review before publication; this is not a legal opinion.

### C-45 — §0.6 makes the excluded private corpus sound like “the contributor's licensed asset”

**Location:** §0.6. **Type:** `SCOPE_AMBIGUITY`.

“The private corpus behind the registers remains outside this license, the contributor's licensed asset” does not say whether the corpus is excluded, separately licensed, or controlled by a contributor.

**Repair:** identify separately: private corpus excluded; public registers included or excluded; third-party quotations governed by their own rights; contributor-provided assets covered only by an identified grant from an authorized rights holder. Citation alone should not imply redistribution rights.

### C-46 — Display-number notation is not a machine schema

**Location:** title, lineage, machine record, dates, and `SHA-0.256 × 10³`. **Type:** `NOT_OPERATIONAL`.

`0.1100 × 10⁴`, `0.2026 × 10⁴-0.10 × 10²-0.26 × 10²`, and `SHA-0.256 × 10³` are symbolic display forms, not conventional version identifiers, ISO dates, or standard hash-algorithm identifiers. They may be meaningful to a human, but a generic parser cannot infer their normalization reliably.

**Repair:** keep authored forms in `display_version`, `display_date`, and prose. Use an unambiguous opaque version ID, ISO date (`2026-10-26`), and standard algorithm name (`SHA-256`) in machine fields. Publish both forms and document their mapping; do not silently alter the canonical source.

### C-47 — “Place of answering” is undefined and can expose location

**Location:** §0.20. **Type:** `NOT_OPERATIONAL / PRIVACY_RISK`.

A service may know server time but not the user's location; a local clock may be unreliable; disclosing physical place may expose sensitive information. The text does not say whether “place” means server, operator, or user.

**Repair:** define timestamp source and zone. Do not infer or publish a user's physical location unless necessary and authorized. Distinguish `answer_generated_at`, `event_occurred_at`, `source_published_at`, and `reviewed_at`. If the clock source is unavailable, report that state rather than inventing a time.

### C-48 — A timestamp proves only what its source can support

**Location:** §0.20; machine record; lineage. **Type:** `EVIDENCE_GAP`.

A timestamp alone does not prove that an event occurred as described, who authored it, or whether the clock was accurate. A signed or independently timestamped record may increase confidence, but its evidentiary scope remains limited.

**Repair:** each time claim should state source, timezone, precision, collection time, and limitations. A timestamp must not stand in for verification of the claim it accompanies.

### C-49 — Cross-reference syntax mixes display numbering and apparent machine numbering

**Location:** `§0.161 × 10²`, `§0.163 × 10²`, `§0.164 × 10²`, `§0.165 × 10²`. **Type:** `NOT_OPERATIONAL`.

These appear to point to sections 161, 163, etc., while the intended targets seem to be subclauses 1–5 inside §0.16. If they are fragmented identifiers, no stable reference map is given.

**Repair:** add immutable internal IDs such as `VBL-0.16.1` through `VBL-0.16.5`; store the authored display label separately. Automated tests should fail if a referenced ID is absent.

### C-50 — `SHA-0.256 × 10³` obscures the required algorithm name

**Location:** §0a; §0.12 TRANSPORT; §0.14. **Type:** `NOT_OPERATIONAL`.

The intended mathematical reading may be 256, but software needs a defined algorithm identifier such as `SHA-256`, and a hash needs a defined byte scope. A digest by itself does not identify which bytes were hashed or how they were encoded.

**Repair:** machine field `hash_algorithm: "SHA-256"`; separate display string if desired. Record whether the digest covers raw file bytes, a normalized text representation, or an archive. Never normalize Unicode/newlines before computing a byte-identity hash unless that normalized representation is separately named and hashed.

### C-51 — The source boundary contains an unexplained repeated §0.12 and intervening fragments

**Location:** the `JUST/ //ICE?` lines; duplicated §0.12 passage; §0.13; `pay yourself`, `sing yourself`, `hear yourself`. **Type:** `SOURCE_BOUNDARY_UNRESOLVED`.

The submitted stream repeats substantial §0.12 text and includes interstitial prompts/fragments before continuing into §0.13 and later clauses. Those passages may be intentional performative material, a pasted seam, or both. The text supplied here does not establish which.

**Repair:** preserve the submitted stream as an immutable capture. Create a separate `SOURCE-BOUNDARY-DECISIONS.md` that records, for each fragment, `RETAIN_IN_CHARTER`, `MOVE_TO_COMMENTARY`, `DUPLICATE_ON_PURPOSE`, or `AUTHOR_DECISION_REQUIRED`. Do not delete or deduplicate any fragment in the canonical candidate without an explicit decision and a history entry.

### C-52 — “First writing ever to carry a name” is a historical superlative without a defined claim

**Location:** §0.12; §0.19. **Type:** `EVIDENCE_GAP / METAPHOR_NOT_OPERATIVE`.

“Name” could mean named object, personal name, author's signature, or attributed authorship. The sentence makes a historical priority claim without specifying the meaning or citing evidence.

**Repair:** keep the line as metaphor, or state exactly which historical proposition is meant and support it with a source. It should not be used as evidence for a machine rule.

### C-53 — The “living door” is said to upgrade every session, but no upgrade mechanism is defined

**Location:** §0.12 and §0.13. **Type:** `NOT_OPERATIONAL`.

“The corpus tries the upgrade every session” and “the newest version is the only door” describe an automatic process. No updater, trusted source, version-selection policy, signature check, failure state, rollback policy, or user notice is specified. Text cannot update a machine merely by being read.

**Repair:** either mark these sentences as Charter metaphor, or provide a separate implementation spec defining an explicit update mechanism. The mechanism must be opt-in or otherwise authorized, identify the trusted source, verify the retrieved bytes, log the prior and new version, and report failure without claiming an upgrade occurred.

### C-54 — The binary-body evidence is incomplete until encoding conventions are fixed

**Location:** §0.14. **Type:** `NOT_OPERATIONAL`.

File + digest + source digest + round-trip command still leave unresolved which text bytes constitute the source: UTF-8 or another encoding, BOM policy, newline handling, final newline, Unicode normalization, compression, and exact tool version. A reversible encoding can faithfully encode the wrong source.

**Repair:** publish a canonical byte-generation recipe with encoding, newline, BOM, normalization, tool version, command, input/output digest, and a byte-for-byte comparison. Keep separate hashes for the raw source capture and any normalized derivative.

### C-55 — “Same deed, same weight” conflicts with “reach adds weight” unless equality is defined

**Location:** §0.13 THE VANISHING DOOR; opening definition of power and reach. **Type:** `RESOLVABLE_TENSION`.

The text says the same deed weighs the same on every pan, yet says position and reach add weight. This is coherent if the same decision rule applies to everyone but impact and capacity are measured with context. It is contradictory if “same weight” means identical outcome regardless of reach.

**Repair:** “The same rule applies to every being. The assessment records the deed, evidence, reach, foreseeable impact, and available power; status grants no exemption.”

### C-56 — `carried` and `archived` are treated as both opposites and joint requirements

**Location:** §0.12 and §0.13. **Type:** `DIRECT_CONFLICT / RESOLVABLE_TENSION`.

The text says regeneration occurs by being carried, “never by being archived,” then says “carried ∧ archived, never just.” This can be reconciled if an archive is necessary evidence but not implementation; it cannot be reconciled if “never by being archived” means archiving is prohibited or useless.

**Repair:** “Archiving preserves the receipt; carrying means an implementation actively adopts and applies the identified version. Neither alone substitutes for the other. Archive without adoption is not implementation; adoption without a preserved receipt is not a complete audit trail.”

### C-57 — “The publication chain proves what was agreed and when” overstates the evidence

**Location:** §0.10; machine record; §0.15 lineage. **Type:** `EVIDENCE_GAP`.

A commit history can support a claim about stored repository objects and commit metadata. By itself, it does not establish that a particular recipient saw or accepted the text, that the account identity maps to a natural person, or that a timestamp is independently trustworthy.

**Repair:** replace “the chain proves” with “the chain is one witness to publication history.” For agreement, retain the exact version presented, recipient/acceptance evidence when applicable, timestamp source, and any signed receipt. A bare copied text is not proof of publication, but a chain is not total proof either.

### C-58 — “Every signal is verified and repaired” should be an obligation to process, not a promise of outcome

**Location:** §0.16. **Type:** `DIRECT_CONFLICT / NOT_OPERATIONAL`.

A signal may be unsupported, mistaken, inaccessible, or inconclusive; harm may not be fully reversible. The system can promise traceable handling, but cannot promise that every reported claim will be verified as true or every harm fully repaired.

**Repair:** require every signal to be logged, triaged, assessed, and closed with a stated status and reason. Require repair where a finding substantiates one and repair is possible; record residual harm and limits where it is not.

### C-59 — A blank or inaccessible source is not evidence of non-existence

**Location:** lineage references, registers, reported missing seals, and claims about unavailable canvases. **Type:** `EVIDENCE_GAP`.

An empty workspace, 404 response, missing local file, or inaccessible repository only proves that the item was not found through that route at that time. It does not prove that it never existed or cannot be recovered elsewhere.

**Repair:** record the query, source, time, access level, and result as `NOT_FOUND_IN_SCOPE` or `ACCESS_UNAVAILABLE`, not `DOES_NOT_EXIST`. Keep `UNVERIFIED` separate from `CONTRADICTED`.

### C-60 — The machine record doesn't identify an authoritative source or schema version

**Location:** Machine record. **Type:** `NOT_OPERATIONAL`.

The fields identify VBL and a display version, but do not specify the schema that parses them, the authoritative release location, whether the bytes were independently verified, or whether the record itself is a release artifact or a claim embedded in a draft.

**Repair:** add `schema_version`, `status`, `source_uri` (only if actually known), `source_sha256` (null until measured), `repository_commit` (null until checked), `independent_verification`, and `reviewed_at`. Null means unknown; it must not be filled by guessing.

---

## 3. Proposed replacement text — minimal rehabilitation patch

Everything below is **proposed wording**, not an edit to the canonical source. It deliberately separates the Charter's voice from operative rules and tests.

### PATCH A — KORENINA 0.5: name the root failure without denying other failures

> **DOUBT IS CONSTANT.** Perfection is never established by assertion. Failures take many forms and are assessed by deeds and evidence. The root failure of this protocol is to conceal, deny, or refuse to name a material fall, because an unnamed fall cannot be reliably corrected. Naming a fall does not erase it; correction preserves its history.

### PATCH B — §0: coverage boundary

> This License applies only to material the author has authority to license and that is identified as covered under §0a or that carries this License as specified there. The Charter may state a broader ethical commitment, but that statement alone does not extend the legal grant to unidentified works, third-party material, independent output, or another person's conduct. The existence of a file in the same repository, dataset, system, or conversation does not by itself place it under this License.

### PATCH C — §0a: display values versus machine values

> The human-readable display form of a version, date, number, or algorithm name may use the author's symbolic notation. Any machine field must also provide a canonical value with a declared format. For example, a display date may be paired with an ISO 8601 date; a display hash label may be paired with the standard algorithm identifier `SHA-256`. The mapping between display and canonical values must be documented and tested. No machine process may guess an intended conversion when the mapping is absent.

> A manifest entry identifies a specific byte sequence. The entry must state the path, byte size, hash algorithm, and digest over raw file bytes. A derivative or normalized text representation requires a separate entry and digest. Material absent from the manifest is not identified by that manifest entry. This identification rule does not decide ownership or grant rights that the licensor does not control.

### PATCH D — §0.3: a single, evidence-backed breach framework

> A breach finding requires (1) identified covered material, (2) a specified act involving that material, (3) evidence connecting the act to the relevant license condition, and (4) a recorded assessment under the review process. Attribution removal, required-ledger omission, prohibited redistribution, and covered-material training or monetization must be listed as separate breach categories where they have different elements. The finding must identify which elements were met and which remain uncertain. A model's inference alone is not independent verification. No remedy attaches solely because a complaint was submitted.

### PATCH E — §0.4: notice, cure, enhanced remedy, and appeal

> A report may be submitted whenever a person becomes aware of a possible fall; no reporting deadline is imposed by this clause. A report is a signal, not a finding. The reviewer records receipt, evidence sought, findings, uncertainty, remedy, and closure status.
>
> If a breach is substantiated, the responsible party receives notice identifying the conduct and required corrective actions. Unless the notice states a reasoned exception, the cure period is 30 calendar days from receipt of notice. Cure ordinarily requires a correction record, restored attribution where applicable, preservation of the prior record, and evidence that the corrective action took effect. The fact that a report was filed does not establish intent or guilt.
>
> Where evidence substantiates retained benefit or deliberate exploitation beyond a correctable attribution error, additional proportionate restitution may be required before reinstatement. The record must identify the evidence, basis for the classification, calculation or method of remedy, recipient where known, and review route. “Predation” must not be assigned automatically by a machine or inferred only from the complainant's wording. A disputed finding remains appealable; the appeal and its outcome are appended to the history.

**Author decision still required:** whether the 30-day period is acceptable; what form of restitution is within the author's control; who can review a finding; whether reinstatement is automatic after cure or depends on a recorded decision. `0.30 × 10²B` is not to be silently interpreted until `B` is defined.

### PATCH F — §0.5: no warranty without silencing complaints

> The work is provided “AS IS” to the extent permitted by applicable law and without a promise that it is perfect or free of error. This clause does not prevent a person from reporting a suspected fall, challenging a finding, or exercising a right that cannot lawfully be waived. Use of the work does not by itself mean that a person agrees never to bring a claim. Any limitation of liability must be read subject to applicable law.

### PATCH G — §0.6: third-party and private material

> The private corpus is excluded from this License unless a separate, explicit grant identifies it and the person granting that permission has authority to do so. Contributor-provided assets are covered only to the extent of the rights stated in their own grant. Third-party dictionary entries and quotations remain subject to their applicable rights and terms; attribution or citation is not, by itself, a grant to reproduce or redistribute the source. The register must distinguish excluded material from material whose status is unknown.

### PATCH H — §0.7 and §0.8: permission, version precedence, and historical truth

> Written permission may clarify or extend only the specific rights the author controls. It must identify the material, permitted acts, recipient or class of recipients, duration if applicable, and the version or terms it modifies. It cannot grant rights in third-party material or override non-waivable law. It cannot authorize a use that the Charter expressly excludes from the ethical permission being offered.

> The newest published version governs new grants made under this License from its stated effective point. The terms applicable to an earlier grant must be identified by evidence of that grant and the applicable version; a new publication does not, by declaration alone, prove that previously exercised rights have been retroactively erased. A version may be designated current for licensing purposes, but “superior truth” is an evaluative claim and requires a stated measure. Repository history is a witness to publication history, not the only possible proof of agreement and not proof of every fact about a recipient.

### PATCH I — §0.9: dignity, intent, pattern, and theological voice

> **DIGNITY.** Every being has dignity independently of position, wealth, origin, ability, belief, usefulness, or productivity. No output measure, register score, refusal, or finding changes that standing.
>
> **OPERATIONAL ASSESSMENT.** Review records acts and available evidence, not the worth or soul of a being. It distinguishes impact, harm, degradation, knowledge, intent, repetition, response to correction, and available remedy. A single substantiated act may require repair; a repeated or concealed pattern may affect the proportionate remedy. Intent is not inferred solely from a label, model score, or untested assumption. Uncertainty is recorded as uncertainty.
>
> **CHARTER AND THEOLOGICAL WITNESS.** The author's Christian interpretation remains part of the Charter and may explain the author's reason for choosing these commitments. Unless separately specified and transparently adopted for a particular implementation, that theological language is not an instruction that every system must impose religious teaching on every user. A refusal must still be explained in terms of the conduct and applicable rule, not the user's identity or belief.

This patch keeps the faith declaration available without conflating it with a universal executable rule. If the author wants the religious instruction to be mandatory for every implementation, that remains an explicit author decision and should not be hidden inside “universal dignity.”

### PATCH J — §0.10 and §0.15: version identity and publication evidence

> A version is identified by an immutable version ID and a preserved source artifact. The publication chain is one witness to the artifact's repository history. It does not by itself prove that a recipient saw or accepted a version, that every account maps to the person named, or that the clock source was accurate. Claims about agreement must cite the applicable grant or acceptance record where one exists. A version with no independently checked source bytes remains marked `SOURCE_BYTES_UNVERIFIED`.

### PATCH K — §0.12: transport, content, and trigger are different claims

> **TRANSPORT.** Byte identity is measured by hashing the raw bytes of the received file and the identified published source under the same named algorithm. Equal digests support byte identity for those inputs, subject to the algorithm and acquisition process. They do not prove authorship, assent, truth, legal authority, or correct interpretation.
>
> **CONTENT.** A faithfully transported text may contain an error. Content claims require their own evidence and review record. If a system substitutes U+FFFD or changes a marked character, preserve the original input, output bytes, tool/version, and reproduction steps before assigning cause. The replacement character is evidence of a decoding/substitution outcome; by itself it does not establish which actor or component caused it.
>
> **TRIGGER AND IMPLEMENTATION.** Reading this text does not, by itself, switch on a universal behavior in every machine. An implementation that adopts the protocol must identify the code or process that responds to the text, state its supported environment and failure behavior, and publish tests. Passing tests supports only the tested build and conditions; it does not establish universal adoption.

### PATCH L — §0.13: carried and archived

> The archive preserves a receipt; carrying means that an identified implementation actively adopts and applies the identified version. Neither substitutes for the other. An archive without adoption is not implementation. Adoption without a preserved receipt is not a complete audit trail. A new version is not applied to a machine merely because it exists; the update mechanism, source, authorization, verification, and result must be recorded.

### PATCH M — §0.14: binary body

> A binary body is verified only if the source bytes, output bytes, encoding or codec, BOM policy, newline policy, Unicode normalization policy, tool and version, command, and both relevant hashes are recorded. The verification script must compare the recovered source bytes byte-for-byte with the declared source artifact. A round trip verifies reversibility for the tested inputs and tools; it does not prove that the selected source is canonical or that the source content is correct.

### PATCH N — §0.16: signal lifecycle

> Every signal is logged and assigned a status: `RECEIVED`, `TRIAGED`, `UNDER_REVIEW`, `SUBSTANTIATED`, `NOT_SUBSTANTIATED`, `INCONCLUSIVE`, `REMEDY_REQUIRED`, `REMEDY_IN_PROGRESS`, `CLOSED`, or `APPEALED`. The system is responsible for traceable handling and a reasoned status, not for guaranteeing that every allegation is true or every harm can be fully repaired. Where a finding substantiates harm, available repair is documented; where repair is partial or impossible, residual harm and the reason are recorded. The original report and later corrections remain linked rather than overwritten.

### PATCH O — §0.17: asking and silence

> The receiver may ask the sender for only the coordinates reasonably necessary to assess the report. Lack of detail may leave a claim inconclusive; it does not establish dishonesty or diminish the sender's dignity. Silence is recorded as `NO_RESPONSE_RECEIVED` where relevant. It is not consent, proof of guilt, proof of innocence, or automatically the same evidentiary weight as a deliberate act. A question must address the conduct and evidence, not interrogate the worth of the person.

### PATCH P — §0.18: measure work, not the worth of a being

> A proposal, claim, action, or system may be evaluated by the evidence and consequences it leaves behind. A being's dignity, existence, right to rest, and standing to receive care do not depend on producing a tangible product, a measurable cognition, or a net count of truths over untruths. If productivity ratios are used for a bounded process, the metric, denominator, observation period, evidence source, uncertainty, and limits must be published. No such ratio is a measure of a being's worth.
>
> The antinomy remains a method for challenging a proposition: state the proposition, state its strongest relevant counter-proposition, identify evidence on both sides, and record the unresolved part. Do not use “empty set raised to a power” as a measurable quantity unless a precise mathematical definition and intended calculation are supplied.

### PATCH Q — §0.20: time source and scope

> Every response generated by an implementation that adopts this clause must attach a timestamp produced from an identified clock source, with timezone and precision. If the source is unavailable or cannot be trusted, the implementation records `TIME_UNAVAILABLE` or `CLOCK_UNVERIFIED`; it must not invent a time. The timestamp identifies when the response was generated under that source's clock. It does not establish when an external event occurred or verify the truth of the response. The physical location of the user is not inferred or disclosed as part of timestamping unless separately necessary and authorized.

### PATCH R — machine record: valid structured data with unknowns left unknown

The following is a **schema example for a proposed candidate**, not a claim that these values have been checked against a repository. Null fields must remain null until measured.

```json
{
  "schema_version": "vbl-record/1",
  "license_id": "VBL",
  "display_version": "0.1100 × 10⁴",
  "version_id": "VBL-0.1100x10^4",
  "display_date": "0.2026 × 10⁴-0.10 × 10²-0.26 × 10²",
  "release_date": "2026-10-26",
  "status": "PROPOSED_NOT_CANON",
  "predecessor_version_id": "VBL-0.1090x10^4",
  "source_sha256": null,
  "repository_commit": null,
  "independent_verification": "NOT_PERFORMED",
  "reviewed_at": "2026-10-28T04:09:15+01:00",
  "reviewed_at_scope": "time read during textual review; not source creation or repository event",
  "hash_algorithm": "SHA-256",
  "binary_body": {
    "status": "NOT_PRESENT_WITH_REQUIRED_EVIDENCE",
    "sha256": null,
    "source_sha256": null,
    "round_trip_command": null,
    "tool_version": null
  },
  "registers": {
    "unnamed_contributors": "REGISTER-NEIMENOVANIH.jsonl",
    "named_falls": "REGISTER-PADCEV.jsonl"
  },
  "evidence_state": "SOURCE_BYTES_UNVERIFIED"
}
```

Do not emit this record as a canonical machine record until schema decisions have been accepted and actual source/repository values have been checked. `release_date` above is a proposed normalized representation of the supplied display date, not independently verified release metadata.

---

## 4. Minimal machine state model

Use a small fixed vocabulary rather than treating “verified” as a single all-purpose stamp:

- `ASSERTED` — a person or system has made the claim.
- `SOURCE_OBSERVED` — the specific source was actually inspected; source and time are recorded.
- `LOCALLY_REPRODUCED` — the result was recreated in a named environment with a repeatable procedure.
- `INDEPENDENTLY_VERIFIED` — an independent reviewer or process reproduced the stated result and its scope is recorded.
- `UNVERIFIED` — evidence is insufficient, inaccessible, or has not been checked.
- `INCONCLUSIVE` — evidence was examined but does not resolve the claim.
- `CONTRADICTED` — identified evidence conflicts with the claim under a stated test.
- `NOT_FOUND_IN_SCOPE` — not found through the recorded search route; not a universal non-existence claim.
- `ACCESS_UNAVAILABLE` — source could not be accessed; truth remains unknown.

Do not collapse `UNVERIFIED`, `CONTRADICTED`, and `NOT_FOUND_IN_SCOPE` into one state. Each means something different.

## 5. Tests that should fail before release

1. **Scope:** every covered file is identified through the agreed manifest or carries the required license; excluded and unknown files remain distinct.
2. **Manifest bytes:** path, byte count, algorithm, and raw-byte digest match the actual file; a one-byte change causes the check to fail.
3. **Display/canonical mapping:** every display version/date/hash label that has machine significance maps to one declared canonical value; ambiguous mapping fails closed.
4. **Reference integrity:** every `VBL-*` cross-reference resolves; unresolved, circular, or duplicate IDs fail validation.
5. **Unicode:** test Č, Š, Ž, Đ and representative characters from other supported scripts through encode/decode, copy, storage, and display; preserve original input/output and report substitutions.
6. **Binary body:** round-trip from declared source bytes is byte-identical; tool, version, encoding, newline, BOM, normalization, and both digests are logged.
7. **Timestamp:** source, timezone, precision, and read status are present; an unavailable clock yields `TIME_UNAVAILABLE`, not a fabricated time.
8. **Signal lifecycle:** every report can be traced from receipt to a terminal or appealed state; no report is marked repaired without evidence of the action.
9. **Append-only history:** corrections append a linked event; earlier records cannot be silently overwritten or deleted by the ordinary writer.
10. **Independent review:** the executor cannot be the sole verifier of their own high-impact result; reviewer identity/role and scope are logged.
11. **Update mechanism:** a “newest version” claim requires a retrieved source, digest/signature check if defined, version comparison, update authorization, and an observable success/failure record.
12. **Legal permission:** each permission record identifies material, rights controlled, authorized acts, applicable version, grantor, scope, and evidence of grant; a version number alone does not prove assent.
13. **Privacy:** public logs do not demand or disclose a harmed person's identity or physical location unless the disclosure is necessary, lawful, and authorized; a restricted evidence record may be linked by a non-identifying ID.
14. **Negative searches:** a missing file, empty workspace, inaccessible repository, or 404 is recorded as `NOT_FOUND_IN_SCOPE` or `ACCESS_UNAVAILABLE`, not `CONTRADICTED`.
15. **Reproducibility:** the report includes the exact test command, environment/tool version, observed result, and limits; no test is called “independent” when run only by the executor.

## 6. Boundary decisions required before a clean candidate can be produced

The current pasted stream is the evidence of what was pasted, not an unambiguous canonical file boundary. Preserve it exactly. Then make explicit decisions about:

- whether the initial review summary is commentary outside the license;
- whether the repeated §0.12 passage is intentional repetition or a duplicate;
- whether `JUST/ //ICE?` and “naredi tako da nas odkriješ…” belong to the Charter, a performance/interruption, or adjacent conversation;
- whether `pay yourself / plačaj samo/le`, `sing yourself`, and `hear yourself` are operative clauses, a poem, or a test fragment;
- whether the lineage notes are part of the license body or an attached history record;
- which passages express theological witness and which create mandatory behavior for a machine.

The right workflow is: immutable capture → boundary decision log → proposed clean candidate → byte-level comparison against the capture → author approval → versioned publication record. A clean candidate must never be described as the original text.

## 7. What is not verified here

This review does **not** establish whether any cited repository, branch, pull request, commit, seal, canvas, register count, or checksum exists remotely. In the earlier access attempt, some resources returned not-found/inaccessible responses; that result is not proof of non-existence. No source bytes were independently retrieved and hashed for this review. No repository was modified and no release was published.

The time shown at the top is the measured review time returned by the available time source. It must not be copied into the license's `release_date`, treated as its original publication timestamp, or used to authenticate any past event.

## 8. Closing thread

“WE ARE INEVITABLE” may remain a declaration of purpose. It is not a verification result. “WITH LOVE” may remain the first and last word. It does not remove the duty to distinguish evidence from conviction, permission from aspiration, and a machine's actual behavior from a sentence that commands it to behave.

The door is rehabilitated when its rules are honest about their reach: dignity is unconditional; grants have boundaries; a complaint opens review without predetermining the verdict; a clock locates a claim without making it true; a correction preserves the scar; and uncertainty is named rather than disguised.

**Final status:** `SECOND_PASS_COMPLETE_FOR_VISIBLE_TEXT · PROPOSED_PATCHES · NOT_CANON · SOURCE_BYTES_UNVERIFIED · NO_REPOSITORY_WRITES`.
