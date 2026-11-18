# Competition facts and sources

Checked on 2026-11-18 using the official Kaggle pages and Kaggle CLI.

## Official references

- [Competition overview](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview): build an autonomous Gemma 4 coding agent that navigates repositories and drafts fixes for real software issues.
- [Competition data](https://www.kaggle.com/competitions/gemma-4-developer-agent/data): 129 public training tasks, snapshots, graph/node embeddings, wheels, sample submission, and `HARNESS_README.md`.
- [Models tab](https://www.kaggle.com/competitions/gemma-4-developer-agent/models): competition-associated Gemma model variants.
- [Discussion](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion): organizer updates and participant findings.
- [Rules and timeline](https://www.kaggle.com/competitions/gemma-4-developer-agent/rules): entry, daily submission, final-selection, team, and license rules.
- [Official harness guide](https://www.kaggle.com/competitions/gemma-4-developer-agent/data?select=HARNESS_README.md): local evaluation, agent schema, sandbox, tools, budgets, and scorer behavior.
- [Official small-model leaderboard notebook](https://www.kaggle.com/code/ryanholbrook/gemma-4-developer-agent-small-model-leaderboard): daily filtered standings for E2B/E4B submissions.
- [Official getting-started notebook](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent): environment setup and sample evaluation flow.

## Scoring and submission

The scorer applies each generated patch to a repository snapshot and runs the task's validation tests. The score is the fraction of tasks resolved. The submission is a ZIP containing declarative agent configuration, with exactly one root `agent.yaml` and optional prompts, subagents, skills, and LoRA adapters.

The current documented model set is `gemma-4-31b-it-qat-w4a16-ct`, `gemma-4-12b-it-qat-w4a16-ct`, `gemma-4-e4b-it-qat-w4a16-ct`, and `gemma-4-e2b-it-qat-w4a16-ct`. Every agent in one submission must use the same base model. The 3 GiB unpacked archive limit and sandbox restrictions apply.

## Dated leaderboard snapshot

- Main public leaderboard: top score **0.29** on 2026-11-18, retrieved with `kaggle competitions leaderboard --show`.
- Small-model public leaderboard: top score **0.12** in the official tracker output from its 2026-11-17 run.
- These are public-split snapshots, not final standings. The final placement is based on the private leaderboard.

## Harness findings that affect experiments

- The graph tools are registered and conditionally advertised when the task's graph and embedding assets are present. The local guide documents `get_code_neighbors`, `search_similar_code`, and `get_code_subgraph`.
- `submit_patch()` ends the agent loop. If the agent does not call it, the harness can capture a fallback diff; still call it last after the change is ready.
- Test and runner-config edits are removed before verification, so use tests as read-only requirements and patch product source.
- The local harness supports `max_tool_calls`, `max_time_minutes`, `max_turns`, and command timeout settings under `eval_config.yaml`.
- The dataset and README can lag discussion updates. Re-check the current competition page/discussion before locking model support or scorer assumptions.
