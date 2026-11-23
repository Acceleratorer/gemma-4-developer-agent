# Kaggle wheelhouse compatibility audit — 2026-11-23

## Finding

Kaggle staff announced a patch to preserve `reasoning_content` between tool calls and later said it should be in the current wheelhouse. The public wheelhouse still exposes a vLLM build without that normalization. The scorer's deployed build is unverified, so private local evaluations use a compatibility patch to model the staff-described behavior; local results remain training-task evidence and are not leaderboard scores.

## Evidence

- Kaggle CLI 2.2.5 reported `metric/gemma-4-developer-agent-wheelhouse` last updated at 2026-10-12 19:51:31 UTC. Its vLLM file was created at 19:51:41 UTC that day: `vllm-0.19.1-cp38-abi3-manylinux_2_31_x86_64.whl`.
- The exact wheel SHA-256 is `73c69bafca24fbdad44690c44d6c6446514351e6f3cc9a6057cba05e66051310`.
- Its `vllm/entrypoints/openai/chat_completion/protocol.py` contains no `reasoning_content` normalization in `ChatCompletionRequest`. Upstream [vLLM PR #42664](https://github.com/vllm-project/vllm/pull/42664) adds a pre-validation step that moves `reasoning_content` to `reasoning`; it merged on 2026-05-21.
- Kaggle staff described the scoring fix as incoming, later said it should be in the current wheelhouse, and noted they could not rescore every existing submission ([discussion #744354](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/744354)). The published dataset's timestamp and exact wheel do not prove which build the scorer uses; Kaggle has not published a scorer wheel or hash that verifies deployment.
- The same public vLLM 0.19.1 wheel retains the Gemma array-parser no-progress hazard described in [discussion #753973](https://www.kaggle.com/competitions/gemma-4-developer-agent/discussion/753973). Keep graph-enabled experiments behind the existing no-graph comparison and trace review.

## Evaluation handling

`evals/kaggle_runtime.py` now checks the installed wheel after installation. If upstream normalization is absent and the expected `ChatCompletionRequest` layout is present, it inserts the same pre-validation behavior and records `local-compatibility-shim-vllm-42664` in the evaluation summary. If the upstream patch is already present, the summary records `upstream-reasoning-content-normalizer`. An unknown source layout stops evaluation instead of silently running under an unverified setup.

This shim changes only the private training-task evaluator. It does not alter the submitted agent bundle or Kaggle's scorer. Recheck the public dataset and kernel source before the next runs, rebuild the saved notebooks so they embed the updated runtime, and preserve the compatibility label in every result log.
