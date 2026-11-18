# Project guidance

This repository optimizes a Kaggle coding agent. Read [`sources/competition.md`](sources/competition.md) for current rules and [`milestone/PLAN.md`](milestone/PLAN.md) for the active experiment sequence.

- The submitted agent lives in `module/agents/current/`. Build it with `py -3.12 module/build_submission.py`; do not hand-edit generated ZIPs.
- Keep Kaggle inputs and generated traces under ignored `data/local/` and `evals/results/`. Never commit credentials, model weights, snapshots, or imported notebook source.
- Keep each evaluation comparable: record model, task set, budgets, prompt/config hash, result split, and whether the score came from Kaggle or local training tasks in `/log/experiment-log.csv`.
- Before a competition submission, run the package tests and rebuild the exact archive to be submitted. Record the Kaggle submission status and score before changing the candidate.
- Do not claim a rank or score without a current Kaggle leaderboard/submission result.
