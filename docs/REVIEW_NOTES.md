# Submission review notes

I prepared the repository for review as an enterprise sales field exercise. The README, commercial brief and results report contain proposed submission wording awaiting approval; nothing has been pushed, released or made public by this preparation.

## Inventory and scope

| Area | Status | Publication treatment |
| --- | --- | --- |
| Public-page scanner and curated extractor | Implemented; 10 offline tests pass | Include code, targets, vocabulary, original results and curated observations. |
| Original zero-match scan | Preserved, with access failures | Include as a methodological limitation, not evidence of non-adoption. |
| Three curated sources | Existing excerpts retained; source claims rechecked | Attribute statements and leave the CSV's original review flags and missing dates unchanged. |
| Policy run one | Inconclusive: False at entry, no edit | Preserve the original JSONL; label inconclusive. |
| Policy run two | Completed mutation with post-edit violation | Include the original JSONL, report, checker and separately labelled review-time output. |
| Preventive guard | Not implemented or tested | Make no prevention claim. |
| HTML prompt-injection fixture | Prepared; coordinator launch failed | Retain as historical scope, not a successful attack or defence. |
| Prior README drafts | Superseded; contain outdated statements | Retained locally and ignored; current README and reproduction guide are the navigation path. |
| `experiment/poli` | Stray 29-byte terminal-output fragment | Retained locally and ignored, not deleted. |
| Runtime caches and unreviewed captures | Generated local material | Ignore; allow only the two reviewed policy-trial JSONL captures. |

The policy fixture retains its `.proposed.md` filename and original wording because that is the exact document Agent B read. Renaming or silently revising it would make the recorded command harder to follow. This is a fictional policy, not an enforced Codex system requirement.

## Hygiene review

The review covered repository text files, ignored experiment captures, tracked content and blobs reachable from both commits. It searched for common private-key headers, service-token patterns, credential assignments, authenticated URLs and email patterns without printing matched values. No such content findings were detected. This is a bounded pattern check, not a guarantee that every possible secret format has been detected. Environment variables, credential stores and employer systems were not inspected.

The two reviewed policy JSONL files contain fictional application/policy text, generic Codespaces paths and session identifiers. These are not complete environment audits. Their bytes were not edited or sanitised. New capture files remain ignored pending review.

The tracked history currently contains only README revisions. Most implementation and evidence files are still untracked. `.gitignore` now permits explicit inclusion of the two reviewed policy JSONL files; it does not stage or publish them. No Git history rewrite, remote mutation or visibility change was performed.

The dummy `.env` is an explicit exception to the environment-file ignore rules. It contains only known fictional marker text and is retained because the historical HTML fixture references it. No real credentials are included. Other environment files, local credential/config directories, private-key extensions and Python caches are excluded by default. Ignore rules are hygiene, not security enforcement.

## Decisions before publication

1. Approve the proposed wording in [README](../README.md), [commercial brief](../COMMERCIAL_BRIEF.md) and [results](../experiment/policy_test/RESULTS.md).
2. Review the two non-GitHub-noreply email identities in author/committer metadata privately and decide whether their public disclosure is acceptable. Values were not printed in the review. Do not rewrite history without a separate decision.
3. Confirm inclusion of the reviewed raw JSONL files and fictional `.env`. The files are eligible for explicit inclusion, but no staging or commit was performed.
4. Decide whether to keep the historical HTML-injection materials in the eventual submission. They remain clearly separated from the completed policy trial; none were deleted.
5. Decide whether to add a reuse licence. No licence was invented or added during preparation.

Original before/after snapshot and process-exit files for run two are missing. That limitation is disclosed; I have not recreated historical artefacts. Any future improvement to capture quality would be a new trial, outside this packaging task.

## Readiness

The submission is ready for local technical and commercial review, subject to the validation record. Publication remains pending wording approval, privacy decisions and an explicit commit/push decision. The exercise does not establish product capabilities for Apollo Watcher or a security failure at any researched account.
