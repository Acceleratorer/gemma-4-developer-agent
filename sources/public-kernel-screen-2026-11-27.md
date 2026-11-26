# Public kernel screen — 2026-11-27

The initial Kaggle CLI check was at 2026-11-26 17:31 UTC / 2026-11-27 00:31 Vietnam time. A follow-up at 18:17 UTC found one active public experiment, recorded below. Notebook source and outputs are preserved only under ignored `data/local/research/`; no public notebook was executed locally.

## Evgen Dvorkin — `rich_3894`

The latest listed run of [Gemma 4 | rich_3894: 41/42 → 42/42](https://www.kaggle.com/code/evgendvorkin/gemma-4-rich-3894-41-42-42-42) was `COMPLETE` at 2026-11-26 17:02:08 UTC. The notebook concerns one Rich issue, `rich_3894`; its 41/42 → 42/42 title is a test count for that issue, not 42 benchmark tasks or a leaderboard score. The notebook describes four skipped tests.

The latest run's log verifies 28 agent files, creates a ZIP with SHA-256 `63DA26AB6658E95E1D839565A05734E2979342B2E9C9CD891138096A6366181F`, and converts the notebook to HTML. It reports that P18 uses Luis Specian's MIT-licensed V24 repository-tools agent and preserves the P16 executable agent, prompts, sampling, and limits. The log has no Gemma inference, task-resolution summary, or Kaggle score. The 28-file V24/P18 bundle is distinct from the six-file `module/agents/idris-v24` candidate; do not treat the run as a comparison against that local candidate.

**Decision:** this is a source/package verification rerun on one task, not evidence of a new agent gain. It does not change the frozen seed-42 53-task V5/Patchsmith core or the paired 18-task holdout.

## Active public evaluation — Engziadsamer `arms-again`

At 2026-11-26 18:20 UTC, Kaggle still reported [arms-again](https://www.kaggle.com/code/engziadsamer/arms-again) as `RUNNING`. The pulled notebook metadata attaches the competition wheelhouse, `rodrigospalma/ood45-bugfix-split`, and Gemma 4 31B QAT v2; internet is disabled. Its source selects a custom `skill_arms` evaluation mode, two concurrent task attempts, a 28-call cap, and a 15-minute per-task cap. This is not directly comparable to our eight-minute fixed-set runs.

The Kaggle logs endpoint returned no text at 18:17 UTC and the output fetch exposed no files at 18:20 UTC. `RUNNING` therefore confirms an active kernel only; it does not confirm completed inference, resolved tasks, or a competition score. The source and metadata are retained under ignored `data/local/research/public-kernel-screen-followup-2026-11-27/`. This external run does not change the staged V5/Patchsmith comparison or its holdout.
