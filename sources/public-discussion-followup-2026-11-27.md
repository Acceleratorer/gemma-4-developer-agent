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

## Limits

This was a read-only Kaggle CLI screen, not an exhaustive archive of every notebook or discussion. Public thread claims remain author-reported unless independently reproduced; Kaggle `COMPLETE` or a high test-count title is not itself a competition score.
