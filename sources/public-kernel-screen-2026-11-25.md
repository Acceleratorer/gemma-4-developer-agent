# Public kernel screen — 2026-11-25

Checked at 2026-11-25 08:24 UTC. Notebook sources were inspected as text and were not executed. The pulled metadata and notebook files remain under ignored `data/local/research/latest-public-kernel-screen-20261125/`.

## Nusrati's SWEKit GPU notebook

[gemma4-swekit-gpu-dev](https://www.kaggle.com/code/nusrati/gemma4-swekit-gpu-dev) describes a six phase, script driven workflow for Gemma 4. The notebook claims version 63 resolved 40 of 68 tasks on its local ruler and says version 69 changes the per task limit from five to eight minutes. These are author reported local results. The pulled notebook has no completed evaluation output for version 69. Kaggle's API reported the kernel `RUNNING` at 08:24 UTC, so that result is still pending. The author's account appears at 0.18 in the archived public leaderboard; that row does not identify this notebook's current bundle.

The Kaggle metadata lists an L4 GPU, 31B and E4B model inputs, and competition access. It does not provide a license field. Eight minutes is already the time cap in our current candidate setup, and there is no measured gain to support spending quota on a separate run.

## Robina's budget calibrated bundle

[Robina Gemma 4 Sovereign Budget Calibrated Agent](https://www.kaggle.com/code/robinamirbahar/robina-gemma-4-sovereign-budget-calibrated-agent) packages a 31B configuration with seed 42, temperature 0.2, thinking budget 3,584, 28 tool calls, and a seven minute task limit. Kaggle reported `COMPLETE`, but the notebook output log only shows configuration checks and ZIP packaging; it contains no agent evaluation. The author's account appears at 0.18 in the archived public leaderboard, with no verified link from that row to this ZIP.

The downloaded `submission.zip` is 2,029 bytes with SHA-256 `86892b2d6d4e1cc841f48062c0169c2a710e56543225e54ba766db9b6cd9f1de`. It contains `agent.yaml`, `eval_config.yaml`, `configs/sampling.yaml`, and `prompts/system.md`; it has no license file. The kernel metadata does not state a license. Keep the archive local and use the configuration only as a comparison reference.

## Sankalp Thakur's leaderboard update

Comparing the 08:03 and 08:38 UTC leaderboard snapshots shows team `sankalpsthakur` moving from 0.18 (41 submissions) to 0.20 (42 submissions), with its latest submission dated 2026-11-24 00:13 UTC. `kaggle kernels list --user sankalpsthakur --competition gemma-4-developer-agent` returned `Not found`, so no public competition kernel or exact source-to-score mapping was available to inspect. Treat the row as a public score change only; it does not provide a reproducible candidate.

## Decision

Neither notebook supplies verified task level evidence or a source to score mapping that changes the reset week experiment order. Keep the paired V5/Patchsmith core suite and unseen holdout as the first quota wave. Do not add either public bundle to the candidate set until a comparable evaluation shows a gain.

At the 08:24 UTC check, Kaggle reported 0.04 GPU hours and 18.70 TPU hours remaining, with both quotas refreshing at 2026-11-28 00:00 UTC / 07:00 Vietnam time. The local TPU smoke v5 remained `QUEUED`; Kaggle returned no queue ETA.

## Follow-up check — 2026-11-25 09:22 UTC

- Nusrati's `gemma4-swekit-gpu-dev` remains `RUNNING`. The latest pulled source is version 69; its stated change from version 63 is only the per-task cap increasing from five to eight minutes. The pulled notebook has 51 code cells with no execution counts or outputs, and the filtered Kaggle output request returned no log, summary, or result files. This is pending evidence, and the eight-minute cap already matches the current candidate.
- The latest-run kernel listing also surfaced `xvmhieu/linear-merging-diagnosis-l4x4`, which remains `RUNNING`. Its metadata and source notebook identify a Qwen2.5-3B cross-lingual LoRA-merging study using FLORES/SIB-200/Belebele data, not a Gemma SWE-agent candidate. Exclude it from agent comparisons.
- The full public leaderboard snapshot generated at 09:18:32 UTC still has 18 teams at 0.24; `Accelra` is rank 2,073 at 0.18. No newer scored public candidate was identified in this screen.

## Follow-up check — 2026-11-25 09:45 UTC

- Nusrati's `gemma4-swekit-gpu-dev` remains `RUNNING` at the latest status check. The Qwen LoRA study `xvmhieu/linear-merging-diagnosis-l4x4` is now `COMPLETE` and remains unrelated to this competition.
- Kaggle listed [Evgen Dvorkin's six-agent `rich_4076` notebook](https://www.kaggle.com/code/evgendvorkin/gemma-4-rich-4076-20-24-six-failed-agents) with a 09:29 UTC last-run time and reports `COMPLETE`. Its current output is package-only: metadata disables GPU and TPU, the output log verifies 8/8 P7 package files and repeats `rich_4076` at 20/24 with `resolved=false` and competition score unknown. The 15,606-byte `submission.zip` SHA-256 (`28c5ae6810e4ef9de3aee577be3ffe325cff1d9b80fbb0e64e2c365eceb14493`) matches the 2026-11-24 output exactly. This is not new agent inference or score evidence, so it does not change the reset-week experiment order. Pulled source and output are under ignored `data/local/research/public-recheck-20261125/`.
- The one-time core launcher passed `-ValidateOnly` at 09:44 UTC without attempting a push; the staged hashes match and Kaggle reports the core kernel `COMPLETE`. The scheduled task remains `Ready` for 2026-11-28 07:00 Vietnam time, with `WakeToRun` and `StartWhenAvailable` enabled.

## Follow-up check — 2026-11-25 10:30 UTC

- Kaggle search surfaced [Arsen's Reproducible Bundles and Evidence Audit](https://www.kaggle.com/code/arsen123/gemma-4-reproducible-bundles-and-evidence-audit). Its attached run dataset is Apache-2.0. The notebook combines Idris v31's 31B configuration with v30's multi-file completeness prompt and reports a historical 50-task completion-intersection comparison: hybrid 24/50, baseline 22/50; 6 hybrid-only and 4 baseline-only outcomes; exact McNemar p=0.754; repository-cluster bootstrap 95% interval for the paired gain [-0.082, 0.163]. The interval includes both losses and gains, so this does not establish an improvement. The sample came from 50 completed pairs out of runs with 50 baseline and 52 candidate records, leaving possible completion-selection bias; it used concurrent arms on one A100 rather than the competition L4 setup.
- The author reports the unchanged v31 submission scored 0.18 and hybrid submission 58831811 was still pending at the notebook's 2026-11-25 check. At 10:30 UTC Kaggle still reports the notebook `COMPLETE`; its metadata disables GPU and TPU, and its log shows analysis, packaging and synthetic control checks, not a new Gemma inference run. The author reports no raw traces for the 50-pair comparison. Its declared/attached Apache-2.0 licensing permits a future controlled evaluation, but there is not enough evidence to add it to the first quota wave.
- The public dataset's separate 66-task v30/v31 records are 33/66 for each policy, but that comparison changes more than the prompt: v30 uses a 240-second command timeout, 8,192 output tokens and a 4,096-token thinking budget; v31 uses 120 seconds, 4,096 output tokens and a 2,048-token thinking budget. Treat those records as confounded, not as a prompt-only result.
- **Decision:** keep the staged V5/Patchsmith core and paired holdout order. Revisit the completeness prompt only if the reset-week results leave quota and enough submission-scoring time; do not infer a public score for the hybrid from the pending report.

## Follow-up check — 2026-11-25 10:52 UTC

- Kaggle CLI still reports Nusrati's [`gemma4-swekit-gpu-dev`](https://www.kaggle.com/code/nusrati/gemma4-swekit-gpu-dev) as `RUNNING`; its latest listed run is 08:07 UTC. The previously pulled v69 source has no execution outputs, so no result is available to compare.
- Evgen Dvorkin's [`rich_4076` follow-up](https://www.kaggle.com/code/evgendvorkin/gemma-4-rich-4076-20-24-six-failed-agents) remains `COMPLETE`. Its last run is the already audited package-only artifact; there is no new agent inference or score evidence.
- Dennis's [`exact-budget-aware-package`](https://www.kaggle.com/code/dennis6886/gemma-4-agent-0-18-exact-budget-aware-package) is `COMPLETE`. Its downloaded log contains notebook conversion only, and its 3.08 KB ZIP contains four config files; no evaluator result or score-to-archive mapping is present.
- Kaggle denied `kernels.get` for the `ccuuuy/lb-0-22-4-config-files-no-training` slug. The source could not be inspected in this check, so its title is not treated as score evidence.
- **Decision:** no newly verified public kernel result changes the reset-week candidate order.
