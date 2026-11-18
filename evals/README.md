# Evaluation workflow

## Evidence levels

1. **Package check**: validates the exact ZIP sent to Kaggle.
2. **Local development run**: evaluates fixed IDs from the public 129-task training set. It is useful for comparing prompts and budgets, but it is not a leaderboard estimate.
3. **Kaggle public score**: scores the official public test slice. Record the submission ID, score, and date. A single score is noisy; use repeated evidence before attributing a gain.
4. **Final standing**: the private leaderboard determines final placement.

## Inputs

Kaggle's competition data contains `tasks.jsonl`, 129 training tasks across four repositories, repository snapshots, graph and embedding files, test wheels, and the official sample submission. The full snapshot bundle is about 20.5 GB; the workspace keeps competition inputs under ignored `data/local/` and does not fetch every snapshot by default.

```powershell
New-Item -ItemType Directory -Force data/local | Out-Null
kaggle competitions download gemma-4-developer-agent --file tasks.jsonl --path data/local --unzip
kaggle competitions download gemma-4-developer-agent --file HARNESS_README.md --path data/local --unzip
```

Download only the snapshots, graphs, embeddings, and wheels needed for the chosen task IDs. Kaggle's L4x4 scoring environment mounts these inputs automatically; local Windows CPU/GPU results are not a substitute for that runtime.

## Local harness

The official `HARNESS_README.md` documents `swegemma eval`. A representative command is:

```bash
swegemma eval \
  --tasks data/local/tasks.jsonl \
  --snapshots-dir data/local/snapshots \
  --submission-dir dist/unpacked \
  --results-dir evals/results/<run-id> \
  --sandbox docker \
  --task-ids <task-id-1> <task-id-2>
```

Use the same task IDs for each comparison. `task_results.jsonl`, `summary.json`, traces, patches, and verification logs belong under the ignored `evals/results/` directory. Preserve only aggregate findings in `/log/experiment-log.csv`.

The checked-in getting-started notebook's saved smoke run used Gemma 4 12B, the sample agent, a one-minute/10-call budget, and the first two FastAPI tasks. Both ended without a patch. Treat that as evidence that the sample budget/prompt can stall, not as a baseline for the 31B candidate.

The 14-task `dev` set has a no-patch verifier baseline of 0/14. Five tasks have known environment failures and should be excluded when comparing candidate patch quality: `fastapi_14455` lacks `inline_snapshot`, `requests_7505` and `requests_6592` have a recursive `httpbin` fixture, `httpx_3672` cannot collect because `httpx.Stream` is missing, and `rich_4070` cannot open `/dev/tty`. The fixed `dev-valid` set contains the other nine tasks. It is a cleaner local comparison set, not a leaderboard estimate.

## Current comparisons

- `module/agents/reference-budget-v2/`: notebook says its upstream configuration scored 0.18; the notebook's modified candidate is explicitly unscored.
- `module/agents/reference-40-calls/`: notebook title says 0.22, but the checked-in notebook has no score output or submission ID. Keep that score unverified until Kaggle history confirms it.
- `module/agents/current/`: clean, no-LoRA candidate. Compare it against these references on a fixed task set before allocating a public submission.
