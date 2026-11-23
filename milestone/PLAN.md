# Optimization plan

## Goal

Reach rank 1 on the final Kaggle private leaderboard. Continue optimizing until the final deadline and claim success only after the private leaderboard confirms it.

## Latest Kaggle state - checked 2026-11-23 14:34 UTC

- **Competition:** 6,551 teams; `accelra` is rank 4,026 with a best public score of 0.15. The final deadline is 2026-12-02 23:59 UTC.
- **Leaderboard:** 16 teams remain tied at 0.24; the next score is 0.22. No private score is shown. Ties go to the earlier submission.
- **Submissions:** `58729936` is still `PENDING`; `58624160` is complete at 0.10 and `58527796` at 0.15. Do not attempt another public submission while one is pending.
- **Quota:** GPU is 29.96/30.00h used (0.04h left); TPU is 0.17/20.00h used (19.83h left). Both refresh at 2026-11-28 00:00 UTC / 07:00 Vietnam time.
- **TPU smoke:** version 2 of `accelra/gemma-4-qat-on-kaggle-tpu-v5e-8-smoke-v1` remains `QUEUED`. Kaggle provides no ETA in the status response. Check its logs when the status changes; do not treat queued quota usage as a successful model run.
- **Best tested agent:** Budget-Fit V5 scored 20/44 on local training tasks; its public submission is still pending. This is not a leaderboard score.
- **Staged after reset:** seed-42 V5 and source-faithful Patchsmith kernels share the fixed 53-task set. The paired unseen holdout has 18 tasks. Existing candidate notebooks are saved without inference.

## Deadlines and guardrails

- Entry/team-merge deadline: 2026-11-25 23:59 UTC. Final submission deadline: 2026-12-02 23:59 UTC.
- Target the final public upload by 2026-11-29 23:59 UTC to preserve at least 72 hours for queueing and scoring.
- Tune prompt flow and call/time budgets first; keep model and sampling fixed. Pair comparisons on task IDs, tools, and budgets, and promote only with aggregate and holdout evidence. Local task results are not leaderboard scores.
- Keep the 28-call/eight-minute setup until the seeded comparison justifies a change. Recheck quota after every run and reserve 5.2-6.6 GPU hours for the paired 18-task holdout.
- Preserve the final archive, submission ID, public result, and selected final submission in the log. The current pending submission blocks new uploads.
- Use the two final-selection slots for the strongest distinct candidates. Verify submission IDs, public scores, model variants, and selected final submissions.

## Reset-week experiment order

1. After quota refresh, run version 4 of the staged seed-42 validation-wording probe on `fastapi_15588` ([kernel](https://www.kaggle.com/code/accelra/v5-validation-contract-fastapi-seed-42-probe)). Skip the full prompt comparison if it fails.
2. Run the seed-42 V5 control on the 53 wheelhouse-qualified IDs ([kernel](https://www.kaggle.com/code/accelra/v5-28-call-seed-42-wheelhouse-qualified-53)).
3. Run source-faithful Patchsmith exp021 on the same 53 IDs ([kernel](https://www.kaggle.com/code/accelra/patchsmith-exp021-seed42-wheelhouse-qualified-53)) if quota and the final-submission buffer allow it.
4. Compare V5 with the selection leader on the paired 18-task unseen holdout: V5 ([kernel](https://www.kaggle.com/code/accelra/v5-28-call-seed42-unseen-gold-verified-18)) and Patchsmith ([kernel](https://www.kaggle.com/code/accelra/unseen-gold-verified-patchsmith-exp021-31b)). Avoid rerunning V5 if it is already the leader and the matching result exists.
5. Run the full validation-contract comparison ([kernel](https://www.kaggle.com/code/accelra/v5-validation-contract-seed42-53)) only if its one-task probe passes and quota remains after reserving the holdout budget.
6. Choose the strongest distinct candidates for the two final-selection slots, build exact 31B archives, and submit only when Kaggle accepts uploads and the 72-hour buffer remains.
7. Verify submission IDs, public scores, model variants, and selected final submissions. Check the private leaderboard after the competition closes and record the final result.

The API-shape pilot is an optional low-priority probe after these comparisons. It is based on the `rich_3061` trace and is documented with other deferred work in [`DEFERRED.md`](DEFERRED.md). Completed milestone details are preserved in [`COMPLETED.md`](COMPLETED.md).

## Evidence and references

- Current competition rules, queue observations, official links, and dated Kaggle snapshots: [`sources/competition.md`](../sources/competition.md).
- Per-run model, task set, budgets, hashes, and score provenance: [`log/experiment-log.csv`](../log/experiment-log.csv).
- Active evaluation sets and scoring conventions: [`evals/README.md`](../evals/README.md).
- Prompt workflow findings: [`evals/prompt-test-loop-audit.md`](../evals/prompt-test-loop-audit.md).
- Deferred transfer study: [`sources/validation-dataset-compatibility-2026-11-23.md`](../sources/validation-dataset-compatibility-2026-11-23.md).
