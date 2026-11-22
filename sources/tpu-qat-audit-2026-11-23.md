# TPU feasibility audit: Gemma 4 31B QAT W4A16

Checked 2026-11-22 20:50 UTC. This is a runtime feasibility check, not competition scoring evidence.

## Result

**GO for the already queued model-load/tool-call smoke; NO-GO for treating TPU results as comparable NvidiaL4 evaluations.** Official vLLM JAX code supports the relevant QAT linear-layer format and has served Gemma 4 31B QAT W4A16 on one v6e chip. The exact Kaggle setup remains only partially validated: it uses TPU v5e-8 and tensor parallelism 8, while the upstream implementation author explicitly says v5e and tensor parallelism above 1 were untested. Let the existing smoke answer that question before spending TPU quota on an evaluator probe.

## Evidence

- Google's [Gemma QAT guide](https://gemma.ai/get-started/qat/) maps `-qat-w4a16-ct` to vLLM/SGLang and lists 31B as an available size. The Kaggle competition's allowed model is the same named checkpoint; the private notebook metadata attaches `google/gemma-4/Other/gemma-4-31b-it-qat-w4a16-ct/2`.
- The official [vLLM JAX PR #3653](https://github.com/vllm-project/tpu-inference/pull/3653) adds compressed-tensors W4A16 linear support for symmetric int4, `group`/`channel`, `pack-quantized` checkpoints. It reports that 31B served on one v6e chip, but explicitly says v5e and TP>1 were untested; its measured serving setup took about 27 minutes to cold-compile 31B. The change was merged Sep 27 and included in the v0.31 release; the currently pinned [v0.33.0 release](https://github.com/vllm-project/tpu-inference/releases/tag/v0.33.0) is newer.
- The [vLLM JAX support matrix](https://github.com/vllm-project/tpu-inference/blob/61899c6dff45253fd69b71acda7de425ad5345f6/README.md) lists v5e as a recommended TPU generation, and lists single-host tensor parallelism for the Flax/JAX path. However, its quantization table does not list compressed-tensors INT4 W4A16 as a validated checkpoint format (it lists AWQ INT4 and compressed-tensors FP8). Thus the release/merged implementation evidence is stronger than the matrix's explicit validation status, but neither establishes the exact v5e-8/TP8 run.
- Upstream [issue #3225](https://github.com/vllm-project/tpu-inference/issues/3225) reports an older E2B/E4B-specific QAT loading failure for KV-shared layers and a separate W4A16 scheme-resolution failure. The competition's 31B model has no KV-shared layers; PR #3653 subsequently added the JAX W4A16 linear method. Do not transfer that old E2B/E4B failure directly to this 31B setup.
- A Kaggle CLI check at 2026-11-22 20:50 UTC reported the private smoke `accelra/gemma-4-qat-on-kaggle-tpu-v5e-8-smoke-v1` as `QUEUED`, with empty logs. Its pulled, ignored source is at `data/local/research/gemma4-tpu-qat-smoke-current/`; metadata selects `TpuV5E8`, attaches QAT model v2, enables internet for the pinned install, and its notebook installs `vllm-tpu==0.33.0`, serves with TP=8, then checks one text response and one function call. It does not run the repository evaluator.

## Evaluator integration gap

The existing `evals/kaggle_runtime.py` is NvidiaL4-specific: it installs the competition CUDA wheelhouse, requires `torch.cuda.device_count() >= 4`, selects vLLM GPU-memory settings and TP=4. Reuse its task and scoring setup only; a TPU probe needs a separate JAX server launch path and must keep the local TPU result distinct from NvidiaL4 comparisons.

## Recommendation

Keep the existing smoke queued and inspect its startup log after it reaches a terminal state. If model load, a text response, and a parsed tool call all pass, run only the planned two-task evaluator integration probe; label any results as TPU-backend local evidence. If loading or tool parsing fails, use the failure logs to decide whether the environment/path setting is repairable, then stop TPU comparisons if not. Do not spend the 20-hour TPU allowance on the 44-task suite before that probe passes.

The competition's tested evaluation environment remains NvidiaL4/vLLM from its Python 3.12 wheelhouse; a successful TPU smoke does not establish score comparability or a competition submission result.
