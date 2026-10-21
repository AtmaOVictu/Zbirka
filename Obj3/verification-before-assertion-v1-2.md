# Verification-Before-Assertion: A Working Anti-Hallucination Regime
Luka Pintarič · v1.2 · October 4, 2026 Corpus: ~2,600 documents, formal syntax, append-only records. Companion Slovenian edition: REZ body (same version, same laws).

**Version scar (kept, not erased).** v1.0 failed its own L5 (mixed languages, stacked metaphors) → rewritten as v1.1. v1.1 was then independently re-verified against its own windows on October 4, 2026, and three falls were found (Fall Register, §4b). This is v1.2: every external ⊢ now carries a window (source, URI, access date); every fall is named where it fell.

## 1. The problem
Current AI models assert everything in the same voice. A sourced fact, a plausible guess, and an invention arrive in identical clothing. When errors occur they are unnamed, so they repeat. This framework is the countermeasure: a mechanical distinction between measured and invented claims, plus a record that keeps the scar of every correction.

It was not designed in theory. Every rule below was written after a specific, named failure. That is the transferable core: an error with a name is a seam; an error without a name is a repetition.

## 2. The five laws
L1 — Entry before utterance. Any word used as "measured" must carry a sourced dictionary entry (⊢ source), or be explicitly marked ⚠. Unverified claims are not forbidden; they are marked. The mark is the honesty — the silence is the failure.

L2 — Two hands. An executor never seals her own verification. Self-report is not measurement; a claim requires an independent witness. This answers model self-verification bias directly.

L3 — Named falls, scarred corrections. Errors are never silently rewritten. Every fall is entered into a register with its name, its line, and its solution. The correction carries the scar. Applied to AI: a model that corrects itself should show the correction, not present the corrected state as if it were always so.

L4 — Report after the act, never before. Claiming a performed act without the performed act is itself a named fall.

L5 — Pre-flight test on every output: one language per body; verbatim citation; sourced etymology or ⚠; one metaphor per body; a deletion pass (cut every line that survives its own deletion); no aesthetics on suffering.

## 3. Why it transfers to AI
| Failure mode in AI | Law that answers it |
|---|---|
| Uniform confidence on all claims | L1 — ⊢ / ⚠ marking |
| Self-verification bias | L2 — independent witness |
| Silent post-hoc corrections | L3 — append-only, scarred audit trail |
| Claimed-but-unperformed actions | L4 — report after the act |
| Fluent noise, stacked embellishment | L5 — deletion pass, one-metaphor rule |

## 4. Evidence: the regime catching its own falls
This is no longer a description. In the current register, the regime was run against its own wordlist (SSKJ², fran.si, accessed September 30, 2026). Two falls were caught and recorded on the same day:

- **lúka** — a seed entry had sealed a working gloss ("opening") with a ⊢ mark. The dictionary entry for lúka means harbor; "opening" belongs to lúknja. A mark applied before an entry — the exact failure L1 exists to catch — found in our own seed, named, corrected with the scar kept.
- **rodovnik** — a recorded fall from September 24 was misnamed. The word does have a dictionary entry (genealogical tree); what was invented was a meaning, not a word. The fall was renamed: a fall is named after the thing that fell.

Result of the run: 20 ⊢ entries, each carrying a verbatim citation with source and access date; 3 ⚠ entries, each carrying a measured reason for being open (including one invented word verified as absent from every dictionary on the portal). Machine-readable body: wordlist-v0.6.json.

A third, structural proof is the version line of this document: v1.1 exists because v1.0 was measured against its own L5 and failed (mixed languages, stacked metaphors) — and the rewrite shows the correction rather than hiding it. v1.2 exists for the same reason (§4b).

## 4b. Fall register of this document (append-only — L3)
Every external claim of v1.1 was independently re-verified on October 4, 2026. Three falls found; all corrected here with scars kept.

