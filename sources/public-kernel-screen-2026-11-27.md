# Public kernel screen — 2026-11-27

The initial Kaggle CLI check was at 2026-11-26 17:31 UTC / 2026-11-27 00:31 Vietnam time. A follow-up at 18:17 UTC found one active public experiment, recorded below. Notebook source and outputs are preserved only under ignored `data/local/research/`; no public notebook was executed locally.

## Evgen Dvorkin — `rich_3894`

The latest listed run of [Gemma 4 | rich_3894: 41/42 → 42/42](https://www.kaggle.com/code/evgendvorkin/gemma-4-rich-3894-41-42-42-42) was `COMPLETE` at 2026-11-26 18:49:28 UTC. The notebook concerns one Rich issue, `rich_3894`; its 41/42 → 42/42 title is a test count for that issue, not 42 benchmark tasks or a leaderboard score. The notebook describes four skipped tests.

The latest run's log verifies 28 agent files, creates a ZIP with SHA-256 `63DA26AB6658E95E1D839565A05734E2979342B2E9C9CD891138096A6366181F`, and converts the notebook to HTML. It reports that P18 uses Luis Specian's MIT-licensed V24 repository-tools agent and preserves the P16 executable agent, prompts, sampling, and limits. The log has no Gemma inference, task-resolution summary, or Kaggle score. The 28-file V24/P18 bundle is distinct from the six-file `module/agents/idris-v24` candidate; do not treat the run as a comparison against that local candidate.

**Decision:** this is a source/package verification rerun on one task, not evidence of a new agent gain. It does not change the frozen seed-42 53-task V5/Patchsmith core or the paired 18-task holdout.

### Follow-up — checked 2026-11-26 21:32 UTC

The Kaggle CLI now lists the 18:49 UTC run as latest and reports `COMPLETE`. Its downloaded log shows 28 agent files verified, the same ZIP SHA-256 `63DA26AB6658E95E1D839565A05734E2979342B2E9C9CD891138096A6366181F`, and notebook-to-HTML conversion; it contains no Gemma inference, task-resolution summary, or competition score. The 42/42 figure remains a test count from the single-issue notebook, not an agent or leaderboard result. The refreshed source, log, and output archive are preserved under ignored `data/local/research/refresh-2026-11-26-2128utc/`.

## Engziadsamer — `arms-again`

At 2026-11-26 18:20 UTC, Kaggle still reported [arms-again](https://www.kaggle.com/code/engziadsamer/arms-again) as `RUNNING`. The pulled notebook metadata attaches the competition wheelhouse, `rodrigospalma/ood45-bugfix-split`, and Gemma 4 31B QAT v2; internet is disabled. This run uses a custom `skill_arms` evaluation mode and task set, so it is not directly comparable to our fixed 53-task run.

The Kaggle logs endpoint returned no text at 18:17 UTC and the output fetch exposed no files at 18:20 UTC. At that check, `RUNNING` confirmed an active kernel only; it did not confirm completed inference, resolved tasks, or a competition score.

### Outcome — checked 2026-11-26 19:48 UTC

Kaggle later reported the kernel `COMPLETE`. Its downloaded log and outputs are under ignored `data/local/research/arms-again-complete-output-2026-11-26-1945utc/`. The run loaded Gemma 4 31B QAT on four Nvidia L4 GPUs and evaluated one `sk_a2` arm on nine custom `rtrain` tasks from `/kaggle/input/datasets/ziadsamer/rebench-new-cp312/rebench`, repeating the same task IDs for three passes at concurrency 2. Its actual run log selects `skill_arms`, a 28-call cap, 240-second command timeout, eight-minute task cap, and 80 turns. The base `submission/eval_config.yaml` says 15 minutes; the active arm's `submissions/sk_a2/eval_config.yaml` and run log both say eight minutes.

The task-resolution counts were 5/9, 3/9, and 4/9 across the three passes: 12 resolved attempts out of 27 attempts, with one timeout. These are repeated results on nine tasks, not a 27-task score. The run has a single candidate arm and no paired baseline; it produces no Kaggle competition submission score. Treat it as exploratory evidence about that custom setup, not a promotion signal. It does not change the frozen V5/Patchsmith 53-task core or 18-task holdout.

## Jorgerome — `GemmaGraph-Agent`

Checked with the Kaggle CLI at 2026-11-26 23:07 UTC. The latest listed run was `COMPLETE` at 22:56:14 UTC on a Tesla T4. The [notebook](https://www.kaggle.com/code/jorgerome/gemmagraph-agent) and its output were pulled to ignored `data/local/research/gemmagraph-agent-2026-11-26-2303utc/` for static inspection; the notebook was not executed locally.

The run is a submission-builder/package demo, not an agent evaluation. Its log says no model was found under `/kaggle/input/` and takes an offline fallback that writes placeholder LoRA files. The published code hard-codes the 692-task telemetry and 84.6% pass rate in the function that writes `paper_metrics_summary.json`; it also constructs the comparison table from constants. Each `adapter_model.safetensors` is only 39 bytes (`SAFE_TENSORS_PAYLOAD_FOR_ADK_VALIDATION`), and the generated submission ZIP is 2,376 bytes. The log shows setup, synthetic fixture generation, syntax smoke check, static metric export, ZIP creation, and notebook-to-HTML conversion; it has no Gemma inference, competition task-resolution results, or Kaggle submission score. Therefore, neither the 84.6% claim nor the `COMPLETE` status is evidence of a competition result.

The code also contains a token-shaped literal as an `HF_TOKEN` fallback. We did not use it or verify whether it is valid; do not copy it into our environment. This audit does not change the frozen V5/Patchsmith comparison or its experiment order.

## Follow-up — checked 2026-11-26 23:55 UTC

The Kaggle CLI search surfaced [Pajak Chaithongchai's `Gemma 4 Developer Agent Competition`](https://www.kaggle.com/code/pajakchaithongchai/gemma-4-developer-agent-competition), whose current kernel status is `ERROR`. Its pulled notebook is preserved under ignored `data/local/research/pajak-gemma4-developer-agent-2026-11-26-2350utc/`; SHA-256 `3EF67487361414651FAE49C35B87FD11959F8055E496854FE2CFB0550EB084BE`. The execution log fails in the first code cell after 12.14 seconds with `NameError: name 'true' is not defined` on the JSON boolean `"enableCodeExecution": true`. Metadata attaches no GPU, TPU, dataset, competition, or model input. No task evaluation, agent result, or score was produced. The unexecuted manifest in a Markdown cell is not a runnable submission. This is not a candidate or performance result and does not change the staged comparison.

## Tuyến Nguyễn — `mainmainmain`

Checked with the Kaggle CLI at 2026-11-27 00:11 UTC. Kaggle reports the kernel as `COMPLETE`; its latest run is dated 2026-11-25 09:23 UTC. The pulled notebook SHA-256 is `7A7754E4B8F3BB43A7732C6C61E01BD0643E2C4D03F49238087A0BE68BDD3A6B`. Metadata enables an Nvidia L4 GPU, disables internet, lists the Gemma 4 Developer Agent competition as a source, and attaches no Kaggle model source.

The notebook describes **EvidenceKD-MedVQA**, a VinDr chest-X-ray pipeline: detector and decision-branch training, anatomical regions, optional MedGemma teacher/distillation, optional Flan-T5 generator, and VQA/localization reports. The competition-source metadata is not evidence that this notebook runs the coding-agent benchmark. Its source has no SWE-Gemma task runner, coding-agent bundle, or competition submission flow.

The downloaded run log says `OFFLINE = True`; no MedGemma base with a vision tower was attached, so the MedGemma teacher/KD and pretrained/B4 baselines were skipped. The notebook still trained/evaluated its separate VinDr pipeline and reports author-side validation/test metrics, including VQA accuracy/F1 of 0.822/0.558 on 659 validation examples and 0.834/0.582 on 300 test examples. The log says it wrote a 1,172 MB `evidencekd-full.zip` for resuming that pipeline. These are not Gemma coding-agent task scores or Kaggle competition leaderboard results.

The notebook and raw run log are retained only in ignored `data/local/research/tuyen-mainmainmain-2026-11-27-0011utc/`; the large output bundle and unrelated derived data were not retained. **Decision:** this kernel adds no comparable agent-performance evidence. Keep the frozen seed-42 V5/Patchsmith 53-task core and 18-task holdout unchanged.

## Follow-up — checked 2026-11-27 10:42 UTC

### Dheeraj Piduru — `what-moved-the-score-and-what-didn-t-e4b-31b`

The [notebook](https://www.kaggle.com/code/dheerajpiduru/what-moved-the-score-and-what-didn-t-e4b-31b) ran at 06:05:59 UTC and completed. Its two-cell CPU package builder has no internet or model accelerator; it writes a submission ZIP and does not run the agent evaluator. The output contains four runtime files. Their bytes exactly match the four runtime files in `module/agents/budget-aware-v2-no-graph-v1/`.

The write-up reports two public draws for its 31B v8 package, 0.20 and 0.17 (11/58 tasks on average), and six E4B draws from 0.03 to 0.08. Its E4B local study reports 11/115 resolved at 4,096 thinking tokens versus 10/115 at 1,024; three 31B-to-E4B adapter attempts did not improve held-out solves. These are author-reported results, not independently reproduced. The identical runtime files make v8 a useful external reference for the local no-graph candidate, but the two public draws do not establish a reliable gain over our 0.18 V5 draw. Keep the candidate separate from the frozen pair.

### Ayush Barai — `version-1-added-adaptor`

The [notebook](https://www.kaggle.com/code/ayush04barai/version-1-added-adaptor) completed at 10:25:10 UTC. Its metadata disables GPU and internet and attaches the competition only. It packages an adapter from [the author's training notebook](https://www.kaggle.com/code/ayush04barai/lora-step-2): Gemma 4 31B, rank 16, 90 LoRA modules targeting `down_proj`, `o_proj`, and `q_proj`, with 54,503,808 bytes of weights. The log checks non-zero `lora_B` tensors and the base-model name. The 40.6 MB output ZIP contains the agent config, prompt, sampling/evaluation config, and adapter; it has no `LICENSE` or `NOTICE`. The builder does not run task inference, and no competition score or resolved-task result is reported. Keep the weights out of the repository and require license plus evaluator evidence before considering this adapter.

**Decision:** these code-page updates do not change the primary experiment order. Dheeraj's v8 is preserved as a separate candidate; Ayush's adapter remains an unscored external artifact. The core and holdout kernels still report `COMPLETE`, while the 10:42 UTC output-file checks returned no files for either run.

## Follow-up — checked 2026-11-27 11:11 UTC

### Flexonafft — updated `Gemma 4 | Budget-Aware - Short-Prompt`

The Kaggle CLI lists the [notebook](https://www.kaggle.com/code/flexonafft/gemma-4-budget-aware-short-prompt) as last run at 10:53:57 UTC and `COMPLETE`. Its metadata attaches the competition only, with no GPU, TPU, Kaggle model, dataset, or source-kernel input. The downloaded output contains a 1,858-byte `submission.zip` with SHA-256 `44de36285f5714be29fb7e22085641325c22fbf57b4e56903d0797f5c051b4b1`; the ZIP has four runtime files and passes its CRC check. The execution log validates the configuration, packages the ZIP, and explicitly says model compilation and leaderboard scoring were not run. `COMPLETE` here is package conversion, not agent inference.

The notebook's short prompt uses 28 tool calls, a 10-minute task cap, 1,024 thinking tokens, and a 240-second command timeout. It proposes a focused behavior check before editing and repeats that same check afterward, capped at 30 seconds, while requiring a non-empty patch. The notebook identifies submission `58886757` at 0.18 as its *baseline*; it reports no score or evaluation for this updated variant. The generated ZIP has no `LICENSE` or `NOTICE`, and the pulled metadata declares no license field, so keep the external source out of the repository and do not copy its bundle.

**Decision:** retain this as an unscored prompt hypothesis for later independent implementation and paired evaluation. Its 10-minute cap adds two minutes per task versus our frozen 8-minute comparison and has no measured gain. It does not change the scheduled core or holdout candidates.

## Follow-up — checked 2026-11-27 11:45 UTC

### Allan Kipruto — `Getting Started - Gemma 4 Developer Agent`

Kaggle listed the [kernel](https://www.kaggle.com/code/allankipruto/getting-started-gemma-4-developer-agent) as last run at 08:49:51 UTC and returned `COMPLETE`. Its metadata enables an Nvidia L4, disables internet, and attaches the official competition, wheelhouse, and Gemma 4 31B QAT v2. The notebook uses a separate `tasks2.jsonl` dataset and its run log evaluates only `fastapi_14786` and `rich_3518`; this is a two-task author-side run, not a competition submission score. The notebook source and raw Kaggle logs are kept under ignored `data/local/research/kernel-screen-2026-11-27-1145utc/allan-default/`; the notebook SHA-256 is `3705C3FAC477B83645256D497DD818BABAF60FFABC515E4ECABEEC2AD0B2A594`.

The log shows `fastapi_14786` unresolved: the model rejected an 8,192-token output request with at least 24,577 prompt tokens against a 32,768-token context window. `rich_3518` resolved with a 2,053-character patch in 20 tool calls. Our [current sampling config](../module/agents/current/configs/sampling.yaml) uses the same 8,192 output cap and 4,096 thinking budget, so the failure is a relevant risk signal, not a result for our candidate.

**Decision:** keep the staged seed-42 V5/Patchsmith core and holdout unchanged so their paired comparison stays exact. Inspect their task-level summaries for context-window failures before deciding whether to test a lower output cap; this two-task, single-arm run does not justify a candidate change or promotion.

## Follow-up — checked 2026-11-27 12:07 UTC

### Recent code-page runs

- Kaggle lists a new 11:50:37 UTC run of [Evgen Dvorkin's `rich_3894` kernel](https://www.kaggle.com/code/evgendvorkin/gemma-4-rich-3894-41-42-42-42) as `COMPLETE`. Its only listed output is an 871-byte `submission.zip` with the previously observed SHA-256 `63DA26AB6658E95E1D839565A05734E2979342B2E9C9CD891138096A6366181F`; the filtered log shows package/archive verification and no inference result.
- Kaggle lists [Nthday's `dich-qwen`](https://www.kaggle.com/code/nthday/dich-qwen) at 11:57:01 UTC as `COMPLETE`. The notebook source describes an offline Chinese-to-Vietnamese translation pipeline and uses OCR/voting datasets; it does not run the Gemma developer-agent evaluator. Its listed output artifacts date to 2026-11-23, so no new coding-agent result is available from this run.

At 12:07 UTC the paired V5/Patchsmith core and holdout kernels still reported `COMPLETE`, but both Kaggle output-file listings were empty. These code-page updates add no comparable agent result and do not change the staged experiment order.

## Local V5 trace context check — checked 2026-11-27 12:32 UTC

The existing `evals/results/train-gold-44-v5-40-calls/output/dev_results/` contains 44 task traces and 1,192 model-call metric records. The maximum recorded prompt was 19,359 tokens, the maximum recorded total for a call was 20,255 tokens, and the largest completion was 5,100 tokens. No prompt exceeded 24,576 tokens, and no context-window error was recorded. With the current 8,192-token output cap, the largest observed prompt plus the full requested output allowance is 27,551 tokens, 5,217 below the reported 32,768-token context limit.

This is an older local 44-task 40-call V5 run, not the staged 53-task V5/Patchsmith pair or its Kaggle run. Allan Kipruto's separate `fastapi_14786` run exceeded the limit with at least 24,577 input tokens plus an 8,192-token output request. Keep the staged pair unchanged; inspect its actual summaries and traces after the reset run before considering a lower cap. The earlier public-kernel note records the two-task run and its limitations.
