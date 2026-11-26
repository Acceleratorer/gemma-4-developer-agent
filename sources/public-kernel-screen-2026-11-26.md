# Public kernel screen — 2026-11-26

Checked at 2026-11-26 08:20 UTC with the Kaggle CLI competition-kernel listing. The relevant Sankalp source is retained as text under ignored `data/local/research/public-kernel-screen-2026-11-26/sankalpsthakur/`; no notebook was executed. Three unrelated notebook copies were removed after screening.

## Sankalp Thakur's paired rerun study

[Gemma 4 agent: a setting change looks like a rerun](https://www.kaggle.com/code/sankalpsthakur/gemma-4-agent-a-setting-change-looks-like-a-rerun) was `COMPLETE` at the check; Kaggle listed its last run at 2026-11-25 17:58 UTC. The notebook embeds a `RUNS_CSV` with task-level rows and computes its paired tables from those rows. The pulled notebook has no saved cell outputs, so the reported calculations were not independently rerun here; its inference results remain the author's evidence, not ours.

The author reports 291 paired task comparisons across eight one-change tests. Identical-bundle reruns disagreed on 42/481 task outcomes (8.7%); changed bundles disagreed with controls on 20/195 (10.3%). Eleven public draws of one unchanged bundle ranged from 7/58 to 12/58. These findings reinforce paired evaluation and caution against promoting a candidate from one public score.

The most task-specific result is a reproduction-command `timeout 20` prompt line: the author reports `rich_3480` resolved in 4/4 such runs and 0/6 runs of the corresponding `fast` bundle. Across both 43-task runs, totals were 20 vs 17 and 19 vs 18; pooled discordant outcomes were 6 vs 2 (exact McNemar p=0.29), so the resolved-count gain was not established. The notebook separately reports that lowering thinking budget from 4096 to 1024 reduced mean time by 46 seconds per task (95% interval -92 to -1) without a statistically established resolved-count difference (10/23 vs 9/23). A prompt demanding a text call-number preamble before every tool call performed poorly (0/24 vs 8/24); do not add such a preamble.

`rich_3480` is present in our staged 53-task core notebook. Our exact Patchsmith candidate already bounds focused verification commands at 35 seconds and has a 60-second tool timeout; Budget-Fit V5 uses a 240-second tool timeout. The public study's `timeout 20` was a command prefix for reproduction, not an evaluated change to our candidates. Keep the staged V5/Patchsmith paired core and unseen holdout order: this source supports inspecting the `rich_3480` trace, but its overall timeout comparison is inconclusive and does not justify replacing an arm before the controlled run. Consider a separate timeout-focused comparison only if the core and holdout leave quota and submission time.

## Other recent kernels

- [Huy Pham Thai's TPU v5e-8 public benchmark](https://www.kaggle.com/code/huypt94/tpu-v5e8-public-benchmark) contains one JAX smoke cell for device discovery and basic numerical operations. It does not load Gemma or vLLM, so it provides no evidence that our queued Gemma QAT smoke will start or fit in HBM.
- [PARKWAVE_1's notebook recode rebuttal](https://www.kaggle.com/code/parkwave1/notebook-recode-rebuttal) is a jina-ColBERT text-retrieval/RVQ pipeline, unrelated to coding-agent evaluation.
- [xvmhieu's linear-merging diagnosis](https://www.kaggle.com/code/xvmhieu/linear-merging-diagnosis-l4x4) is a Qwen2.5-3B cross-lingual LoRA-merging study, unrelated to this competition's Gemma SWE agent.

## Decision

No newly inspected kernel changes the reset-week experiment sequence. The Sankalp study's task-level, repeated evidence is useful context but supplies neither an exact winning bundle nor a source-to-score link for our candidate. Preserve the staged comparison and treat every external score or task result above as author-reported.
