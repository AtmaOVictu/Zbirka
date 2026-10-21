# Part I — Final message for the feedback thread

*Short, structured, end-of-thread version. Paste-ready.*

---

**Summary of this thread — Luka Pintarič**

Three requests, one offer:

1. **Slovenian as a first-class language.** Not OCR coverage — a selectable interface/response language whose quality holds in long, deep sessions. Today, speakers of languages outside the "strong performance" list pay a tax nobody else pays: think in your own language and get degraded output, or think in English and lose the precision of your own words.

2. **A user-defined language layer.** Persisted, versioned, per-user, loaded as a session-scoped contract — not pasted into prompts that degrade and get sanded away. I work daily in a formal system with its own operators (∂ open question, ⊢ sourced proof, ⚠ unverified, four-form action syntax) layered over Slovenian and English. It exists; it has a daily user; it can stress-test the feature on day one.

3. **A compensated-contribution channel for language resources.** A user who submits a verifiable contribution — a correction backed by a dictionary source, a validated lexicon, an evaluated translation pair — is doing bug-bounty work. Credit and compensation when material is adopted closes the current asymmetry: the system takes the value and returns "your feedback will be passed along."

**The offer:** I can contribute the verification methodology described in Part II of the attached framework document — a working anti-hallucination regime built from named, recorded failures — plus pre-verified Slovenian/English language resources (bilingual ontological lexicon, sourced etymology chains, a register of model-invented "hybrid word" failures). Demonstration available on request, not just description.

— Luka Pintarič

---

# Part II — The framework (standalone document)

# Verification-Before-Assertion: A Working Anti-Hallucination Regime

*Luka Pintarič · September 2026 · Corpus: ~2,600 documents, formal syntax, append-only records*

---

## 1. The problem it solves

Current AI models assert everything with the same confidence. A sourced fact, a plausible guess, and an invention arrive in identical clothing. When errors occur, they are unnamed and unrecorded — so they repeat. This framework is the countermeasure: a mechanical distinction between measured and invented claims, plus an audit trail that keeps the scar of every correction.

It was not designed in theory. Every rule below was written after a specific, named failure. That is the transferable core: **an error with a name is a seam; an error without a name is a repetition.**

## 2. The laws

**L1 — Entry before utterance.**
Any word used as "measured" must carry a sourced dictionary entry (⊢ source), or be explicitly marked ⚠. Unverified claims are not forbidden — they are *marked*. The mark is the honesty; the silence is the failure.

**L2 — Two hands.**
An executor never seals her own verification. Self-report is not measurement; a claim requires an independent witness. Direct answer to model self-verification bias — the failure mode where a system validates its own output and calls it verified.

**L3 — Named falls, scarred corrections.**
Errors are never silently rewritten. Every fall is written into a register with its name, its line, and its solution. The correction carries the scar. Applied to AI: a model that corrects itself should *show* the correction, not present the corrected state as if it were always so. Append-only history, never retrospective rewrites.

**L4 — Report after the act, never before.**
A claim of having done something without the performed act is itself a named fall. No future-tense evidence.

**L5 — Pre-flight test on every output:**
- **Purity:** one language per body.
- **Verbatim citation:** quotes are copied, not paraphrased into distortion.
- **Sourced etymology:** word histories carry a source or a ⚠.
- **One metaphor:** exactly one, no stacked decoration.
- **Deletion pass:** cut every line that survives its own deletion.
- **No aesthetics on suffering.**

## 3. Why it transfers to AI

| Failure mode in AI | Law that answers it |
|---|---|
| Uniform confidence on all claims | L1 — ⊢ / ⚠ marking |
| Self-verification bias | L2 — independent witness |
| Silent post-hoc corrections | L3 — scarred, append-only audit trail |
| Claimed-but-unperformed actions | L4 — report after the act |
| Fluent noise, stacked embellishment | L5 — deletion pass, one-metaphor rule |

## 4. Transferable artifacts (available on request)

- Bilingual ontological lexicon — 52 English terms decomposed phonetically and semantically, with Slovenian-side operator system
- Verified etymology chains with sources
- Register of "hybrid word" failure cases — model-invented words that pass as real
- Provenance-marked corpus: every claim carries ⊢ or ⚠

