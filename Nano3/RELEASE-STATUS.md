# VBL implementation release status

**State: locally implemented and validated; remote integration blocked.**

## Verified locally

- Core unit suite: 48 tests passed.
- Prepared cookbook overlay suite: 45 tests passed.
- Prepared Slovenian-language/Unicode overlay suite: 5 tests passed.
- Manifest matches the byte-preserved user-provided source: 67,966 bytes; SHA-256 `67170a4ae79abf551c489a014a9175e8d0d51e9dedc5e13dc4904ab352e56e83`.
- Nine core-to-overlay file pairs match byte-for-byte; see `reports/overlay-integrity.json`.
- Apperception schema validates and recursively rejects person-level moral-worth / soul-verdict fields.
- Installer tests prove the overlay is additive and idempotent in temporary Git repositories, rejects `main`, refuses tracked-file modifications, and preflights collisions before writes.

The three test suites overlap; their counts are suite executions, not a claim of 98 unique tests.

## Not delivered remotely

The connected GitHub API returned HTTP 403 `Resource not accessible by integration` for branch creation in all three target repositories. No remote branch, commit, pull request, canonical-license modification, or merge was made. The local overlay installer was not run against actual repository clones because none are mounted in this workspace.

## Release gates still open

1. Apply the additive overlays on the named feature branches through an authorized Git checkout; review diffs and CI, then open pull requests.
2. Obtain independent human and legal review. Mechanical checks are not a legal opinion or proof of ethical correctness.
3. Verify canonical publication history and decide whether there is an evidenced lineage bridge between the supplied `0.1190 × 10⁴` source and the existing 10.x-era repository lineage. Do not merge the lineages by assumption.
4. The supplied source has no §0.26 body and its machine record states no qualifying binary body is present. Both remain visible as unresolved source facts.
5. Configure an authorized mail provider and confirmed recipient before enabling the source's automatic-email requirement. No email was sent.
6. Integrate and adversarially test the policy adapter in each actual runtime. Reading the license or loading an agent skill alone cannot force arbitrary machines to comply.
7. Configure signed release attestations / a trusted timestamp authority and independently preserve register checkpoints if stronger tamper evidence is required.

## Interpretation

`PASS` means only the listed mechanical checks passed. It does not prove source authenticity, authorship, legal authority, global runtime enforcement, or final permission. The apperception gate can refuse a degrading use or hold a dossier for review; even a complete dossier reaches `READY_FOR_HUMAN_AUTHORIZATION`, never automatic permission. The policy targets conduct and uses, not a person's worth or soul.
