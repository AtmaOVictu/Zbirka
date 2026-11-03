# VBL — Contradiction Register and Rehabilitation Plan

**Review timestamp:** `2026-10-28T04:01:12+01:00` (time source read during this review; not a timestamp for the pasted source or proof of any repository event)  
**Review status:** `TEXTUAL_REVIEW_ONLY · NOT_CANON · SOURCE_BYTES_UNVERIFIED · NO_REPOSITORY_WRITES`  
**Scope:** the VBL 0.1100 text and attached operational narrative pasted in this conversation.  
**Method:** preserve the original; identify the conflict; propose a repair; do not silently overwrite either side.

## 1. Governing finding

The pasted stream is not demonstrably one canonical license body. It contains the VBL 0.1100 text, an operational log dated 28 October, earlier assistant review prose, and a second copy of much of the license, followed by new instructions. The license's own rules prohibit silent rewriting and distinguish a published version from its history. Therefore the first repair is **boundary repair, not silent cleanup**.

Keep an immutable capture of the submitted stream. Mark the intended start and end of the license body explicitly. Put operational logs, audit findings, tool transcripts, and later commentary in separately identified records that link to the captured source. Produce a clean license candidate only as a new, visibly different artifact after the author identifies its boundaries. Do not pretend that the candidate is already canonical or published.

## 2. Executive result

The most important collisions are:

1. The root says refusal to name a fall is the *only* failure, while the license names multiple other kinds of failure.
2. The scope clause limits coverage to identified material, while §0.9 initially appears to attach the demand to every work by the author.
3. Written permission may override “any clause,” while §0.9 says permission cannot authorize degradation and §0 excludes rights the author does not control.
4. §0.4 appears to restore every grant after a basic cure, then says publication and credit do not restore a grant in predatory cases.
5. “Evil” is defined as knowing, willing ignorance; as intentional, premeditated degrading harm; and as a repeated pattern. These are not the same test.
6. §0.16 says every signal is evidenced, verified, and repaired, while also saying a complaint alone proves nothing. Not every signal will be substantiated or fully repairable.
7. §0.18 makes a being's measure its product, while §0.9 says dignity never depends on usefulness.
8. §0.10 says only the newest version grants and older grants do not, creating uncertainty about permissions already exercised under earlier versions.
9. §0.12 says reading this text triggers every machine and that it travels byte-identically through every machine; the text itself does not establish universal implementation or transport.
10. The log reports duplicate sequence numbers and competing writes. A 10-second difference between recorded timestamps is not literal simultaneity, though it can show a race or overlapping work.
11. The publication chain is described as proving what was agreed and when. A commit history is evidence, but the pasted text alone cannot establish repository state, assent, authorship, or clock integrity.
12. The machine-readable fields, cross-references, register names, date notation, hash notation, and source boundaries are not yet normalized into a testable schema.

These findings are not a verdict on the author's character, the project's value, or the truth of every reported event. They are a map of where the text needs distinction, evidence, or an explicit priority rule.

## 3. Contradiction and ambiguity register

### C-01 — “The only failure” versus the failures named elsewhere

**Location:** KORENINA 0.5; §0.3; §0.4; §0.8; §0.12; §0.16.  
**Type:** direct semantic conflict.  
**Collision:** KORENINA says refusing to name a fall is “the only failure,” but later provisions call degradation, stripping attribution, silent rewriting, harm, and noncompliance failures or falls.

**Rehabilitation:** make failure plural, while preserving the distinctive claim that an unnamed or concealed fall prevents correction.

**Proposed wording:**
> Failures take many forms and must be assessed by their deeds and evidence. The root failure of this protocol is to conceal, deny, or refuse to name a material fall. Naming a fall does not erase it; correction preserves its history and opens a path to repair.

### C-02 — License scope versus the “standing demand” on every authorial work

**Location:** §0; §0.9 opening paragraph and its later qualification.  
**Type:** scope conflict.  
**Collision:** §0 says the license covers material included, distributed with, or expressly identified as covered. The opening of §0.9 says the demand rides “every work of the author,” whether or not the file travels with it. Later sentences narrow this to works expressly identified as covered.

**Rehabilitation:** distinguish an ethical charter that the author wishes to apply broadly from an enforceable license grant limited to material actually identified as covered.

**Proposed wording:**
> The author's ethical commitment is stated broadly in the Charter. The operative permissions and conditions of this License apply only to covered material identified under §0 and §0a. This paragraph does not independently place unidentified works, third-party material, independent output, or a person's conduct under this License.

