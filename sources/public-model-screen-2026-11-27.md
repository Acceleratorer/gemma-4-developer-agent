# Public model screen — 2026-11-27

Checked Kaggle model listings and model-card metadata with the Kaggle CLI at 2026-11-26 17:31 UTC / 2026-11-27 00:31 Vietnam time. This was a metadata and evidence screen only; no model weights were downloaded or loaded. Local metadata and the related notebook output are under ignored `data/local/research/public-model-screen-2026-11-27/`.

## Candidate cards

| Model | Kaggle metadata | Evidence and limitation |
|---|---|---|
| [Scott Weeden — Gemma 4 31B SWE Tool-Use LoRA](https://www.kaggle.com/models/scottweeden/gemma-4-31b-swe-tool-use-lora) | Transformers `main-lora`, v2; rank 16; 244,982,949 bytes (234 MiB); Apache 2.0. The card describes 83 assistant-turn samples from 22 resolved A1 runs on 14 of 81 public repo-train tasks. | The model card says its Rich-fold resolve-rate comparison was pending because of GPU quota. It gives no competition score or completed held-out resolve result. Its training distribution includes A1's prompt and graph-tool policy, so compatibility with our current prompt needs a controlled test. |
| [King-damon — Gemma 4 Dev Agent WSP Policy Adapter](https://www.kaggle.com/models/kingdamon/gemma-4-dev-agent-policy) | Two Apache 2.0 variations: a 75,691,975-byte PyTorch `.pt` policy checkpoint; and a 189,015,903-byte rank-32 PEFT LoRA. | The `.pt` card describes serialized-state/action-embedding inputs and action logits, not a drop-in `main_lora`. The rank-32 card claims lower held-out cross-repository token loss (0.0230 → 0.0123) on its own setup, but reports no resolved-task rate or Kaggle score. Confirm the scorer's rank support and prompt compatibility before any trial. |
| [Robina Mirbahar — Gemma 4 31B Loop-Breaker & Code-Graph LoRA](https://www.kaggle.com/models/robinamirbahar/gemma-4-31b-loop-breaker-lora) | Transformers `v1-main-and-tool-lora`; rank 4; 655,008 bytes; Apache 2.0. The card describes separate main/tool adapters for a graph-enabled agent. | Its [G-CCR & Trap-25 verification kernel](https://www.kaggle.com/code/robinamirbahar/gemma-4-loop-breaker-g-ccr-trap-25-verification) reports 24/25 for its adaptive arm, but the notebook sets `BACKEND = 'markov-theory'`: a zero-GPU analytical simulation, not live Gemma inference. The code generates 25 synthetic trap tasks rather than evaluating the competition's task set. Its ZIP contains four config/skill files and omits the model-card adapter weights. The reported 24/25 is not a Kaggle score or agent-evaluation result. |

## Decision

No screened model has verified task-resolution evidence that justifies changing the current candidate. Keep LoRA evaluation behind the paired V5/Patchsmith core and holdout. If quota and the final-upload buffer remain afterward, first validate serving compatibility, then run the adapter against the same frozen task IDs, model, seed, tools, and budgets; promote only if task-level resolved outcomes and the holdout support it. See [`milestone/DEFERRED.md`](../milestone/DEFERRED.md).
