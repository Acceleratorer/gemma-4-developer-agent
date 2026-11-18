# Optimization plan

## Goal

Reach rank 1 on the final Kaggle private leaderboard. Current evidence is only a public-leaderboard snapshot; no project submission has a verified score yet. Continue optimizing until the final deadline and claim success only after the private leaderboard confirms it.

## Deadlines

- Entry and team-merge deadline: 2026-11-25 23:59 UTC (2026-11-26 06:59 Vietnam time).
- Final submission deadline: 2026-12-02 23:59 UTC (2026-12-03 06:59 Vietnam time).
- Optional paper-track deadline: 2026-11-12; passed.

## Milestones

### M0 — Clean, reproducible workspace

- [x] Preserve the imported notebooks under `notebooks/source/` and record their source links.
- [x] Extract reference submission configs into separate local-only folders.
- [x] Add a deterministic ZIP builder and focused tests.
- [ ] Run the package tests and build the 31B and E4B archives.

### M1 — Comparable development evaluation

- [x] Define and freeze a four-task smoke set with one task each from FastAPI, Rich, Requests, and HTTPX; retain the 14-task development set for broader checks.
- [ ] Run the reference 40-call configuration and the current candidate on the same tasks/model.
- [x] Record current-candidate smoke runs, including per-task outcomes, patches, and config hashes. V2 exposed context overflow at 16,384 output tokens; V4 restored 8,192 but scored 0/4. V5 still scored 0/4 but corrected the malformed `write_file` loop and captured verifier output: FastAPI imported the wrong new module path, Rich had 12 failures, Requests had 185 recursive `httpbin` fixture errors, and HTTPX failed collection because `httpx.Stream` was missing.
- [ ] Reject prompt changes that improve one or two tasks while reducing aggregate pass rate.

### M2 — Improve general leaderboard candidate

- [ ] Tune prompt flow and call/time budget first; keep model and sampling fixed.
- [x] Re-run the fixed smoke set with the `write_file` argument reminder and captured verifier diagnostics; the v5 results are recorded in `/log/experiment-log.csv`.
- [ ] Separate candidate failures from baseline verifier issues on Requests and HTTPX before using the four-task smoke score to select prompts.
- [ ] Ablate code-graph tools and a read-only analyzer separately.
- [ ] Try LoRA only after the no-adapter prompt baseline is repeatable and scorer compatibility is verified.
- [ ] Run a full Kaggle public submission only after fixed-set evaluation improves.

### M3 — Compete for the small-model prize

- [ ] Compare E4B and E2B with the same prompt and fixed task set.
- [ ] Keep the better small-model variant as a separate eligible submission.
- [ ] Use the two final-selection slots for the strongest distinct candidates.

### M4 — Final selection and audit

- [ ] Verify Kaggle submission IDs, public scores, model variants, and selected final submissions.
- [ ] Check the private leaderboard after the competition closes.
- [ ] Update this plan and the log with the verified final result.
