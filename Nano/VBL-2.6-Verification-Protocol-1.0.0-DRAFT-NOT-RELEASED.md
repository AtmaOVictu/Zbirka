# VBL 2.6 — Verification Protocol 1.0.0

**Status:** `DRAFT · LOCAL PREFLIGHT ONLY · NOT RELEASED · NOT LEGAL ADVICE`

## Version boundary

- **Outer framing label:** `10.1.0` — proposed framing label only, not the licence version.
- **Licence text version:** `2.6` — retain the embedded header `Version 2.6 · October 23, 2026` unchanged.
- **Verification procedure:** `VBL Verification Protocol 1.0.0` — separate document describing how evidence is checked; it does not amend the licence.
- **Workstream / branch label:** `vbl/2.6-verification-v3` — proposed label only. No GitHub branch, commit, or PR was created.
- **VBL 10.x drafts:** separate line of work. No supersession or canonical lineage is inferred.

The original export begins with `10.0.0` and later identifies the licence as `Version 2.6`. The proposed derivative changes only the first framing line to `10.1.0`, as requested, while preserving the inner licence version. Because the source export contains copied/export material and its publication chain is not independently established, the derivative remains `DRAFT-NOT-CANONICAL`.

## Core rule

A check returns `PASS`, `FAIL`, or `UNVERIFIED` with a named scope and evidence. A missing test, absent witness, self-certification, or blocked external operation must never be silently converted to `PASS`. Structural validation is not proof of truth; a hash is not proof of authorship; passing a local fixture is not proof of production behavior.

## VBL-001 — Source identity and preservation

Preserve the submitted source bytes. Record source location, exact size, SHA-256, encoding, and extraction boundaries. Recompute the digest from the actual file. Treat a mismatch as `FAIL`; where the original source is unavailable, use `UNVERIFIED`.

## VBL-002 — Version-boundary consistency

Keep the frame label, embedded licence version, procedure version, and workstream/branch label in separate fields. Do not rewrite `Version 2.6` to `10.1.0`. Do not infer that the framing label is an official licence version. Any ambiguity about the intended semantics must be resolved by an explicit author decision before release.

## VBL-003 — Byte-preserving transformations

For an explicitly proposed transformation, preserve the original, create a separate derivative, and enumerate the allowed byte changes. Verify that every byte outside the declared change is identical. A visual/textual match is not a substitute for byte comparison. Round-trip success proves only that measured transformation.

## VBL-004 — Terms and scope review

Check that the declared grant, reserved rights, conditions, registers, cure, termination, warranty disclaimer, and ethics clause are all present in the reviewed artifact. Record conflicts and open interpretation questions; do not make a legal conclusion using string tests. In particular, qualified counsel should review repository-wide scope, third-party rights, automated termination, cure/remedy wording, permissions override, liability disclaimer, and jurisdiction-specific effects.

## VBL-005 — Unicode integrity

Decode and encode strictly as UTF-8; record the relevant code points for `Č Š Ž Đ č š ž đ` and VBL marks such as `⊨ ⊢ ⚠ × ∴`. Flag replacement characters and any lossy normalization. This is an encoding check, not proof that all intended glyphs render correctly in every browser/font/audio path.

## VBL-006 — Registers and correction history

Verify that `REGISTER-NEIMENOVANIH.jsonl` and `REGISTER-PADCEV.jsonl` exist and their schema is available. Empty registers mean no rows were supplied in that snapshot; they do not prove that no incidents or contributors exist. Corrections must append a new record linked to the earlier record with the reason, changed fields, and evidence reference. Lawful deletion/redaction must preserve only the minimum permitted audit metadata and must not retain data that law requires to be deleted.

## VBL-007 — Independent verification

The author or implementer may provide a first-party check but cannot label that same check `INDEPENDENT`. A separate reviewer must be identifiable, competent for the scope, state conflicts, list procedures and evidence, and preserve the result. Until that happens, the release gate remains `UNVERIFIED / NOT RELEASED`.

## Release gates (not interchangeable)

| Gate | Required evidence | Current status |
|---|---|---|
| Source bytes preserved | SHA-256 and byte count match known local source metadata | `PASS_LOCAL` |
| Version boundary | Frame, licence, protocol and branch labels separated | `PASS_LOCAL_PROPOSAL` |
| Derivative integrity | Only the declared first framing line differs | `PASS_LOCAL` |
| Canonical provenance | Verifiable upstream commit/tag/release or signed publication record | `UNVERIFIED` |
| Content/legal review | Scope-specific review by qualified reviewer/counsel | `NOT_PERFORMED` |
| Independent review | Distinct reviewer and recorded method/result | `NOT_PERFORMED` |
| Remote implementation | Verified branch, commit, and PR URLs/results | `NOT_CREATED` |
| Production behavior | Test evidence from named deployed version and scoped cases | `NOT_PERFORMED` |

## Run the local check

```sh
python verify_protocol_preflight.py
python -m unittest discover -s tests -v
```

Do not call this protocol a guarantee of legal validity or ethical compliance. It defines evidence gates that may reveal whether the required proof exists. The protocol itself is also subject to review under the same rules.