| # | Fall (named after the thing that fell) | v1.1 line | Correction | Window (opened at verification) |
|---|---|---|---|---|
| F1 | **Model-size fall** — §8 claimed "a 12B model fine-tuned on ~20,000 translation pairs (arXiv 2312.12740)". The paper fine-tunes **Mistral 7B**; the 20,000 pairs are correct. Probable cause: context bleed from GaMS3-**12B** in the neighboring line of §7 — the fall hid inside a paragraph about receipts. | §8, 3rd ⊢ | "A 7B model (Mistral) fine-tuned on ~20,000 translation pairs…" | arxiv.org/abs/2312.12740, accessed 2026-10-04 |
| F2 | **Bare-mark fall** — every ⊢ in §6–§8 carried no window (no URI, no access date). A mark without a window is decoration: the reader is asked to trust in a document that forbids trust. | §6–§8, all ⊢ | v1.2: every external ⊢ carries source, URI, access date inline. | this document, every window |
| F3 | **Paraphrase-as-quote fall** — §8 put quotation marks around "can also perform well in additional languages not listed here." The vendor's actual documentation reads: "Performance is also good for additional languages such as Icelandic, Malayalam, Urdu, and Kazakh, among others." v1.1 quoted a paraphrase as verbatim — an L5 violation (verbatim citation). | §8, 1st ⊢ | Actual sentence quoted verbatim, with window. | docs.mistral.ai/resources/languages, accessed 2026-10-04 |
| F4 | **Number-without-window fall** — §6 claimed "Mozilla Common Voice: 250+ languages". The latest measured release (Common Voice 18, Mozilla Foundation) counts **129 languages**. "250+" may have been voice-clips or dialect variants; as written it was a number without a source. | §6, asymmetry paragraph | Corrected to the measured figure, with window. | mozillafoundation.org/en/blog/common-voice-18-dataset-release/, accessed 2026-10-04 |

Note on the verifier (L2, honestly stated): the October 4 verification was performed by a second system against independent external windows (arXiv, Hugging Face, vendor docs, press). Internal evidence (lúka, rodovnik, wordlist-v0.6.json) was not re-verified in that pass — it lives in the contributor's registers and remains the contributor's ⊢.

