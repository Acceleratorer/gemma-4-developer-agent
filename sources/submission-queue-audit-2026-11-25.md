# Submission queue audit — 2026-11-25

Checked at 11:53 UTC with the Kaggle CLI. The queue discussion is operational risk evidence, not a new scoring rule or an estimate for our own submission.

## Official estimate and follow-up

Kaggle's [19 November queue update](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/760471) estimated 8–9 hours waiting, 9–10 hours of notebook runtime, and 2–2.5 hours for scoring. It said about 94% of submissions were completing within 24 hours, usually in 20–24 hours end to end.

The thread had 26 comments when checked; its newest visible comments were participant reports posted on 25 November. No organizer reply or revised estimate appeared in that thread. The newer [27-hour pending report](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/761733) had no comments.

## Participant reports

- On 25 November, M. Ahmed reported a first submission taking over 25 hours end to end and a second still running after 14 hours. MRIGESH_THAKUR separately reported a run lasting over a day.
- Michael Jordan reported submission `58799005` reaching `COMPLETE` after about 31.4 hours, but said the public score field was empty. This is an author-reported status, not independently verified here.
- Earlier follow-ups in the same thread claimed 33.5- and 36.5-hour pending periods for `58799005`; those durations conflict with the UTC timestamps and submission time cited in the posts. Do not use those figures as a measured queue distribution.
- A participant asked whether a submission still pending at the 2 December deadline could be selected as a final submission. No organizer answer was visible in the retrieved thread.

These reports show that the 20–24-hour estimate may not cover every recent submission, but they do not establish a new typical turnaround or predict our result. Do not cancel or duplicate a pending submission.

## Our current submission and planning

Kaggle accepted `58883031` at 11:06:25 UTC on 25 November. The submissions endpoint still reported it as `PENDING` at 11:53 UTC, with no score. Its age was about 47 minutes at that check; there is no evidence it is stuck.

Keep the 72-hour final-upload buffer in [`milestone/PLAN.md`](../milestone/PLAN.md) as a minimum. Recheck submission status and remaining upload allowance before any later upload. Do not assume a pending run will finish or receive a score by the final deadline.

## Follow-up — 2026-11-26 17:31 UTC

The Kaggle CLI showed submission `58883031` still `PENDING` with both score fields empty, about 30h25m after acceptance. The 17:31 UTC public leaderboard top-only check still showed 19 teams at 0.24 and the next score at 0.22; it does not expose our private score.

The queue-update thread had 30 comments. Its newest comment, posted 2026-11-26 11:53 UTC, asks Kaggle staff for an update; no organizer reply or revised official ETA was visible. A participant post at 09:28 UTC says submission `58872395` had been pending for about 35 hours, but the post cites a 2026-11-25 06:37 UTC submission time, which would make its age about 26h51m at the post time. Record the reported 35 hours as an inconsistent anecdote, not a measured queue duration. Another participant reported a completed run with no public score; that report remains unverified here.

Separate 26 November threads report a baseline notebook stuck in `Notebook Running` or `Scoring` for over 24 hours. In the notebook-running thread, the author says the notebook itself finished in 19.9 seconds and packaged a ZIP; no evaluator result or submission reference was supplied, and the visible date/time details do not independently establish a 24-hour duration. Its newest comment says a repeat was blocked by the one-pending-submission rule. These reports are not evidence that our submission is stuck. See the [notebook-running report](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762046) and [scoring-delay report](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762009).

The question asking whether selected submissions will be rerun for final ranking still had zero replies at this check ([discussion #762074](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/762074)). Do not assume pending submissions will be rerun or that a public score predicts the final private ranking. The official 20–24-hour estimate remains the 19 November staff update; all later queue durations above are participant reports.

## Outcome for submission 58883031 — checked 2026-11-26 19:17 UTC

The Kaggle submissions endpoint now reports `58883031` as `COMPLETE` with public score 0.17; its private score is not shown. It completed about 32h11m after Kaggle accepted it at 11:06:25 UTC on 25 November. This is the measured turnaround for this submission, not a new queue-wide estimate. It is no longer pending, and its public score is below our existing 0.18 V5 submission. The exact archive still awaits paired 53-task and 18-task local evidence before promotion.
