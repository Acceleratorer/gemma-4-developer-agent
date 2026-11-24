# Public candidate audit — 2026-11-24

## Summary

Kaggle CLI's latest-run listing surfaced six recently updated notebooks worth checking. Their current revisions do not supply a stronger competition-tested candidate, so keep the existing seeded V5/Patchsmith comparison plan. The first five pulled copies are under ignored `data/local/research/recent-public-agents/`; the later Mr Liang notebook is under `data/local/research/public-recheck-20261124/jnliang-envfix/`. Notebook code was inspected as text and not executed.

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

## Mr Liang's environment-fix bundle

Notebook: [Gemma4 Envfix 020x3](https://www.kaggle.com/code/jnliang/gemma4-envfix-020x3), last run 2026-11-24 19:53 UTC. Its current kernel status is `ERROR`. The metadata uses CPU only, has no model input, and attaches `muhammedidris28/locbench-129`. The log reports a dependency census, then fails in a later cell with `FileNotFoundError: scored_manifest.json`; that run did not evaluate an agent.

The notebook reports 0.20 on submissions `58485496`, `58531526`, and `58642247`, and embeds eight files labeled as the `58642247` bundle. That bundle adds an `envfix` skill whose script installs stand-ins for `inline_snapshot` and `dirty_equals` into the Python environment. The notebook attributes the stand-in semantics to LocBench-129 (Apache-2.0), but the eight embedded submission files contain no `LICENSE` or `NOTICE`; neither the Kaggle leaderboard nor this failed notebook run independently maps the source to a score-bearing archive hash. Treat the 0.20 results and exact bundle link as the author's report.

This is an evaluation hypothesis, not a promotion. Our current 53-task set is gold-patch-qualified without environment shims, and Kaggle staff said the held-out competition tasks pass with their reference patches ([discussion](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/747248)). That makes transfer from the reported public-training dependency census to the private test uncertain; the stand-ins could also give incomplete test feedback. Keep it out of the first GPU wave. Revisit only if the V5/Patchsmith comparisons leave quota for a small, gold-verified screen.

## Latest-run candidate screen — checked 2026-11-24 21:21 UTC

A fresh Kaggle CLI listing surfaced several recently run notebooks; none warrants priority over the staged V5/Patchsmith comparison and unseen holdout:

- [The 0.24 config is below median](https://www.kaggle.com/code/coltondowning/the-0-24-config-is-below-median) reanalyzes Idris's local run dataset and reports v24 at 23/66, with six configurations higher. It does not verify a source-to-submission mapping for the 0.24 public score, so this is selection-noise evidence rather than a new candidate.
- [Same Bytes, Two Scores](https://www.kaggle.com/code/lucifer19/same-bytes-two-scores-gemma-4-agent-lab) reports `model_inference_ran=false` and zero new paired agent runs; its 40-call combo-prompt remains untested.
- [EC RAG Train A](https://www.kaggle.com/code/atunx375/ec-rag-train-a) is a Qwen3-VL video QA/caption workflow, not a coding-agent experiment.
- [Gemma4 Agent Eval](https://www.kaggle.com/code/xbzouzx/gemma4-agent-eval) reports 7/30 for an E4B dual-agent setup. It resolves 3/21 tasks overlapping our qualified 53-task set and 3/18 overlapping V5's prior 44-task run, with no E4B-only pass. This is unpaired and changes model, call cap, and time cap, so it is not causal evidence or a main-track promotion.

Keep the seed-42 V5/Patchsmith core comparison and paired holdout at the top of the reset-week sequence. The E4B result is outside the 31B main-track candidate decision.

## Evgen Dvorkin's six-agent `rich_4076` follow-up

Notebook: [Gemma 4 | rich_4076: 20/24 — Six Failed Agents](https://www.kaggle.com/code/evgendvorkin/gemma-4-rich-4076-20-24-six-failed-agents), latest run 2026-11-24 21:08:11 UTC, `COMPLETE`. The saved run verifies the P7 package (8/8 files) and records a `rich_4076` result of 20/24 tests with `resolved=false`; it does not run new agent inference. The notebook's six GPU runs all report 20/24 and `resolved=false`. P7 proposes an AST scout and skill checker, but its trace makes zero scout calls. P8 is a future tool-control proposal; the notebook reports synthetic CPU checks, not a Gemma evaluation. This follow-up provides no pass gain or reason to promote either candidate ahead of the seeded V5/Patchsmith core and holdout.

## Decision

Do not add these public bundles or unverified prompt hypotheses to the first post-reset GPU wave. The Flexonafft notebook does not measure its bundle, the Arsen prompt hybrid lacks a significant paired gain, the Ziad Samer run is too small and overlapping to support promotion, and the Dheeraj, Dvorkin, and Mr Liang reports do not establish a stronger private-test candidate. Preserve the planned one-task validation-contract screen, then compare the seeded V5 and source-faithful Patchsmith candidates on the same 53 tasks and unseen 18-task holdout. Keep all outside notebook source and data out of the public repository.
