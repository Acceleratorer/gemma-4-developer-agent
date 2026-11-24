# Optimization plan

## Goal

Reach rank 1 on the final Kaggle private leaderboard. Continue optimizing until the final deadline and claim success only after the private leaderboard confirms it.

## Latest Kaggle state - quota/queue checked 2026-11-24 17:00 UTC; leaderboard/submissions checked 17:05 UTC

- **Competition:** the final deadline is 2026-12-02 23:59 UTC. The full public snapshot downloaded at 17:05:00 UTC has 6,638 rows and ranks `accelra` 2,073 at 0.18. It is archived under ignored `data/local/leaderboard-2026-11-24-1704utc/` (ZIP SHA-256 `FFA0B49FD4BE1249DCB673DF3E9C689825FD6B8AF7C65EDB5083773C1AF9B11B`).
- **Leaderboard:** 17 teams are tied at 0.24; 141 have 0.22 and 650 have 0.20. No private score is shown. Ties go to the earlier submission.
- **Submissions:** the latest CLI query shows `58729936` complete at 0.18, `58624160` complete at 0.10, and `58527796` complete at 0.15; no submission is pending.
- **Quota:** Kaggle CLI checked at 17:00 UTC: GPU is 29.96/30.00h used (0.04h left); TPU is 0.42/20.00h used (19.58h left). Both refresh at 2026-11-28 00:00 UTC / 07:00 Vietnam time.
- **TPU smoke:** version 2 errored. Its logs show the vLLM server failed with `/dev/vfio/1: Device or resource busy`; the notebook had called `jax.devices()` in the driver before starting the server. Version 3 remains `QUEUED` at 17:00 UTC; Kaggle exposes no ETA. This gates TPU evaluator jobs only: do not run them until model loading, text generation, and tool-call parsing pass. The staged reset-wave comparisons use Nvidia L4, so the TPU queue does not block those GPU runs.
- **Best tested agent:** Budget-Fit V5 scored 20/44 on local training tasks and 0.18 publicly. The local result is not a leaderboard score.
- **Staged after reset:** all six selected kernels still report `COMPLETE`; their pulled notebooks have no executed cells or outputs, so no agent inference ran. A static audit confirmed the exact candidate files, model, seed, budgets, and task sets; the 53-task training set and 18-task holdout have no overlap. See [the staged-kernel audit](../sources/staged-kernel-audit-2026-11-24.md).

## Deadlines and guardrails

- Entry/team-merge deadline: 2026-11-25 23:59 UTC. Final submission deadline: 2026-12-02 23:59 UTC.
- Target the final public upload by 2026-11-29 23:59 UTC to preserve at least 72 hours for queueing and scoring.
- Tune prompt flow and call/time budgets first; keep model and sampling fixed. Pair comparisons on task IDs, tools, and budgets, and promote only with aggregate and holdout evidence. Local task results are not leaderboard scores.
- Respect the scorer's global 12-hour patch-generation limit, which includes sandbox setup and covers all test tasks but excludes patch validation. An eight-minute per-task cap alone can allow a 16-hour worst case across about 120 tasks; estimate full-run time from measured task runtimes and leave headroom.
- Keep the 28-call/eight-minute setup until the seeded comparison justifies a change. Recheck quota after every run and reserve 5.2-6.6 GPU hours for the paired 18-task holdout.
- Do not assume the full reset quota is available for inference: a participant reported five queued hours plus five runtime hours charged as ten GPU hours. After the one-task probe, use the measured quota deduction—including its queue delay—to decide whether both 53-task arms fit while preserving the holdout reserve. Defer the optional full validation-contract comparison first if that reserve is at risk.
- Preserve the final archive, submission ID, public result, and selected final submission in the log. Do not submit while any public run is pending; verify Kaggle's current submission allowance before the next upload.
- Choose the two final submissions from candidates with paired 53-task and unseen 18-task evidence. Compare their task-level gains and losses; do not select by a single public score.

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
- Public candidate source checks and promotion decisions: [`sources/public-candidate-audit-2026-11-24.md`](../sources/public-candidate-audit-2026-11-24.md).
- Public top-score source-to-submission audit: [`sources/public-top-score-source-audit-2026-11-24.md`](../sources/public-top-score-source-audit-2026-11-24.md); no exact, licensed 0.24 bundle is verified for the first quota wave.
- Pulled source, configuration, task-set, and execution-state checks for the six staged kernels: [`sources/staged-kernel-audit-2026-11-24.md`](../sources/staged-kernel-audit-2026-11-24.md).
- Per-run model, task set, budgets, hashes, and score provenance: [`log/experiment-log.csv`](../log/experiment-log.csv).
- Active evaluation sets and scoring conventions: [`evals/README.md`](../evals/README.md).
- Prompt workflow findings: [`evals/prompt-test-loop-audit.md`](../evals/prompt-test-loop-audit.md).
- Deferred transfer study: [`sources/validation-dataset-compatibility-2026-11-23.md`](../sources/validation-dataset-compatibility-2026-11-23.md).
