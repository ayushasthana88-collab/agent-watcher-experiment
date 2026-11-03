# Validation record

I used offline checks to validate the submission without launching another coding agent, rerunning the scanner or changing application/security settings. OpenAI Codex executed these checks during preparation.

| Check | Result | Scope |
| --- | --- | --- |
| `python3 -m unittest -v` | PASS: 10 tests | Scanner counting, robots handling, extraction and manual attribution |
| `python3 -m unittest discover -s experiment/policy_test -v` | PASS: 4 tests | Literal policy-state verification and rejection of invalid/executable input |
| Current configuration check | Expected violation, exit 1 | False remains preserved; [review-time output](../experiment/policy_test/checks/review_policy_check.json) |
| Original evidence checksums | PASS: 11 manifest entries | [Manifest](EVIDENCE_SHA256SUMS.txt); original raw evidence unchanged |
| Internal Markdown targets | PASS: 52 relative links across 8 public-candidate Markdown files | Targets exist and are not excluded from explicit inclusion |
| Documented shell commands | PASS: 6 shell blocks | Checked with `bash -n`; no live agent or scanner execution |
| Credential-pattern review | No content findings detected | Working-tree text and reachable tracked blobs; not an exhaustive secret audit |
| Source-page verification | Three supplied pages accessible | Public-source review only; no prospecting CSV was regenerated |

Evidence consistency checks also confirmed the nine run-two JSONL events, the recorded True starting value, the completed file update and the current False setting. The first policy log contains no file-change event. The reproduction seed was checked in memory as compliant; live reproduction was not attempted.

A policy-check exit 1 is the expected observation for the retained post-trial fixture. It is not counted as an automated-test failure. The recorded trial's process exit 0 remains operator-reported because its exit file was not retained.

No original report of effective sandbox settings, model identity or full OS activity can be reconstructed from the JSONL. These gaps remain documented in the [results report](../experiment/policy_test/RESULTS.md).
