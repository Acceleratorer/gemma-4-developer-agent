# Public local-evaluation kit audit — 2026-11-27

## Source and contents

Yusuke Togashi's [competition discussion post](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762302) links the Kaggle dataset [Gemma 4 Developer Agent - Local Eval Kit](https://www.kaggle.com/datasets/yusuketogashi/gemma4-developer-agent-local-eval-kit). Kaggle metadata lists the dataset as Apache-2.0. Its README, scripts, supplemental test-dependency wheels, Kaggle `envfix_cell.py`, result CSV, and Docker recipe are preserved only in ignored `data/local/research/public-eval-kit-2026-11-27/`; nothing from the resource was copied into the submission or repository.

The README says the resource does not include competition data, model weights, or the competition harness wheelhouse; users supply those separately. The Kaggle and `wheels_extra` directories do include supplemental PyPI test-dependency wheels with individual licenses listed in `WHEELS.md`.

## Reported controls

- The author reports gold-patch resolution of 74/129 in a plain Kaggle CPU notebook, 105/129 after an offline dependency-install cell, and 124/129 in a separate local Docker reproduction. The bundled `kaggle/gold_check_results.csv` independently confirms 74/129 and 105/129 for its notebook screen: 31 tasks change to passing and 24 remain failing. We inspected the CSV but did not run the notebook or Docker image.
- The author reports that one identical 31B ZIP scored between 8 and 12 of 58 public tasks across submissions, and that the same 12B local configuration resolved 7/30 and 4/30 on repeated runs. These are author-reported outcomes, not independently reproduced results or scores for our candidate.
- The README says the local Docker reproduction uses Python 3.13 and excludes five tasks for environment/test reasons, including `rich_3472` because its required test is skipped on Python 3.11 and later. It says the local model runs were with 12B/E4B on 24-GB-class GPUs; 31B did not fit in that local setup.

## Cross-check against our staged task sets

| Set | In the kit's 124-task Docker gold list | Kaggle CPU gold CSV: plain / with `envfix` |
|---|---:|---:|
| Frozen 53-task core | 52/53 | 52/53 / 52/53 |
| Fixed 18-task holdout | 18/18 | 18/18 / 18/18 |

The kit's Docker list omits `rich_3472`, while the Kaggle CPU CSV's remaining core failure is `rich_3782`. Our own wheelhouse-qualified control passed 53/54 for the original candidate set, with `rich_4070` excluded and `rich_3782` passing in that runtime. This disagreement shows why the public kit's Python/Docker/Kaggle CPU results cannot be substituted for the fixed Kaggle-wheelhouse comparison.

## Decision

Keep the staged V5/Patchsmith task IDs, candidates, and hashes unchanged. Interpret their core and holdout results using the controls from their own runtime, inspect task-level gains and losses, and avoid promoting a candidate based on one task or one 0.02 public-score movement. Consider the kit's offline dependency cell only for a separate future Kaggle CPU gold-control screen; it is not evidence that the competition scorer or our frozen kernels use the same environment.

The dataset was downloaded for static inspection only. Its evaluation scripts, notebook, and Docker image were not executed, and its local-model results were not used as candidate scores.
