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
