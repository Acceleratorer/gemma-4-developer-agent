# Optimization plan

## Goal

Reach rank 1 on the final Kaggle private leaderboard. Current evidence is only a public-leaderboard snapshot; no project submission has a verified score yet. Continue optimizing until the final deadline and claim success only after the private leaderboard confirms it.

The 2026-11-18 public snapshot has a top score of 0.24 shared by 14 teams. Since Kaggle breaks score ties by earliest submission, target above 0.24 on the public split while treating the private leaderboard as the final result.

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
- [x] Re-run the fixed smoke set with the `write_file` argument reminder and captured verifier diagnostics; the v5 results are recorded in `/log/experiment-log.csv`.
- [x] Separate candidate failures from baseline verifier issues on Requests and HTTPX: a no-patch evaluation reproduced both failures.
- [x] Record the 14-task no-patch baseline (0/14) and freeze a nine-task `dev-valid` set that excludes the five known verifier environment failures.
- [x] Pin new Kaggle evaluation kernels to the competition-compatible Python 3.12 image; the unpinned reference attempt failed under Python 3.13, and the pinned reference comparison completed at 0/4.
- [ ] Ablate code-graph tools and a read-only analyzer separately.
- [ ] Try LoRA only after the no-adapter prompt baseline is repeatable and scorer compatibility is verified.
- [ ] Run a full Kaggle public submission only after fixed-set evaluation improves.

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
