# Notebook provenance

The original Kaggle notebooks were moved into local-only `notebooks/source/`. They are ignored by Git because the directory contains imported third-party code and notebook outputs. Their authors and source links are retained here; use Kaggle's current notebook version as the source of truth.

| Local notebook | Kaggle source | Use |
| --- | --- | --- |
| `gemma-4-budget-aware-coding-agent-v2.ipynb` | [flexonafft](https://www.kaggle.com/code/flexonafft/gemma-4-budget-aware-coding-agent-v2) | Single-agent budget/navigation reference; notebook reports 0.18 for its upstream config and says its modified candidate is unscored. |
| `lb-0-22-3-tweaks-40-tool-calls-no-training.ipynb` | [bliverrigpdoge](https://www.kaggle.com/code/bliverrigpdoge/lb-0-22-3-tweaks-40-tool-calls-no-training) | 40-call prompt/config reference; 0.22 is in the title, with no score record in the local copy. |
| `version-1-added-adaptor.ipynb` | [ayush04barai](https://www.kaggle.com/code/ayush04barai/version-1-added-adaptor) | Adapter packaging reference; depends on an external LoRA notebook output and is not reproducible from this folder alone. |
| `getting-started-gemma-4-developer-agent.ipynb` | [Ryan Holbrook](https://www.kaggle.com/code/ryanholbrook/getting-started-gemma-4-developer-agent) | Official starter and local evaluation example. |
| `gemma-4-developer-agent-small-model-leaderboard.ipynb` | [Ryan Holbrook](https://www.kaggle.com/code/ryanholbrook/gemma-4-developer-agent-small-model-leaderboard) | Official small-model leaderboard output. |

The extracted `module/agents/reference-*` directories are local-only comparisons. The tracked candidate in `module/agents/current/` is independently maintained.
