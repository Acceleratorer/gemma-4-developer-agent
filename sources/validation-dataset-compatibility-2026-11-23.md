# Public task-soundness dataset compatibility audit

Checked 2026-11-23 against the locally downloaded [public Kaggle dataset](https://www.kaggle.com/datasets/dmitriigluzdov/gemma-4-task-soundness-and-local-results), stored under the ignored `data/local/research/dmitriigluzdov-task-soundness/`, and this repository's Kaggle evaluation builders.

## Findings

- The export contains 165 tasks across 35 repositories. Its JSONL has the competition task fields (`instance_id`, `repo`, `base_commit`, `patch`, `test_patch`, `problem_statement`, `created_at`, `hints_text`) plus `FAIL_TO_PASS` and `PASS_TO_PASS`. No task ID overlaps the active 53-task selection set or the 18-task holdout, and none uses the competition's FastAPI, Rich, Requests, or HTTPX repositories.
- The release controls record all 165 admitted tasks as sound: empty-patch test exit code 1, reference-patch exit code 0, and a fresh reference repeat exit code 0. These are CPU controls with the bundle's pinned Python 3.12.14 environments and import router. The dataset itself cautions that hidden scoring uses different images, runtime, repositories, and tests; sound controls therefore establish verifier behavior, not agent performance or hidden-score prediction.
- Task shape is compatible with the official SWE-Gemma task loader, but the current project notebook builders are ID-set based: `evals/build_kaggle_eval.py` reads task IDs from the competition's `tasks.jsonl` and resolves snapshots from the competition input mount. The added tasks cannot run by adding their IDs to an existing list. The dataset also ships neither repository snapshots nor the original build logs.
- Rebuilding needs the bundle's `validation_rebuild.py snapshots` and per-repository `environment` steps, which fetch source commits and install pinned dependencies. An agent comparison then needs a custom invocation/notebook wired to the rebuilt task JSONL, snapshots, and environment router. The gold `patch` and `test_patch`, source manifests, and verifier evidence must remain inaccessible to the candidate agent.
- This is useful as a later repository-transfer screen: it broadens coverage beyond the four competition training repositories and has no task-ID overlap with the current panels. It is not a clean hidden holdout: the upstream tasks are public, the dataset already publishes per-task agent outcomes and baseline runs, pretraining exposure is unknown, and its 165 rows all use source split `train`. Choose and freeze any comparison panel before inspecting those outcome files. Preserve the bundle's CC BY 4.0 attribution and original repository license notices.

## Recommendation

Keep the existing paired 53-task selection and 18-task holdout as the active quota-gated sequence. Do not add this 165-task suite to the current comparison wave: snapshot/environment reconstruction and a custom evaluator path are extra work, while current GPU quota and the final-submission window are constrained. Revisit it after the active comparisons as an explicitly labeled cross-repository transfer study, with a pre-frozen repository-disjoint panel and task patches/tests withheld from the agent.

## Sources

- Bundle files inspected in the local download: `VALIDATION_README.md`, `validation_index.csv`, `validation_controls.csv`, `validation_env_recipes.json`, and `validation_rebuild.py`. The bundle credits the [SWE-rebench-v2 clean Python tasks source](https://huggingface.co/datasets/whitecircle/swe-rebench-v2-clean-python-tasks).
- Project evaluator entry points: [`build_kaggle_eval.py`](../evals/build_kaggle_eval.py), [`kaggle_runtime.py`](../evals/kaggle_runtime.py), and [`evals/README.md`](../evals/README.md).
- Competition facts and the official harness reference: [`competition.md`](competition.md), including the [official harness guide](https://www.kaggle.com/competitions/gemma-4-developer-agent/data?select=HARNESS_README.md).
