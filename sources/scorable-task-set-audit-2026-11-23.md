# Scorable task set audit — 2026-11-23

## Source and method

Purnima Pathak's [scoring notebook](https://www.kaggle.com/code/purnimapathak15/score-gemma4-agent-on-72-scorable-tasks) and [CC BY 4.0 dataset](https://www.kaggle.com/datasets/purnimapathak15/gemma4-agent-selftest-scorable-tasks-and-traces) publish gold-patch and empty-patch controls for the 129 public training tasks. The dataset README says the author ran the competition harness (`swegemma 0.2.11`); `control/gold_patch_control_129.csv` contains 258 rows, two controls per task. The `control/scorable_tasks_72.txt` set contains tasks where the gold patch resolves and the empty patch does not. The other tasks are excluded because the gold patch fails locally (54) or an empty patch already resolves them (3).

The downloaded dataset is retained under ignored `data/local/research/purnima-72-scorable/`; imported traces and patches are not tracked. Its external arm scores and leaderboard claims are not our evaluation results.

## Selection and holdout split

All 44 IDs in `evals/dev-valid-training-gold-verified-task-ids.json` and all 18 IDs in `evals/dev-valid-unseen-gold-verified-task-ids.json` appear in the 72-task set. The ten remaining IDs are all Rich tasks: `rich_3043`, `rich_3105`, `rich_3480`, `rich_3772`, `rich_3782`, `rich_3930`, `rich_3942`, `rich_4006`, `rich_4070`, and `rich_4076`. In the source control CSV, each extra task's gold patch resolved with exit code 0 and its empty patch did not resolve; three empty-patch runs exited 124.

`evals/dev-valid-training-gold-scorable-54-task-ids.json` preserves the existing 44-task order, appends the ten additional scorable IDs, and remains disjoint from the 18-task holdout. This gives a wider paired selection set without consuming the holdout. All results remain local training-task evidence and do not predict a Kaggle leaderboard score.

## Runtime revalidation before use

The external 72-task control is not enough to qualify this 54-task set for the current local runtime: `rich_3782` is included in the ten additions, but it failed the gold patch in both the `dev-valid-unseen` and `fastapi-rich-issue-only` local controls because of unrelated lexer assertions. Kaggle staff has separately confirmed that the private test repositories differ from the public training repositories and validate with gold patches; that does not repair this public task's local verifier. CPU-only kernel `accelra/scorable-54-gold-empty-controls-v1` now checks gold and empty patches on all 54 IDs under the current wheelhouse. Do not run the saved 54-task agent kernels until the selection is rebuilt from IDs whose gold patch passes and empty patch fails in that paired control.
