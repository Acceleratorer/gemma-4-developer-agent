# Experiment log

Append one row per evaluation run to `experiment-log.csv`. Keep local training-task results separate from Kaggle public scores. Never fill in an unknown score from a notebook title or a one-off claim.

Track the exact model, fixed task set, call/time budget, prompt/config hash, request seed, run environment, resolved count, failures, and source of the score. New Kaggle evaluation notebooks default to request seed `42`; use the same seed for paired comparisons. `legacy-unrecorded` marks older rows whose request-level seed was not captured. Store detailed traces under ignored `evals/results/<run-id>/` and summarize only the findings that change the next experiment.