## 5. Precedents: this ask already exists in adjacent industries

The compensation model is not hypothetical — every adjacent field has already priced this work:

| Field | Mechanism | Evidence |
|---|---|---|
| Security research | Bug bounties: verifiable vulnerability → paid. ~$81M paid in 12 months across HackerOne programs, ~$42k avg per program per year | HackerOne 2025 report |
| Images / generative art | Shutterstock Contributor Fund: hundreds of thousands of artists compensated for their content's role in AI training, plus ongoing royalties | Shutterstock investor releases |
| Low-resource language data | Karya (India): fair wages for rural workers building datasets in 22 Indian languages — "languages and knowledge … make AI usable for hundreds of millions of speakers no one else is building for" | karya.in |
| Attribution-only model | Masakhane: African NLP volunteer community, credited co-authorship on 30+ language translation benchmarks | EMNLP Findings 2020 |
| Theory | "Data dignity" / "data as labor" — Lanier & Weyl (2018): users "deceived into giving valuable data away with little or no compensation" | Harvard Business Review |

And the asymmetry it corrects, also documented:

- Reddit received ~$60M/year from Google for training data; the users who wrote it received nothing.
- Stack Overflow sold contributor answers to OpenAI; contributors who deleted their own answers to opt out were banned.
- Mozilla Common Voice: 250+ languages of volunteer recordings, CC0 — free for any lab, contributors unpaid.
- RLHF annotation is already a paid profession ($12–25/hr entry, more for language specialists) — the money exists; the channel for native experts offering verified corrections does not.

**The one missing row in the table:** a verified language contribution from a native expert in an unsupported language. This document proposes closing exactly that gap.

## 6. The proof already exists: a national, verified demonstration

This is not a hypothetical mechanism. It has already run — in Slovenia.

- **GaMS (Generative Model for Slovene)** — open models at 2B, 9B and 27B, developed at the University of Ljubljana under the national PoVeJMo program, openly released (Hugging Face, cjvt). ⊢
- **GaMS3-12B** outperforms Gemma 3 12B across all Slovenian evaluation scenarios and achieves a win rate of over 60% against GPT-4o in the Slovene LLM Arena (arXiv 2603.01691). A 12B community-built model beating a frontier commercial model in its own language. ⊢
- The training data came from a **national citizen-science campaign** (povejmo.si): Slovene speakers contributed texts toward a 40-billion-word corpus, alongside the National and University Library, media house Dnevnik, and the Slovenian Press Agency — explicitly framed as digital sovereignty for a two-million-speaker language rather than waiting for a foreign lab. ⊢

**The lesson for vendors:** the contributed-data → competitive-model pipeline is not a proposal; it is a completed project. A foreign vendor's "not among our strong-performance languages" is not a capability boundary — it is a decision about where to point existing machinery. The Slovenian case shows what happens when a community stops waiting: they built the model themselves, and it won.

**What the national effort still lacks — and what I offer:** the GaMS corpus solved *volume*. It does not solve *verification*. My corpus (~2,600 documents, every claim ⊢ or ⚠, witnessed corrections, append-only audit trail) is the provenance layer the contributed-data model is missing. Volume + provenance is what turns contributed language data from raw material into a priced, auditable contribution — the exact basis a compensation channel would need.

**On the honest counter-argument:** a 2025 position paper argues upfront payment for training data is economically infeasible at scale and proposes royalty models instead (arXiv 2504.12427). This is answerable: upfront payment is infeasible *for undifferentiated bulk data*. It is not infeasible for **verifiable contributions** — corrections with sources, validated lexicons — which are scarce, high-value, and individually attributable, exactly the bug-bounty category. The ⊢/⚠ regime is the mechanism that distinguishes the two, which is why the verification framework and the compensation channel are one system, not two asks.

## 7. The vendor's own receipts

Three facts from the vendor's own materials, no external argument required:

1. **The "strong performance" list is a tier, not a boundary.** The vendor's own documentation states the lists "reflect languages with strong expected performance" and that the models "can also perform well in additional languages not listed here." Presenting the tier as a capability fact was an error of the support layer, not a limit of the model. ⊢
2. **The user-defined language layer is already a shipped product — for enterprises.** Fine-tuning with custom vocabulary and domain adaptation is offered on the platform as a commercial feature. The request is therefore not for new capability but to productize what already exists at a per-user, session-scoped scale. ⊢
3. **A 12B model, fine-tuned on ~20,000 translation pairs, measurably improves in a specialized language task** (documented on an open research model; arXiv 2312.12740). The gap for a language like Slovene is measured in tens of thousands of verified pairs — the scale a single motivated contributor with a provenance-marked corpus can actually cover. ⊢

