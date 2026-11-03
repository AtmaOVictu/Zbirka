# VBL — public distribution audit and unresolved evidence

**Audit date:** 2026-10-25  
**Status:** Public invitations verified in three relevant PR discussions · PRs open and unmerged · independent verification not evidenced by the inspected endpoints.

## 1. Verified public discussion links

The connected GitHub integration returned the following state at audit time. Each PR remained open and unmerged. Six public VBL-call comments were present, two per PR, followed by an additional comment per PR pointing to a central issue link that returned 404 through the current connected API.

### A. `AtmaOVictu/cookbook` — PR #1
URL: https://github.com/AtmaOVictu/cookbook/pull/1  
Title: `vbl/ — kanon-kopija VBL 10.3.1 + registri (§2/§5) + preverjevalni protokol`  
Observed state: open, unmerged; 10 files changed, +443 / −0.  
Changed files include a VBL README, repo map, checksum manifest, provenance note, copied license, history, verification checklist, and two JSONL register files.

VBL invitation comments:
- https://github.com/AtmaOVictu/cookbook/pull/1#issuecomment-6396919501
- https://github.com/AtmaOVictu/cookbook/pull/1#issuecomment-6396929843
- Later central-link comment: https://github.com/AtmaOVictu/cookbook/pull/1#issuecomment-6396965889

### B. `AtmaOVictu/Slovenian-Language-Technologies-Overview` — PR #1
URL: https://github.com/AtmaOVictu/Slovenian-Language-Technologies-Overview/pull/1  
Title: `VBL/ — označene črke (§12): prevoz ⊥ vsebina; U+FFFD = padec stroja`  
Observed state: open, unmerged; 2 files changed, +25 / −0. The transport note says individual file round-trip/hash measurements remain UNVERIFIED.

VBL invitation comments:
- https://github.com/AtmaOVictu/Slovenian-Language-Technologies-Overview/pull/1#issuecomment-6396920017
- https://github.com/AtmaOVictu/Slovenian-Language-Technologies-Overview/pull/1#issuecomment-6396929873
- Later central-link comment: https://github.com/AtmaOVictu/Slovenian-Language-Technologies-Overview/pull/1#issuecomment-6396965909

### C. `AtmaOVictu/agents-cli` — PR #1
URL: https://github.com/AtmaOVictu/agents-cli/pull/1  
Title: `skills/vbl-verification-before-assertion — agent protokol hiše VBL`  
Observed state: open, unmerged; 1 file changed, +33 / −0.

VBL invitation comments:
- https://github.com/AtmaOVictu/agents-cli/pull/1#issuecomment-6396920444
- https://github.com/AtmaOVictu/agents-cli/pull/1#issuecomment-6396929853
- Later central-link comment: https://github.com/AtmaOVictu/agents-cli/pull/1#issuecomment-6396965987

## 2. Correction to earlier delivery claims

Earlier conversation notes reported HTTP 403 on write attempts. A subsequent live read found the six public VBL-call comments above. Current evidence therefore supports that those comments are present and publicly linkable. The earlier 403 reports are preserved as historical reports, but their raw responses were not independently re-examined during this audit. Do not continue saying those six comments were never delivered.

Each PR also has a later comment that links to `https://github.com/AtmaOVictu/Atmavictu/issues/753`. That target returned HTTP 404 through the current connected GitHub API. The owner repository listing accessible in this connection did not include `AtmaOVictu/Atmavictu`. The reason is unresolved (wrong path, unavailable repository, or permission/access issue); do not treat issue #753 as a verified central ledger.

A new issue and a corrective follow-up comment were attempted during this audit. Both were rejected with HTTP 403 `Resource not accessible by integration`. Thus, no new central issue or corrective follow-up was created. The incorrect/failed central-link history is recorded here rather than concealed.

## 3. Independent review and CI state

The inspected PR endpoints reported no submitted PR reviews, no inline review threads, and no status checks for the inspected head commits. This means those endpoints did not evidence an independent review or CI success; it does not prove that no person reviewed the work somewhere else.

## 4. Provenance and license limitations

The cookbook provenance note identifies `AtmaOVictu/Atmavictu` and `LICENSE.md @main` as the purported source and records a VBL 10.3.1 blob/commit. However, current API calls to read repository metadata and `LICENSE.md` at that source path returned 404. Therefore this audit cannot independently verify the source file, live canonical version, source hash, ownership, or enforceability. A 404 alone does not establish whether the source is absent or merely inaccessible.

The copied license text itself names © 2026 Luka Pintarič and describes its scope and terms. This audit does not determine whether the author owns all included rights, whether the license is legally enforceable, or whether downstream recipients complied.

The Slovenian government’s official copyright guidance states that copyright does not protect ideas, principles, or discoveries, while qualifying expressed works of authorship may be protected: https://www.gov.si/teme/avtorska-in-sorodne-pravice/ . This supports distinguishing the particular VBL text from general principles, but it does not establish who owns every component of the VBL license or whether this specific license is enforceable.

## 5. Test claims

The counts `134/134` and `16/16` were mentioned in the conversation, but were not matched to raw output, exact commands, implementation revision, environment, or a reachable CI run in this audit. They remain `REPORTED / UNVERIFIED` here. A checksum manifest is not proof that the correct target bytes were recalculated, and hash agreement is not proof that content is true.

The cookbook checklist itself leaves independent reruns and some browser/transport measurements pending. The Slovenian language PR explicitly leaves per-file round-trip/hash measurements unverified.

## 6. Public reach and limits

These comments are visible at three project-relevant PR discussions. That does **not** prove delivery to every individual, to Penny or Alexei, to mailing lists, or to a general public outside those pages. No private contact list was inferred or used. Further distribution should use relevant public project channels or recipient details supplied and authorized by the user, with a delivery record for each target.

## 7. Review requested

Please review:
- canonical source, version lineage, and provenance for the license copy;
- legal scope and separation of protected expression from general ideas or methods;
- privacy, access controls, and append-only register handling;
- mapping of each proposed control to actual code and registries;
- exact test commands, raw results, commit, environment, and independent reproduction;
- adversarial cases listed in `04-ADVERSARIAL-TEST-PLAN.md`.

For every finding, cite exact path/commit, method, observed result, limitation, and a proposed correction. Mark a reviewer as independent only after identity, scope, evidence, and conflicts of interest are documented.

## Conclusion

The public invitation is present in three relevant PR discussions. All three PRs remain open and unmerged. The canonical source/license, independent test results, legal status, and broad reach remain unverified. A new central issue could not be created because the GitHub integration returned 403. These distinctions are part of the history and must remain visible.