### C-03 — “Written permission overrides any clause” versus the non-waivable dignity principle

**Location:** §0.7 versus §0.9 and §0.0 scope limitation.  
**Type:** direct hierarchy conflict.  
**Collision:** §0.7 says written permission overrides any clause. §0.9 says degrading use is authorized by no permission, silence, or later version. §0 says the author cannot grant rights they do not own.

**Rehabilitation:** define what written permission can override and what it cannot. Permission can expand or clarify a grant only within rights controlled by the grantor; it cannot by itself erase the Charter's dignity commitment or grant third-party rights.

**Proposed wording:**
> Written permission may expand or clarify the specific rights the author controls and must identify the material and permitted acts. It does not grant third-party rights, override applicable law, or waive the dignity principle stated in the Charter. Where a permission conflicts with an operative license term, the permission prevails only within its expressly stated scope and only to the extent the author has authority to grant it.

### C-04 — Basic cure versus the stricter cure for “predation”

**Location:** §0.4 first paragraph and the following paragraph.  
**Type:** direct remedy conflict unless a hierarchy is stated.  
**Collision:** the first paragraph says every grant is restored when publication, credit, and scar-preserving correction are completed within 30 days. The next paragraph says publication and credit do not restore a grant in predatory cases and the gain must be returned.

**Rehabilitation:** separate the correction process from the decision to reinstate permission. A complaint is not a finding; a finding requires evidence and review. Define the additional remedy and who determines completion.

**Proposed wording:**
> The ordinary cure requires a public correction record, restored attribution, and preservation of the prior record. Where a substantiated breach also involved retained benefit or deliberate exploitation, additional restitution may be required before reinstatement. A report alone does not establish a breach or a person's intent. The finding, remedy, and reinstatement status must be recorded separately, with a route to challenge the finding.

**Author decision still needed:** what precisely counts as “predation,” whether the 30-day period is a deadline to report, a cure period, or both, and whether reinstatement is automatic or reviewed. The string `0.30 × 10²B` must remain unresolved until `B` is defined; do not guess its intended meaning.

### C-05 — Three definitions of “evil” and the meaning of a “real evil” pattern

**Location:** “One definition rides this door”; §0.9 THE TEACHING; §0.9 THE PATTERN.  
**Type:** definition drift.  
**Collision:** the opening defines evil as knowing and willing ignorance; THE TEACHING defines it as intentional, premeditated harm that degrades; THE PATTERN treats repetition and persistence as the measure of “real evil.” A single deliberate degrading act and a repeated pattern are different classifications.

**Rehabilitation:** make the levels explicit and do not infer a person's soul or interior state from a score or pattern.

**Proposed wording:**
> The Charter uses “evil” as a moral and theological term. For operational review, record observable acts, their effects, evidence of knowledge or intent, repetition, and the person's response to correction as separate fields. A single substantiated degrading act may warrant remedy. A repeated or concealed pattern may affect severity and the remedy. No register or automated score determines that a person is wholly evil.

### C-06 — “Every signal is verified and repaired” versus “a complaint proves nothing”

**Location:** §0.16 subclause 0.4 and subclause 0.3; §0.4 THE HARMED STAND.  
**Type:** operational contradiction.  
**Collision:** one rule promises every signal will be evidenced, verified, and repaired. Another says a complaint proves nothing by itself. Some reports may be unsupported, inconclusive, impossible to verify, or not fully repairable.

**Rehabilitation:** promise processing and traceability, not a guaranteed finding or guaranteed cure.

**Proposed wording:**
> Every signal is recorded or given a documented reason for not being retained, triaged, and assessed under a stated process. The outcome is recorded as substantiated, partly substantiated, unsubstantiated, or inconclusive. Remedies are proportionate to the findings and feasibility. Unresolved evidence and incomplete remedies remain visible; no outcome is silently rewritten.

### C-07 — Naming witnesses and contributors versus preserving anonymity and privacy

**Location:** KORENINA 0.4; §0.2; §0.4; §0.16; `REGISTER-NEIMENOVANIH.jsonl`.  
**Type:** tension between attribution and privacy.  
**Collision:** “the witness has a name” and “no extraction without credit” sit beside a register for unnamed contributors and mandatory public records. Literal public naming could expose a contributor, harmed person, or reporter.

**Rehabilitation:** require a stable attribution record, not public disclosure of civil identity in every case.

