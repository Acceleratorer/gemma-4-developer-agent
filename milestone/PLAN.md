# Optimization plan

## Goal

Reach rank 1 on the final Kaggle private leaderboard. Local fixed-set results are available, and public submission ref `58527796` is pending; no public score is verified yet. Continue optimizing until the final deadline and claim success only after the private leaderboard confirms it.

The latest public leaderboard check on 2026-11-19 03:22 UTC still has 14 teams tied at 0.24. Kaggle submission ref `58527796` for the 31B reference-budget-v2 candidate is pending; a 03:22 UTC CLI poll still showed no score. Since Kaggle breaks score ties by earliest submission, target above 0.24 on the public split while treating the private leaderboard as the final result.

Historical public config draws show that eight runs of one identical bundle scored between 7/58 and 13/58, so a single public score is noisy; use paired local comparisons before spending another daily submission.

## Deadlines

- Entry and team-merge deadline: 2026-11-25 23:59 UTC (2026-11-26 06:59 Vietnam time).
- Final submission deadline: 2026-12-02 23:59 UTC (2026-12-03 06:59 Vietnam time).
- Optional paper-track deadline: 2026-11-12; passed.

## Milestones

### M0 — Clean, reproducible workspace

- [x] Preserve the imported notebooks under `notebooks/source/` and record their source links.
- [x] Extract reference submission configs into separate local-only folders.
- [x] Add a deterministic ZIP builder and focused tests.
- [x] Run all five package tests and build the exact 31B archive for the tested 3/9 candidate; defer the E4B archive because its fixed-set score was 0/9.

### M1 — Comparable development evaluation

- [x] Define and freeze a four-task smoke set with one task each from FastAPI, Rich, Requests, and HTTPX; retain the 14-task development set for broader checks.
- [x] Run the reference 40-call configuration and current v5 on the same tasks/model; both scored 0/4. FastAPI still lacked the tested module path and Rich failed the tab-span assertions. Requests and HTTPX reproduced the no-patch verifier failures. The v6 smoke also scored 0/4: FastAPI again used the wrong module path, Rich failed 12 tests and added an unnecessary repro file, and the Requests/HTTPX verifier errors persisted; HTTPX also reached its time limit.
- [x] Record current-candidate smoke runs, including per-task outcomes, patches, and config hashes. V2 exposed context overflow at 16,384 output tokens; V4 restored 8,192 but scored 0/4. V5 still scored 0/4 but corrected the malformed `write_file` loop and captured verifier output: FastAPI imported the wrong new module path, Rich had 12 failures, Requests had 185 recursive `httpbin` fixture errors, and HTTPX failed collection because `httpx.Stream` was missing. A no-patch baseline run reproduced the Requests and HTTPX verifier failures, so those scores do not measure the agent patch.
- [ ] Reject prompt changes that improve one or two tasks while reducing aggregate pass rate.

### M2 — Improve general leaderboard candidate

- [x] Run v7 with the same 31B model, smoke tasks, and 40-call/eight-minute budget. It scored 0/4; the prompt constraints did not prevent FastAPI's wrong file path or Rich's failing source change. Use a hard call-budget ablation next.
- [x] Evaluate v8 with the v7 prompt and a 28-call cap on the same smoke set. It scored 0/4; Rich exhausted the cap without a patch and FastAPI retained the wrong path. Revert the cap and widen to `dev-valid` for the next 31B run.
- [x] Evaluate v9 with the v7 prompt, 40 calls, and the fixed nine-task `dev-valid` set. It scored 2/9 locally, passing FastAPI's license identifier docs example and File/Form body-order regression.

