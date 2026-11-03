# Separate technical debt: manifest version metadata

The currently observed `LICENSE-MANIFEST.json` on `main` says `0.1210 × 10⁴`. The current `scripts/manifest_gen.py` generator returns a top-level manifest version of `0.1100 × 10⁴`.

The `--check` function compares only `current.get("items")` with `fresh["items"]`. It does not compare the top-level `version`, `date`, `law`, or other metadata. Therefore this particular mismatch is not currently guarded by that check.

This issue is deliberately **not** included in the attribution correction proposal. It changes release metadata and verification logic and should receive its own finding, tests, and review. Do not silently change the generator in the attribution patch.

Suggested independent follow-up:

- Add a failing regression fixture proving that a manifest version differing from the generator's expected version is detected.
- Decide explicitly which component owns the canonical version value. Avoid reintroducing a separate hard-coded version in the generator if the release artefact is authoritative.
- Compare generated metadata and file items independently and report both classes of mismatch.
- Record the expected version in an explicit input or verified release record, not a guessed literal.
- Run the complete existing CI and update the manifest only through the established workflow.
