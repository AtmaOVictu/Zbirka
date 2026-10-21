# Paste-ready texts — 15 Oct 2026

Three deliverables, in the order you need them. Everything stated below is verifiable by link — that is the whole point.

---

## 1. Clarinsi resubmission PR — one click + paste

**Open this link** (it jumps straight to the "Open a pull request" form):

```
https://github.com/clarinsi/Slovenian-Language-Technologies-Overview/compare/main...AtmaOVictu:Slovenian-Language-Technologies-Overview:vba-benchmark-entry?expand=1
```

**Title:**

```
Add Verification-Before-Assertion (VBA) to Benchmarks (resubmission of #1)
```

**Body:**

````markdown
## Resubmission: VBA benchmark entry

This is a resubmission following the review of #1 (closed 2026-10-03), which ended with an invitation to resubmit. Thank you for the detailed review — this PR addresses each of the three points raised:

**1. Working solution is now open and available.** The entry links to [AtmaOVictu/verification-before-assertion](https://github.com/AtmaOVictu/verification-before-assertion), an open-source (MIT for code, CC BY 4.0 for methodology) Python framework. It is dependency-free and runs with a single command (`python test_vba.py`), so anyone can verify the claims in the entry description directly.

**2. One entry in one section.** The diff is exactly one bullet, added under **Benchmarks** in the *Generative Models (LLMs) for Slovenian* section, right after the Slovenian LLM Evaluation entry. The branch is based on the current upstream `main`, so no other lines change.

**3. Hand-written description.** The entry text was written by hand, not machine-translated.

**What the entry describes:** Verification-Before-Assertion (VBA) is a framework for measuring *claim provenance* in Slovenian LLM output — every word a model uses as "measured" must carry a sourced dictionary entry (SSKJ²/Fran) or an explicit unverified mark, and failure modes are recorded in an append-only register of named falls. It ships with a pre-registered measurement protocol and a live comparison of mistral-large-latest with and without the contract (sourced claims 9 → 36 per run; caught hybrids 0 → 1).

This complements the existing task-performance benchmarks (SloBench, Slovenian LLM Evaluation) by measuring a different axis: not how well a model performs a task, but whether its factual claims about language are verifiable. It may be especially relevant for evaluating models on less-resourced languages, where invented words that pass as real Slovenian are a documented failure mode.

Happy to adjust the wording, placement, or length of the entry — or to withdraw it if the curators feel it does not fit the overview's scope.
````

---

## 2. Welo Data — Generative AI Analyst | Slovenian (Slovenia)

**Apply here:** https://jobs.lever.co/weloglobal/feb01370-aede-4ac7-a6e1-c0169ba83755
**Terms:** $13/hour, 4-week freelance contract, remote (Slovenia). Form asks "a few quick questions" — the answers below are sized to paste into typical free-text fields. Trim as the form allows.

**Short summary (for "Tell us about yourself" / intro field):**

```
I am a native Slovenian speaker living in Slovenia, working as an independent language-QA specialist for Slovenian AI output. I am the author of Verification-Before-Assertion (VBA), an open-source Python framework for claim provenance in Slovenian LLM output (github.com/AtmaOVictu/verification-before-assertion): every claim must carry a sourced dictionary entry (SSKJ²/Fran) or an explicit unverified mark, and all model failure modes are logged in an append-only register — currently 28 documented entries. I have completed two full review passes of a 4,500-word Slovenian technical text, identifying 20 named language failures and fixing 22, each verified against the Fran/SSKJ² dictionary infrastructure. I also review and improve AI documentation as a contributor to Mistral AI's public docs (platform-docs PR #602, cookbook PR #420). English: strong written (all of the above is in English). Available immediately, fully remote, flexible hours — the 4-week commitment fits.
```

**"Describe your experience in annotation / content review / QA":**

```
My entire practice is content review and quality assurance for Slovenian AI output, done independently and in the open:

- Review & evaluation of AI-generated Slovenian text: two complete annotated review passes (prede) of a 4,500-word Slovenian technical README, with 20 named failure modes identified and 22 corrections applied. Every correction is verified against a source dictionary (SSKJ² via Fran) — no fix without a citation.
- Building QA methodology, not just applying it: I designed VBA (Verification-Before-Assertion), a pre-registered measurement protocol for claim provenance. It produces concrete, reproducible numbers — e.g., mistral-large-latest with the contract produces 36 sourced claims per run versus 9 without, and the contract caught an invented "hybrid" Slovenian word that passed as real in the unguarded run.
- Register discipline: all failures are recorded in an append-only register (28 entries), with corrections keeping visible scars — the same audit-trail thinking annotation guidelines require.
- Multilingual + AI content: I evaluate a French-built LLM (mistral-large-latest) on Slovenian material, and contribute corrections to English-language AI documentation for Mistral AI.
```

**"Why are you a good fit for this role?" / motivation:**

```
Three reasons, each measurable:

1. Native Slovenian with a verification habit, not just fluency. Anyone can say a sentence "looks wrong" in Slovenian; I can point to the SSKJ/Fran entry that proves it, which is exactly the calibration-and-alignment work this role describes.

2. I already do this work daily — unpaid, in public. The VBA register (github.com/AtmaOVictu/verification-before-assertion) is a standing portfolio: 28 documented model-failure entries, a reproducible protocol (runs with zero dependencies, python test_vba.py), and published numbers. Reviewing Slovenian AI content for Welo Data would be the same discipline, with guidelines and compensation.

3. Attention to detail is my documented failure mode, in the good sense: in my last review pass I rejected my own first-choice word (ugíb) as obsolete and replaced it after checking the source — the register records the scar. Edge cases and inconsistencies are what I collect.
```

**Availability / logistics:**

```
Remote in Slovenia (native, resident). Immediate start. Flexible hours, can align to project calibration schedules. Freelance contract is fine.
```

---

## 3. CLARIN helpdesk introduction — draft (send AFTER the clarinsi PR is merged)

**To:** helpdesk.classla@clarin.si
**Subject:** Open-source Slovenian LLM claim-provenance framework (VBA) — introduction and offer

````markdown
Dear CLASSLA helpdesk,

My name is Luka Pintarič, an independent researcher of Slovenian language-technology evaluation. I am writing to introduce a resource that may be useful to the Slovenian LT community, and to offer my help.

I maintain Verification-Before-Assertion (VBA), an open-source, dependency-free Python framework for measuring claim provenance in Slovenian LLM output (github.com/AtmaOVictu/verification-before-assertion). In brief: every word a model uses as "measured" must carry a sourced dictionary entry (SSKJ² via Fran) or an explicit unverified mark, and all model failure modes are recorded in an append-only register of named falls (currently 28 documented entries). The framework ships with a pre-registered measurement protocol and a live comparison of mistral-large-latest with and without the contract (sourced claims 9 → 36 per run; caught "hybrid" invented words 0 → 1). Methodology is CC BY 4.0, code MIT.

VBA is now listed among the Benchmarks in the Slovenian Language Technologies Overview (I recently submitted the entry there — PR "Add Verification-Before-Assertion (VBA) to Benchmarks").

Where I believe this may interest CLASSLA:

1. It complements task-performance benchmarks such as SloBench by measuring a different axis — not how well a model performs a task, but whether its factual claims about Slovenian are verifiable.
2. It documents concrete, named failure modes of a major LLM on Slovenian, in a reproducible, citable form — potentially useful material for anyone studying LLM quality on less-resourced languages.
3. I would be glad to help: if the helpdesk or the community needs evaluation or review of Slovenian LLM output — annotation, QA, or verification work — this is precisely my daily practice.

Thank you for your time, and thank you for curating the Overview — it is a genuinely useful map of the field.

Lep pozdrav,
Luka Pintarič
github.com/AtmaOVictu
````

*Note: the PR reference line should be updated with the actual PR number/merge link before sending.*