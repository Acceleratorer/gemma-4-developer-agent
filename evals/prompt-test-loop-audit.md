# Test-aware prompt audit

## V1 pilot evidence

Private Kaggle kernel [`accelra/v5-test-aware-fastapi-rich-2-task-seed-42-pilot`](https://www.kaggle.com/code/accelra/v5-test-aware-fastapi-rich-2-task-seed-42-pilot) ran `fastapi_15588` and `rich_3061` with Gemma 4 31B, request seed 42, 28 calls, and an eight-minute task cap. It resolved 0/2 in 7.45 evaluator task-minutes and used 0.54 GPU hours (run `30f36d4e709e`). This is local training-task evidence, not a leaderboard score; the earlier V5 results on these tasks were unseeded.

Trace review found a workflow gap in the V1 prompt:

- **FastAPI:** The patch added both newline validators, but six assertions failed because the test expected an error matching `SSE 'event' must be a single line`; the patch said `must not contain newlines`. The agent ran a temporary script and submitted without running the existing focused test.
- **Rich:** The patch tried to carry the tab character's style onto generated spaces. The verifier still reported ten `test_tabs_to_spaces_spans` failures, plus two other failures, and the agent used all 28 calls. Its trace also shows an ad-hoc script rather than the existing regression test.

The observed issue is that V1's general instruction to inspect test failures did not make the agent use the repository's focused tests or compare exact expected and actual behavior before submission.

## V2 pilot

`module/agents/budget-fit-v5-test-aware-v2/` is a prompt-only follow-up to V1. It explicitly requires an existing focused regression test, prohibits substituting a temporary script, and tells the agent to inspect exact outputs and error messages, fix product failures, and rerun the focused tests. The model, tools, sampling, and budgets match V1.

The repeatable task set is `v5-test-aware-pilot` in `evals/build_kaggle_eval.py`, backed by `evals/v5-test-aware-pilot-task-ids.json`. The generated private notebook uses the same two IDs, seed 42, 28 calls, eight minutes, and NvidiaL4. Kaggle kernel [`accelra/v5-test-aware-v2-seed-42-2-task-pilot`](https://www.kaggle.com/code/accelra/v5-test-aware-v2-seed-42-2-task-pilot) version 2 was saved with `--no-run`; its `COMPLETE` status indicates notebook conversion only. No inference or GPU quota was used.

The V2 prompt SHA-256 embedded in that notebook is `94d53c0ebd18d073f754d6fb5c180aac281c8a8706d8d257eca23c93ba4b2ce4`.

## Single-task V2 probe

To use the remaining GPU quota for a high-signal screen, a separate one-task kernel ran `fastapi_15588` with the same model, seed, call limit, and task cap. Its repeatable task set is `v5-test-aware-fastapi-probe` in `evals/build_kaggle_eval.py`, backed by `evals/v5-test-aware-fastapi-probe-task-ids.json`. Private kernel [`accelra/v5-test-aware-v2-fastapi-seed-42-probe`](https://www.kaggle.com/code/accelra/v5-test-aware-v2-fastapi-seed-42-probe) version 2 completed at 0/1 (run `5b53002055fe`; 214.38 evaluator seconds; 16 tool calls; about 0.40 GPU hours). The task also failed in V1's same-seed pilot.

The V2 trace confirms that the prompt contained the new test instructions, but the agent read `tests/test_sse.py`, decided it lacked newline-validation coverage, used temporary reproduction scripts, and submitted without running the repository tests. The evaluator again reported six message mismatches: it expected `SSE '<field>' must be a single line`, while the patch said `must not contain newlines`. The V2 instruction did not change the task result or workflow on this case.

Do not promote V2 to a full 44-task comparison based on this evidence. Preserve its two-task notebook as an unrun artifact and prioritize the seed-42 V5 28-call control and disjoint 18-task holdout after the 2026-11-28 quota refresh. Keep the 40-call comparison lower priority because its earlier unseeded run tied V5 28-call at 20/44 while taking 26.43 more evaluator task-minutes.

## V5 repeat trace review — 2026-11-23

The exact V5 repeat on `dev-valid-expanded` scored 5/20; `rich_3061` remained unresolved. Its trace (`evals/results/dev-valid-expanded-budget-fit-v5-repeat-31b/output/dev_results/3a7eb3f3c6a5/traces/trace_rich_3061.json`) shows the agent spent several calls retrying searches that returned no match, then read the existing `Text.expand_tabs` and `Style` implementations. It submitted a patch using `Style(tab_style)` and `Style(span_style)`, although `Style.__init__` accepts keyword-only arguments. Its standalone `verify_tabs.py` then failed with `Style.__init__() takes 1 positional argument but 2 were given`; the agent spent the remaining calls inspecting the constructor and exhausted the 28-call budget without running the repository regression test. The patch also added that scratch verification script.

This is a confirmed failure mode for `rich_3061`, not evidence that a larger generic test instruction will help: V2 already asked for focused repository tests and exact failure inspection, but the FastAPI probe still ignored that instruction. Keep the current one-task validation-wording probe as the next quota-gated screen. Do not expand a prompt candidate based on this single trace; if the probe fails, prioritize the seeded V5 control and Patchsmith comparison on the active 53-task set, then the paired unseen holdout, as recorded in [`milestone/PLAN.md`](../milestone/PLAN.md).

## V5 44-task patch artifact scan — 2026-11-23

A static scan of `evals/results/train-gold-44-v5-31b/output/dev-eval-731c4e8cb5a6.json` found 24 unresolved tasks; 13 of those 24 failed patches include a root-level `repro*.py`, `reproduce*.py`, or `check_*.py` file, 12 used all 28 calls, and one produced no patch. This is a recurring workflow symptom, not proof that scratch files caused the test failures: `fastapi_11194` passed despite adding `repro.py`. The separate patch-preserve candidate made cleaner patches but scored 5/20 versus V5's 6/20 on its matched set. Do not spend quota on another cleanup-only prompt variant without a distinct behavioral hypothesis.

## Next prompt-only check: validation wording

The V2 run shows the model chose `must not contain newlines` even though the evaluator expected the invariant wording `must be a single line`. `module/agents/budget-fit-v5-validation-contract-v1/` tests one narrow generalization of that failure: validation messages should state the required invariant in positive terms, and exact wording is part of API behavior. The only semantic bundle change from `module/agents/current/` is this prompt instruction; `configs/sampling.yaml` differs by line endings only.

Private kernel [`accelra/v5-validation-contract-fastapi-seed-42-probe`](https://www.kaggle.com/code/accelra/v5-validation-contract-fastapi-seed-42-probe) is saved with `--no-run` for `fastapi_15588`, seed 42, 28 calls, and an eight-minute cap. The prompt SHA-256 embedded in the staged notebook is `e06a2e62eba99c0a5984e8887a3f171ec9480ca48f0e9e4bfc72062e12d6bd4a`. Kaggle reports `COMPLETE`, but the downloaded log contains only notebook-to-HTML conversion and no inference. After quota refresh, run this one-task screen; if it resolves the task, compare the candidate on the active 53-task set only when the remaining quota covers its projected cost plus the paired 18-task holdout reserve. If it fails, skip the full comparison. The active sequence is tracked in [`milestone/PLAN.md`](../milestone/PLAN.md).
