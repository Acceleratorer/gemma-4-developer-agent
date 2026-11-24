# Public candidate audit — 2026-11-24

## Summary

Kaggle CLI's latest-run listing surfaced five recently updated notebooks worth checking. Their current revisions do not supply a stronger competition-tested candidate, so keep the existing seeded V5/Patchsmith comparison plan. Pulled copies are under ignored `data/local/research/recent-public-agents/`; notebook code was inspected as text and not executed.

## Flexonafft short-prompt bundle

Notebook: [Gemma 4 | Budget-Aware Short-Prompt](https://www.kaggle.com/code/flexonafft/gemma-4-budget-aware-short-prompt), last run 2026-11-24 06:46 UTC, 68 votes.

Its own opening cell calls the bundle a combination of a reported 0.22 prompt, 40 calls, 4,096 thinking tokens, issue pinning, fast exit, and a five-minute cap. The logged execution only validates and packages four configuration files; it explicitly says a global runtime and leaderboard score require competition evaluation. Kaggle `kernels status` is `COMPLETE`, but the notebook output contains no agent inference or score. Since the changes are bundled and the current revision is unscored, neither its title nor vote count establishes an improvement.

## Arsen evidence audit

Notebook: [Gemma 4 Agent | Completeness Checks and Paired Validation](https://www.kaggle.com/code/arsen123/gemma-4-reproducible-bundles-and-evidence-audit), last run 2026-11-24 08:58 UTC, 5 votes.

The notebook reports an unchanged Idris v31 submission at 0.18 public. Its candidate combines the v30 multi-file completeness prompt with v31's generation budget and has no official score. The reported local comparison is 24/50 versus 22/50, with exact McNemar `p=0.75390625` and a repository-cluster bootstrap 95% interval of `[-0.082, 0.163]`; it is compatible with no gain. The 50-pair data came from a prior A100 run at concurrency 5 per arm, and the revision explicitly says it did not perform new model inference. This is useful methodology and negative evidence, not a candidate to promote over the current V5/Patchsmith plan.

## Ziad Samer's skill-arm run

Notebook: [Fork of generation - all shards - GPU](https://www.kaggle.com/code/ziadsamer/fork-of-generation-all-shards-gpu), last run at 2026-11-24 15:49 UTC and `COMPLETE` when checked at 16:36 UTC. Its output log reports eight runs across four tasks: `sk_a2` resolved 1/4, and `sk_a2p2g2` resolved 2/4. Both arms passed `rich_3278`; only `sk_a2p2g2` passed `rich_3521`; both failed to resolve `fastapi_14419` and `fastapi_15589`. On the same four IDs, our local V5 44-task result resolved `fastapi_14419`, `rich_3278`, and `rich_3521` (3/4). This is descriptive rather than a matched-seed comparison, but neither skill arm adds a pass over the recorded V5 outcomes. The arms share a `skills/agent` tool and helper script; `sk_a2p2g2` also changes the system prompt and helper implementation, so the one-pass difference cannot be attributed to a single change. The run used concurrency 2, unlike the competition scorer's concurrency 1. All four task IDs are in our 53-task training set, and none is in the frozen 18-task holdout. This is a small, overlapping local experiment, not a competition score; do not add it to the first quota wave.

## Dheeraj Piduru's E4B and 31B progress report

Notebook: [Gemma 4 E4B: what moved the score and what didn't](https://www.kaggle.com/code/dheerajpiduru/gemma-4-e4b-what-moved-the-score-and-what-didn-t), last run 2026-11-24 16:45 UTC, 6 votes. The notebook is a markdown-only write-up and publishes no agent bundle to reproduce.

The author reports 31B public scores of 0.20 and 0.17 from unchanged v8 files, and 11/115 versus 10/115 resolved tasks for 4,096 versus 1,024 thinking tokens on E4B. These are the author's results, not our matched comparison; they reinforce run-to-run noise and do not justify changing our model or thinking budget. In 50 selected solved 31B runs, the author counted 64 failed `edit_file` calls among 123 attempts and reported recovery afterward. This suggests a possible edit-retry prompt ablation, but the selected solved-run sample and lack of our own tool-call traces make it a hypothesis only. The two completed LoRA adapters reduced held-out resolution and often exhausted the call budget, so this report adds no reason to revisit LoRA before the planned base-model comparisons.

## Evgen Dvorkin's Patchsmith P3 report

Notebook: [Can Gemma 4 Become a Software Engineer?](https://www.kaggle.com/code/evgendvorkin/can-gemma-4-become-a-software-engineer), latest run 2026-11-24 17:50 UTC, `COMPLETE`. The latest notebook has one unexecuted code cell; Kaggle's downloaded output is a package-only `submission.zip`, not an agent evaluation. Its SHA-256 is `6c4f1c8a581c3e1a8e97a3f37015aa7e3e08c03cadf12b697cf4bfc4ab9a35d9`; the ZIP includes the Apache-2.0 license and notice, preserves five Patchsmith exp021 files, and changes only `prompts/system.md` (prompt SHA-256 `5bd031fb882bd84c68fe43d3163a4fc4e2c4b80ba063b82e609afd721b32a5d7`).

The author reports P3 at 1/2 PASS on `rich_4076` and `rich_3894`, the same pass count as P2, with 33 versus 40 calls across those two individual runs. The sample is too small and order differs, so it does not establish a gain; the candidate has no matched public score. Its `rich_4076` trace is more useful than the score: the prompt searched newline-related words, then patched Markdown `rstrip()` logic, while the verifier checked the separate `Text.from_ansi()` contract. P3's proposed P4—tie a terse issue to its concrete API and regression test before editing—is untested. Both `rich_4076` and the `rich_3894` control are in our 53-task training set. Defer an original, prompt-only P4 screen on this pair until after the V5/Patchsmith 53-task comparison and unseen holdout; do not add a full 53-task P4 run unless the screen improves over the seeded V5 outcomes and quota plus the final-submission buffer allow it.

## Decision

Do not add these public bundles or unverified prompt hypotheses to the first post-reset GPU wave. The Flexonafft notebook does not measure its bundle, the Arsen prompt hybrid lacks a significant paired gain, the Ziad Samer run is too small and overlapping to support promotion, and the Dheeraj and Dvorkin write-ups do not establish a stronger candidate. Preserve the planned one-task validation-contract screen, then compare the seeded V5 and source-faithful Patchsmith candidates on the same 53 tasks and unseen 18-task holdout. Keep all outside notebook source and data out of the public repository.
