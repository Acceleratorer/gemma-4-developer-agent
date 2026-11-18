# Competition facts and sources

Competition pages checked on 2026-11-19; leaderboard refreshed on 2026-11-19 with the official Kaggle CLI.

## Official references

- [Competition overview](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview): build an autonomous Gemma 4 coding agent that navigates repositories and drafts fixes for real software issues.
- [Competition data](https://www.kaggle.com/competitions/gemma-4-developer-agent/data): 129 public training tasks, snapshots, graph/node embeddings, wheels, sample submission, and `HARNESS_README.md`.
- [Models tab](https://www.kaggle.com/competitions/gemma-4-developer-agent/models): competition-associated Gemma model variants.
- [Official small-model prize and eligibility](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview/prizes): E2B/E4B bonus prize and cross-track eligibility.
- [Organizer announcement](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/748287): support for 12B, E4B, and E2B variants.
- [Discussion](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion): organizer updates and participant findings.
- [Rules and timeline](https://www.kaggle.com/competitions/gemma-4-developer-agent/rules): entry, daily submission, final-selection, team, and license rules.
- [Official harness guide](https://www.kaggle.com/competitions/gemma-4-developer-agent/data?select=HARNESS_README.md): local evaluation, agent schema, sandbox, tools, budgets, and scorer behavior.
- [Official small-model leaderboard notebook](https://www.kaggle.com/code/ryanholbrook/gemma-4-developer-agent-small-model-leaderboard): daily filtered standings for E2B/E4B submissions.
- [Official getting-started notebook](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent): environment setup and sample evaluation flow.

## Scoring and submission

The scorer applies each generated patch to a repository snapshot and runs the task's validation tests. The score is the fraction of tasks resolved. The submission is a ZIP containing declarative agent configuration, with exactly one root `agent.yaml` and optional prompts, subagents, skills, and LoRA adapters. The private leaderboard determines final placement; exact-score ties go to the submission entered first.

The official overview gives the agent 12 hours to submit patches across the test set, including sandbox setup but excluding patch validation. Kaggle staff estimate validation can add about two hours when every task has a patch; a no-patch run takes about ten minutes. A per-task time cap must fit inside that global limit, so extrapolate local task runtimes cautiously ([official overview](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview), [staff clarification](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/743663)).

Kaggle staff confirmed the thinking-token loss between tool calls was a harness incompatibility and said the fix should be in the current wheelhouse. Since candidates enable thoughts, record the wheelhouse/runtime version for future comparisons ([discussion](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/744354)).

The competition supports `gemma-4-31b-it-qat-w4a16-ct`, `gemma-4-12b-it-qat-w4a16-ct`, `gemma-4-e4b-it-qat-w4a16-ct`, and `gemma-4-e2b-it-qat-w4a16-ct`. All agents in a submission must use the same base model. E2B and E4B submissions remain eligible for the general leaderboard and can also qualify for the $10,000 small-model bonus if selected as one of the team's two final submissions; an official notebook publishes filtered daily standings. The submission is a ZIP with a root `agent.yaml`; the 3 GiB unpacked archive limit and sandbox restrictions apply.

The official overview lists $65,000 for the main competition, $35,000 for the optional paper track, and a $10,000 small-model bonus. The final submission deadline is 2026-12-02 23:59 UTC; the entry/team-merge deadline is 2026-11-25 23:59 UTC.

## Dated leaderboard snapshot

- Main public leaderboard: top score **0.24**, tied by 14 teams in the snapshot timestamped 2026-11-18 18:04 UTC; downloaded on 2026-11-19 with `kaggle competitions leaderboard --download`.
- Small-model public leaderboard: top score **0.12** in the official tracker output, last updated 2026-11-16 23:55 UTC; refreshed from the Kaggle notebook on 2026-11-18.
- These are public-split snapshots, not final standings. The final placement is based on the private leaderboard.

## Harness findings that affect experiments

- The graph tools are registered and conditionally advertised when the task's graph and embedding assets are present. The local guide documents `get_code_neighbors`, `search_similar_code`, and `get_code_subgraph`.
- `submit_patch()` ends the agent loop. If the agent does not call it, the harness can capture a fallback diff; still call it last after the change is ready.
- Test and runner-config edits are removed before verification, so use tests as read-only requirements and patch product source.
- The local harness supports `max_tool_calls`, `max_time_minutes`, `max_turns`, and command timeout settings under `eval_config.yaml`.
- The dataset and README can lag discussion updates. Re-check the current competition page/discussion before locking model support or scorer assumptions.
