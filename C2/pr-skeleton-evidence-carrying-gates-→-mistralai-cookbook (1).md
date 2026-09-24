# PR skeleton: Evidence-carrying gates → mistralai/cookbook

*Vse, kar potrebuješ za oddajo. Manjka eno polje: tvoj GitHub handle.*

---

## 1. Njihove zahteve (preverjeno ob repozitoriju)

| Zahteva | Kako je izpolnjena |
|---|---|
| Format: `.md` ali `.ipynb` | `.md`, v korenu repozitorija (precedens: `01-glm-game-generator.md`) |
| Avtorstvo na začetku datoteke: ime, GitHub handle, afiliacija | Glava datoteke — **dopolni handle** |
| Vrstica v tabeli README (kategorija + opis) | Pripravljena spodaj |
| Nevtralen ton | Ostri stavki ublaženi v oddajni različici (canvas ostaja celi) |
| Reproducibilnost: verzije paketov | Pin v glavi kode |
| Pre-commit hooks (varovalo ključev) | V ukazih spodaj |
| Kriteriji: izvirnost, jasnost, vrednost | Izpolnjeno — kompozicija je nova, infrastruktura dokumentirana |

---

## 2. Datoteka za oddajo: `evidence-carrying-gates.md`

```markdown
# Evidence-carrying gates: a verification pattern for agent actions

Author: Luka Pintarič
GitHub: @AtmaOVictu
Affiliation: Independent

> Use this pattern when agent actions depend on factual claims that must be
> checked before execution.

## Problem

Approval gates approve actions; they do not validate claims.

When an agent asks "approve this action?", the human approves or denies a tool
call — send the email, modify the record, run the query. Nothing in the gate
tells the human whether the claims the action depends on are true.

The two obvious fixes both fail:

- Lowering temperature makes runs repeatable. Repeatability measures the
  instrument, not the claim — a model can be consistently wrong, and a stable
  fabrication passes every consistency check.
- Asking the model for self-assessment asks the system to grade itself. Model
  self-evaluation can fabricate confidence.

This pattern closes the gap using documented Mistral primitives plus one piece
of application logic.

## Pattern

retrieval → generation with citations → evidence extraction →
confirmation gate carrying an evidence payload → human review

Key idea: the gate carries checkable evidence — spans, coverage, unverified
items — not just the action.

A citation that comes from retrieval is machine-checkable: the span either
exists in the source or it doesn't. Evidence a model was merely instructed to
output is still generation, and generation can fabricate. This pattern uses
retrieval-backed citations as the anchor, never prompt-requested confidence.

## The evidence payload

Every checkable claim in the output (names, dates, sources, numbers) carries a
pointer to its exact span and one of four states:

- verified — span found in source, content matches
- contradicted — span found, content conflicts
- unverified — checkable claim, no source available
- unchecked — counted in coverage, not examined

Coverage is quantified including the unread. A gate that says "3 verified,
1 unverified, 6 unchecked" gives the human a real decision. A gate that
reports only an aggregate mark hides it.

## Implementation

### Anchor layer — documented primitives

```python
# Requires: mistralai==1.10.0
from mistralai import Mistral

client = Mistral()

# 1. Generate with citations (documented: Citations & References)
response = client.chat.stream(
    model="mistral-medium-latest",
    messages=messages,          # RAG-backed query
)
# response carries citations: [{index, source_uri, span}, ...]

# 2. Extract checkable claims from the output
claims = extract_checkable_claims(response.text)
#   names, dates, sources, numbers — each anchored to its citation span

# 3. Verify each claim against its source (application logic)
for claim in claims:
    claim.status = check_span_against_source(claim.span, claim.source_uri)
    # verified | contradicted | unverified

# 4. Build the payload
payload = {
    "action": action,
    "evidence": {
        "claims": [claim.to_dict() for claim in claims],
        "coverage": {
            "checked": sum(c.status != "unverified" for c in claims),
            "contradicted": sum(c.status == "contradicted" for c in claims),
            "unchecked": count_unchecked_spans(response),
        },
    },
}

# 5. Gate: requires_confirmation intercepts the tool call (documented:
#    Human-in-the-loop). The approval UI renders the payload:
#    "1 verified · 1 unverified · 6 unchecked — approve?"
```

`requires_confirmation` already intercepts the call before execution. This
pattern changes only what the human sees at the gate: the action, its claims,
their states, and the coverage count.

### Targeting layer — application logic (not a platform feature)

Uniform spot-checks miss the tail, and fabrication lives in the tail: rare
names, obscure dates, plausible-but-invented sources. Human validation is
aimed, not sampled uniformly.

```python
# 1. Disagreement sampling — run N times via Batch API (documented, 50% cost)
runs = client.batch.run(prompt, n=5)

