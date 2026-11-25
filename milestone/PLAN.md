# Optimization plan

## Goal

Reach rank 1 on the final Kaggle private leaderboard. Continue optimizing until the final deadline and claim success only after the private leaderboard confirms it.

## Latest Kaggle state — full leaderboard snapshot 2026-11-25 09:24:27 UTC; top rechecked 10:34 UTC; quota and kernels rechecked 10:52 UTC; submission 58883031 accepted 11:06 UTC; staged suite audit unchanged from 2026-11-24

- **Competition:** the final deadline is 2026-12-02 23:59 UTC. The public snapshot generated at 09:24:27 UTC has 6,691 rows and ranks `accelra` 2,073 at 0.18. It is archived under ignored `data/local/leaderboard-2026-11-25-0924utc/` (ZIP SHA-256 `c444f14ad67318ba5ac28de32f72d7db590d4a071895c86c52d4570369c8db25`).
- **Leaderboard:** the 09:24 UTC full snapshot has 18 teams at 0.24, followed by 146 at 0.22, 662 at 0.20, and 1,306 at 0.18. The 10:34 UTC top-only check still shows 0.24 as the high score. No private score is shown. Exact ties go to the submission entered first; do not infer tie priority from public row order or `LastSubmissionDate` alone. See the [tie-break check](../sources/public-top-score-source-audit-2026-11-24.md#tie-break-check).
- **Submissions:** Kaggle accepted Patchsmith exp021 exact-source archive `58883031` at 11:06 UTC; it is `PENDING` with no score. The three earlier submissions remain complete: `58729936` at 0.18, `58624160` at 0.10, and `58527796` at 0.15. Before the upload, the limits endpoint showed 0 submissions today and 1 remaining; the submit command then reported 0 remaining today, and the submissions list now contains 4 entries. Do not submit again until `58883031` reaches a terminal status.
- **Quota:** Kaggle CLI rechecked at 10:52 UTC: GPU is 29.96/30.00h used (0.04h left); TPU is 1.30/20.00h used (18.70h left). Both refresh at 2026-11-28 00:00 UTC / 07:00 Vietnam time. Preserve the remaining GPU quota for now.
- **TPU smoke:** versions 1–4 are `ERROR`. Version 3's log shows an XLA compile-time HBM OOM: 16.61 GiB used of 15.75 GiB, exceeding capacity by 883.69 MiB. Version 4, with max model length reduced from 4096 to 2048, still used 16.62 GiB and exceeded HBM by 898.41 MiB. Version 5 keeps model length at 2048 and adds `--max-num-batched-tokens 1024`; it remained `QUEUED` at 10:52 UTC, and Kaggle returned no queue ETA. The quota refresh does not guarantee that this queued run will start. Inspect its result before any TPU evaluator job. The paired core and holdout notebooks still report `COMPLETE` from conversion only, with no inference run. This gates TPU evaluator jobs only: do not run them until model loading, text generation, and tool-call parsing pass. The staged reset-wave comparisons use Nvidia L4, so the TPU status does not block those GPU runs.
- **Best tested agent:** Budget-Fit V5 scored 20/44 on local training tasks and 0.18 publicly. The local result is not a leaderboard score.
- **Staged after reset:** the six core single-agent kernels and the P4 Rich-pair screen were saved as notebook versions, not evaluation results. The paired core and 18-task holdout suites were rebuilt from the task-checkpoint runtime and saved as version 2 with `--no-run`; both report `COMPLETE` after notebook conversion, with unexecuted code cells and no inference. A static audit confirmed the embedded candidates, task IDs, seed, budgets, and model. The 53-task training set and 18-task holdout have no overlap. The one-time Windows task `CodexKaggleCore53Reset` is `Ready` for 2026-11-28 07:00 Vietnam time; a fresh validation-only preflight passed without a push. Its trigger and hashes are valid, and it will launch the core suite only if quota reaches 28 GPU hours, staged hashes match, and the kernel is inactive. The task wakes the PC but requires an interactive login and AC power. See [the staged-kernel audit](../sources/staged-kernel-audit-2026-11-24.md).

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
- Latest public kernel screen and evidence check: [`sources/public-kernel-screen-2026-11-25.md`](../sources/public-kernel-screen-2026-11-25.md).
- Public top-score source-to-submission audit: [`sources/public-top-score-source-audit-2026-11-24.md`](../sources/public-top-score-source-audit-2026-11-24.md); no exact, licensed 0.24 bundle is verified for the first quota wave.
- Public evaluation-noise source audit: [`sources/public-evaluation-methods-audit-2026-11-25.md`](../sources/public-evaluation-methods-audit-2026-11-25.md); the released Glassbox project has no agent prompt or winning configuration.
- Pulled source, configuration, task-set, and execution-state checks for the six staged kernels: [`sources/staged-kernel-audit-2026-11-24.md`](../sources/staged-kernel-audit-2026-11-24.md).
- Per-run model, task set, budgets, hashes, and score provenance: [`log/experiment-log.csv`](../log/experiment-log.csv).
- Active evaluation sets and scoring conventions: [`evals/README.md`](../evals/README.md).
- Prompt workflow findings: [`evals/prompt-test-loop-audit.md`](../evals/prompt-test-loop-audit.md).
- Deferred transfer study: [`sources/validation-dataset-compatibility-2026-11-23.md`](../sources/validation-dataset-compatibility-2026-11-23.md).
