# Gemma 4 Developer Agent

Build and compare Gemma 4 coding-agent submissions for Kaggle's Google - The Gemma 4 Developer Agent competition.

The current public leaderboard leader is **0.29** as checked on 2026-11-18. This workspace has no verified submission score yet. The target is to improve measured pass rate and select the strongest final 31B and small-model submissions before the competition closes.

## Build a submission

```powershell
py -3.12 module/build_submission.py --agent current --model gemma-4-31b-it-qat-w4a16-ct --output dist/main-31b.zip
py -3.12 module/build_submission.py --agent current --model gemma-4-e4b-it-qat-w4a16-ct --output dist/small-e4b.zip
```

The build checks archive paths, file types, model consistency, the required root `agent.yaml`, archive integrity, and the 3 GiB unpacked-size ceiling. It refuses to replace an existing output unless `--overwrite` is passed.

## Evaluate changes

Start with the fixed task set and local evaluation notes in [`evals/README.md`](evals/README.md). Use the same tasks, model, and seed across prompt or budget comparisons. Record every run in [`log/experiment-log.csv`](log/experiment-log.csv). Kaggle public scores and local training-task scores are separate evidence.

## Project map

- [`module/`](module/README.md): submission source and deterministic ZIP builder.
- [`evals/`](evals/README.md): benchmark procedure and result conventions.
- [`tests/`](tests/): focused package-builder checks.
- [`log/`](log/README.md): experiment history.
- [`milestone/`](milestone/PLAN.md): current optimization plan and competition deadlines.
- [`sources/`](sources/competition.md): official competition sources and dated leaderboard snapshot.
- [`notebooks/`](notebooks/README.md): provenance for the imported Kaggle notebooks, kept locally.

Competition data and imported third-party notebooks are excluded from Git. Fetch data with the Kaggle CLI when needed; never commit credentials, raw snapshots, graph/embedding assets, or model weights.
