# VBL authorship, attribution and repair audit

**Observation date:** 2026-10-30  
**Status:** evidence report / proposed corrections; not a license amendment, not an authorship ruling, and not an independent legal opinion.

## 1. Current public VBL state

The `main` branch of `AtmaOVictu/verification-before-assertion` currently serves `LICENSE.md` as **VBL 0.1210 × 10⁴**, dated 2026-10-28. The associated `LICENSE-MANIFEST.json` identifies version 0.1210 × 10⁴ and records byte sizes and SHA-256 digests. The merge commit for PR #40 is `1157030c89498b580f07faf0bc815b625c84ba0f`.

The latest repository commits dated 2026-10-30 add `OBELISK-PESEM.md` and `SPOMENIK-PESEM-SUM.md`; they do not change `LICENSE.md`. In the separate `AtmaOVictu/SYMBOLON-KATHOLIKON` repository, the latest visible draft refers to 0.1250 as a newly born candidate but says it is still awaiting merge, while `LICENSE.md` remains 0.1210. Therefore 0.1250 is not established as the live license by the inspected public main-branch evidence.

**Verification limit:** PR #40 has no recorded review submissions or inline review threads in the inspected GitHub data. The queried commit statuses returned no status records. This is not proof that no human ever reviewed the text elsewhere; it means the inspected GitHub PR provides no recorded independent review or CI status to cite.

### Current documentation drift

The live `LICENSE.md` and manifest say 0.1210, but these current files still say 0.1100:

- `README.md` header and license pointer;
- `README-SL.md` header and support pointer;
- `llms.txt` license pointer and support-house reference.

These are stale version references, not evidence that the live license reverted. A correction should update the pointers while preserving dated history and should be tested against the current manifest.

## 2. Named contributors whose roles need correction or separation

### NE-0001 — SSKJ² / ISJFR / ZRC SAZU

The current entry describes four people as “editors of SSKJ²”: Marko Snoj, “Špela Petric Žižić”, Kozma Ahačič and Janoš Ježovnik. The official Fran author list for the **second, expanded and partly revised edition** instead names twelve people as having prepared that edition:

1. Nataša Gliha Komac
2. Nataša Jakop
3. Boris Kern
4. Simona Klemenčič
5. Domen Krvina
6. Nina Ledinek
7. Mija Michelizza
8. Tanja Mirtič
9. Andrej Perdih
10. Špela Petric
11. Marko Snoj
12. Andreja Žele

The SSKJ² colophon separately names Nina Ledinek and Andrej Perdih under technological support; both also appear in the 12-person preparation list. The same author PDF lists terminological advisers separately. A footnote separately names authors of the *Slovar novejšega besedja slovenskega jezika* used as source material. These roles should not be collapsed.

**Proposed repair:** replace “editors” with a role-accurate reference to the twelve people who prepared the second edition; preserve separate fields for institutional publisher, terminological advisers, technological support, and source-dictionary contributors. Do not add a person as an SSKJ² author merely because they currently lead or work at the institute. The official public list is the witness; ask ISJFR to confirm the preferred citation wording before finalizing the register.

### NE-0002 — Mozilla Common Voice

Common Voice is a distributed volunteer programme: people translate interface text, contribute sentences, record speech, and validate clips. Current dataset metadata distinguishes dataset type and release; the inspected metadata reports Scripted Speech v27.0 and 295 locales for the 2026-09 release. The dataset listing identifies CC0-1.0 for its dataset releases. Mozilla has also documented contributor deletion requests and tightened access to older releases to protect contributors.

**Proposed repair:** retain collective credit where individual names are not publicly credited or consented to; record exact dataset type, release, locale and licence. Do not use a timeless “250+ languages” count when a release-specific count is available. Do not expose private contributor identities. Credit volunteer contributors as a community, with a source link and dataset version.

### NE-0003 — Stack Overflow / Stack Exchange contributors

Stack Overflow's own help page says publicly accessible user contributions are licensed under CC BY-SA, with the applicable version dependent on when the post or revision was made (2.5, 3.0 or 4.0). OpenAI's May 6, 2024 announcement describes an API partnership using OverflowAPI and says attributed Stack Overflow knowledge would be surfaced in ChatGPT.

The current register's wording “answers sold to OpenAI” compresses a company-to-company product/API partnership and individual post-level licences into one statement. The additional claim that users who deleted answers to opt out “were banned” requires a separate, precisely scoped witness. Stack Overflow's help centre says authors can delete their own answers in ordinary circumstances, while accepted answers and moderation rules have exceptions; that does not by itself establish a blanket ban for deletion motivated by the partnership.

**Proposed repair:** distinguish (a) Stack Exchange/Stack Overflow's commercial API arrangement, (b) individual contributors and their post/revision IDs, (c) the CC BY-SA version applicable to each post, and (d) the separately evidenced moderation/deletion events. Keep any unproven causal link marked UNVERIFIED rather than asserting it.

