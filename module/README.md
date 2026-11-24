# Submission source

`agents/current/` is the active single-agent candidate. It has no LoRA adapter and mirrors the measured 28-call Budget-Fit V5 runtime in `agents/budget-fit-v5-prompt/`; its Apache-2.0 `LICENSE.txt` and attribution `NOTICE.txt` travel in the submission archive. V5 resolved 20/44 on the gold-verified training set versus the reference's 19/44; the seed-matched budget comparison and unseen holdout remain pending. The reference notebook configurations are retained locally under ignored `agents/reference-*` directories.

`build_submission.py` packages an agent directory into a deterministic Kaggle `submission.zip`. The builder accepts all four supported quantized Gemma 4 variants: 31B, 12B, E4B, and E2B. Every agent in one submission must use the same base model; check [`sources/competition.md`](../sources/competition.md) against the live rules before submission.

The primary agent uses the complete competition tool set, including graph retrieval. It uses graph tools when a relevant symbol is known and falls back to repository search when graph retrieval does not return a useful match.
