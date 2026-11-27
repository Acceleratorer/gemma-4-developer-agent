# Public kernel screen — 2026-11-27

The initial Kaggle CLI check was at 2026-11-26 17:31 UTC / 2026-11-27 00:31 Vietnam time. A follow-up at 18:17 UTC found one active public experiment, recorded below. Notebook source and outputs are preserved only under ignored `data/local/research/`; no public notebook was executed locally.

## Evgen Dvorkin — `rich_3894`

The latest listed run of [Gemma 4 | rich_3894: 41/42 → 42/42](https://www.kaggle.com/code/evgendvorkin/gemma-4-rich-3894-41-42-42-42) was `COMPLETE` at 2026-11-26 18:49:28 UTC. The notebook concerns one Rich issue, `rich_3894`; its 41/42 → 42/42 title is a test count for that issue, not 42 benchmark tasks or a leaderboard score. The notebook describes four skipped tests.

The latest run's log verifies 28 agent files, creates a ZIP with SHA-256 `63DA26AB6658E95E1D839565A05734E2979342B2E9C9CD891138096A6366181F`, and converts the notebook to HTML. It reports that P18 uses Luis Specian's MIT-licensed V24 repository-tools agent and preserves the P16 executable agent, prompts, sampling, and limits. The log has no Gemma inference, task-resolution summary, or Kaggle score. The 28-file V24/P18 bundle is distinct from the six-file `module/agents/idris-v24` candidate; do not treat the run as a comparison against that local candidate.

**Decision:** this is a source/package verification rerun on one task, not evidence of a new agent gain. It does not change the frozen seed-42 53-task V5/Patchsmith core or the paired 18-task holdout.

### Follow-up — checked 2026-11-26 21:32 UTC

The Kaggle CLI now lists the 18:49 UTC run as latest and reports `COMPLETE`. Its downloaded log shows 28 agent files verified, the same ZIP SHA-256 `63DA26AB6658E95E1D839565A05734E2979342B2E9C9CD891138096A6366181F`, and notebook-to-HTML conversion; it contains no Gemma inference, task-resolution summary, or competition score. The 42/42 figure remains a test count from the single-issue notebook, not an agent or leaderboard result. The refreshed source, log, and output archive are preserved under ignored `data/local/research/refresh-2026-11-26-2128utc/`.

## Engziadsamer — `arms-again`

At 2026-11-26 18:20 UTC, Kaggle still reported [arms-again](https://www.kaggle.com/code/engziadsamer/arms-again) as `RUNNING`. The pulled notebook metadata attaches the competition wheelhouse, `rodrigospalma/ood45-bugfix-split`, and Gemma 4 31B QAT v2; internet is disabled. This run uses a custom `skill_arms` evaluation mode and task set, so it is not directly comparable to our fixed 53-task run.

The Kaggle logs endpoint returned no text at 18:17 UTC and the output fetch exposed no files at 18:20 UTC. At that check, `RUNNING` confirmed an active kernel only; it did not confirm completed inference, resolved tasks, or a competition score.

### Outcome — checked 2026-11-26 19:48 UTC

Kaggle later reported the kernel `COMPLETE`. Its downloaded log and outputs are under ignored `data/local/research/arms-again-complete-output-2026-11-26-1945utc/`. The run loaded Gemma 4 31B QAT on four Nvidia L4 GPUs and evaluated one `sk_a2` arm on nine custom `rtrain` tasks from `/kaggle/input/datasets/ziadsamer/rebench-new-cp312/rebench`, repeating the same task IDs for three passes at concurrency 2. Its actual run log selects `skill_arms`, a 28-call cap, 240-second command timeout, eight-minute task cap, and 80 turns. The base `submission/eval_config.yaml` says 15 minutes; the active arm's `submissions/sk_a2/eval_config.yaml` and run log both say eight minutes.

The task-resolution counts were 5/9, 3/9, and 4/9 across the three passes: 12 resolved attempts out of 27 attempts, with one timeout. These are repeated results on nine tasks, not a 27-task score. The run has a single candidate arm and no paired baseline; it produces no Kaggle competition submission score. Treat it as exploratory evidence about that custom setup, not a promotion signal. It does not change the frozen V5/Patchsmith 53-task core or 18-task holdout.

## Jorgerome — `GemmaGraph-Agent`

Checked with the Kaggle CLI at 2026-11-26 23:07 UTC. The latest listed run was `COMPLETE` at 22:56:14 UTC on a Tesla T4. The [notebook](https://www.kaggle.com/code/jorgerome/gemmagraph-agent) and its output were pulled to ignored `data/local/research/gemmagraph-agent-2026-11-26-2303utc/` for static inspection; the notebook was not executed locally.

The run is a submission-builder/package demo, not an agent evaluation. Its log says no model was found under `/kaggle/input/` and takes an offline fallback that writes placeholder LoRA files. The published code hard-codes the 692-task telemetry and 84.6% pass rate in the function that writes `paper_metrics_summary.json`; it also constructs the comparison table from constants. Each `adapter_model.safetensors` is only 39 bytes (`SAFE_TENSORS_PAYLOAD_FOR_ADK_VALIDATION`), and the generated submission ZIP is 2,376 bytes. The log shows setup, synthetic fixture generation, syntax smoke check, static metric export, ZIP creation, and notebook-to-HTML conversion; it has no Gemma inference, competition task-resolution results, or Kaggle submission score. Therefore, neither the 84.6% claim nor the `COMPLETE` status is evidence of a competition result.

The code also contains a token-shaped literal as an `HF_TOKEN` fallback. We did not use it or verify whether it is valid; do not copy it into our environment. This audit does not change the frozen V5/Patchsmith comparison or its experiment order.

## Follow-up — checked 2026-11-26 23:55 UTC

The Kaggle CLI search surfaced [Pajak Chaithongchai's `Gemma 4 Developer Agent Competition`](https://www.kaggle.com/code/pajakchaithongchai/gemma-4-developer-agent-competition), whose current kernel status is `ERROR`. Its pulled notebook is preserved under ignored `data/local/research/pajak-gemma4-developer-agent-2026-11-26-2350utc/`; SHA-256 `3EF67487361414651FAE49C35B87FD11959F8055E496854FE2CFB0550EB084BE`. The execution log fails in the first code cell after 12.14 seconds with `NameError: name 'true' is not defined` on the JSON boolean `"enableCodeExecution": true`. Metadata attaches no GPU, TPU, dataset, competition, or model input. No task evaluation, agent result, or score was produced. The unexecuted manifest in a Markdown cell is not a runnable submission. This is not a candidate or performance result and does not change the staged comparison.