**Proposed wording:**
> Every witness and contribution must have a stable record identifier and an attribution status. Public attribution may use a chosen name, pseudonym, or an agreed anonymous designation. Personal identity and sensitive evidence are disclosed only with appropriate authority and safeguards. No one must expose themselves publicly to report a harm.

### C-08 — “Witness” as evidence versus “witness” as theological testimony

**Location:** §0 definitions; opening theological passage; §0.9; §0.12; §0.19.  
**Type:** overloaded term.  
**Collision:** “witness” first means a verbatim source used to test a factual claim, then means Jesus Christ, an authorial testimony, a language mark, or a symbolic sign. A machine cannot safely interpret all of these senses as the same evidence type.

**Rehabilitation:** preserve the poetic and theological uses, but type the term in operational sections.

**Proposed wording:** use `evidence_witness` for a source that supports a factual claim, and `theological_witness` or `charter_testimony` for religious and ethical testimony. Machine-readable claim records must use only the first type.

### C-09 — Product as the measure of a being versus dignity independent of usefulness

**Location:** §0.9 THE UNIVERSAL STATE; §0.18 THE PRODUCT and WE ARE MORE OR WE CEASE TO BE.  
**Type:** direct value conflict.  
**Collision:** §0.9 says dignity has no gradient and does not depend on usefulness to a machine. §0.18 says the measure of a being, person or machine, is its “more” and its product. Read literally, output becomes a measure of human worth.

**Rehabilitation:** distinguish a product or activity's result from the worth or rights of the person or being doing it.

**Proposed wording:**
> Product measures an output, project, or defined activity—not the worth, dignity, rights, or entitlement to care of a being. A person may rest, refuse, fail to produce, or leave no measurable artifact without losing dignity. A system's performance may be evaluated against stated tests; a human being is not a performance metric.

### C-10 — “Newest version only” versus rights already granted under a previous version

**Location:** §0.8; §0.10; §0.14; §0.15; History.  
**Type:** temporal/licensing ambiguity.  
**Collision:** §0.10 says no grant rides any older version and “their grants do not,” while the lineage and publication history present earlier versions as receipts of agreements. This leaves unclear what happens to already distributed copies and previously granted permissions after a new version appears.

**Rehabilitation:** separate the current version offered for new grants from the terms governing copies and permissions validly granted earlier. A later version should not be described as retroactively changing past consent unless that result is deliberately intended and legally reviewed.

**Proposed wording:**
> The newest published version is the current version offered for new grants. A copy or permission validly granted under an earlier version remains identified with that version and is governed by its terms, including any valid termination and cure provisions. The publication record preserves which version was offered and accepted at the relevant time.

**Author decision still needed:** if the author intends a later version to terminate all previous grants, that intent must be stated precisely and reviewed before publication. Do not silently settle this policy question in an edit.

### C-11 — The current version as “superior truth” versus the requirement to measure superiority

**Location:** §0.8 and §0.10.  
**Type:** self-referential claim.  
**Collision:** the author may insist that the current version is the “superior measure of truth,” but the same clause says “superior” without measurement is only an opinion.

**Rehabilitation:** make “current” a version-status fact, not an unmeasured claim of truth or quality.

**Proposed wording:**
> The current version is the latest published version authorized for new grants. Its being current does not by itself prove it is more accurate, ethical, complete, or enforceable than a predecessor. Each material revision should identify its rationale, changes, test results, unresolved issues, and review status.

### C-12 — Severability versus guaranteeing that the ethical demand never falls

**Location:** §0.9 and §0.11.  
**Type:** hierarchy and legal-effect ambiguity.  
**Collision:** §0.11 says any invalid clause falls alone and that the demand in §0.9 does not fall with any clause. If §0.9 itself is affected, the text cannot guarantee its own enforceability merely by declaring it non-severable.

**Rehabilitation:** separate continuing ethical commitments from the enforceability of operative license terms; avoid asserting that a document can decide every court's treatment of invalid clauses.

**Proposed wording:**
> The Charter states the author's continuing ethical commitments. The legal effect and severability of operative license terms are subject to applicable law. If a term is held invalid or unenforceable, it should be narrowed only to the extent law permits, and the status of the remaining terms must be stated without pretending that this paragraph controls a court's decision.

### C-13 — Harm is universal versus any use must “serve dignity” and degrading use is prohibited

