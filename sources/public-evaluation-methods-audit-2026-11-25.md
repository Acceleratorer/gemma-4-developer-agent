# Public evaluation-methods audit — 2026-11-25

## Radek Maciaszek's Glassbox release

Sources: the author's [competition write-up](https://medium.com/@rathko/competing-in-kaggle-competitions-with-old-gpus-9b8a67d1c0b9), [Apache-2.0 toolkit and anonymized data](https://github.com/rathko/kaggle-glassbox), and its [Gemma 4 campaign paper](https://github.com/rathko/kaggle-glassbox/blob/main/competitions/gemma4-swe-agent/paper/paper.md).

The author reports a 0.24 public score (14/58) after starting at 7/58. The release contains 3,985 anonymized task attempts across 197 runs and scripts to reproduce its measurements. The author explicitly withholds agent code, prompts, task content, and the best configuration, so the release supplies no candidate bundle to copy or compare.

The paper reports about 1.5 tasks of score variation between identical-byte public reruns, compared with 2.9 tasks under a coin-flip model; 32.1% of released attempts used the full call budget, while 5.7% hit the time cap. In its local funnel, 4 of 23 small-screen ideas passed a +1-task bar, within the estimated 12.6–20.9% false-pass range, and none of five cheap-stage positives was confirmed at the next stage. These are the author's campaign measurements, not estimates validated on our exact candidate or private leaderboard.

## Effect on this experiment

The findings reinforce using task-paired comparisons and a disjoint holdout, and treating a single public score as noisy. They do not support adding a generic prompt or tool change. Our V5 40-call run tied the 28-call V5 at 20/44, so keep the call cap and sampling fixed in the staged V5/Patchsmith comparison. The 53-task core and 18-task holdout remain the decision evidence. No toolkit code or raw dataset from this release was copied into tracked files; a read-only clone for inspection remains under ignored `data/local/research/kaggle-glassbox/` at commit `55a81f4ffc979e33941781f98d86cb34682568d5`.

## Follow-up — Gemma E4B factorial prompt screen, checked 2026-11-26 22:55 UTC

Matisdsp's [pre-registered screening](https://github.com/matisdsp/gemma-4-developer-agent/blob/main/docs/paper/preregistration_screening.md) and [paper draft](https://github.com/matisdsp/gemma-4-developer-agent/blob/main/docs/paper/draft_screening.md) report 32 prompt/sampling configurations across 72 public FastAPI/Rich tasks (2,304 attempts) with Gemma 4 E4B. Six of eight recipes were bounded within ±3 percentage points; the other two remained unresolved, and no recipe's upper 90% bound exceeded +1.5 points. The best first-run configuration (`s04`) scored 15/72 against 9/72 for the base prompt, but it was selected after comparing 32 configurations. A [pre-registered replication](https://github.com/matisdsp/gemma-4-developer-agent/blob/main/docs/paper/preregistration_screening_addendum.md) on 576 fresh attempts reported +1.4 points for `s04` (90% interval −1.4 to +4.2; p=0.56), which is unresolved.

The paper also reports that imposed verification increased post-edit checks from 78% to 93%, while its resolved-rate effect was −0.2 points (90% interval −1.5 to +1.3); a “useful test” instruction raised the share of pytest calls that ran tests from 59% to 74%, with a −0.9-point resolved-rate effect (−2.3 to +0.5). These are author-reported E4B results, not a 31B comparison. The study used two public repositories, tasks that had appeared in earlier work, and a 36-call/10-minute budget, so it does not directly predict our 31B hidden-task score. It reinforces keeping the staged 31B V5/Patchsmith pair frozen and judging changes by resolved tasks, not by compliance alone; it does not change the experiment order.
