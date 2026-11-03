# VBL attribution repair package — 2026-10-30

This package contains a repeatable local patch for the measured `AtmaOVictu/verification-before-assertion` checkout.

**It does not change GitHub `main`, push a branch, or open a pull request.** The connected GitHub integration rejected branch creation with HTTP 403 (`Resource not accessible by integration`). The package is therefore prepared for a local branch and review rather than claiming a remote write that did not happen.

## Apply in Windows PowerShell

1. Download/extract this package.
2. In PowerShell, run the script against a clean checkout whose HEAD is exactly `a6fba5af94110b2107531c6cbe141afb393d10f5`:

```powershell
python .\apply_repair.py --repo "C:\path\to\verification-before-assertion" --dry-run
python .\apply_repair.py --repo "C:\path\to\verification-before-assertion"
```

The second command creates local branch `repair/attribution-evidence-2026-10-30`, saves originals inside `.git/vbl-repair-backup-2026-10-30`, applies the patch and runs `scripts/manifest_gen.py --check`. It refuses to run if the checkout is dirty or on another base commit. It never pushes or merges.

If a working branch already exists and you have independently inspected it, `--no-branch` skips local branch creation; the exact base commit guard and clean-tree guard still apply.

## Prepare the SYMBOLON-KATHOLIKON mirror

The mirror was measured separately at `98322f993aff5d25a8d287cca091f2d76cb25155`. Its license body is byte-identical to VBL 0.1210, but its contributor register contains only NE-0001 through NE-0006, omitting the source repository's NE-0007 and later attribution distinctions. There is no `LICENSE-MANIFEST.json` at the measured mirror root; the script does not invent one.

After the source repair has been independently reviewed and committed in the `verification-before-assertion` checkout, run the mirror script first in dry-run mode:

```powershell
python .\apply_symbolon_repair.py --source-repo "C:\path\to\verification-before-assertion" --mirror-repo "C:\path\to\SYMBOLON-KATHOLIKON" --dry-run
python .\apply_symbolon_repair.py --source-repo "C:\path\to\verification-before-assertion" --mirror-repo "C:\path\to\SYMBOLON-KATHOLIKON"
```

It requires the source register to contain the corrected 13 consecutive IDs and the mirror checkout to be clean and exactly at its measured base. It creates local branch `repair/symbolon-credit-register-sync-2026-10-30`, backs up touched files inside `.git`, copies the 13-entry source register, appends a mirror-specific fall 35 and adds a review note. It does not change the license body, create a manifest, push or merge. Merge the source repair before (or in a coordinated transaction with) the mirror sync; do not let the mirror claim a correction that has not been accepted in the source repository.

## Proposed changes

- Correct SSKJ² attribution: institution, 12 edition authors, five terminological advisers, two technology-support roles, and 15 authors of the separately credited 2012 source dictionary are distinguished.
- Separate PoVeJMo project collaborators from public text submitters; correct the campaign's direction and copyright-submission condition.
- Separate GaMS3-12B research authors from people acknowledged for data collection/preparation.
- Correct Common Voice, Reddit and Stack Overflow records; leave individual payment as unverified unless evidence supports it.
- Preserve the reported Stack Overflow protest suspension without generalizing it to ordinary self-deletion.
- Append named fall 35; retain previous register history.
- Synchronize current live pointers to VBL 0.1210 × 10⁴ while leaving the license body and its historical lineage untouched.
- Make the manifest generator derive the version from `LICENSE.md` and verify version identity.
- Recalculate SHA-256 and byte sizes for the three files actually listed in the current license manifest. Do not silently add `REGISTER-IZKORISTENJA.jsonl` to formal license scope.

## Required review

The scripts' own checks are not independent verification. A second reviewer must re-fetch sources, inspect each exact diff and confirm the manifest boundary. CI must pass on both final proposed branches before merge. The mirror's only formal scope change is copying its existing contributor/fall registers; no new license scope is asserted.