- [ ] Tune prompt flow and call/time budget first; keep model and sampling fixed.
- [x] Evaluate the imported `reference-budget-v2` prompt on 31B with the same `dev-valid-9` set and its 28-call budget; it scored 3/9, passing FastAPI tasks `15589` and `14492` plus Rich task `3278`, versus v9 at 2/9.
- [x] Review the saved `reference-budget-v2` traces before the next ablation. FastAPI `11194` left only `reproduce_bug.py` and failed two file/form-order checks; its trace shows time spent on a reproduction script without a source patch. FastAPI `15588` had six remaining failures across CR and CRLF values for SSE `event`/`id`. Rich `3472` changed only the `Column` docstring and still failed `test_dataclass_no_attribute`. FastAPI `15661` and Rich `3935` ended without a patch under the existing budget; Rich `3061` patched `rich/text.py` but failed tab-span and Unicode cases. Treat these as failure-mode evidence, not proof that a prompt change will fix them.
- [x] Validate the original nine-task Hanh v6 and graph-enabled artifacts: both use the same task IDs, 31B model, 28-call/eight-minute limits, and identical non-prompt files; only `prompts/system.md` differs. The archived Hanh notebook's four embedded agent files exactly match `evals/results/dev-valid-honghanhhh-v6-31b/source/honghanhhh-v6`, including registered graph tools, despite a conflicting secondary description. The wheelhouse dataset slug is `metric/gemma-4-developer-agent-wheelhouse`.
- [x] Run a CPU-only no-patch verifier screen on the 11 Requests tasks outside `dev`. Five tasks had issue-level test failures without fixture or collection errors (`requests_6757`, `requests_7205`, `requests_7309`, `requests_7315`, `requests_7427`); five hit recursive `httpbin` fixture errors; `requests_6644` passed without a patch. The diagnostic scored 1/11, which is not an agent score.
- [x] Add `evals/dev-valid-crossrepo-task-ids.json` and register `dev-valid-crossrepo` in the notebook builder. It preserves the fixed nine tasks and adds the five Requests tasks that fail on the expected issue assertions.
- [x] Prepare unique, unrun 14-task notebook artifacts for the reference-budget-v2 baseline, Hanh v6, and graph-enabled prompt. A static audit confirms the same task IDs, model, budgets, and runtime files; the two ablations differ from the baseline only in `prompts/system.md`.
- [x] Prepare two more 14-task single-factor notebooks: task-statement pinning appends `{problem_description}` and optional `{hints?}` to the system prompt while keeping 28 calls; none of the 14 tasks has hints, so this isolates the duplicated issue statement. The 40-call ablation changes only `max_tool_calls` from 28 to 40. Both keep the model, sampling, task set, and eight-minute cap fixed.
- [x] Prepare a 14-task short-contract prompt candidate from Hitarth's public ablation notebook. The source calls its prompt an unscored starting point; local traces show repeated exploration and late or absent edits, making its concise contract-first procedure worth testing. The candidate preserves the reference prompt's graph-tool prohibition, and static audit confirms only `prompts/system.md` differs from the baseline.
- [x] Pin 104 previously unseen FastAPI/Rich task IDs (61 FastAPI, 43 Rich) and launch CPU-only no-patch kernel `accelra/gemma-4-fastapi-and-rich-verifier-screen-v1` while submission `58527796` is pending. This adds broader development-set evidence without opening another GPU kernel.
- [x] Retrieve and classify the completed 104-task screen: 55 tasks fail only on issue tests, nine also fail unrelated tests, 35 fail collection, three time out, and two pass without a patch. Store per-task evidence under `evals/results/fastapi-rich-verifier-screen-v1/output/fastapi-rich-verifier-baseline/task-classification.json`.
- [x] Freeze and register `dev-valid-expanded` (20 tasks): preserve the 14-task cross-repository set and add six issue-only FastAPI/Rich tasks; keep the original sets unchanged.
- [x] Generate private, offline Python 3.12 notebooks for the 20-task reference-budget-v2 baseline and short-contract prompt; static audit confirms identical tasks, model, budgets, tools, and runtime files, with only `prompts/system.md` changed. Both remain unrun.
- [x] Generate private, offline Python 3.12 notebooks for the 20-task Hanh v6 and graph-enabled prompt ablations. Static audit confirms each matches the baseline in task IDs, model, budgets, tools, and runtime, changing only `prompts/system.md`; neither has been uploaded or run. The graph prompt also avoids bracket-containing values in `get_code_subgraph` arrays to reduce the reported vLLM 0.19.1 parser-hang risk on `fastapi_14616`.
- [x] Retrieve the Repair Lab's exact exp021 `score_022_submission.zip` via Kaggle CLI and prepare a 20-task source-bundle comparison. The local notebook keeps model, sampling, task set, call and time budgets fixed, and normalizes only `timeout_seconds` from 60 to 240; it retains Patchsmith's no-graph tool set and is not a prompt-only ablation. The archived source's reported 0.22 does not apply to this normalized, unrun candidate.
- [x] Inspect the `fastapi_11194` baseline trace: the agent applied a plausible source fix, then spent calls creating and running a scratch repro, reverted the source to check the no-patch case, and exhausted its call budget before restoring the fix. Prepare a prompt-only patch-preservation candidate that forbids no-patch controls/reverts and keeps checks in the task Python environment; its 20-task notebook matches the baseline in task IDs, model, tools, sampling, and budgets, with only `prompts/system.md` changed.
- [x] Pull the public icfoer notebook source and prepare its 3,728-character phase-based system prompt as `phase-budget-v1`, with no adapter. The author's 8/11 no-adapter result is from a different 11-task local held-out set, not a Kaggle score; the 20-task local notebook matches the baseline outside `prompts/system.md`.
- [ ] After submission `58527796` completes, establish the reference-budget-v2 baseline on `dev-valid-expanded` (20 tasks); the 3/9 nine-task result and future 14-task results remain separate historical comparisons.
- [ ] Run `phase-budget-v1` on the same 20 tasks after the reference baseline; keep model, sampling, registered tools, and budgets fixed.
- [ ] Then run `patch-preserve-v1` on the same 20 tasks; keep model, sampling, registered tools, and budgets fixed.
- [ ] Then run the short-contract prompt candidate on the same 20 tasks; keep model, sampling, registered tools, and budgets fixed against the reference baseline.
- [ ] Run the Hanh v6 prompt-only candidate on the same 20-task set, keeping model, sampling, tool budget, and time budget fixed.
- [ ] Then run the graph-enabled reference-budget-v2 candidate on the same 20 tasks as a separate prompt ablation; inspect array-valued `get_code_subgraph` calls and confirm the run does not stall after `fastapi_14616`.
- [ ] Run the normalized Patchsmith exp021 bundle on the same 20 tasks as a package-level comparison; record its different tool set and do not attribute the source archive's 0.22 public score to this local run.
- [ ] After Hanh v6 and graph results, run the prepared task-pinning and 40-call candidates separately; the public 0.22 notebook's score remains unverified locally.
- [ ] Check the 8-minute per-task cap against the competition-wide 12-hour runtime using public submission `58527796` before changing the budget.
- Preliminary local timing only: the nine-task reference run took 47.51 minutes total (mean 5.28, median 5.01, p90 7.53, max 8.12 minutes); three tasks took at least seven minutes. Linear scaling to 129 tasks would be 11.35 hours before setup, but the hidden task count and runtime distribution are unknown and this nine-task sample is not representative evidence. Keep the cap unchanged until submission `58527796` completes and its actual runtime is available.
- [x] Re-run the fixed smoke set with the `write_file` argument reminder and captured verifier diagnostics; the v5 results are recorded in `/log/experiment-log.csv`.
- [x] Separate candidate failures from baseline verifier issues on Requests and HTTPX: a no-patch evaluation reproduced both failures.
- [x] Record the 14-task no-patch baseline (0/14) and freeze a nine-task `dev-valid` set that excludes five verifier failures: missing `inline_snapshot`, recursive Requests `httpbin` fixtures, the Rich `/dev/tty` error, and the HTTPX no-patch import mismatch. The HTTPX snapshot exports `Stream` from `src/httpx/__init__.py` even though the verifier's imported `httpx` module lacks it.
- [x] Pin new Kaggle evaluation kernels to the competition-compatible Python 3.12 image; the unpinned reference attempt failed under Python 3.13, and the pinned reference comparison completed at 0/4.
- [ ] Test a read-only analyzer only if the graph-enabled run beats the current candidate.
- [ ] Try LoRA only after the no-adapter prompt baseline is repeatable and scorer compatibility is verified.
- [x] Run the first full Kaggle public submission after the fixed-set score improved to 3/9: ref `58527796`; CLI rechecks through 03:22 UTC still show `PENDING` with no score. At the latest check it had been pending about 4h42m; participant reports include multi-hour scoring, so this is not evidence of a failed run.

### M3 — Compete for the small-model prize

- E2B and E4B submissions are also eligible for the general leaderboard; an E2B/E4B final selection can compete for both the general ranking and the small-model bonus.
- [x] Compare E4B with the v9 prompt on the same `dev-valid-9` set: it scored 0/9 versus 31B's 2/9, despite much shorter per-task runtimes.
- [x] Compare E2B with the same prompt and fixed task set: 0/9, matching E4B; summed task runtime was 15.7 minutes versus 10.2 minutes for E4B.
- [x] Defer separate E2B/E4B submissions because neither small model resolved a task in the local fixed set.
- [ ] Use the two final-selection slots for the strongest distinct candidates.

### M4 — Final selection and audit

- [ ] Verify Kaggle submission IDs, public scores, model variants, and selected final submissions.
- [ ] Check the private leaderboard after the competition closes.
- [ ] Update this plan and the log with the verified final result.
