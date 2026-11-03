# Intake record — VBL conversation attachments, 2026-10-27

**State:** received-text evidence only; not canonical license bytes, not a source-code review, not independent verification.

The three attachments are distinct byte sequences. Their hashes identify these attachment files only; they do not identify the VBL source, prove authorship, or prove the embedded claims.

| Attachment role | Bytes | SHA-256 | Classification and limit |
|---|---:|---|---|
| VBL review/composite excerpt | 9,801 | `B0FFCE79DFC80815CE2D0704087DCE9D07A798A32B6E24C6F5FDB09D17882013` | Contains review commentary mixed with a license excerpt that visibly stops at `wa`; not a clean canonical license copy. |
| User correction/request plus composite | 11,186 | `EAFF4C30A6ACE25E44CCC36149151AC8BB18E95205A7827316C44449110780D9` | Begins with “ni isti / isti ne obstaja / daj globje in boljše / računaj z nami”; it is not byte-identical to the first attachment. |
| PowerShell transcript in Atmavictu worktree | 11,974 | `151C444C104AB1CCB874CAA80BEA3737A2A10AA551F8CD53436E83D97E992473` | Shows `PS>` followed by `>>` continuation prompts and a parser error on the Unicode multiplication sign. This supports a shell-input diagnosis; it does not establish an Atmavictu application defect. No application source was changed. |

## Findings

1. **Byte identity:** all three attachment SHA-256 values differ, so these exact attachment files are not byte-identical.
2. **Semantic sameness:** not established by the hashes. The second file adds an explicit request; the third adds a terminal transcript. Their contents and purposes differ.
3. **License identity:** none of these three hashes is a verified hash of the canonical VBL license. The first is visibly composite and truncated.
4. **Terminal failure:** `>>` is PowerShell's continuation prompt. Pasting prose while the parser is waiting causes it to parse symbols such as `×` as code. Based on the supplied transcript, this is a shell-input failure, not evidence that Atmavictu code failed.

## Safe next step for the terminal

At the live `>>` prompt, press `Ctrl+C`; confirm `PS>` returns. Then run only an intended command, such as `Get-Location`. Do not paste the VBL document into the terminal. No repository modification is warranted from this transcript alone.

## Protocol decision

Use separate labels for `BYTE_IDENTICAL`, `NORMALIZED_TEXT_EQUAL`, `SEMANTICALLY_EQUIVALENT`, and `SAME_PROVENANCE`. Never collapse them into an unqualified “same.” Preserve composite inputs and label any extracted segment `DERIVED_EXCERPT` with source hash, boundaries, and extraction method.
