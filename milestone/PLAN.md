# Optimization plan

## Goal

Reach rank 1 on the final Kaggle private leaderboard. Continue optimizing until the final deadline and claim success only after the private leaderboard confirms it.

## Latest Kaggle state — submissions, quota, and TPU smoke rechecked 2026-11-24 22:41 UTC; staged suite statuses rechecked 22:31 UTC; latest public kernel rechecked 22:38 UTC; paired suite v2 conversions completed 22:04 UTC; full leaderboard generated 22:33:47 UTC

- **Competition:** the final deadline is 2026-12-02 23:59 UTC. The full public snapshot generated at 22:33:47 UTC has 6,663 rows and ranks `accelra` 2,072 at 0.18; the top score remains 0.24, tied by 17 teams. It is archived under ignored `data/local/leaderboard-2026-11-24-2231utc/` (ZIP SHA-256 `d96ca742f7bcdf9daf6d6d67d23482861431814da2ac40e59e05010e4ec07ab6`).
- **Leaderboard:** 17 teams tie at 0.24, followed by 142 at 0.22, 653 at 0.20, and 1,306 at 0.18. No private score is shown. Exact ties go to the submission entered first; do not infer tie priority from public row order or `LastSubmissionDate` alone. See the [tie-break check](../sources/public-top-score-source-audit-2026-11-24.md#tie-break-check).
- **Submissions:** the 22:41 UTC CLI query shows `58729936` complete at 0.18, `58624160` complete at 0.10, and `58527796` complete at 0.15; no submission is pending. Submission limits were last reported at 19:31 UTC as 3 lifetime submissions and 1 currently allowed; recheck before an upload.
- **Quota:** Kaggle CLI rechecked at 22:41 UTC: GPU is 29.96/30.00h used (0.04h left); TPU is 0.42/20.00h used (19.58h left). Both refresh at 2026-11-28 00:00 UTC / 07:00 Vietnam time. Preserve the remaining GPU quota for now.
- **TPU smoke:** versions 1 and 2 are `ERROR`. Corrected version 3 was rechecked at 22:41 UTC and remains `QUEUED`; the log query returned no text, and Kaggle exposes no ETA. Version 2's logs show the vLLM server failed with `/dev/vfio/1: Device or resource busy`; the notebook had called `jax.devices()` in the driver before starting the server. Version 3 removes that parent-side device enumeration. The paired core and holdout notebooks still report `COMPLETE` from conversion only, with no inference run. This gates TPU evaluator jobs only: do not run them until model loading, text generation, and tool-call parsing pass. The staged reset-wave comparisons use Nvidia L4, so the TPU status does not block those GPU runs.
- **Best tested agent:** Budget-Fit V5 scored 20/44 on local training tasks and 0.18 publicly. The local result is not a leaderboard score.
- **Staged after reset:** the six core single-agent kernels and the P4 Rich-pair screen were saved as notebook versions, not evaluation results. The paired core and 18-task holdout suites were rebuilt from the task-checkpoint runtime and saved as version 2 with `--no-run`; both report `COMPLETE` after notebook conversion, with unexecuted code cells and no inference. A static audit confirmed the embedded candidates, task IDs, seed, budgets, and model. The 53-task training set and 18-task holdout have no overlap. See [the staged-kernel audit](../sources/staged-kernel-audit-2026-11-24.md).

## Deadlines and guardrails

- Entry/team-merge deadline: 2026-11-25 23:59 UTC. Final submission deadline: 2026-12-02 23:59 UTC.
- Target the final public upload by 2026-11-29 23:59 UTC to preserve at least 72 hours for queueing and scoring.
- Tune prompt flow and call/time budgets first; keep model and sampling fixed. Pair comparisons on task IDs, tools, and budgets, and promote only with aggregate and holdout evidence. Local task results are not leaderboard scores.
- Respect the scorer's global 12-hour patch-generation limit, which includes sandbox setup and covers all test tasks but excludes patch validation. An eight-minute per-task cap alone can allow a 16-hour worst case across about 120 tasks; estimate full-run time from measured task runtimes and leave headroom.
- Kaggle GPU notebook sessions stop at 12 hours. The paired core suite's configured ceiling is 14h16m, but a conservative runtime estimate based on the V5 44-task run puts p95 at 10.70 hours after stressing the new Rich tasks and Patchsmith timing; see the [staged-kernel runtime estimate](../sources/staged-kernel-audit-2026-11-24.md#runtime-sizing-for-the-combined-core-suite). Use the combined core suite as the first reset-week run to save queue cycles, and keep the single-arm kernels as fallbacks. The 18-task paired holdout's configured task cap is 4h48m before setup.
- The runtime now closes an appended JSONL checkpoint after each completed task. This supports recovery if Kaggle exposes outputs for a failed run; hard-timeout persistence is not guaranteed, so inspect the kernel's output-file list before choosing a fallback.
- The competition's Nvidia L4×4 notebooks consume GPU quota at twice the older T4×2/P100 rate. The estimated core use is about 21.4 GPU quota hours at p95; reserve 5.2–6.6 hours for the paired 18-task holdout. Kaggle's report of five queued plus five running hours charged as ten is consistent with a five-hour L4×4 run at 2×; it does not establish that queue time consumes quota. Recheck actual quota after each run and account for queue delay against the 72-hour final-upload buffer. Skip the optional full validation-contract comparison if the core or holdout leaves quota or time tight.
- Keep the 28-call/eight-minute setup until the seeded comparison justifies a change. Check that the combined suite outputs include all three expected results; Kaggle `COMPLETE` alone may mean notebook conversion only.
- Preserve the final archive, submission ID, public result, and selected final submission in the log. Do not submit while any public run is pending; verify Kaggle's current submission allowance before the next upload.
- Choose the two final submissions from candidates with paired 53-task and unseen 18-task evidence. Compare their task-level gains and losses; do not select by a single public score.

## Reset-week experiment order

1. After quota refresh, recheck quota, the TPU smoke, and the staged kernel statuses. Launch the combined core suite ([kernel](https://www.kaggle.com/code/accelra/v5-probe-patchsmith-exp021-core-53-seed42)) directly; it starts with the seed-42 validation-contract probe on `fastapi_15588`, then runs V5 and Patchsmith exp021 on the same 53 training tasks. Do not run the probe separately first.
2. Confirm the outputs contain the probe and both 53-task summaries. If the suite stops early, inspect saved outputs before choosing a single-arm fallback; only run the missing arm if quota, holdout reserve, and final-upload buffer still fit.
3. Run the paired V5/Patchsmith 18-task unseen holdout ([combined suite](https://www.kaggle.com/code/accelra/v5-patchsmith-exp021-holdout18-seed42)) when the 5.2–6.6 GPU quota-hour reserve and 72-hour final-submission buffer remain. Compare task-level gains and losses; avoid rerunning V5 if a matching result already exists.
4. Run the full validation-contract comparison ([kernel](https://www.kaggle.com/code/accelra/v5-validation-contract-seed42-53)) only if the probe passes and actual quota remains after the holdout; otherwise skip it.
5. Choose the strongest distinct candidates for the two final-selection slots, build exact 31B archives, and submit only when Kaggle accepts uploads and the 72-hour buffer remains.
6. Verify submission IDs, public scores, model variants, and selected final submissions. Check the private leaderboard after the competition closes and record the final result.

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