# 2. Cluster by meaning, not by text (application logic)
clusters = cluster_by_meaning([r.text for r in runs])

# 3. Entropy over meaning-clusters: high disagreement = soft ground.
#    Research grounding: semantic entropy (Farquhar et al., Nature 630, 2024)
disagreement = semantic_entropy(clusters)

# 4. Rank what the human validates
priority = rank(by=[disagreement, rare_entity_score(claims)])
# The top of `priority` goes to human validation — not a uniform sample.
```

## Guardrail

The system aims attention; it never replaces judgment. Two rules keep it
honest:

1. Every gate shows what was checked, how, and what was not. Quantified
   coverage includes the unread.
2. The chain terminates in a human decision. A verification chain that ends
   in a document has not ended — it has only moved the trust elsewhere.

## Documented vs. application-level

| Layer | Status |
|---|---|
| Citations with spans | Documented (Citations & References) |
| Confirmation gates | Documented (`requires_confirmation`, Workflows: Waiting for Conditions) |
| Batch sampling at half cost | Documented (Batch API) |
| Judge-based evaluation | Documented (Observability); validate judges against human spot-checks before scaling |
| Disagreement sampler + rare-entity ranker | Application logic — the novel part of this pattern |

## Acknowledgments

The pattern was developed in dialogue with a Mistral AI agent, which scoped
the gap: "approval gates let humans approve actions, not validate claims."
The disagreement-sampling logic is grounded in *Detecting hallucinations in
large language models using semantic entropy* (Farquhar, Kossen, Kuhn, Gal —
Nature 630, 2024).

## Appendix: the evidence payload

```json
{
  "action": { "tool": "send_email", "args": { "to": "...", "body": "..." } },
  "evidence": {
    "claims": [
      { "text": "acquired in March 2024", "span": [142, 163],
        "source_uri": "doc://library/report-q1", "status": "verified" },
      { "text": "€2.1M revenue", "span": [201, 214],
        "source_uri": null, "status": "unverified" }
    ],
    "coverage": { "checked": 1, "contradicted": 0, "unchecked": 6 }
  }
}
```
```

---

## 3. Vrstica za tabelo v `README.md`

Dodaj v tabelo **Main Notebooks**:

```markdown
| evidence-carrying-gates.md | agents, evaluation, guardrails | Verification pattern: make approval gates carry checkable evidence (citations, spans, coverage) before an action is approved |
```

---

## 4. Ukazi (fork → PR)

```bash
# 1. Fork na github.com/mistralai/cookbook (gumb Fork)
# 2. Kloniraj svoj fork:
git clone https://github.com/<TVOJ-UPORABNISKI-IME>/cookbook.git
cd cookbook

# 3. Pre-commit hooks (obvezno — varovalo ključev):
pip install pre-commit
pre-commit install

# 4. Veja:
git checkout -b add-evidence-carrying-gates

# 5. Dodaj evidence-carrying-gates.md v koren + vrstico v README.md

# 6. Preverba in oddaja:
pre-commit run detect-private-key --all-files
git add evidence-carrying-gates.md README.md
git commit -m "Add cookbook: evidence-carrying gates — a verification pattern for agent actions"
git push origin add-evidence-carrying-gates

# 7. Odpri PR na mistralai/cookbook (main)
```

---

## 5. Besedilo PR

**Title:** `Add cookbook: evidence-carrying gates — a verification pattern for agent actions`

**Description:**

> Adds a community cookbook entry describing **evidence-carrying gates**: an approval-gate pattern where the gate carries checkable evidence (claim spans from citations, verification states, coverage counts including unchecked items) instead of only the action to approve.
>
> Built entirely on documented primitives (Citations & References, `requires_confirmation`, Batch API, Observability). The only application-level logic is the targeting layer: disagreement sampling and rare-entity ranking to prioritize human validation. Research grounding: semantic entropy (Farquhar et al., Nature 630, 2024).
>
> Format: `.md`, authorship at top, README table row included, neutral tone, no external images.

---

## 6. Kontrolna lista pred oddajo

- [ ] GitHub handle v glavi datoteke
- [ ] Verzija `mistralai` pinjana na tisto, ki jo dejansko poganjaš
- [ ] Vrstica v README tabeli dodana
- [ ] Pre-commit nameščen in zagnan
- [ ] PR besedilo prilepljeno