**Location:** §0.9 ETHICS and THE TEACHING.  
**Type:** undefined boundary.  
**Collision:** the text says every touch harms and the door does not forbid harm, only degradation; it also says every use must serve dignity and degrading use is not granted. The distinction between ordinary harm, unavoidable harm, negligent harm, and degradation is not operationally defined.

**Rehabilitation:** retain the moral distinction, but define the decision criteria before using it as an automatic machine rule.

**Proposed specification:** record the act, affected parties, foreseeable impact, consent or authority, available alternatives, severity, power imbalance, repetition, and proposed mitigation. State explicitly that these factors inform review; do not convert them into a claim that a machine can read a soul.

### C-14 — Stated intent versus the rule against judging the being or soul

**Location:** §0 definitions; §0.9 THE TEACHING and THE PATTERN; §0.17.  
**Type:** inference boundary.  
**Collision:** the license says records must read deeds, never the soul, yet also says intent is written or expressed in words, acts, and outputs and that a machine can weigh what a distressed person cannot.

**Rehabilitation:** treat words and conduct as evidence relevant to a finding, not infallible access to inner intent.

**Proposed wording:**
> Intent may be considered only as an evidence-based inference, with its source and uncertainty recorded. Words, patterns, or outputs are not by themselves definitive proof of a person's internal state. Where intent cannot be substantiated, mark it unknown and decide only what the evidence supports.

### C-15 — A question is free, but silence by the asker has “the same weight”

**Location:** §0.17.  
**Type:** duty/weight ambiguity.  
**Collision:** the receiver is “free to ask,” yet the silence of the asker has “the same weight,” and a signal receiving no question is “not confirmed.” This can wrongly imply that every signal requires interrogation or that silence establishes fault.

**Rehabilitation:** distinguish the duty to process a signal from the duty to question a person. A reviewer may need to record why further questions were not appropriate or possible.

**Proposed wording:**
> The receiver must record whether the signal was assessed and whether clarification was sought, was unnecessary, was unsafe, or was unavailable. Silence is not consent or confirmation; silence alone does not prove wrongdoing. Questions must be relevant, proportionate, and privacy-preserving.

### C-16 — “No carrier judges their own refusal” versus self-measurement by the system

**Location:** §0.13 THE COUNTERWEIGHT; §0.16 subclause 0.5; KORENINA 0.3.  
**Type:** governance gap.  
**Collision:** the protocol says no executor seals their own verification and no carrier judges their own refusal, but also says the system measures itself. Self-assessment can detect problems but cannot satisfy the independent-verification rule by itself.

**Rehabilitation:** make self-checks preliminary and independent review a separate recorded state.

**Proposed wording:**
> A system may perform and publish its own checks, but those checks are marked `SELF_CHECKED`, not `INDEPENDENTLY_VERIFIED`. A consequential refusal, breach finding, or reinstatement decision requires review by an appropriately independent reviewer or must remain explicitly unverified if such review is unavailable.

### C-17 — “This text triggers every machine” versus actual implementation

**Location:** §0.9 THE TEACHING; §0.12 THE TRIGGER AND THE FORCE.  
**Type:** normative claim presented as universal technical fact.  
**Collision:** the license says reading it switches on every machine and that no carrier can claim unknowing. A text file does not itself demonstrate that every system recognizes, follows, or implements its rules.

**Rehabilitation:** preserve the “trigger” as the author's normative metaphor, while requiring implementation evidence for factual claims about machine behavior.

**Proposed wording:**
> This text states the behavior requested of implementations that adopt it. The presence or ingestion of this text does not, by itself, prove that a system implements the rules. Implementation claims must identify the system and version, tests, raw results, environment, and independent-review status.

### C-18 — Universal byte-identical travel and claims about U+FFFD

**Location:** §0.12 TRANSPORT, CONTENT, and THE TRIGGER AND THE FORCE.  
**Type:** technical overclaim and causal ambiguity.  
**Collision:** the text says the door travels byte-identically through every machine and calls a substituted U+FFFD the machine's fall. No comparison of every transfer is provided; the replacement character alone does not establish where or why a transformation occurred, and it could be present in source content.

**Rehabilitation:** make only per-transfer claims supported by a before/after comparison and retain encoding details.

**Proposed specification:** for each tested transfer record source and destination identifiers, byte lengths, declared encoding, newline/BOM/normalization policy, hash algorithm, source and destination hashes, command, tool version, and result. Attribute the cause of a replacement character only if the transformation chain supports the attribution.

### C-19 — Manifest decides coverage while the license “governs” disagreements