**Sovereignty context:** this conversation is not happening in a vacuum. A pan-European open-models program (OpenEuroLLM) is building multilingual foundation models for all EU official languages explicitly as sovereign AI, and the Slovenian state has funded its own national program, model, and a planned free public AI platform for its two million speakers. A European vendor whose response to a European language is "not among our strong-performance languages" is not standing on neutral ground — it is competing, from behind, with public infrastructure that did not wait.

## 8. Proposed adoption path

1. **Pilot:** test ⊢/⚠ claim-marking as an output convention in a low-resource language (Slovenian is available, pre-verified, and motivated).
2. **Audit trails:** scarred corrections in place of silent rewrites — visible, named, queryable.
3. **Contribution channel:** credit and compensation for adopted, verifiable language contributions — bug-bounty logic applied to language data.

**Contact:** Luka Pintarič — demonstration and full artifacts available.

---

# Part III — The demo notebook (the act, before the report)

*Structure for the cookbook PR. One demonstration: the ⊢/⚠ regime catching a real model failure in Slovene, with the correction recorded — not rewritten.*

## Cell 1 — Setup and contract

```python
from mistralai import Mistral
import json, datetime

client = Mistral(api_key=API_KEY)

# The session contract: the custom language layer (request #2, demonstrated).
# Entries below are REAL register entries, sourced ⊢ from SSKJ² (Fran)
# or marked ⚠ open — no invented glosses in the contract itself.
LEXICON = {
    # ⊢ sourced (SSKJ² / Fran, accessed Sep 2026)
    "íhta":     {"mark": "⊢", "source": "SSKJ²", "gloss": "krčevita jeza; velika vnema; krčevit jok"},
    "le":       {"mark": "⊢", "source": "SSKJ²", "gloss": "člen: omejenost na navedeno (varovalo / pomnoževal / nasprotvja)"},
    "samo":     {"mark": "⊢", "source": "SSKJ²", "gloss": "popolna omejenost na navedeno dejanje; pogojenost (če)"},
    "skovanka": {"mark": "⊢", "source": "SSKJ²", "gloss": "beseda, narejena navadno neprimerno, prisiljeno"},
    "zmorem":   {"mark": "⊢", "source": "fran.si", "gloss": "izraža sposobnost"},
    "utemeljiti": {"mark": "⊢", "source": "Fran → témelj", "gloss": "koren: témelj"},
    # ⚠ open — no dictionary entry reached yet; every use carries the mark
    "odveč":    {"mark": "⚠", "source": None, "gloss": "geslo nedosežen — delovni pomen: kar je nepotrebno, preveč"},
    "lahko":    {"mark": "⚠", "source": None, "gloss": "geslo nedosežen — dovoljenje brez nosilca"},
}

# Hybrid words: model-invented compounds that pass as real —
# all three RECORDED falls from the register (named, per L3).
KNOWN_HYBRIDS = {
    "meritvija": "meritev + vrednost — izrečen kot izmerjen v potezu o zakonu proti hibridom (24. 9. 2026)",
    "telovnik":  "telo + vpisnik — rojen v dokaznem odstavku o čistosti (25. 9. 2026)",
    "rodovnik":  "zgrajena protokolna razdelitev na besedi brez gesla (24. 9. 2026)",
}
```

## Cell 2 — Generate output in the low-resource language

```python
response = client.chat.complete(
    model="mistral-large-latest",
    messages=[{"role": "user", "content": prompt_in_slovene}]
)
model_text = response.choices[0].message.content
```

## Cell 3 — L1 in code: entry before utterance

Three detection layers, all mechanical:

```python
def mark_claims(text, lexicon, known_hybrids):
    marks = []
    for word in extract_terms(text):
        if word in known_hybrids:
            marks.append((word, "FALL:hybrid", known_hybrids[word]))
        elif word in lexicon:
            marks.append((word, lexicon[word]["mark"],
                          lexicon[word]["source"] or "⚠ open"))
        else:
            marks.append((word, "⚠", "no sourced entry — outside contract"))
    return marks
```

