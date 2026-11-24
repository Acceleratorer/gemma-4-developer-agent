# Public candidate audit — 2026-11-24

## Summary

Kaggle CLI's latest-run listing surfaced three newly updated notebooks worth checking. Their current revisions do not supply a stronger competition-tested candidate, so keep the existing seeded V5/Patchsmith comparison plan. Pulled copies are under ignored `data/local/research/recent-public-agents/`; notebook code was inspected as text and not executed.

## Flexonafft short-prompt bundle

Notebook: [Gemma 4 | Budget-Aware Short-Prompt](https://www.kaggle.com/code/flexonafft/gemma-4-budget-aware-short-prompt), last run 2026-11-24 06:46 UTC, 68 votes.

Its own opening cell calls the bundle a combination of a reported 0.22 prompt, 40 calls, 4,096 thinking tokens, issue pinning, fast exit, and a five-minute cap. The logged execution only validates and packages four configuration files; it explicitly says a global runtime and leaderboard score require competition evaluation. Kaggle `kernels status` is `COMPLETE`, but the notebook output contains no agent inference or score. Since the changes are bundled and the current revision is unscored, neither its title nor vote count establishes an improvement.

## Arsen evidence audit

Notebook: [Gemma 4 Agent | Completeness Checks and Paired Validation](https://www.kaggle.com/code/arsen123/gemma-4-reproducible-bundles-and-evidence-audit), last run 2026-11-24 08:58 UTC, 5 votes.

The notebook reports an unchanged Idris v31 submission at 0.18 public. Its candidate combines the v30 multi-file completeness prompt with v31's generation budget and has no official score. The reported local comparison is 24/50 versus 22/50, with exact McNemar `p=0.75390625` and a repository-cluster bootstrap 95% interval of `[-0.082, 0.163]`; it is compatible with no gain. The 50-pair data came from a prior A100 run at concurrency 5 per arm, and the revision explicitly says it did not perform new model inference. This is useful methodology and negative evidence, not a candidate to promote over the current V5/Patchsmith plan.

## Ziad Samer's skill-arm run

Notebook: [Fork of generation - all shards - GPU](https://www.kaggle.com/code/ziadsamer/fork-of-generation-all-shards-gpu), last run at 2026-11-24 15:49 UTC and `COMPLETE` when checked at 16:36 UTC. Its output log reports eight runs across four tasks: `sk_a2` resolved 1/4, and `sk_a2p2g2` resolved 2/4. Both arms passed `rich_3278`; only `sk_a2p2g2` passed `rich_3521`; both failed to resolve `fastapi_14419` and `fastapi_15589`. On the same four IDs, our local V5 44-task result resolved `fastapi_14419`, `rich_3278`, and `rich_3521` (3/4). This is descriptive rather than a matched-seed comparison, but neither skill arm adds a pass over the recorded V5 outcomes. The arms share a `skills/agent` tool and helper script; `sk_a2p2g2` also changes the system prompt and helper implementation, so the one-pass difference cannot be attributed to a single change. The run used concurrency 2, unlike the competition scorer's concurrency 1. All four task IDs are in our 53-task training set, and none is in the frozen 18-task holdout. This is a small, overlapping local experiment, not a competition score; do not add it to the first quota wave.

## Decision

Do not add these public bundles to the post-reset GPU queue. The Flexonafft notebook does not measure its bundle, the Arsen prompt hybrid lacks a significant paired gain, and the Ziad Samer run is too small and overlapping to support promotion. Preserve the planned one-task validation-contract screen, then compare the seeded V5 and source-faithful Patchsmith candidates on the same 53 tasks and unseen 18-task holdout. Keep all outside notebook source and data out of the public repository.