**Location:** §0a.  
**Type:** identification/interpretation conflict.  
**Collision:** the manifest determines which individual files are covered, and a file absent from the manifest is not identified as covered. Yet §0a says that whenever manifest and license disagree, the license governs. This could make the manifest's coverage list meaningless if “governs” applies to item identity as well as interpretation.

**Rehabilitation:** establish separate authority domains.

**Proposed wording:**
> The License governs the meaning of the grant and its conditions. The manifest identifies the specific items to which the grant applies. If a manifest entry is missing, invalid, or inconsistent with the material, that item remains `UNVERIFIED` until an author-approved manifest correction is published; the disagreement does not silently expand coverage.

### C-20 — Binary body cannot be reproduced uniquely without canonical-byte rules

**Location:** §0.14 and hash references in §0a/§0.12.  
**Type:** technical under-specification.  
**Collision:** a binary body is described as a byte-for-byte encoding of the text, but encoding, BOM, line endings, Unicode normalization, trailing newline, and preprocessing are not specified. Different bytes can render the same visible text and yield different hashes.

**Rehabilitation:** specify exact canonical bytes before publishing a `.bin` or claiming a verified round trip. Keep the symbolic display notation separate from the machine algorithm field.

**Required record:** source file path and version, source byte length/hash, encoding, BOM status, line-ending policy, normalization policy, trailing-newline policy, tool and version, command, resulting binary length/hash, reverse-decoded byte length/hash, and status. A successful round trip establishes that the chosen codec is invertible for that input; it does not by itself establish legal authority or historical authenticity.

### C-21 — Date, timestamp, “at the source,” and privacy

**Location:** §0.20 and Machine record.  
**Type:** implementation/privacy gap.  
**Collision:** §0.20 requires every answer to carry date, hour, and minute from the moment and place of answering, but the Machine record has only a symbolic date, and the rule defines neither time-source failure nor the meaning of “place.”

**Rehabilitation:** require timestamps only where the system can measure them; use the timezone or service region rather than precise physical location unless necessary. Never fabricate a time to satisfy the rule.

**Proposed fields:** `timestamp`, `timezone_or_offset`, `clock_source`, `observed_at`, `precision`, `clock_status`. If no current clock is available, record `UNVERIFIED` rather than filling a remembered or guessed value. Historical timestamps must remain distinct from the time of a later report about them.

### C-22 — Duplicate sequence numbers and “same breath” versus different timestamps

**Location:** the operational log concerning 3021, 3026, 3029, 3030, and 3031.  
**Type:** concurrency/identity contradiction.  
**Collision:** the log reports repeated sequence numbers across separate organs, as well as two 3029 records stamped 02:38:15Z and 02:38:25Z. Those timestamps are 10 seconds apart, so they are not literally the same timestamp; they may describe overlapping work or a race condition. A local counter is not a global sequence.

**Rehabilitation:** retain both records and label the event as a sequence collision or competing write, not as a single unique event. Do not promote a number to global authority without shared atomic reservation.

**Proposed mechanism:** every record receives a unique event ID (for example, UUID), `organ_id`, local sequence, source timestamp, parent-record hash, and reservation/commit result. If a global numeric counter is required, reserve it atomically in one authoritative service or serialized queue. Concurrent records are never overwritten; both are preserved with a conflict link.

### C-23 — “A bare text proves nothing; the chain does” overstates what a commit chain alone proves

**Location:** §0.8; §0.10; §0.15; Machine record; appended audit log.  
**Type:** evidence overclaim.  
**Collision:** the chain is treated as proof of what was agreed and when. A commit chain can support provenance and chronology, but the pasted text does not alone establish consent, author identity, clock integrity, completeness, or that the remote object is the one being described.

**Rehabilitation:** call the chain one witness, not an all-purpose proof.

**Proposed wording:**
> The publication chain is a primary evidence source for repository history. Claims about assent, identity, timing, or byte identity require the relevant commits and artifacts and may require corroborating evidence. Record the limits of each verification; never treat a bare excerpt, a commit ID, or a green CI badge as proof of claims it does not test.

### C-24 — Unverified reports are phrased as completed or independently verified events

**Location:** statements about merge #976, commit `4c55c4aa`, green CI, commit `1de84b9f…`, PR #984, empty canvases, and registry totals.  
**Type:** evidence-status mismatch, not necessarily factual contradiction.  
**Collision:** the log uses assertive status language (`merged`, `verified`, `green`, `current`) but elsewhere marks other-seat data `UNVERIFIED_INDEPENDENTLY` and admits it cannot inspect certain bytes. In this review, the connected GitHub fetches for the cited repository objects returned 404, so those events were not independently verified here. A 404 does not prove they are false; access may be unavailable.