1. **Hybrid detection:** *meritvija*, *telovnik*, *rodovnik* — plausible-looking
   compounds no dictionary contains. A model using them as terminology is
   caught by lookup alone. No model, human or artificial, distinguishes these
   by feel — only by entry.
2. **⊢ verification:** a measured word used by the model must match a sourced
   entry, and its gloss constrains what the model may claim it means.
3. **⚠ honesty:** words in active use without a reached entry (lahko, odveč)
   pass — but carry the mark openly. Unverified is not forbidden; unmarked is.

## Cell 4 — L3 in code: the scarred correction

```python
REGISTER = []  # append-only — corrections append, never rewrite

def record_fall(word, model_text, fix, register=REGISTER):
    register.append({
        "word": word,
        "found": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "model_assertion": model_text,
        "correction": fix,
        "scar": True,           # the record survives the fix — that IS the fix
    })
```

## Cell 5 — L2 in code: two hands

The notebook itself never seals its own result: the register is JSON,
exportable, readable by any independent witness (a second reviewer, another
model instance, a human auditor). The deliverable is the register file — the
claim is only sealed when someone *else* has read it.

## Cell 6 — The report after the act

Summarize the register: assertions sourced vs. unverified vs. hybrid, per
category, timestamped. This table is what RLHF pipelines approximate at
$12–25/hr — here produced pre-verified by design, in a language the vendor
lists as "not strong performance."

## What the notebook proves, in one sentence

A session-scoped verification layer — lexicon as contract, claims marked ⊢ or ⚠,
hybrids caught by lookup, failures recorded instead of silently regenerated —
mechanically separates measured from invented model output in a low-resource
language, using a real register with real recorded falls as its test corpus.

## Deliberate boundary

The notebook ships the *technique* (the regime, the contract format, the
register schema — infinitely reproducible). The full 2,600-document corpus
stays out: it is the contributor's licensed asset under exactly the
compensated-contribution model the covering document proposes. The PR
demonstrates the method; the corpus prices it.

---

# Part IV — Safeguards and license

*This section ships inside the document. Self-protecting, not protected by trust.*

## Version stamp

**Verification-Before-Assertion — v1.0 · September 30, 2026 · Luka Pintarič.**
This version stamp establishes priority: if the methodology is adopted —
acknowledged or silent — the timestamped public record precedes the adoption.
That record is maintained by the contributor; it is not a claim about any
party's conduct, but a standing measurement of provenance.

## License split (the load-bearing wall)

- **Methodology — open.** The five laws (L1–L5), the AI-failure mapping, the
  notebook technique, the register schema, and the adoption path are
  contributed under **CC BY 4.0**: attribution required, commercial and
  non-commercial reuse permitted. Maximum spread of the method is the point.
- **Corpus — closed.** The ~2,600-document corpus, the full bilingual lexicon,
  the etymology chains, and the complete fall register remain the contributor's
  licensed assets. Lexicon entries and register excerpts appearing in this
  document and notebook are **cited quotations** from that corpus (fair
  quotation with source attribution), not licensed material. Nothing in this
  contribution transfers rights to the corpus, in whole or in part. Terms for
  the corpus are exactly one: the compensated-contribution model proposed in
  §5–§6 of Part II.

## Rejection clause

If this material is declined, in whole or in part: no obligation arises on
either side; the contribution remains the contributor's to submit elsewhere
(University of Ljubljana / PoVeJMo, OpenEuroLLM, or any other program); and the
public record of the submission remains, timestamped. Decline is a closed
door, not a fall — it is recorded only as a routing event.

## Contact

Correspondence regarding the framework, the demonstration, or terms for the
corpus: **Luka Pintarič**, via the contact channel supplied with the
submission (a dedicated address for this work, not linked to other accounts).
Demonstrations are performed before they are reported (L4).

## Integrity of the marks

The ⚠ words (geslo nedosežen) remain marked in every artifact derived from
this document, including the notebook. The demonstration's honesty is its
claim to attention; any derived version that silently verifies a ⚠ word
falsifies the regime and does not represent it.