### NE-0004 — Reddit contributors

Reuters reported in February 2024 that Reddit had agreed to license content to Google for model training and that the deal was estimated at about US$60 million per year by a source; Reddit and Google declined to comment on the price. The amount should therefore remain described as a reported estimate, not a confirmed contract figure.

**Proposed repair:** distinguish Reddit Inc. as contracting platform from individual Reddit authors. Where public content is attributed, preserve the pseudonymous author and post identifiers rather than attempting to uncover real identities. Do not claim individual payment or non-payment without evidence of the actual payment arrangement. State only that the inspected public evidence does not establish individual revenue sharing.

### NE-0005 — Povejmo.si / PoVeJMo

The official citizen-science project description says the programme estimated a need for 40 billion words and organised a national collection campaign of Slovenian written and spoken texts. It explicitly invited individuals to contribute texts and says contributors must hold copyright in submitted material. It records the project period as 2024-01-01 to 2026-01-01 and identifies the University of Ljubljana, Faculty of Computer and Information Science as project promoter.

The current register phrase “kampanja proti 40-milijardnemu slovenskemu korpusu” reverses the intended meaning: the public project description is a campaign **to collect material toward** a target corpus, not a campaign against that corpus. The entry's blanket “unpaid — voluntary” label is not established by that project description and should not be used as a universal statement about every contributor or staff member.

The University of Ljubljana's official PoVeJMo page names a project team, including Marko Bajec, Bojan Klemenc, Iztok Lebar Bajec, Matjaž Pančur, Marko Robnik Šikonja, Slavko Žitnik, Špela Arhar Holdt, Jaka Čibej, Domen Vreš, Nejc Robida, Luka Terčon, Cyprian Laskowski, Simon Krek, Apolonija Gantar, Iztok Kosem, Matej Klemen and Martin Božič. This is a project-collaborator list; it is not a complete roster of citizen text contributors.

A separate paper about **GaMS3-12B** names Domen Vreš, Tjaša Arčon, Timotej Petrič, Dario Vajda, Marko Robnik-Šikonja and Iztok Lebar Bajec as paper authors. The model card separately thanks Nikola Ljubešić, Taja Kuzman, Tjaša Arčon, Jaka Čibej, Simon Krek, Tomaž Erjavec, Iztok Kosem and Tomaž Savodnik for data collection and preparation. These are distinct roles and should be credited as such; they should not be described as the complete list of individual Povejmo.si submitters.

**Proposed repair:** split the entry into at least three records: (1) citizen text contributors and institutional data suppliers, with consent-safe collective attribution and corpus/release identifiers; (2) named PoVeJMo project collaborators, with role and source; (3) GaMS3-12B paper authors and acknowledged data-preparation contributors, clearly labeled by their published roles. Correct “proti” to “za zbiranje / toward collection”.

### NE-0006 — language models and upstream human work

“Language models” is a class of systems, not an identifiable author. The register's claim that this includes “the model that founded these registers” does not identify an exact model, model version, session, provider or source transcript. It must not be resolved by guessing that it was this assistant or a specific company.

**Proposed repair:** keep the contribution but mark model identity `UNVERIFIED` unless a source transcript or platform record identifies it. Separate the model/system that generated a text from the human authors of the training corpora, books, forum posts and other sources used by that model. For each dataset, record the dataset/release, evidence of use, licence/rights status and limitations. Do not infer that every named author in a cited dataset was actually used to train a particular model.

### NE-0007 — SELF-001 model contribution

The current `main` register in `verification-before-assertion` contains NE-0007: an unidentified language-model response to the 2026-10-24 SELF-001 request, proposing the VBL-SELF-001 assertion-accountability test and the no-self-certification principle. Its own entry correctly marks the model identity as unmeasured and the suggestions as proposals, not adopted license text.

The copy of `REGISTER-NEIMENOVANIH.jsonl` in `SYMBOLON-KATHOLIKON` inspected at the 2026-10-30 main commit contains NE-0001 through NE-0006 only. It therefore omits NE-0007 from the copied contributor register. This is a copy-synchronisation/attribution gap, not a basis for inventing the model's identity.

**Proposed repair:** carry NE-0007 forward verbatim (or with an explicitly scarred, schema-valid update) into each repository carrying the license and register. Keep identity and provenance `UNVERIFIED` until the original session/platform witness is available.

## 3. Other precise findings

