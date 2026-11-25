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
