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

## Follow-up check — 2026-11-26 09:59 UTC

- The latest-run competition listing surfaced `narenthirabalaji/gemma4-submission` (last run 04:35 UTC, `COMPLETE`). Its metadata disables GPU and TPU and lists no model or data sources. The log installs a PyTorch wheelhouse, checks the one-agent / eight-minute / 28-call / 240-second configuration, and explicitly says official model compilation and leaderboard scoring were not run. Its four-file ZIP has SHA-256 `20e1540ca605857db0cf6f9b3738edc0f3784b3a74811e9e356a94cb9fa5e659`; the kernel metadata provides no license field. Treat it as a packaging reference, not score evidence or reusable source. Pulled files are under ignored `data/local/research/public-kernel-screen-2026-11-26-0959utc/narenthirabalaji/`.
- Evgen Dvorkin's `gemma-4-rich-4076-20-24-14-experiments` completed at 08:10 UTC. Its metadata disables GPU and TPU; the output log only verifies the four P15 files and packages them. The archive SHA-256 `aa9d6f89f5299d16c9a2261e80cb75d2e369464cb5029ec4aef4d5790d4e91dc` matches the included Apache-2.0 attribution notice for unmodified Budget-Fit V5. No evaluator inference ran, so this is not new score evidence. Pulled files are under ignored `data/local/research/public-kernel-screen-2026-11-26-0959utc/evgen/`.
- Ziad Samer's generation and skill-arm kernels last ran at 09:14 and 09:16 UTC and still reported `RUNNING` at the 09:56 UTC check. Their listed output artifacts were created on 2026-11-25, before those runs; no fresh task-level result was available.

**Decision:** these checks add no comparable agent result or source-to-score link. Keep the paired V5/Patchsmith 53-task core and unseen 18-task holdout as the next controlled comparison.

## Competition pages and follow-up — checked 2026-11-26 15:13 UTC

- The public [discussion thread](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/761941) reports 31B same-bundle public draws of 9/58 and 12/58; on a 40-task holdout, its baseline and three prompt variants each scored 18/40. Its E4B fixer/reviewer pipeline scored 7/40 and 8/40 on repeat runs, with the author attributing many failures to malformed `edit_file` old-string matches. These are author-reported results, not independently reproduced here. They support keeping the base model fixed, pairing candidates on identical tasks, and treating small score changes as inconclusive.
- The same author recommends repeating a 40-task holdout; our planned GPU budget cannot safely cover that in addition to the 53-task core and 18-task holdout. Keep the staged sequence and treat a one-task holdout swing as weak evidence; do not promote a candidate on one public draw.
- The competition [Models tab](https://www.kaggle.com/competitions/gemma-4-developer-agent/models) displayed best public scores of 0.20 (31B QAT), 0.05 (E4B QAT), and 0.03 (12B QAT). The official [small-model leaderboard notebook](https://www.kaggle.com/code/ryanholbrook/gemma-4-developer-agent-small-model-leaderboard), version 37, showed a 0.12 top score in its output. These are current page outputs, not controlled model comparisons or verified final/private scores.
- The [queue update](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/760471) still states Kaggle staff's 20–24-hour estimate from November 19. Recent comments include participant reports over 30 hours and a completed run without a public score. No newer official ETA was visible, so keep those reports labeled as anecdotes and preserve the 72-hour upload buffer.

**Decision:** no new evidence changes the reset-week experiment order. Continue with the staged 53-task paired core and 18-task unseen holdout; keep the 31B model and sampling fixed. Treat the forum numbers as directional context only.

## Follow-up public kernel screen — checked 2026-11-26 15:26 UTC

Kaggle's competition-kernel listing surfaced Evgen Dvorkin's [Gemma 4 | rich_4076: 20/24 — Fourteen Experiments](https://www.kaggle.com/code/evgendvorkin/gemma-4-rich-4076-20-24-14-experiments). The notebook is a one-issue diagnostic series on `Textualize/rich`'s `rich_4076`, not a broad benchmark. Its embedded report records **0/14 resolved episodes**. Eleven completed validations passed 20/24 tests; passing most tests did not satisfy the evaluator's resolved outcome. The included Budget-Fit V5 P15 control and the original Patchsmith episode both report 20/24 and `resolved=false`.

The report isolates two actionable failure modes on this issue. P11 made 44 consecutive invalid tool-format calls; its author says no probe executed and cannot distinguish generation from parsing as the cause. P12 reproduced the newline behavior but ended without a patch. These traces are useful diagnostics for the gap between identifying a defect and delivering a valid repair, but one issue and repeated variants do not estimate hidden-task performance or support promoting a candidate. No new comparable multi-task result or source-to-score link was found.

**Decision:** keep the staged V5/Patchsmith seed-42 53-task core and unseen 18-task holdout unchanged. If those runs leave quota and time, inspect our `rich_4076` trace and consider a narrowly scoped tool-format/newline follow-up; do not replace a paired arm based on this one-issue report.

## Follow-up public kernel screen — checked 2026-11-26 15:43 UTC

The Kaggle Code listing showed [Anh Tuan Nguyen's v2 lab GPU run](https://www.kaggle.com/code/anhtunnguyen/getting-started-gemma-4-developer-agent-6119c5) as `COMPLETE`, last run at 15:16 UTC. The notebook expects Gemma 4 31B on L4×4. Its E13 arm uses temperature 0.2, top-p 0.95, 1,024 thinking tokens, a 6,144-token output cap, 40 tool calls, eight minutes, and a 120-second tool timeout. The downloaded report records 16/42 resolved (0.38), six empty patches, four run records with errors, 307 seconds mean agent time, and a 12.2-hour projection for 120 tasks with 60 seconds of assumed setup per task. These are the author's local-task results, not a Kaggle Public Score; the projected runtime exceeds the competition's 12-hour patch-generation limit.

The run provenance limits the comparison. The exported `runs.jsonl` contains 42 E13 rows started on 2026-11-23 between 13:06 and 16:48 UTC; the report's paired-comparison table is empty and contains no E5 rows, despite the README describing an E5 control. The included runner skips completed `(task, arm, rep)` pairs, so the listing's 2026-11-26 last-run time is not evidence of fresh E13 inference. Treat 16/42 as a single-arm external result, not a paired gain.

The E13 task IDs overlap 32 of our 53 training tasks and 10 of the 18 holdout tasks. The holdout is still unseen by our candidate runs, which were staged before this screen, but it is no longer community-unseen. Keep the already-staged V5/Patchsmith comparison; do not tune or promote using E13's per-task matrix. The public output and notebook are retained only in ignored `data/local/research/public-kernel-screen-2026-11-26-1543utc/anhtunnguyen/` (notebook SHA-256 `C272EA0A0741467DEBB43C783B8FB39CC7F14F91144F905C1F36C24E537BBB0A`; output ZIP SHA-256 `CBBAC3D1F0300CDF511F78017176CB2A1257F7ADBEFD09269B1A8BEAD096943D`).

**Decision:** this result does not justify changing the staged candidate or increasing our call budget. Keep the already-staged seed-42 paired run and interpret its 18-task arm as a fixed holdout relative to our prior evaluations, not as a globally unseen public set.