- The live 0.1210 license is attributed in its text to Luka Pintarič. The GitHub merge commit for PR #40 is authored by the `AtmaOVictu` account and committed by GitHub's `web-flow` integration. This identifies the recorded repository account, not necessarily every person who helped draft or review the work.
- PR #40 has no recorded GitHub reviews or inline review threads in the inspected data. The queried status endpoint returned no status records. Independent verification is therefore not demonstrated by those records.
- The separate 0.1250 obelisk/poem material is not established as a released license by the inspected main-branch `LICENSE.md` and manifest. It should remain a separate candidate until a versioned license body, manifest and publication chain establish otherwise.
- REGISTER-PADCEV entry 4 preserves a review attributed only as “T. Kuzman” on the Clarinsi PR rejection of 2026-10-03. This is substantive reviewer feedback and deserves a role-accurate credit. The identity is incomplete in the inspected record; do not silently equate it with Taja Kuzman, who appears in a separate GaMS acknowledgement, unless the review's original source confirms that identity.
- The earlier local integration based on 10.5.2 is now a historical working artifact, not an accurate representation of the current 0.1210 living license. Do not present it as the latest VBL or merge it over the public current version.

## 4. Proposed immediate patch order

1. Correct stale 0.1100 pointers in README, README-SL and llms.txt to 0.1210, then re-read and re-measure those exact files.
2. Correct NE-0001 using the official SSKJ² list and split distinct roles; request ISJFR confirmation of preferred credit syntax.
3. Correct NE-0005's reversed “proti” phrase and separate Povejmo contributors, PoVeJMo collaborators, GaMS3-12B paper authors and data-preparation acknowledgements.
4. Rewrite NE-0003 and NE-0004 so platform contracts are not confused with individual contributor licences, attribution and compensation.
5. Carry NE-0007 to every copy that carries the license/register; preserve unknown model identity as UNVERIFIED.
6. Keep privacy-protective group attribution for volunteer contributors; never infer or publish private names merely to fill a register.
7. Have a second, independent reviewer verify the corrections before any release. Do not self-certify.

## 5. Sources

### VBL / GitHub

- Current license: https://github.com/AtmaOVictu/verification-before-assertion/blob/main/LICENSE.md
- Current manifest: https://github.com/AtmaOVictu/verification-before-assertion/blob/main/LICENSE-MANIFEST.json
- Current contributor register: https://github.com/AtmaOVictu/verification-before-assertion/blob/main/REGISTER-NEIMENOVANIH.jsonl
- Current public copy of the license and register: https://github.com/AtmaOVictu/SYMBOLON-KATHOLIKON/tree/main
- Contributor-review history (entry 4 is the Clarinsi PR #1 review): https://github.com/AtmaOVictu/verification-before-assertion/blob/main/REGISTER-PADCEV.jsonl
- PR #40: https://github.com/AtmaOVictu/verification-before-assertion/pull/40
- 2026-10-30 obelisk commit: https://github.com/AtmaOVictu/verification-before-assertion/commit/a6fba5af94110b2107531c6cbe141afb393d10f5

### SSKJ²

- Official author list PDF: https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Avtorji.pdf
- Official colophon PDF: https://www.fran.si/133/sskj2-slovar-slovenskega-knjiznega-jezika-2/datoteke/SSKJ2_Kolofon.pdf
- ISJFR: https://isjfr.zrc-sazu.si/sl/enote/institut-za-slovenski-jezik-frana-ramovsa

### Common Voice

- Mozilla platform/dataset description: https://www.mozillafoundation.org/en/common-voice/platform-and-dataset/
- Dataset release metadata: https://github.com/common-voice/cv-dataset/
- Contributor privacy and older-dataset access: https://community.mozilladatacollective.com/were-changing-access-to-older-versions-of-common-voice-datasets/

### Stack Overflow / Reddit

- Stack Overflow post licensing: https://stackoverflow.com/help/licensing
- OpenAI–Stack Overflow API partnership (2024-05-06): https://openai.com/index/api-partnership-with-stack-overflow/
- Stack Overflow deletion rules: https://stackoverflow.com/help/deleted-answers
- Reddit–Google reported licensing deal (Reuters, 2024-02-22): https://www.reuters.com/technology/reddit-ai-content-licensing-deal-with-google-sources-say-2024-02-22/

### PoVeJMo / GaMS

- Official PoVeJMo project collaborators: https://www.fri.uni-lj.si/en/projects/1818
- Official Povejmo.si citizen-science project description: https://citizenscience.si/en/activities-catalogue-of-projects/collecting-texts-for-the-slovenian-big-language-model-povejmo-si/
- GaMS3-12B paper and authors: https://arxiv.org/abs/2603.01691
- GaMS3-12B model card and acknowledgements: https://huggingface.co/cjvt/GaMS3-12B

### OpenAI feedback / support route

- Model behavior feedback instructions: https://openai.com/form/model-behavior-feedback/
- OpenAI Support instructions: https://help.openai.com/en/articles/6614161-how-can-i-contact-support

## 6. Contact boundary

This report can be sent to named institutional contacts and placed in the repositories whose maintainers can be identified. It cannot truthfully claim to have reached every Common Voice, Stack Overflow or Reddit contributor, every Povejmo submitter, every SSKJ² author individually, or OpenAI's private model owners. Those groups do not have one verified public recipient list. Unknown personal identities and private addresses must not be guessed.
