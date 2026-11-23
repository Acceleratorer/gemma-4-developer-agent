# Scorable task set audit — 2026-11-23

## Source and method

Purnima Pathak's [scoring notebook](https://www.kaggle.com/code/purnimapathak15/score-gemma4-agent-on-72-scorable-tasks) and [CC BY 4.0 dataset](https://www.kaggle.com/datasets/purnimapathak15/gemma4-agent-selftest-scorable-tasks-and-traces) publish gold-patch and empty-patch controls for the 129 public training tasks. The dataset README says the author ran the competition harness (`swegemma 0.2.11`); `control/gold_patch_control_129.csv` contains 258 rows, two controls per task. The `control/scorable_tasks_72.txt` set contains tasks where the gold patch resolves and the empty patch does not. The other tasks are excluded because the gold patch fails locally (54) or an empty patch already resolves them (3).

The downloaded dataset is retained under ignored `data/local/research/purnima-72-scorable/`; imported traces and patches are not tracked. Its external arm scores and leaderboard claims are not our evaluation results.

## Selection and holdout split

All 44 IDs in `evals/dev-valid-training-gold-verified-task-ids.json` and all 18 IDs in `evals/dev-valid-unseen-gold-verified-task-ids.json` appear in the 72-task set. The ten remaining IDs are all Rich tasks: `rich_3043`, `rich_3105`, `rich_3480`, `rich_3772`, `rich_3782`, `rich_3930`, `rich_3942`, `rich_4006`, `rich_4070`, and `rich_4076`. In the source control CSV, each extra task's gold patch resolved with exit code 0 and its empty patch did not resolve; three empty-patch runs exited 124.

`evals/dev-valid-training-gold-scorable-54-task-ids.json` preserves the existing 44-task order, appends the ten additional scorable IDs, and remains disjoint from the 18-task holdout. This gives a wider paired selection set without consuming the holdout. All results remain local training-task evidence and do not predict a Kaggle leaderboard score.

## Runtime revalidation against the current wheelhouse

CPU-only kernel `accelra/scorable-54-gold-empty-controls-v1` completed on 2026-11-23. Its output is under ignored `evals/results/scorable-54-gold-empty-controls-v1/output-kaggle-2026-11-23/`. The paired control produced **53/54 gold-patch passes** and **0/54 empty-patch passes**. `rich_4070` is the sole gold-patch failure: `test_input_password` raises an input error in the non-interactive subprocess, so it is excluded. `rich_3782`, which failed two older controls on unrelated lexer assertions, passes in the current wheelhouse.

All 54 empty-patch rows failed, but five had non-assertion exits: `fastapi_15661` and `rich_3930` failed collection because the gold patches add the missing release script and Unicode-data package; `rich_3480`, `rich_3772`, and `rich_4006` reached the 300-second verification timeout, matching the three empty-control timeouts in the external source CSV. The active task set follows the established gold-pass/empty-fail criterion and preserves those rows for comparison; inspect their agent traces and runtimes when evaluating candidates.

The 53 IDs are pinned in `evals/dev-valid-training-wheelhouse-qualified-53-task-ids.json`. This retains the 44-task verified training core, appends nine additional Rich tasks, and remains disjoint from the 18-task unseen holdout. Tests assert that it equals the 54-task candidate minus `rich_4070`. Seed-42 V5, no-graph V5, and validation-contract notebooks were rebuilt from the same 53 IDs and saved privately with `--no-run`; no agent inference ran and no GPU quota was used. These are public training-task verifier controls, not agent scores or leaderboard estimates. Kaggle staff separately confirmed that private test repositories differ from the public training repositories and pass gold-patch validation; that does not make these local controls evidence about the scorer's hidden set.
