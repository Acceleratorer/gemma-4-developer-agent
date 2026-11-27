# Public Kaggle surface screen — 2026-11-27

Checked at `2026-11-27 17:56 UTC` (`2026-11-28 00:56` Vietnam time) with the authenticated Kaggle CLI and a read-only web check. The pulled notebook sources and metadata are preserved under ignored `data/local/research/public-kernel-screen-2026-11-28/`; no public notebook was executed locally.

## Canonical competition surfaces

- [Competition overview](https://www.kaggle.com/competitions/gemma-4-developer-agent)
- [Competition data](https://www.kaggle.com/competitions/gemma-4-developer-agent/data)
- [Competition code](https://www.kaggle.com/competitions/gemma-4-developer-agent/code)
- [Competition models](https://www.kaggle.com/competitions/gemma-4-developer-agent/models)
- [Competition discussion](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion)

The web pages are client-rendered, so the browser text view exposes the competition shell but not a complete authenticated listing. The CLI listing is the source for the dated inventory below. Public discussion findings remain in [`public-discussion-followup-2026-11-27.md`](public-discussion-followup-2026-11-27.md); no new organizer policy was verified in this screen.

## Code-tab inventory

The competition-code listing returned these relevant public entries. Hashes are for the downloaded `.ipynb` files and identify the exact source screened here.

| Notebook | Latest listed run | Metadata | Downloaded source SHA-256 | Evidence decision |
|---|---:|---|---|---|
| [Allan Kipruto — Getting Started](https://www.kaggle.com/code/allankipruto/getting-started-gemma-4-developer-agent) | 2026-11-27 14:49:47 UTC | GPU, NvidiaL4; official tasks, graphs, embeddings, wheelhouse, and all four Gemma variants attached | `3705C3FAC477B83645256D497DD818BABAF60FFABC515E4ECABEEC2AD0B2A594` | End-to-end starter/package and serving reference. The pulled notebook has no saved evaluator output or score. |
| [Dheeraj Piduru — What moved the score](https://www.kaggle.com/code/dheerajpiduru/what-moved-the-score-and-didn-t-e4b-31b) | 2026-11-27 06:05:59 UTC | CPU package builder; two cells | `93B39FCCC2F3B5971AF9291DEF7D3CC9D4A336A68DFB8DF4A877D5782BD7D4B6` | The write-up reports author-side 31B draws of 0.20 and 0.17 and E4B experiments, but the notebook only writes/verifies a ZIP. Treat scores as author-reported, not a paired reproduction. |
| [Flexonafft — Budget-Aware Short-Prompt](https://www.kaggle.com/code/flexonafft/gemma-4-budget-aware-short-prompt) | 2026-11-27 10:53:57 UTC | CPU package builder; no accelerator | `654616E3976856771C24B3A1F9E396259905639686B8D36FDB694ADE8A83777B` | A short-prompt/1,024-thinking-token hypothesis with configuration and CRC checks. It does not run model inference or leaderboard scoring. |
| [Ayush Barai — Version 1 added Adaptor](https://www.kaggle.com/code/ayush04barai/version-1-added-adaptor) | 2026-11-27 10:25:10 UTC | CPU package builder; attaches the author's `lora-step-2` notebook output | `33E179BA4AA2C3507DC9201EACB30EFDC1A49CBF227A5B1409458D095AB8CAF1` | Adds `adapter: main_lora` to an earlier six-tool 31B package and validates safetensor headers/values. The notebook contains no measured leaderboard score; its “usual range” is advice, not evidence. |
| [C R Suthikshn Kumar — TestGraph-AI](https://www.kaggle.com/code/crsuthikshnkumar/gemma4-testgraph-ai-code-comp-crsk) | 2026-11-17 16:07:41 UTC | GPU, NvidiaL4 | `DBC6ACF01D76A8201BB8142DEC7427C123765D8F93BADE87A3B8F58534777AED` | v1–v6 graph/prompt package builders; the notebook explicitly says it does not run the official evaluator. No comparable score evidence. |
| [Purnima Pathak — 72-task scorer](https://www.kaggle.com/code/purnimapathak15/score-gemma4-agent-on-72-scorable-tasks) | 2026-11-22 22:53:59 UTC | CPU package/self-test path; GPU path is optional | `C669BE360C19737D72827D4A783DB68B9DCA927E39837B5E68661C7E9970C7AC` | Reusable local scorer and gold/empty-patch controls. Its 72-task rates are local evidence, not hidden leaderboard scores; use paired runs in the same session. |

The web-rendered code index also surfaces [Black Cat SWE Agent | Second Strike](https://www.kaggle.com/code/azouzibillel/black-cat-swe-agent-second-strike), with a displayed 0.06 public score. Its source pull was forbidden by the API because the competition rules must be accepted for that resource, so this is web-only metadata and not a source audit. No entry in this screen supplies a verified, licensed, directly comparable improvement over the frozen seed-42 V5/Patchsmith pair. Keep the staged core and holdout unchanged until their own summaries pass the launcher gates.

## Models-tab recheck

The newest model search results included E2B/BFCL artifacts from LangZhe Lu, three generic Penguin SFT adapters, King-damon's policy adapter, Omallo's E4B distillation adapter, Robina Mirbahar's graph/loop-breaker adapters, and Scott Weeden's tool-use LoRA. The cards do not provide a new paired repository-repair result or a verified competition score for our 31B track. The detailed adapter evidence remains in [`public-model-screen-2026-11-27.md`](public-model-screen-2026-11-27.md); do not promote a model card from metadata alone.

## Decision

This screen adds documentation and provenance only. It does not change the candidate, task split, seed, model, prompt, or budgets. The next decision remains the quota-reset core run, followed by the conditional 18-task holdout if the exact output and quota gates pass.
