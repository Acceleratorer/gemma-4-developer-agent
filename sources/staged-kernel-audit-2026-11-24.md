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