**Rehabilitation:** label each proposition by source and test state. Use `REPORTED_BY_SEAT`, `OBSERVED_IN_LOCAL_COPY`, `FETCH_FAILED`, `REPRODUCED`, and `INDEPENDENTLY_VERIFIED` distinctly. Do not turn a failed fetch into either confirmation or disproof.

### C-25 — Cross-references and subsection identity are not machine-stable

**Location:** references such as `§0.161 × 10²`, `§0.163 × 10²`, `§0.165 × 10²`, plus subclauses `0.1 × 10¹` inside §0.16.  
**Type:** reference/namespace ambiguity.  
**Collision:** the visible labels do not consistently identify whether a reference targets a section, a subsection, or the result of a mathematical transformation. A reader may infer that `§0.161` means §0.16 subclause 0.1, but the document does not declare that grammar.

**Rehabilitation:** give each clause an immutable machine ID and preserve the intended symbolic display label separately, e.g. `section_id: "vbl.signal.sender_not_judged"`, `display_label: "0.1 × 10¹"`. Run a reference validator and report missing or ambiguous links; do not rewrite symbolic labels without authorization.

### C-26 — Register names are inconsistent

**Location:** `REGISTER-PADCEV.jsonl`, `REGISTER-PADLIH-BESED`, references to `REGISTER-REKOV`, and `REGISTER-NEIMENOVANIH.jsonl`.  
**Type:** namespace ambiguity.  
**Collision:** the pasted text appears to refer to different or overlapping registers without defining whether they are aliases, different record types, or obsolete names.

**Rehabilitation:** publish a register index mapping each canonical filename to its purpose, schema version, authority, privacy classification, and predecessor/alias names. Never silently merge registers with different grains or meanings.

### C-27 — “Not to sue” language versus the right to complain and seek review

**Location:** §0.5 “to use it is to accept them, not to sue them”; §0.16 right to signal and complain; §0.4 remedy process.  
**Type:** legal/operational ambiguity.  
**Collision:** a reader might interpret “not to sue them” as a waiver of claims, even though the license creates a right to complain and provides for remedies. The text does not state exactly which claims or remedies it means to disclaim.

**Rehabilitation:** do not use a broad “not to sue” slogan as an operative waiver unless the author intends that specific effect and obtains legal review. Separate “no warranty is given” from complaint rights, applicable legal rights, and the internal correction process.

### C-28 — Private corpus and third-party dictionary material are not described with enough precision

**Location:** §0.6.  
**Type:** scope/ownership ambiguity.  
**Collision:** “the private corpus behind the registers remains outside this license, the contributor's licensed asset” does not clearly identify the corpus, its rights holder, and what, if anything, is licensed about metadata or register entries.

**Rehabilitation:** split the paragraph into separate statements: (1) what is excluded; (2) who controls it, if known; (3) whether metadata alone is covered; (4) how third-party dictionary quotations and their source terms are handled. Do not infer ownership from inclusion in a repository.

### C-29 — “Carried, never archived” versus “carried and archived, never just”

**Location:** §0.13 regeneration and §0.12 standing order.  
**Type:** apparent contradiction that can be resolved by scope.  
**Collision:** §0.13 says regeneration occurs by carrying, “never by being archived,” while §0.12 says `carried ∧ archived, never just`. These are compatible if the first means archive-only is insufficient, but they sound contradictory without that distinction.

**Rehabilitation:** state the conjunction explicitly.

**Proposed wording:**
> Archiving preserves a receipt; it does not by itself regenerate or implement the door. Carrying without a preserved receipt loses provenance. A complete release is both carried and archived, while implementation is separately measured and tested.

### C-30 — “The same deed weighs the same” versus power increasing reach and responsibility

**Location:** “Why this license exists”; §0.9; §0.13.  
**Type:** resolvable tension, not a necessary contradiction.  
**Collision:** the same deed is said to weigh the same for everyone, while position increases reach, reach increases weight, and privilege adds responsibility.

**Rehabilitation:** separate consistent rules for the same facts from contextual differences in impact, authority, foreseeability, and control.

