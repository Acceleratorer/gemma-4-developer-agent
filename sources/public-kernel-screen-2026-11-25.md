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
