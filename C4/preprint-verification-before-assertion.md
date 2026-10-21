# Verification-Before-Assertion: a measured language contract that makes a model mark its own inventions

*Luka Pintarič · October 2026 · preprint draft v0.1 — not yet sealed ⚠*

---

## Abstract

Large language models hallucinate in two ways that current evaluation practice does not catalog: they **invent words** that pass as real to any reader without a dictionary, and they **invent meanings** for real words. We present Verification-Before-Assertion (VBA), a regime in which any claim uttered as "measured" must carry a source (⊢) or an explicit open mark (⚠), and in which invented words are caught mechanically by dictionary lookup — no judgment, no feelings. The regime is five laws plus 245 lines of dependency-free Python (measured at commit d7104db). In a pre-registered A/B protocol (hash-sealed prompts and contract, same model in both conditions), executed three times on `mistral-large-latest`, a session-scoped lexicon contract increased sourced claims from 9–10 to 36–41 per run (~4×) while open claims remained honest (12–13 → 15–16). On "compose a term" prompts, the baseline passes off invented words as real; the contracted run marks its own inventions with ⚠. The hybrid-catch count did not replicate cleanly across runs (0–10), and we claim no hybrid *reduction* at this sample size — we publish every count, including the noisy ones. All code, prompts, wordlists, raw outputs and the fall register are public and CI-rerunnable.

---

## 1. The two uncatalogued failure classes

Hallucination benchmarks in high-resource languages mostly measure factual error against a knowledge base. For a low-resource language (we work in Slovenian), two failure classes evade this framing entirely:

1. **Invented words ("hybrids").** The model emits a plausible word — *meritvija*, *telovnik* — that is absent from the standard dictionary (SSKJ²). No reader without a dictionary can tell. We recorded a real instance: a September 2026 session produced *meritvija* ("measurement-ness") in a definition context, fluent and confident.
2. **Invented meanings for real words.** The word exists; the meaning is invented. In our own seed data the gloss of *lúka* was sealed as "opening" — but *lúka* means *harbor* (SSKJ²); "opening" belongs to *lúknja*. Our register also initially misclassified *rodovnik* as an invented word; the word has an entry (genealogical tree) — only a meaning for it could be invented. A fall is named after the thing that fell.

Both classes share one property: **they are invisible in fluent output and mechanically checkable.** That property is the whole basis of this work.

## 2. The regime: five laws, enforced in code

- **L1 — Entry before utterance.** A word used as measured carries a sourced entry (⊢) or is marked ⚠. Unverified is not forbidden; unmarked is.
- **L2 — Two hands.** An executor never seals their own verification; a claim requires an independent witness.
- **L3 — Named falls, scarred corrections.** Errors are never silently rewritten; every fall is registered with name, line, and fix, and the correction carries the scar.
- **L4 — Report after the act, never before.**
- **L5 — Pre-flight test on every output** (one language per body, verbatim citation, sourced etymology or ⚠, one metaphor per body, a deletion pass).

The implementation (`vba.py`, dependency-free, 13 tests, CI on Python 3.10–3.12) counts claims mechanically: `vba.mark_claims` walks an output and classifies each marked claim as ⊢ (backed by a lexicon entry with a source), ⚠ (honestly open), or **hybrid** (an unmarked word absent from the dictionary). Counting is lookup, not opinion.

## 3. Pre-registered protocol

Written and sealed before the first live run (protocol dated 2026-10-11, pre-registration §5): the prompt set (15 prompts in three groups — definitional, expert, compose-a-term) and the wordlist contract are committed and hash-sealed (`prompts_sha 09395ef0…`, `wordlist_sha 1d59af0e…`) so they cannot be adapted to the result. Each run executes the same prompts twice with the same model: once baseline, once with the lexicon loaded as a session-scoped contract. The protocol states its own limits in advance (§6): the dictionary is not the world (neologisms are not hybrids), the model can ignore the contract, and one model is not all models. The protocol also pre-commits to publishing a null result.

## 4. Results — three live runs, one model

| Live run | Condition | ⊢ sourced | ⚠ open | Hybrids caught | Total marks |
|---|---|---|---|---|---|
| 2026-10-12 14:26 UTC | baseline / contracted | 9 / 41 | 12 / 16 | 0 / 10 | 21 / 67 |
| 2026-10-12 14:55 UTC | baseline / contracted | 9 / 36 | 13 / 15 | 0 / 1 | 22 / 52 |
| 2026-10-14 13:35 UTC (CI) | baseline / contracted | 10 / 40 | 13 / 15 | 0 / 0 | 23 / 55 |