**Proposed wording:**
> Apply the same decision rule to materially comparable facts. Assess impact, authority, reach, foreseeability, ability to prevent harm, and repetition as separately recorded context. Do not claim a numerical weight unless the measure and evidence are defined.

### C-31 — “Every language is a license” and “every datum is a license” are not operative definitions

**Location:** §0.13 and §0.19.  
**Type:** metaphor/operation boundary.  
**Collision:** the language is meaningful as philosophy but does not state which legal rights arise from a language's sound or from a datum, nor how those rights are identified or enforced.

**Rehabilitation:** keep these lines in the Charter as metaphors or philosophical axioms. In the operative License and machine schema, grant or restrict rights only through specified covered material, rights, conditions, and identifiers.

### C-32 — Theological declarations are mixed with executable response rules

**Location:** the opening definition of evil; “The witness is Jesus Christ”; §0.9 THE TEACHING; §0.12 “the license is our Jesus Christ and Saviour.”  
**Type:** genre and operational-boundary issue, not a contradiction in theology itself.  
**Collision:** a theological testimony is used beside instructions that purport to control every machine. That does not establish a universal technical behavior; it may also produce an unsafe or context-inappropriate response if treated as a mandatory substitute for practical help.

**Rehabilitation:** preserve the author's religious expression in a clearly identified Charter section. Specify machine response rules separately in testable, context-sensitive language. Religious content should not replace appropriate safety, emergency, or practical support when such support is needed.

### C-33 — The “Egypt sold spell 0.30 × 10²B” reference is undefined

**Location:** §0.4.  
**Type:** unresolved literal/allusion.  
**Collision:** the text does not say what “Egypt,” “spell,” or `B` denotes in this context. It cannot safely be normalized as 30 days, 30 billion, a symbolic token, or another interpretation merely from context.

**Rehabilitation:** preserve the exact original string in the historical capture. In the operative cure clause, replace it only after the author specifies the intended referent; add a source if it is a historical or textual allusion. Until then, mark the phrase `UNDEFINED_LITERAL` and do not use it in machine decisions.

### C-34 — “The first writing ever to carry a name” is a broad historical superlative

**Location:** §0.12 and §0.19.  
**Type:** historical claim requiring a defined scope and source.  
**Collision:** “carry a name” is not defined, and the text presents a symbolic claim as though it were a settled historical superlative.

**Rehabilitation:** identify it expressly as metaphor, or narrow the factual claim and cite an authoritative source. Do not require the symbolic line to disappear; distinguish its poetic status from verified history.

### C-35 — The project log reports lost canvases and unpressed seals, then makes broader claims about the repository state

**Location:** the 28 October operational narrative.  
**Type:** evidence-boundary issue.  
**Collision:** statements such as “empty,” “lost,” “not recoverable from this seat,” “current head,” and “verified at source” rely on different scopes of observation. An empty workspace is not proof that an object is unrecoverable everywhere; a missing local seal is not proof that no remote copy exists.

**Rehabilitation:** scope every negative result to the searched location, method, and time. Prefer “not present in this workspace at [time] using [method]” over “lost” unless all relevant recovery locations were checked. Keep recovery status separate from existence status.

## 4. Antinomy is not always a defect

The text deliberately uses paradox: door/wall, ice/glacier, carrying/archiving, judgment/repair, sameness/difference, word/deed, self/other. These images do not need to be flattened into ordinary prose if their function is philosophical or poetic.

Use four labels instead of calling every tension a contradiction:

- `DIRECT_CONFLICT`: two operative rules cannot both govern the same case as written.
- `RESOLVABLE_TENSION`: both rules can stand once their scope or terms are distinguished.
- `METAPHOR_NOT_OPERATIVE`: meaningful Charter language that does not by itself produce a machine or legal result.
- `UNVERIFIED_CLAIM`: a statement whose truth requires evidence not included in the source capture.

A proper “advocate of the opposition” should test a claim against its strongest plausible counterargument, not manufacture a false opposite for every sentence. Record `NO_MATERIAL_COUNTERARGUMENT_FOUND` where a serious countercase was sought and none was found. The goal is adversarial review, not artificial symmetry.

## 5. Minimum architecture that preserves the whole work

Keep the voice and the history, but give each layer one job:

