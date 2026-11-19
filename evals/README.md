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

The 14-task `dev` set has a no-patch verifier baseline of 0/14. Five tasks have known verifier failures and should be excluded when comparing candidate patch quality: `fastapi_14455` lacks `inline_snapshot`, `requests_7505` and `requests_6592` have a recursive `httpbin` fixture, `httpx_3672` cannot collect because the sandbox's `httpx` module lacks `Stream`, and `rich_4070` cannot open `/dev/tty`. The `httpx_3672` snapshot's own `src/httpx/__init__.py` exports `Stream`, so this appears to be an import mismatch in the no-patch verifier; keep the task excluded until that is resolved. The fixed `dev-valid` set contains the other nine tasks. It is a cleaner local comparison set, not a leaderboard estimate.

A CPU-only `--skip-agent-patch` screen of the 11 other Requests tasks found five more candidates whose verifier reached the issue assertions: `requests_6757`, `requests_7205`, `requests_7309`, `requests_7315`, and `requests_7427`. Five others (`requests_6589`, `requests_6629`, `requests_7328`, `requests_7433`, and `requests_7502`) hit the recursive `httpbin` fixture errors; `requests_6644` passed without a patch and is not discriminative. `dev-valid-crossrepo` adds the five assertion-failing Requests tasks to the existing nine-task set. It covers FastAPI, Rich, and Requests; the only HTTPX training task remains excluded because its verifier cannot collect. Keep `dev-valid` unchanged for historical comparisons.

The CPU-only FastAPI/Rich screen completed all 104 tasks. Comparing each no-patch failure with the task's `test_patch` identified 55 tasks whose failures were limited to issue tests, including two manually confirmed parameterized cases; nine also failed unrelated tests, 35 failed during collection, three timed out, and two passed without a patch. The per-task classification is in `evals/results/fastapi-rich-verifier-screen-v1/output/fastapi-rich-verifier-baseline/task-classification.json`; this is verifier diagnostics, not an agent score. The frozen `dev-valid-expanded` set has 20 tasks: the existing 14-task cross-repository set plus three issue-only FastAPI tasks (`fastapi_14786`, `fastapi_14301`, `fastapi_14616`) and three Rich tasks (`rich_4079`, `rich_3953`, `rich_3938`). These additions cover authorization parsing, dependency scope, JSON list handling, Markdown tables, Unicode cell width, and styled wrapping while retaining a 3/3 split across the two repositories.

## Current comparisons

- `module/agents/reference-budget-v2/`: notebook says its upstream configuration scored 0.18; the notebook's modified candidate is explicitly unscored.
- `module/agents/reference-40-calls/`: notebook title says 0.22, but the checked-in notebook has no score output or submission ID. Keep that score unverified until Kaggle history confirms it.
- `module/agents/current/`: clean, no-LoRA candidate. Compare it against these references on a fixed task set before allocating a public submission.
- `dev-valid-crossrepo` is the expanded 14-task training set for upcoming prompt and budget comparisons. The `dev-valid-9` results remain historical and are not directly comparable to scores from this set.
- `dev-valid-expanded` is the 20-task comparison set built from the 14-task cross-repository set plus six tasks with issue-only no-patch verifier failures. Use it for the baseline and prompt ablations; keep the 14-task set available for historical comparisons. Its reference-budget-v2 baseline is running as private Kaggle kernel `accelra/gemma-4-expanded-reference-baseline-v1`. The short-contract notebook remains unrun; a static audit confirms it differs from the baseline only in `prompts/system.md`.
- The expanded Hanh v6 and graph-enabled prompt notebooks are prepared under `evals/results/dev-valid-expanded-hanh-v6-31b/` and `evals/results/dev-valid-expanded-graph-v2-31b/`. Both use the same 20 task IDs, 31B model, tool registration, runtime, and 28-call/eight-minute limits as the baseline; each changes only `prompts/system.md`. The graph prompt avoids bracket-containing strings in `get_code_subgraph` arrays because the Kaggle wheelhouse's reported vLLM 0.19.1 parser can hang on malformed array arguments; see `sources/competition.md`. Both notebooks remain unrun.
- A source-faithful Patchsmith exp021 comparison is prepared at `evals/results/dev-valid-expanded-patchsmith-v5-31b/`. It uses the same 20 tasks, 31B model, sampling, 28 calls and eight-minute task cap; `timeout_seconds` is normalized from the scored archive's 60 to the baseline's 240. Its tool set and prompt differ from the baseline, so this is a package-level comparison rather than a prompt-only ablation. The original public 0.22 archive is preserved under ignored `data/local/`; the normalized candidate remains unrun and has no score.
- `module/agents/patch-preserve-v1/` adds a trace-driven prompt rule to preserve a passing source patch and avoid no-patch controls, wrong-interpreter checks, and scratch files in `/workspace`. Its 20-task notebook is `evals/results/dev-valid-expanded-patch-preserve-v1-31b/`; static audit confirms only `prompts/system.md` differs from the reference-budget-v2 baseline. It is prepared but unrun.
- `module/agents/phase-budget-v1/` uses the exact 3,728-character no-adapter system prompt from the icfoer Kaggle experiment; that author's 8/11 result is from a different local task set. Its 20-task notebook is `evals/results/dev-valid-expanded-phase-budget-v1-31b/`; static audit confirms only `prompts/system.md` differs from the reference-budget-v2 baseline. It is prepared but unrun.
- `module/agents/budget-fit-v5-prompt/` uses the prompt embedded in the public [Budget-Fit V5 notebook](https://www.kaggle.com/code/ccuuuuy/lb-0-22-4-config-files-no-training). Its four-file source bundle has digest prefix `c9829b6ac709`; the historical config-draw sample has ten runs of the same files at 8–11/58, while the notebook title reports 0.22. The 20-task notebook at `evals/results/dev-valid-expanded-budget-fit-v5-prompt-31b/` matches the baseline in tasks, model, tools, sampling, and budgets, changing only `prompts/system.md`. It remains unrun.
- `module/agents/short-contract-v1/`: concise prompt adapted from Hitarth's public ablation notebook, which calls it an unscored starting point. It preserves the reference prompt's graph-tool prohibition. The generated notebook is under `evals/results/dev-valid-crossrepo-short-contract-31b/`; static audit confirms it uses the same 14 tasks, 31B model, sampling, tools, and budgets as the reference-budget-v2 baseline, changing only `prompts/system.md`. It has not been run.
- `evals/build_kaggle_eval.py` accepts `--kernel-id` and `--kernel-title` so separate candidate notebooks can use unique private kernels.
- `evals/fastapi-rich-verifier-screen-task-ids.json` pins 104 FastAPI/Rich training tasks not present in the original development set. Their CPU-only `--skip-agent-patch` screen is complete; use only the issue-only tasks from its classification in agent comparisons.