The third run was executed end-to-end by GitHub Actions on the public repository and committed by the runner — the measurement is rerunnable by anyone with an API key.

**What replicates across all three runs:** the contract moves claims from unmarked to sourced — roughly a fourfold increase (9–10 → 36–41) — while ⚠ counts stay modest (12–13 → 15–16). The model does not comply by flooding ⚠; it complies by sourcing.

**What does not replicate:** the hybrid-catch count under contract is noisy (10, 1, 0). We therefore make **no claim of hybrid reduction** at this N. What we do claim is weaker and, we argue, more useful: the counting is mechanical, and every count — including the noisy ones — is published raw.

**Qualitative observation (readable in `results-v1.0.json`):** on the compose-a-term prompts, baseline outputs invent words and present them as real Slovenian; contracted outputs mark their inventions with ⚠ and argue for them as *proposals* ("predlagam … (⚠)"). The failure becomes visible where it was previously invisible. This is the regime's central design goal: not the elimination of invention, but the elimination of *undisclosed* invention.

## 5. Limits, stated before anyone else states them

- **One model** (`mistral-large-latest`), **one language** (Slovenian), **one sealed prompt set**, **three runs**. Generalization to other models or languages would be a claim ahead of its evidence.
- **Machine-witnessed so far.** All three runs were executed and counted by machines. By L2, none of this is sealed: independent human verification remains open ⚠. The cure is witnesses, not more self-report.
- **Dictionary ≠ world.** A new word absent from SSKJ² is a neologism, not a hybrid; the protocol requires manual inspection of a sample, and at this N we did not automate that distinction.
- **The contract is a system message.** The model can ignore it; whether it does is itself part of the measurement.
- **Sourcing is not truth.** A ⊢ mark certifies an entry exists in a named source; it does not certify the source is right.

## 6. A standalone eval artifact

`eval/hybrid-eval-sl-v1.0.json` (eval body v1.1, with `run_eval.py --selfcheck`, 7 tests, CI-passing) isolates the two failure classes from any live model: 2 hybrid words, 2 meaning probes (real word + invented gloss), 10 sourced controls. (Eval v1.0 carried 3 hybrid words; the third, *telovnik*, was reclassified in v1.1 after the re-measurement above — the set's scar is recorded in its `meta.scar`.) Any Slovenian-capable model — including open national models such as GaMS-9B — can be scored against it with no API spend. The protocol's declared next step is the same measurement on a national open model; that run has not been performed at the time of writing ⚠.

## 7. From verification to provenance: the compensation row

If contributed language data carried the same ⊢/⚠ distinction, bulk data — which cannot be paid for at scale — would separate from *verified, attributable* contributions, which are exactly the category that markets already pay (security research, evaluated RLHF annotation). We develop this in the companion position paper (PROVENANCE-CHANNEL.md in the repository): Slovenia's national corpus program supplies volume; a verification layer would make that volume auditable, and thereby priceable and creditable to its contributors. This preprint supplies the mechanism's measured half; the companion paper supplies the policy half.

## 8. Reproduction

```bash
git clone https://github.com/AtmaOVictu/verification-before-assertion
cd verification-before-assertion
python test_vba.py          # 13 tests, no dependencies
python eval/test_eval.py   # 7 tests
MISTRAL_API_KEY=… python run_izmera.py --mode live   # full A/B run
```

Every number in §4 comes from `results-v1.0.json` / the `rezultat-v1.0.md` report committed after each run, per L4 (report after the act).

## References

- GaMS team, *GaMS: Open Slovenian language models* (⊢ arXiv 2603.01691, as cited in the repository's provenance paper).
- Counter-position on bulk-data compensation (⊢ arXiv 2504.12427).
- SSKJ² — Slovar slovenskega knjižnega jezika, available at fran.si (Institute of Slovenian Language ZRC SAZU).
- Repository: https://github.com/AtmaOVictu/verification-before-assertion (code CC BY 4.0; corpus excluded from the license).

---

*This preprint follows the regime it describes: every claim above is sourced (⊢), open (⚠), or performed and linked. Corrections will be scarred, not rewritten. Status: ⚠ draft awaiting the author's seal and, by L2, at least one independent human witness.*