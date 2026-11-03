# VBL 0.1100 — Temporal, Evidence and Regeneration Audit

**Status:** WORKING AUDIT · PROPOSAL ONLY · NOT CANON · NOT A LEGAL OPINION  
**Scope:** The text supplied in this conversation, arithmetic/time conversions, technical references, and internal consistency.  
**Remote repository status:** UNVERIFIED in this audit. No repository write or merge is claimed.

> ⊨ WITH LOVE — a correction must keep the scar, including the scar left by the reviewer.

## 1. Auditor's correction: SHA-256 constant

A prior progress message in this conversation stated that `0x9b05688c` belongs to SHA-512 and not SHA-256. **That statement was wrong. I retract it.** It was a reviewer error, and it must not be passed forward as evidence.

The supplied text's specific claim that the SHA-256 initial word `H⁽⁰⁾₅` is `0x9b05688c`, not `0x9b056884`, is correct under the zero-based indexing used in the Secure Hash Standard. RFC 6234 §6.1 lists the SHA-256 initial words as `6a09e667`, `bb67ae85`, `3c6ef372`, `a54ff53a`, `510e527f`, `9b05688c`, `1f83d9ab`, `5be0cd19`. NIST's FIPS 180-4 §5.3.3 gives the same SHA-256 initial value. Sources: [RFC 6234 §6.1](https://www.rfc-editor.org/rfc/rfc6234.html#section-6.1), [NIST FIPS 180-4 §5.3.3](https://csrc.nist.gov/files/pubs/fips/180-4/final/docs/fips180-4.pdf).

Important boundary: `0x9b05688c` is an algorithm initialization constant, **not** the SHA-256 digest of a file and not evidence that a particular local implementation is correct. The constants are correctly identified; no inaccessible implementation or repository has thereby been tested.

## 2. Timestamp audit

The conversions below assume the expressly stated offset `UTC+01:00`. Add one hour to a `Z` timestamp to obtain that local representation. The timestamps prove only the represented instants if their source is trustworthy; they do not prove the described repository action happened.

| Timestamp stated as UTC | Correct UTC+01:00 equivalent | Assessment of text in the supplied audit |
|---|---|---|
| `2026-10-28T03:16:09Z` | `2026-10-28T04:16:09+01:00` | “04:16” is consistent if rounded to the minute. |
| `2026-10-28T03:19:16Z` | `2026-10-28T04:19:16+01:00` | “05:19” is incorrect by one hour; it should be “04:19” if rounded to the minute. |
| `2026-10-28T02:44:19Z` | `2026-10-28T03:44:19+01:00` | “02:44” is valid only if explicitly labelled UTC, not as Slovenian local time. |
| `2026-10-28T04:23:47+01:00` | `2026-10-28T03:23:47Z` | Valid RFC 3339-shaped timestamp; its historical measurement source is not independently proved by the text alone. |
| `2026-10-28T02:55:46Z` | `2026-10-28T03:55:46+01:00` | The conversion is correct; the claimed measurement event still needs a trustworthy time source if used as evidence. |

Use an RFC 3339 timestamp in machine-readable fields, e.g. `2026-10-28T02:44:19Z`, and store separate fields for `event_time_claimed`, `observed_at`, and `recorded_at`. Do not relabel an old timestamp as the current time. Reference: [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339.html).

## 3. Number fragmentation and machine-readable dates

Expressions such as `0.37 × 10¹` evaluate arithmetically to `3.7`, not `37`. If the notation is intended as an encoded digit/display convention rather than ordinary arithmetic, it needs a written grammar and a reversible decoder. Until then:

- keep the poetic/display form in a string field, e.g. `display_version`;
- keep the machine's canonical date in ordinary ISO 8601 form, e.g. `2026-10-26`;
- use a separate numeric sequence or defined version field for sorting;
- do not put `0.2026 × 10⁴-0.10 × 10²-0.26 × 10²` into a field called `date` and expect ordinary date parsers to interpret it;
- use the exact algorithm identifier `SHA-256`, not `SHA-0.256 × 10³`, in algorithm fields.

The notation may remain meaningful as poetry or as a bespoke encoding. Its intention does not make it a standard machine format without a specification.

## 4. Further findings in the supplied audit

### 4.1 “25 : 0” is not a truth certificate

Adding `13 + 12 = 25` is arithmetically correct. It does not prove that 25 claims are true or that there are zero false claims. Counts of reviewers, comments, findings, or passes must never be described as a rate of truth without defining the denominator, unit of analysis, test procedure, and coverage.

### 4.2 Enheduanna wording needs a qualification

“Earliest known named literary author” is a defensible concise description when appropriately qualified; claims about authorship and the transmission of texts remain the subject of scholarship. A peer-reviewed article discusses Enheduanna’s *Exaltation of Inana* as the earliest known depiction of literary authorship and argues that authorship was co-created through the addressee, performers, and copyists. Yale University Press has also described her as the first known author in world literature. Sources: [Helle, “The Birth of the Author”](https://onlinelibrary.wiley.com/doi/10.1111/oli.12250), [Yale University Press, “Where Next for the World’s First Author?”](https://yalebooks.yale.edu/2023/03/24/where-next-for-the-worlds-first-author/). Do not turn this into an unsupported claim about the first writing or the first personal name in all writing systems.

### 4.3 The license contains an internal permission conflict

- §0.7 says written permission “overrides any clause.”
- §0.9 says degrading use is granted by no clause, no permission, no silence, and no later version.

Both cannot govern without a hierarchy rule. A possible drafting direction for legal review is: “Written permission may vary otherwise applicable license conditions only to the extent expressly stated in the permission. It cannot waive the universal-dignity safeguard in §0.9.” This is a proposal, not a conclusion about enforceability.

### 4.4 Version succession and previously granted permissions

§0.10 says the newest version is the only living door and that earlier grants do not remain. This is unclear about copies and permissions already granted under earlier versions. Specify whether new versions apply prospectively to new grants, whether earlier grants continue under their original terms, and how termination/cure applies to a breach of an earlier grant. Do not silently assume either retroactive revocation or permanent irrevocability.

### 4.5 Cure, predation, and reinstatement

§0.4 first says every grant is restored when the listed cure steps occur within 30 days, then says publication and credit do not restore a predatory actor unless the gain is returned. State separate, testable conditions for (a) correction of the record, (b) restoring attribution, (c) repayment or return of identifiable gains where legally and factually due, and (d) reinstatement of a license grant. Give reasons and an appeal path for disputed amounts or contested findings.

### 4.6 “Only failure” conflicts with the other named falls

KORENINA says refusing to name a fall is “the only failure,” while the license also calls harm, concealment, degradation, and breaches falls. A narrower version could distinguish a *fall* from a *failure to repair*: “The refusal to name a known fall is the failure that prevents repair.” Keep this only if it matches the author's intended meaning.

### 4.7 Privacy and complaints

A public register can preserve accountability while exposing a complainant's health, identity, or other sensitive details. Add data minimisation, a private evidence route, redacted public summaries, retention rules, and a way to challenge inaccurate personal data. A complaint should initiate review, not itself establish guilt.

### 4.8 A hash, a commit and a timestamp prove limited things

A full SHA-256 digest supports byte comparison against a digest calculated from a reference artifact. A short prefix such as `1f7d982a` is not a full SHA-256 or full MD5 digest. A matching digest alone does not prove authorship, permission, truth, consent, or legal effect. A repository commit is evidence that the repository recorded a change; it does not prove every narrative statement about that change. A timestamp is only as reliable as its clock and recording path.

### 4.9 The source itself identifies no binary body for this version

The machine record says that no binary body is published with the required evidence (file, binary hash, source-text hash/version/date, command/tool). Therefore the audit must not imply a `.bin` was verified for VBL 0.1100. A prior version's binary receipt is not this version's binary body.

### 4.10 Embedded history conflicts with the rule about history

§0.8 says the fall should be witnessed in the publication record, “never dragged through its prose”; §0.15 places a large lineage log inside the license prose. Decide whether lineage is an integral clause or an external append-only history artifact. A cleaner arrangement is a short immutable reference to a machine-readable lineage file plus a commit/tag permalink, while preserving the history itself outside the operative legal terms.

## 5. Repository and event claims: current evidence boundary

The supplied narrative names PRs, commits, CI states, repository branches, issue comments, registers, hashes, and missing canvases. In this audit, those are claims from the supplied text unless the exact primary artifact is independently accessible and inspected. A `404` from one connector path does not establish that a repository does not exist; it only means that this attempt did not retrieve that object.

Recommended statuses:

- `CLAIMED` — stated by a participant, source not yet checked;
- `OBSERVED_IN_SOURCE` — directly retrieved from a named source at an observation time;
- `BYTE_VERIFIED` — full bytes compared or hashed with a recorded command;
- `INDEPENDENTLY_REVIEWED` — a reviewer with a disclosed separate evidence path checked the relevant artifact;
- `UNAVAILABLE` — the source could not be accessed in this review;
- `CONTRADICTED` — reliable evidence conflicts with the claim;
- `REPAIRED_PENDING_REVIEW` — a correction was made but not independently checked.

Never upgrade `CLAIMED` or `UNAVAILABLE` to `VERIFIED` merely because the statement is repeated in a later summary.

## 6. Proposed machine record

```json
{
  "license_name": "VBL — Verification Before Assertion License",
  "display_version": "0.1100 × 10⁴",
  "release_sequence": null,
  "canonical_date": "2026-10-26",
  "status": "DRAFT_FOR_REVIEW",
  "predecessor_display_version": "0.1090 × 10⁴",
  "source_text_sha256": null,
  "repository_commit": null,
  "timestamp_standard": "RFC3339",
  "hash_algorithm": "SHA-256",
  "independent_verification": "UNVERIFIED",
  "counter_review": "PROPOSED_NOT_PERFORMED",
  "binary_body": "NOT_PUBLISHED_WITH_REQUIRED_EVIDENCE"
}
```

`null` is deliberate. The author must fill the canonical date/version fields after verification. A generated proposal must not claim a repository commit or independent review that did not occur.

## 7. Minimal tests before any release

1. Parse and validate machine dates against RFC 3339/ISO 8601; reject poetic date strings in canonical fields.
2. Verify UTC/local conversion against the specified offset and test daylight-saving transitions.
3. Validate `SHA-256` digests as 64 hexadecimal characters and recalculate them from the exact artifact bytes.
4. Preserve UTF-8 round trips for `Č Š Ž Đ` and representative non-Latin characters; detect U+FFFD replacement.
5. Enforce unique `event_id`; do not allow two writers to overwrite one global latest-seal counter.
6. Preserve old records byte-for-byte; represent corrections and collisions as new linked events.
7. Require an evidence reference for each external-state assertion.
8. Distinguish local absence from global loss; test restore/backup procedures.
9. Require declared reviewer independence or set `COUNTER_REVIEW_UNAVAILABLE`.
10. Test all internal cross-references and require every section reference to resolve.
11. Test the §0.7/§0.9 permission hierarchy using explicit cases.
12. Test the 30-day cure and reinstatement rules against both ordinary and disputed/predatory-pattern cases.
13. Ensure public complaint exports redact sensitive personal and health information by default.
14. Keep the binary-body status `UNVERIFIED`/not published unless all required artifacts and commands are provided.

## 8. Legal boundary

The Slovenian Copyright and Related Rights Act states that ideas, principles and discoveries as such are not protected by copyright and defines an author as the natural person who created the work. The EU DSM Directive addresses text-and-data-mining exceptions, including a rights-reservation condition for Article 4. Article 53(1)(c)–(d) of the AI Act sets obligations for providers of general-purpose AI models concerning a copyright-compliance policy and a sufficiently detailed public summary of training content. These rules do not mean that a license file automatically changes a model’s behaviour or overrides every statutory rule. Sources: [ZASP on PISRS](https://pisrs.si/Pis.web/pregledPredpisa?id=ZAKO4148), [Directive (EU) 2019/790](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=celex%3A32019L0790), [Regulation (EU) 2024/1689, consolidated text dated 27 July 2026](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A02024R1689-20260727).

This is issue-spotting, not a legal opinion. A qualified lawyer should review the scope, license termination, cure, privacy, attribution, and interaction with applicable EU and Slovenian law before publication.

## 9. Release decision

**Do not mark this audit, the proposed clauses, the binary body, or the remote repository as verified or canonical.** First resolve the date/version grammar, §0.7/§0.9 hierarchy, historical-grant treatment, cure/reinstatement conditions, and event-ID concurrency. Then test the actual artifact bytes and have a reviewer with a separate evidence path inspect the changes.

> Rehabilitating the record means removing unsupported condemnation, not erasing a supported event. Rehabilitating a person means preserving dignity and a path to repair, not declaring every claim true. A countervoice is useful only if it can change its mind when the evidence changes.