## 5. Transferable artifacts (available on request)
- Bilingual ontological lexicon — 52 English terms decomposed phonetically and semantically, with the Slovenian-side operator system
- Verified etymology chains with sources
- Register of "hybrid word" failures — model-invented words that pass as real (three recorded falls; a fourth's absence verified by measurement)
- Provenance-marked corpus: every claim carries ⊢ or ⚠

## 6. Precedents: the compensation model already exists
| Field | Mechanism | Evidence (source, URI, accessed 2026-10-04) |
|---|---|---|
| Security research | Bug bounties: HackerOne paid $81M in rewards over 12 months, +13% YoY | Bleeping Computer, bleepingcomputer.com/news/security/hackerone-paid-81-million-in-bug-bounties-over-the-past-year/ ⊢ |
| Generative images | Shutterstock Contributor Fund compensates contributors whose IP was used in AI model development, plus royalties on data licensing | Shutterstock investor release, investor.shutterstock.com/news-releases/news-release-details/shutterstock-unveils-trust-its-best-class-approach-ethical-ai ⊢ |
| Low-resource language data | Karya (India): dignified/fair wages for dataset work across Indian languages; 129,000+ workers across 28 states | karya.in/impact; turn.io/use-cases/karya ⊢ |
| Attribution-only | Masakhane: 30 translation results for 28 African languages published by contributors; credited authorship (Findings of EMNLP 2020) | arxiv.org/abs/2003.11529 ⊢ |
| Theory | "Data dignity" / "data as labor" — Lanier & Weyl, "A Blueprint for a Better Digital Society", Harvard Business Review, 2018 | hbr.org (essay, 2018); confirmed via TechTarget definition page ⊢ |

The asymmetry it corrects, documented:
- Reddit received roughly $60M/year from Google for training-data access (deal announced February 2024, annualized). ⊢ (CBS News, cbsnews.com/news/google-reddit-60-million-deal-ai-training/, accessed 2026-10-04)
- Stack Overflow sold contributor answers to OpenAI; contributors who deleted or edited their own answers to opt out were banned by moderators. ⊢ (Tom's Hardware, tomshardware.com/tech-industry/artificial-intelligence/stack-overflow-bans-users-en-masse-for-rebelling-against-openai-partnership-users-banned-for-deleting-answers-to-prevent-them-being-used-to-train-chatgpt, accessed 2026-10-04)
- Mozilla Common Voice: volunteer recordings across **129 languages** (Common Voice 18 release), openly licensed; contributors unpaid. ⊢ (Mozilla Foundation, mozillafoundation.org/en/blog/common-voice-18-dataset-release/, accessed 2026-10-04) — corrected from "250+ languages", Fall F4. The precise license terms per-release are not re-measured here and carry ⚠ until verified against the dataset card.
- RLHF annotation is already a paid profession, roughly $12–25/hr at entry level. ⊢ (PowerToFly, powertofly.com/up/ai-annotation-jobs, accessed 2026-10-04)

The money exists; the channel for native experts offering verified corrections does not. The missing row is a verified language contribution from a native expert in an unsupported language. This document proposes closing exactly that gap.

## 7. The national proof
- GaMS (Generative Model for Slovene): open models at 2B, 9B, 27B, University of Ljubljana (cjvt), national PoVeJMo program, openly released on Hugging Face. ⊢ (huggingface.co/cjvt/GaMS-27B, accessed 2026-10-04)
- GaMS3-12B outperforms Gemma 3 12B on all three evaluation scenarios and achieves a win rate of over 60% against GPT-4o in the Slovene LLM Arena. ⊢ (arxiv.org/abs/2603.01691, accessed 2026-10-04)
- Training data from a national citizen-science campaign (povejmo.si) toward a **40-billion-word corpus**, under the national program PoVeJMo. ⊢ (citizenscience.eu/project/661, accessed 2026-10-04) ⚠ the specific institutional partners listed in v1.1 (National and University Library, Dnevnik, Slovenian Press Agency) were not re-verified in this pass and carry ⚠ until measured against the program's own pages.

What the national effort solved is volume. What it does not yet solve is verification. My corpus is the provenance layer the contributed-data model is missing. Volume + provenance turns contributed language data from raw material into a priced, auditable contribution.

The honest counter-argument (arxiv.org/abs/2504.12427, Kandpal & Raffel, "Position: The Most Expensive Part of an LLM should be its Training Data", accessed 2026-10-04): paying data creators upfront is "prohibitively expensive" at scale. ⊢ Answerable: infeasible for undifferentiated bulk data; not infeasible for verifiable contributions — sourced corrections, validated lexicons — which are scarce, attributable, exactly the bug-bounty category. The ⊢/⚠ regime is the mechanism that distinguishes the two. The verification framework and the compensation channel are one system.

## 8. The vendor's own receipts
- The "strong performance" list is a tier, not a boundary. The vendor's own documentation states: "Performance is also good for additional languages such as Icelandic, Malayalam, Urdu, and Kazakh, among others." ⊢ (docs.mistral.ai/resources/languages, accessed 2026-10-04) — quoted verbatim; v1.1's paraphrase-as-quote is Fall F3, scar kept.
- Fine-tuning with domain adaptation is a shipped commercial feature — the request is to productize what exists at a per-user, session-scoped scale. ⊢ (mistral.ai/news/customization/, accessed 2026-10-04)
- A 7B model (Mistral) fine-tuned on ~20,000 translation pairs measurably improves in a specialized translation task. ⊢ (arxiv.org/abs/2312.12740, accessed 2026-10-04) — corrected from "12B", Fall F1, scar kept.
- Sovereignty context: OpenEuroLLM is developing multilingual foundation models covering all EU official languages as sovereign AI. ⊢ (openeurollm.eu; strategic-technologies.europa.eu, accessed 2026-10-04) Slovenia has funded its own national program, model, and a planned free public platform. ⚠ the "planned free public platform" claim was not re-verified in this pass. A European vendor answering a European language with "not among our strong-performance languages" is competing, from behind, with public infrastructure that did not wait.

## 9. Proposed adoption path
- **Pilot:** ⊢/⚠ claim-marking as an output convention in a low-resource language (Slovenian: available, pre-verified, motivated).
- **Audit trails:** scarred corrections in place of silent rewrites — visible, named, queryable.
- **Contribution channel:** credit and compensation for adopted, verifiable language contributions.
- **Notebook:** the demo notebook (separate body, notebook.md in the repository) ships the technique: lexicon as session contract, three mechanical detection layers, append-only fall register. Its one open cell awaits an executed run — by L4, the run will be reported when it is performed, not before. The falls in §4 and §4b are the register's current proof.

## 10. Version, license, terms
Verification-Before-Assertion — v1.2 · October 4, 2026 · Luka Pintarič. The timestamped public record precedes any adoption, acknowledged or silent.

- **Methodology — open.** The five laws, the AI-failure mapping, the notebook technique, the register schema, the adoption path: CC BY 4.0, attribution required.
- **Corpus — closed.** The ~2,600-document corpus, the full bilingual lexicon, the etymology chains, and the complete fall register remain the contributor's licensed assets. Entries appearing in this document are cited quotations. Terms for the corpus are exactly one: the compensated-contribution model of §6–§7.
- **Rejection clause.** If declined: no obligation on either side; the contribution remains the contributor's to submit elsewhere (University of Ljubljana / PoVeJMo, OpenEuroLLM, or any program); the timestamped public record remains. Decline is a closed door, recorded as a routing event.
- **Integrity of the marks.** ⚠ words stay marked in every derived artifact. A derived version that silently verifies a ⚠ word falsifies the regime and does not represent it. A derived version that drops the Fall Register (§4b) presents the corrected state as if it were always so — the exact failure L3 exists to catch.

Contact: Luka Pintarič — demonstration performed before it is reported (L4).