# Public discussion follow-up — 2026-11-27

Checked at 2026-11-26 22:10 UTC / 2026-11-27 05:10 Vietnam time with the Kaggle CLI. This follow-up supplements the existing [kernel screen](public-kernel-screen-2026-11-27.md), [model screen](public-model-screen-2026-11-27.md), and [submission-queue audit](submission-queue-audit-2026-11-25.md). No candidate or staged notebook was changed, and no evaluation was launched.

## New author-reported experiment

[Moran Zavdi's 1,350-episode study](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762144), with [supporting evidence and reproduction scripts](https://github.com/Aeterna-Data-AI-ML-Research/Kaggle-Gemma-4-Developer-Agent-Competition), compares 4,096 versus 1,024 thinking tokens across 150 calibration tasks. The author reports 48/150 correct final patches for both budgets. Correct patches with explicit submission rose from 22/150 to 28/150, while time-budget endings fell from 85 to 77. The author also reports nine new solves offset by nine regressions. This is one author-run calibration study, not an independent reproduction or a Kaggle leaderboard score; the post says the separate 150-task test split remained sealed.

**Decision:** it suggests a possible execution-budget effect, but does not show an overall repair-accuracy gain. Keep the frozen 53-task paired core and 18-task holdout unchanged. Consider a paired thinking-budget screen only after those runs, if measured timeout or explicit-submission failures make it worthwhile and quota plus the final-upload buffer allow it.

## Queue and final-selection threads

- Participant posts [reporting more than 24 hours pending](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762009) and [a notebook-only package stuck in “Notebook Running”](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762046) had no Kaggle Staff reply when checked. These reports do not establish a new queue-wide ETA or the status of our submission.
- The [question about whether final scoring reruns selected submissions](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762074) had no reply. It adds no organizer policy; continue following the published competition rules and the queue audit.

## Code and model cross-check

The latest relevant competition-code runs found by the CLI are already captured by the existing screens: `parkwave1/notebook-recode-rebuttal` is unrelated retrieval work, `rich_3894` is a package-only rerun, and `arms-again` is a repeated custom nine-task experiment without a paired baseline. The listed [WSP policy adapter](https://www.kaggle.com/models/kingdamon/gemma-4-dev-agent-policy) is already screened; its card and versions provide no resolved-task or competition-score evidence. No new comparable result changes the immediate experiment order.

## Follow-up — checked 2026-11-26 23:16 UTC

[Deepak Thanam's 31B/E4B experiment report](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/761941) was posted at 03:35 UTC and had no comments when fetched through the Kaggle CLI. On a fixed 40-task public holdout, the author reports 18/40 for a 31B baseline and ties at 18/40 after adding edit-failure, budget, command-hygiene, or heredoc guidance. A 40-call variant with shorter thinking also tied and hit the eight-minute cap more often. The same baseline ZIP reportedly drew 0.15 and 0.20 publicly; these are the author's reports, not a current leaderboard record for that archive. The E4B fixer/reviewer and locate-first pipelines each scored 7–8/40 on the author's holdout; a reproduction-first pipeline scored 4/40, and a two-attempt setup's oracle pass@2 was only 16.7% versus 13% pass@1. These small, author-run samples are not a direct comparison with our staged pair or the hidden-test score.

**Decision:** this independently supports treating prompt-only ties and one public draw cautiously. Keep the seed-42 V5/Patchsmith core and fixed 18-task holdout unchanged. E4B submission `58965387` remained `PENDING` at the 23:00 UTC Kaggle status check; the author's results do not replace its hidden-test result.

### Harness behavior cross-check

The post also describes `submit_patch` as ending the agent loop and the current diff as a fallback when budgets expire first. The local competition `HARNESS_README.md` independently documents both behaviors: the runner exits after the submitted patch's turn, and it extracts a non-empty working-tree diff if no explicit submission was made. Our current `agent.yaml` is a single agent, and its prompt places `submit_patch` after the final edit/check sequence. No harness or prompt change is indicated.

## Follow-up — checked 2026-11-26 23:55 UTC

- [Repeated notebook timeout report](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762131) still has no comments or staff diagnosis.
- [Request to allow daily submissions while another is pending](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/761897) has one participant `+1`, but no organizer response or policy change.
- [Question about learning from failed runs](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762042) has no replies. Its examples are the author's own trace observations, not independently reproduced findings.

These threads add no confirmed queue policy, timeout cause, or candidate improvement. Keep the frozen V5/Patchsmith comparison and existing submission gates unchanged.

## Follow-up — checked 2026-11-27 10:42 UTC

- The author of [the Budget-Aware V2 submission-stall report](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762046) updated it at 00:37 UTC: their notebook-only submission completed after about 36 hours without an error. They did not report a score in that update. This is one participant's result, not a new queue-wide estimate or a status update for our submission.
- [Another participant](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762009) reported at 10:10 UTC that their submission was still pending after 24 hours. No Kaggle Staff reply or revised queue estimate was visible.
- Comments on [the 1,350-episode study](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762144) discuss missing visible reasoning tokens in local/OpenRouter traces while reporting behavior changes when `thinking_budget` changes. The comments do not establish how the competition scorer records thought tokens or add a paired accuracy result; keep the budget fixed in the staged comparison.
- The question about [final-scoring reruns](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762074) still has no organizer answer. It provides no new final-selection policy.

## Follow-up — checked 2026-11-27 14:29 UTC

[Yusuke Togashi's local-evaluation kit post](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762302) links the [Apache-2.0 Kaggle dataset](https://www.kaggle.com/datasets/yusuketogashi/gemma4-developer-agent-local-eval-kit). The author reports that a plain Kaggle CPU notebook resolves 74/129 public gold patches, a supplemental offline dependency cell resolves 105/129, and a separate local Docker setup resolves 124/129. The bundled `gold_check_results.csv` statically confirms the 74/129 and 105/129 counts (31 newly passing; 24 still failing); we did not run the notebook or Docker setup. The author also reports 8–12 resolved tasks across public draws of one identical ZIP and 7/30 versus 4/30 on the same local 12B task set. These are author-reported results, not an independent reproduction or candidate scores. See the [eval-kit audit](public-local-eval-kit-audit-2026-11-27.md) for task-set overlap and environment differences.

**Decision:** use this as a warning to validate gold controls in the same runtime as each local comparison and to treat one-task public-score movements cautiously. It does not justify changing the frozen 53-task core or 18-task holdout before their paired run.

## Limits

This was a read-only Kaggle CLI screen, not an exhaustive archive of every notebook or discussion. Public thread claims remain author-reported unless independently reproduced; Kaggle `COMPLETE` or a high test-count title is not itself a competition score.

## Fresh CLI recheck — 2026-11-27 22:08 UTC

The authenticated discussion search and topic pulls are preserved under ignored `data/local/research/public-discussion-screen-2026-11-27-2208utc/`. No new Kaggle Staff policy or score evidence appeared. The most relevant current threads add three operational signals:

- [vLLM 0.19.1 parser-loop report](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/760830): an independent comment reproduces non-terminating parsing for malformed array-like arguments, including nested objects and the streaming path. This is a scorer-runtime failure mode; our staged V5 prompt already avoids graph calls and the paired run must be judged from actual traces, not from a prompt-only assumption.
- [Variation and public-score noise](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/760924) and [top-score discussion](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/761176): participants report that plain prompts and tool-call/parser reliability can correlate poorly with local scores, and that non-zero temperature makes one draw noisy. These are anecdotal; they support paired same-seed comparisons and do not justify replacing the staged candidates before their core/holdout evidence.
- [Submission queue update](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/760471): recent comments still report 30–40-hour waits without a revised organizer SLA. This affects final-upload scheduling, not candidate quality.

The discussion screen leaves the exact seed-42 V5/Patchsmith core and 18-task holdout unchanged.
