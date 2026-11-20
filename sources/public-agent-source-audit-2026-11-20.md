# Public agent source audit — 2026-11-20

## Result

This pass did not find a public agent bundle with source-linked evidence of a **0.24** run. The [current leaderboard](https://www.kaggle.com/competitions/gemma-4-developer-agent/leaderboard) shows the score target, but does not map the leading teams to public agent files. One historical public source is tied to a reported 0.22 run, but repeat draws put it below V5 on average.

## Candidate checks

- **Flexonafft Budget-Aware v2, version 10:** Kaggle CLI pulled the [versioned source](https://www.kaggle.com/code/flexonafft/gemma-4-budget-aware-coding-agent-v2?scriptVersionId=357955943) and its output ZIP to ignored `data/local/research/flexonafft-v10-2026-11-20/`. The notebook log says it packages the ZIP without running model evaluation. A direct audit confirms the downloaded ZIP matches the four source files; ZIP SHA-256 is `6ff73d104725cc31deadd18787f3f55e5ce534889cec82387e3b280637d34887`, and `sha256(json.dumps(FILES, sort_keys=True))` is `56010e9e9d4c7f33856ce49d12ec3edae5c912261986e999a4aa989b3cd463cb`, matching the [Public Config Draws row](https://www.kaggle.com/datasets/dariushafshar/gemma-4-agent-public-config-draws) that reports **13/58 (0.22)**. The [current notebook page](https://www.kaggle.com/code/flexonafft/gemma-4-budget-aware-coding-agent) now shows only nine versions and best score **0.10 at v7**, so the old score is not visible there today. The companion [draw analysis](https://www.kaggle.com/code/dariushafshar/gemma-4-most-run-public-config-averages-10-58) records seven later runs of the same file hash at 7, 7, 8, 9, 10, 10, and 10 tasks (mean 8.71/58). Treat 0.22 as a real historical report tied to this source bundle, but a noisy high draw, not a repeatable score.
- **Hitarth “What Took LB 0.12 → 0.24”:** The [Kaggle notebook](https://www.kaggle.com/code/hitarthjain0/gemma-4-agent-what-took-lb-0-12-0-24) is a short analysis run, not a scored agent bundle. Its contract-first prompt idea is represented by the existing local `module/agents/short-contract-v1/` candidate and saved 44-task kernel `accelra/train-gold-44-short-contract-31b`; that candidate remains unrun. Do not add a duplicate candidate.

## Recommendation

Do not add the Flexonafft bundle to the first 44-task wave: its same-hash repeat mean is below Budget-Fit V5's 10/58 historical mean, and its current notebook page no longer exposes v10. If quota remains after the reference-v2, V5, corrected V5-40, and Hanh v6 comparisons, consider it as a lower-priority source-faithful candidate. Keep the existing short-contract kernel in the queue; do not add a duplicate prompt candidate.
