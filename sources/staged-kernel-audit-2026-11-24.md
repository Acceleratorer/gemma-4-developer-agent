# Staged Kaggle kernel audit — 2026-11-24

## Scope and result

Pulled the latest source for each planned kernel with the Kaggle CLI into ignored `data/local/research/`. Parsed the notebook cells without executing them, then compared the embedded agent files with the tracked candidates after the evaluation builder's model and seed normalization.

All six kernels report `COMPLETE`, but each pulled notebook has one unexecuted code cell, no execution count, and no cell output. The completion is notebook conversion; no model inference or task evaluation ran. The validation-contract probe log contains only notebook-to-HTML conversion. No experiment result or Kaggle score was produced by this audit.

## Kernel inventory

| Kernel | Exact candidate match | Task set | Tasks |
| --- | --- | --- | ---: |
| [`v5-validation-contract-fastapi-seed-42-probe`](https://www.kaggle.com/code/accelra/v5-validation-contract-fastapi-seed-42-probe) | `budget-fit-v5-validation-contract-v1` | `v5-test-aware-fastapi-probe` | 1 |
| [`v5-validation-contract-seed42-53`](https://www.kaggle.com/code/accelra/v5-validation-contract-seed42-53) | `budget-fit-v5-validation-contract-v1` | `dev-valid-training-wheelhouse-qualified-53` | 53 |
| [`v5-28-call-seed-42-wheelhouse-qualified-53`](https://www.kaggle.com/code/accelra/v5-28-call-seed-42-wheelhouse-qualified-53) | `current` and `budget-fit-v5-prompt` (identical embedded files) | `dev-valid-training-wheelhouse-qualified-53` | 53 |
| [`patchsmith-exp021-seed42-wheelhouse-qualified-53`](https://www.kaggle.com/code/accelra/patchsmith-exp021-seed42-wheelhouse-qualified-53) | `patchsmith-exp021-exact-v1` | `dev-valid-training-wheelhouse-qualified-53` | 53 |
| [`v5-28-call-seed42-unseen-gold-verified-18`](https://www.kaggle.com/code/accelra/v5-28-call-seed42-unseen-gold-verified-18) | `current` and `budget-fit-v5-prompt` (identical embedded files) | `dev-valid-unseen-gold-verified` | 18 |
| [`unseen-gold-verified-patchsmith-exp021-31b`](https://www.kaggle.com/code/accelra/unseen-gold-verified-patchsmith-exp021-31b) | `patchsmith-exp021-exact-v1` | `dev-valid-unseen-gold-verified` | 18 |

Every kernel uses `gemma-4-31b-it-qat-w4a16-ct`, request seed 42, 28 tool calls, an eight-minute task limit, Nvidia L4, and disabled internet. The three comparison candidates use matching controls on the paired 53-task set and the same unseen 18-task holdout. The two task sets are disjoint.

The validation-contract probe embeds the exact tracked candidate prompt, SHA-256 `e06a2e62eba99c0a5984e8887a3f171ec9480ca48f0e9e4bfc72062e12d6bd4a`. Its task is `fastapi_15588`; its remaining agent files also match the candidate exactly after model/seed normalization.

## How to use this audit

After the 2026-11-28 quota refresh, run the one-task validation-contract probe first. Only run its 53-task comparison if the probe passes and the planned unseen holdout reserve remains covered. Then run the V5/Patchsmith fixed-set comparisons as listed in [`milestone/PLAN.md`](../milestone/PLAN.md). Recheck kernel status and quota immediately before each run; `COMPLETE` by itself does not mean inference ran.

## Launch staging

All six kernels were pulled again with Kaggle CLI `--metadata`. The probe folder is `data/local/research/v5-validation-contract-fastapi-seed-42-probe/`; the other five are under `data/local/research/staged-audit/` in the matching table order: `validation-contract-53/`, `v5-53/`, `patchsmith-53/`, `v5-holdout-18/`, and `patchsmith-holdout-18/`. Each `kernel-metadata.json` has the exact kernel ID and notebook filename, private visibility, Nvidia L4 enabled, internet disabled, the competition and wheelhouse inputs, and the Gemma 4 31B model source.

After the quota refresh, `kaggle kernels push -p <folder>` creates a new version and runs it. Do not pass `--no-run` for an experiment; that only saves another conversion artifact without inference.

## Paired comparison suites — saved 2026-11-24 20:30 UTC

Two paired suites were saved with Kaggle CLI `--no-run` and pulled back for inspection:

| Kernel version | Sequential runs | Status |
| --- | --- | --- |
| [`v5-probe-patchsmith-exp021-core-53-seed42/1`](https://www.kaggle.com/code/accelra/v5-probe-patchsmith-exp021-core-53-seed42) | Validation-contract probe (1 task), V5 (53 tasks), Patchsmith exp021 (same 53 tasks) | Saved only; no inference |
| [`v5-patchsmith-exp021-holdout18-seed42/1`](https://www.kaggle.com/code/accelra/v5-patchsmith-exp021-holdout18-seed42) | V5 and Patchsmith exp021 on the same 18 unseen tasks | Saved only; no inference |

Both pulled notebooks contain the expected candidates and task IDs, request seed 42, the 28-call/eight-minute budgets, and empty execution counts and outputs. No GPU quota was used. The existing V5 and Patchsmith single-arm 53-task kernels remain available as fallbacks.

The combined core suite's configured task-time ceiling is 14 hours 16 minutes: 107 tasks at eight minutes each, before package setup and model startup. Kaggle documents a 12-hour maximum for GPU notebook runs, so this version may be terminated before all three runs finish. Use it only if the standalone probe's measured timings leave clear headroom under 12 hours; otherwise use the staged single-arm core kernels. The paired 18-task holdout has a 4-hour-48-minute configured task-time ceiling before setup. These limits are separate from the competition scorer's own patch-generation limit.
