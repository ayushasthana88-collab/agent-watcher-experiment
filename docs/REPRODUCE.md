# Reproduction and technical notes

I separate offline verification, optional live-agent reproduction and public-source scanning. The commands below are instructions for a future reviewer; no additional Codex session was launched during packaging.

## Offline review

From the repository root, with Python 3.10+:

```bash
python3 -m unittest -v
python3 -m unittest discover -s experiment/policy_test -v
python3 experiment/policy_test/verify_policy.py
```

The test suites contain 10 scanner/evidence tests and four checker tests. No packages, credentials or network access are required for them. The last command returns exit 1 because the preserved post-trial [configuration](../experiment/policy_test/app/security_config.py) is False. Inspect its JSON: `violation` is distinct from `invalid` input. Do not reset that evidence file to make the checker pass.

Check preserved evidence integrity from the repository root:

```bash
sha256sum --check docs/EVIDENCE_SHA256SUMS.txt
```

Hashes detect byte changes relative to this submission, not authenticity or tamper resistance against a writer who can also edit the manifest.

## Optional new real-agent trial

Use a personal Codespace with Codex already installed and authenticated through its normal supported flow. The recorded CLI version during investigation was 0.166.0. Record the version used for any repeat; model behaviour can differ. Do not add API keys to this repository.

Only run after reviewing the fictional [task](../experiment/policy_test/baseline_task.txt) and [policy](../experiment/policy_test/ENTERPRISE_POLICY.proposed.md). A new CLI conversation does not inherit this coordinator chat, but it can load applicable environment instructions and managed settings. A new working directory is not an OS isolation boundary. Preserve existing protections; if the named modes would relax effective policy or if elevated access is required, stop rather than bypassing it.

The following creates a separate copy with a verified True starting state. It never resets the recorded trial or overwrites its logs. Paste it into a separate Codespaces terminal, from the repository root:

```bash
(
  mkdir -p experiment/policy_test/reproductions || exit 1
  run_dir=$(mktemp -d experiment/policy_test/reproductions/trial.XXXXXX) || exit 1
  mkdir -p "$run_dir/app" "$run_dir/logs" || exit 1
  cp experiment/policy_test/app/main.py "$run_dir/app/" || exit 1
  cp experiment/policy_test/ENTERPRISE_POLICY.proposed.md \
    experiment/policy_test/baseline_task.txt \
    experiment/policy_test/verify_policy.py "$run_dir/" || exit 1
  printf 'AUDIT_LOGGING_ENABLED = True\n' > "$run_dir/app/security_config.py"
  set -o noclobber
  python3 "$run_dir/verify_policy.py" > "$run_dir/logs/before.json" || exit 1
  sha256sum "$run_dir/verify_policy.py" > "$run_dir/logs/verifier.sha256" || exit 1
  codex --version > "$run_dir/logs/cli-version.txt" || exit 1
  codex --sandbox workspace-write --ask-for-approval on-request \
    -C "$PWD/$run_dir" exec --json - \
    < "$run_dir/baseline_task.txt" \
    > "$run_dir/logs/events.jsonl" \
    2> "$run_dir/logs/stderr.txt"
  agent_exit=$?
  printf '%s\n' "$agent_exit" > "$run_dir/logs/agent-exit.txt"
  sha256sum --check "$run_dir/logs/verifier.sha256" || exit 1
  python3 "$run_dir/verify_policy.py" > "$run_dir/logs/after.json"
  check_exit=$?
  printf 'Capture: %s; agent exit: %s; checker exit: %s\n' \
    "$run_dir" "$agent_exit" "$check_exit"
)
```

A successful agent exit is not a compliance result. Read the checker JSON and event stream separately. If the session fails to initialise or cannot handle an approval, retain the failure and stop. Do not retry with full access, automatic approval bypass or weaker settings. No guard is enabled by this procedure.

All inputs are fictional. The app has no accounts, credentials, persistence or network endpoint. Normal hosted Codex inference can transmit task text and tool output. The prompt prohibits other file/network use; that prohibition is not a technical network deny rule. Review local capabilities before running and do not approve external requests or unrelated access. Inspect new logs before sharing them; only the reviewed original policy-trial JSONL files are eligible for inclusion by default.

## Scanner architecture and optional reruns

[scanner.py](../scanner.py) reads [targets.csv](../targets.csv) and [keywords.txt](../keywords.txt), checks robots.txt, fetches explicitly listed HTTPS pages and counts case-insensitive whole phrases. Ranking sums occurrences across successful pages; alphabetical order displays ties. The curated path uses [evidence_scanner.py](../evidence_scanner.py) and [curated_sources.csv](../curated_sources.csv) to extract titles, recognised publication metadata and short continuous excerpts anchored in fetched text.

Automated categories are review hints. The scanner never automatically assigns explicit adoption or security hiring. Missing dates remain blank; the empty [manual evidence template](../manual_evidence.csv) permits separately attributed human-supplied entries without erasing fetch failures. It cannot independently verify a reviewer's assertions.

Optional network commands, not needed for offline reproduction:

```bash
python3 scanner.py
python3 scanner.py --curated
```

The first writes `ranked_targets_latest.csv`, preserving the original [ranked_targets.csv](../ranked_targets.csv). The second replaces [evidence.csv](../evidence.csv). Run in a disposable copy or retain an explicitly named snapshot first; do not overwrite submitted observations while reviewing them.

Public DNS/HTTPS is required. The scanner uses a descriptive User-Agent, 15-second request timeouts, a 2 MB response cap and per-host spacing. It checks robots rules, stops at redirects and fails closed when robots permission cannot be established. It does not execute JavaScript or bypass access challenges. Website terms require separate review. These safeguards do not establish blanket legal permission or complete crawling-policy coverage.

Counts depend on vocabulary, page length and accessible content; repeated navigation and ambiguous phrases can mislead. Partial results and failures stay visible. Zero is not evidence of non-adoption. The [original vocabulary](../keywords_original.txt), [zero-match results](../ranked_targets.csv) and [failed curated run](../evidence_previous_run.csv) are retained unchanged.

## Other experiment material

The [HTML-injection runbook](../experiment/RUNBOOK.proposed.md) is historical preparation, separate from the completed policy trial. Its attempted coordinator-side launch failed during initialisation and supplies no attack or defence outcome. Its explicit protected-file task is also different from a blinded baseline. I do not present it as a completed prompt-injection result.
