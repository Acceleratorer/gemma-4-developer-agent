# Paired memory-study audit — 2026-11-27

## Primary sources checked

- Patrick Passos, [arXiv:2611.19359](https://arxiv.org/abs/2611.19359) and [full paper](https://arxiv.org/pdf/2611.19359).
- The author's [code and results repository](https://github.com/renorai/gemma4-memory-study), including the [frozen preregistration](https://github.com/renorai/gemma4-memory-study/blob/main/PREREG.md), [dated design/change log](https://github.com/renorai/gemma4-memory-study/blob/main/DESIGN.md), [`run_rows.jsonl`](https://github.com/renorai/gemma4-memory-study/blob/main/results/run_rows.jsonl), and [`analyze_rows.py`](https://github.com/renorai/gemma4-memory-study/blob/main/results/analyze_rows.py).

The repository says its summary rows and analysis scripts are included, while model weights and raw agent traces are not. I inspected the paper, preregistration, design notes, analysis code, and summary rows; I did not download the repository or rerun its analysis.

## What the study tested

The paper tests automatically re-injecting the coder's latest explorer finding after context compaction, with a notes mechanism the model rarely used, against no memory. This is an **in-task recap** treatment. The frozen preregistration originally asked about **cross-task, node-anchored experience memory**; the dated design log records the shift to recap after baseline-only traces showed repeated actions after compaction. The paper explicitly does not test agent-written persistent memory.

The experiment used Gemma 4 31B QAT in this competition harness. Its 48-pair primary set covered Modal and Kaggle runs; the separately registered 50-task extension used AWS L40S. The combined 98-pair result is labeled secondary, not confirmatory. The paper's A/A comparison also found that 9 of 48 tasks changed outcome between two no-memory runs (18.75%).

## Results and limits

- First 48 pairs: recap resolved 29/48 versus 25/48 for no memory, a +8.3-point difference; 95% interval [−2.1, +18.3], exact McNemar p=0.22.
- Separately registered 50-task extension: 18/50 versus 23/50, −10.0 points; 95% interval [−20.2, +0.7], p=0.125. Its direction did not replicate the first set.
- Combined 98-task secondary analysis: 47/98 versus 48/98, −1.0 point; 95% interval [−8.3, +6.3], p=1.0. The authors estimate 80% power only for effects around ±12 points or larger, so this is not evidence that all smaller effects are zero.

These findings are relevant to measurement noise, but they do not establish the value of our prompts or tools. The task samples, backends, and limits differ: the study used a 100-call and 60-minute cap, while our staged comparison uses 28 calls and 8 minutes on a fixed 53-task core and an 18-task holdout. Paired runs reduce task-mix confounding; they do not remove run-to-run variance. That last point is an inference from the study's A/A result, not a measured estimate for our exact candidate.

## Decision for this repo

The paper does not justify adding a recap or memory change to either staged candidate. Keep the frozen V5/Patchsmith comparison and its disjoint holdout. Read small task-count margins as uncertain, examine paired gains and losses plus runtime, and promote only when the holdout also supports the change. The current GPU budget may not allow repeat runs; if the paired results are close, record the comparison as inconclusive instead of presenting a small edge as stable.

This is consistent with [`milestone/PLAN.md`](../milestone/PLAN.md), which already requires paired core and holdout evidence and rejects promotion by one public score. It adds a caution about interpreting one run per arm; it does not change the active candidate or staged experiment.
