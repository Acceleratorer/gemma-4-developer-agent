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

## Limits

This was a read-only Kaggle CLI screen, not an exhaustive archive of every notebook or discussion. Public thread claims remain author-reported unless independently reproduced; Kaggle `COMPLETE` or a high test-count title is not itself a competition score.
