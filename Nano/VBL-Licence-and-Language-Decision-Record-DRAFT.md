# VBL — Licence and Language Decision Record

**Status:** decision draft · no licence selected · not legal advice  
**Prepared:** 2026-10-25

## The necessary distinction

VBL should not use one vague “rights” statement to cover different legal objects. At minimum, distinguish:

1. **Specific expressive text** — the exact wording, structure, examples, diagrams, and original selection/arrangement. Protectability is assessed case by case.
2. **General principles or methods** — Slovenian official guidance says ideas, principles, and discoveries are not protected by copyright as such. This does not decide whether some other legal regime, a valid contract, or a separate protectable expression applies.
3. **Software and tooling** — validators, schemas, scripts, and integrations require their own rights and licence review; do not assume that a document licence is suitable for code.
4. **Marks and identity** — the VBL name, logos, seals, and source-of-origin claims should be treated separately from the copyright licence.
5. **Evidence/data** — examples and incident records may contain personal or confidential information. A public licence is not consent to disclose data.

## Decision to make before the next release

**Question 1 — What is the primary purpose?**
- `OPEN_TEXT`: maximise reuse and adaptation of the documentation.
- `OPEN_TEXT_WITH_ATTRIBUTION`: require attribution for uses of the licensed expression.
- `SHARE_ALIKE`: require certain adaptations of the text to use the same licence, subject to licence scope and exceptions.
- `CUSTOM_CONDUCT_CONDITIONS`: attempt to attach conduct or use conditions; requires counsel review and a careful analysis of enforceability, scope, remedies, and conflicts with open-reuse goals.
- `UNDECIDED`: remain draft and make no licensing claim beyond a rights/status notice.

Do not treat this as a final recommendation to choose a particular licence. The rights-holder and intended use must be known first. Creative Commons offers standard public licences, but they cover copyright and related rights in defined material and should not be presumed to control every use of an idea, brand, dataset, software component, or conduct.

**Question 2 — Who controls each text?**
For every component, record: author/translator/contributor; rights holder or permission basis; third-party material; AI-assisted contribution and human review (where applicable); source file and hash; permitted scope; exclusions; and person authorised to approve a release. Slovenian official guidance describes the author as a natural person and says copyright arises upon creation without registration formalities. A file hash does not establish legal authorship or ownership.

**Question 3 — What is the controlling language?**
Choose one before publishing. Suggested default for practical clarity: one controlling legal text, with translations explicitly marked as reference translations unless counsel and the rights-holder deliberately choose co-equal legally binding texts. The controlling language is a governance decision, not a claim that a translation is unimportant.

Suggested statement for a draft (do not publish as final until approved):

> **Language status — draft:** The Slovenian and English texts are working translations for review. No language is declared authoritative or legally controlling until the rights-holder approves a release record that identifies the controlling text and resolves material translation differences. Translation status, source hash, translator/reviewer, and date must be shown for each language edition.

If one language is selected as controlling, the legal text should state that explicitly and explain how translation differences are handled. If translations are co-equal, the licence should prescribe a conflict-resolution rule; otherwise contradictions can create operational ambiguity.

## Translation workflow

1. Freeze the source version and compute its SHA-256 hash.
2. Build a clause map (`source clause ID` → `target clause ID`) and glossary for terms such as assertion, verification, evidence, independent reviewer, correction, remedy, and release.
3. Translate without silently strengthening, weakening, or adding obligations.
4. Conduct independent bilingual review by a competent human reviewer not responsible for the initial translation.
5. Record every non-equivalent or disputed clause in a translation-variance register with options and an approver decision.
6. Run structural checks: clause counts, numbering, references, defined terms, dates, tables, links, disclaimers, and version labels.
7. Freeze each language artefact separately, hash it, and bind it to the same release record.
8. When the controlling text changes, mark translations `STALE_PENDING_REVIEW` until re-aligned and approved.

## Special caution about Creative Commons translations

Creative Commons' official translation process applies to Creative Commons licence texts. The existence of officially translated CC legal codes is not a general validation procedure for translating a custom VBL licence. If VBL chooses a CC licence for suitable material, use the current official licence text and follow Creative Commons' own guidance. Do not edit a standard CC legal code and continue to represent it as the unmodified standard licence.

## Release-record fields

`release_id`; licence/version; component scope; rights-holder/release authority; controlling language; language editions and hashes; source/provenance references; translation reviewer; licence selection and rationale; jurisdiction(s) reviewed; legal reviewer and scope; approval date; publication URLs/commit/tag; supersedes; changes; known limitations.

## Official sources

- GOV.SI, *Avtorska in sorodne pravice*: https://www.gov.si/teme/avtorska-in-sorodne-pravice/
- ZASP in the Slovenian Legal Information System: https://pisrs.si/Pis.web/pregledPredpisa?id=ZAKO403
- Creative Commons FAQ, official translations: https://creativecommons.org/faq/
- Creative Commons legal-code explanation: https://creativecommons.org/legal-code-defined/

This record is an issue list and decision aid; it is not a formal legal opinion and does not select a final licence on behalf of the rights-holder.