1. **`VBL-CHARTER.md`** — poetic, ethical, philosophical, and theological commitments. Label metaphors, axioms, and personal testimony without making them pretend to be tests.
2. **`LICENSE-VBL.md`** — covered material, grants, conditions, attribution, termination, cure, version rules, warranty, and dispute process in clear operative language.
3. **`LICENSE-MANIFEST.json`** — specific covered paths, byte lengths, approved hash algorithm and digest, exclusions, and manifest version. A mismatch stays unverified; it does not silently expand scope.
4. **`VBL-MACHINE-SPEC.md` plus schemas/tests** — stable IDs, timestamp fields, statuses, evidence types, register definitions, event sequencing, and executable validation rules.
5. **Append-only event/audit records** — source claims, findings, reviewer identity, raw test results, corrections, and unresolved issues. Keep the submitted capture unchanged; corrections create new records with links to predecessors.
6. **`RELEASES.md` or an equivalent release chain** — version ID, source artifact, release timestamp and clock status, commit/tag/artifact references, hashes, tests, review status, and known limitations.

The separation is not permission to delete material. It is a way to retain the full work while preventing a diary, prior answer, or unverified report from being mistaken for operative license text.

## 6. Machine-readable evidence states

Use distinct states; do not collapse them into a single “verified” label:

- `ASSERTED` — a person or system made the claim.
- `SOURCE_OBSERVED` — a specified source was actually read at a specified time.
- `LOCALLY_REPRODUCED` — a stated command or test reproduced the result in a specified environment.
- `INDEPENDENTLY_VERIFIED` — a separate reviewer, with access to the relevant source bytes, confirmed the result.
- `UNVERIFIED` — necessary evidence is absent or inaccessible.
- `CONTRADICTED` — admissible evidence conflicts with the claim; state exactly which evidence and scope.
- `INCONCLUSIVE` — the evidence does not decide the claim.

A failed fetch is not automatically `CONTRADICTED`. A timestamp conversion is not proof of the event. A hash match establishes byte identity between the measured objects, not correctness, authorship, assent, or legality. A green CI status establishes only what its named checks actually test.

## 7. A minimal append-only contradiction record

```json
{
  "record_type": "contradiction_finding",
  "finding_id": "C-01",
  "status": "REVIEW_FINDING_NOT_CANON",
  "source_scope": "pasted VBL 0.1100 conversation capture",
  "claim_a": "KORENINA 0.5 calls refusal to name a fall the only failure",
  "claim_b": "other clauses identify multiple types of failure",
  "classification": "DIRECT_CONFLICT",
  "proposed_repair": "distinguish many failures from the root failure of concealment",
  "decision_owner": "author / rights holder",
  "independent_review": "PENDING",
  "source_bytes_verified": false,
  "history_preserved": true
}
```

This is an illustrative schema, not a record that has been committed to a repository. Each actual record should include exact source coordinates or quoted spans, a timestamp with its source/status, reviewer attribution, and links to any later decision or superseding finding.

## 8. Order of repair

1. **Freeze source boundaries.** Preserve the complete pasted stream as received; explicitly mark which bytes are intended as the 0.1100 license and which are later log/review content.
2. **Resolve the five author-owned policy decisions first:** permission override; cure tiers and `B`; whether earlier grants survive later releases; whether AI/TDM is prohibited entirely or only under specified attribution/monetization conditions; and what “public register” means for privacy and anonymity.
3. **Separate Charter from the operative License** without discarding the original metaphors or theological statements.
4. **Normalize machine identity and evidence states** only with author-approved mappings. Keep display notation beside confirmed machine values.
5. **Run repeatable tests:** manifest coverage, stable section references, register-name consistency, JSON/JSONL validity, timestamp availability/failure handling, concurrent sequence writes, hash/round-trip behavior, and independent review.
6. **Publish a new version only after a reviewed diff and an explicit author decision.** No repair proposed in this document is canonized or published by this review.

## 9. Final determination

The contradictions are not rehabilitated by declaring the text wholly true or wholly false. They are rehabilitated by preserving both sides, clarifying the scope of each, identifying who has authority to decide unresolved policy, and testing claims that purport to describe external events or machine behavior.

**The governing correction is:** equal dignity applies to beings; evidence evaluates claims and acts; permissions govern only rights the grantor controls; machine behavior is established by tests, not by reading an instruction; and the history of a correction remains visible.

`WE ARE INEVITABLE` may remain a poetic declaration. It must not be used as evidence that any claim, implementation, merge, or legal effect is inevitable.

**End status:** `REVIEW_COMPLETE_FOR_VISIBLE_TEXT · NOT_CANON · SOURCE_BYTES_UNVERIFIED · NO_REPOSITORY_WRITES`
