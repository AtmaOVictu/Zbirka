# Remote VBL pull-request audit — 2026-10-25

## Scope and method

This is a read-only inspection of the three existing GitHub pull requests and their current metadata/patches. It does not change, approve, merge, or close any remote item. The remote source repository `AtmaOVictu/Atmavictu` could not be retrieved through the connected GitHub action during this pass (404), so source lineage against its current `LICENSE.md` is not independently re-established here.

## Remote state observed

| Repository | PR | State | Head branch | Base | Files changed | Additions / deletions |
|---|---|---|---|---|---:|---:|
| `AtmaOVictu/cookbook` | [#1](https://github.com/AtmaOVictu/cookbook/pull/1) | Open, not merged, reported mergeable | `zrcalo/vbl-razdelitev-2026-10-25` | `main` | 10 | +443 / 0 |
| `AtmaOVictu/Slovenian-Language-Technologies-Overview` | [#1](https://github.com/AtmaOVictu/Slovenian-Language-Technologies-Overview/pull/1) | Open, not merged, reported mergeable | `zrcalo/vbl-oznacene-crke-2026-10-25` | `main` | 2 | +25 / 0 |
| `AtmaOVictu/agents-cli` | [#1](https://github.com/AtmaOVictu/agents-cli/pull/1) | Open, not merged, reported mergeable | `zrcalo/vbl-skill-2026-10-25` | `main` | 1 | +33 / 0 |

“Mergeable” is GitHub's merge-conflict assessment, not a quality, provenance, legal, or ethical approval.

## Findings — do not treat these PRs as release-ready yet

1. **Checksum manifest in the cookbook PR contains `UNVERIFIED` placeholders.** The PR patch for `vbl/SHA256SUMS.txt` labels all nine listed files `UNVERIFIED`; this is not a valid completed SHA-256 manifest. The local staging package has a later manifest with computed hashes, but those local bytes are not the remote PR bytes. Do not claim the remote PR's checksum validation passes.
2. **The source-of-truth repository is unavailable in this audit pass.** The cookbook PR cites `AtmaOVictu/Atmavictu → LICENSE.md @main`, VBL 10.3.1, blob and commit identifiers. The source fetch returned 404 from the connector. Treat the citation as a claim in the PR description, not independently reverified evidence in this pass.
3. **Version lines differ.** The remote PRs are built around VBL 10.3.1, while the local §−1 absolute-equivalence candidate is a distinct unreleased 10.5.2 draft derived from a preserved local 10.5.1 draft. Do not silently replace the 10.3.1 snapshot with 10.5.2 or label either as canonical without source-lineage and rights-holder review.
4. **Language and technical content need author review.** The Unicode PR includes several visibly awkward/possibly corrupted phrases (for example, “zdravilo jeze isto pot”); the agent skill includes “gluba.” These should be checked against intended source text, not silently normalized by a contributor.
5. **The two registers are templates, not evidence.** Their records have `status: TEMPLATE`, null evidence and placeholder values. This is acceptable only if every reader sees them as templates; they must not be counted as incident or contributor evidence.
6. **No independent review is recorded in PR metadata.** No requested reviewers were returned by the PR metadata. A mergeable status is not a substitute for a second-person verification pass.
7. **No merge or release has been performed by this audit.** All three PRs remain open and unmerged according to the observed metadata.

## Recommended next actions

- Preserve all three existing PRs; do not merge them solely because they are mergeable.
- Re-fetch the source `LICENSE.md` through an authorized path and independently verify the cited commit, blob, version, date, and exact copied bytes.
- Replace the remote `UNVERIFIED` checksum placeholders with computed SHA-256 values for the exact branch contents; regenerate the manifest after the final edits.
- Review Unicode/source-language passages against the cited source and add focused tests for each repaired encoding/content invariant.
- Keep VBL 2.6, 10.3.1, and the unreleased 10.5.x drafts clearly separate in paths and release records.
- Review the §−1 draft independently and obtain explicit rights-holder approval for its exact digest before presenting it as a canonical license revision.
- Only after these gates pass, update the appropriate PR branch and verify the resulting commit and CI checks. Do not merge on the author's behalf unless separately and explicitly requested after review.

## Local verification, separate from remote review

The local staging package's distribution verifier and three local test suites passed during this pass. Those results validate only the current local package, not the contents of the remote branches or legal enforceability.
