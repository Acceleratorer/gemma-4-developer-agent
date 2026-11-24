# TPU feasibility audit: Gemma 4 31B QAT W4A16

Checked 2026-11-22 20:50 UTC. This is a runtime feasibility check, not competition scoring evidence.

## Result

**NO-GO for evaluator work until the model-load/text/tool-call smoke passes; TPU results are not comparable to NvidiaL4 evaluations.** Official vLLM JAX code supports the relevant QAT linear-layer format and has served Gemma 4 31B QAT W4A16 on one v6e chip. The exact Kaggle setup remains only partially validated: it uses TPU v5e-8 and tensor parallelism 8, while the upstream implementation author explicitly says v5e and tensor parallelism above 1 were untested. Let the existing smoke answer that question before spending TPU quota on an evaluator probe.

## Evidence

- Google's [Gemma QAT guide](https://gemma.ai/get-started/qat/) maps `-qat-w4a16-ct` to vLLM/SGLang and lists 31B as an available size. The Kaggle competition's allowed model is the same named checkpoint; the private notebook metadata attaches `google/gemma-4/Other/gemma-4-31b-it-qat-w4a16-ct/2`.
- The official [vLLM JAX PR #3653](https://github.com/vllm-project/tpu-inference/pull/3653) adds compressed-tensors W4A16 linear support for symmetric int4, `group`/`channel`, `pack-quantized` checkpoints. It reports that 31B served on one v6e chip, but explicitly says v5e and TP>1 were untested; its measured serving setup took about 27 minutes to cold-compile 31B. The change was merged Sep 27 and included in the v0.31 release; the currently pinned [v0.33.0 release](https://github.com/vllm-project/tpu-inference/releases/tag/v0.33.0) is newer.
- The [vLLM JAX support matrix](https://github.com/vllm-project/tpu-inference/blob/61899c6dff45253fd69b71acda7de425ad5345f6/README.md) lists v5e as a recommended TPU generation, and lists single-host tensor parallelism for the Flax/JAX path. However, its quantization table does not list compressed-tensors INT4 W4A16 as a validated checkpoint format (it lists AWQ INT4 and compressed-tensors FP8). Thus the release/merged implementation evidence is stronger than the matrix's explicit validation status, but neither establishes the exact v5e-8/TP8 run.
- Upstream [issue #3225](https://github.com/vllm-project/tpu-inference/issues/3225) reports an older E2B/E4B-specific QAT loading failure for KV-shared layers and a separate W4A16 scheme-resolution failure. The competition's 31B model has no KV-shared layers; PR #3653 subsequently added the JAX W4A16 linear method. Do not transfer that old E2B/E4B failure directly to this 31B setup.
- A Kaggle CLI check at 2026-11-22 20:50 UTC reported the private smoke `accelra/gemma-4-qat-on-kaggle-tpu-v5e-8-smoke-v1` as `QUEUED`, with empty logs. Its pulled, ignored source is at `data/local/research/gemma4-tpu-qat-smoke-current/`; metadata selects `TpuV5E8`, attaches QAT model v2, enables internet for the pinned install, and its notebook installs `vllm-tpu==0.33.0`, serves with TP=8, then checks one text response and one function call. It does not run the repository evaluator.

## Kaggle smoke outcome and correction — 2026-11-24

- Kernel version 2 ended `ERROR`. Its log shows `SERVER_EXIT=1`, `SERVER_READY=False`, and `jax.errors.JaxRuntimeError: FAILED_PRECONDITION: TPU initialization failed: open(/dev/vfio/1): 16: Device or resource busy; Couldn't open iommu group /dev/vfio/1`. The smoke did not pass model serving, text generation, or tool-call parsing.
- The notebook called `jax.devices()` in its driver process before launching the vLLM server subprocess. This is a plausible cause of the TPU resource conflict, not a proven root cause. The earlier torchaudio import failed on an undefined Torch symbol, but the notebook removed that package and continued to the vLLM launch.
- The ignored staging notebook at `data/local/research/gemma4-tpu-qat-smoke-current/` now removes the `jax` import, parent-side device enumeration, and derived device summary field. Kernel version 3 was pushed and run on 2026-11-24; it remained `QUEUED` at 13:45 UTC, and its log query returned no text. TPU quota remained 0.42/20.00h at 13:45 UTC, confirming that the corrected run had not started by the latest status check.
- At 2026-11-24 14:17 UTC, the Kaggle CLI still reported version 3 as `QUEUED`; `kaggle quota` showed GPU 0.04/30.00h and TPU 19.58/20.00h remaining. Both quotas refresh at 2026-11-28 00:00 UTC / 07:00 Vietnam time. Kaggle exposes no queue ETA, and no new kernel version or run was started.
- At 2026-11-24 15:17 UTC, the Kaggle CLI still reported version 3 as `QUEUED`; quota remained GPU 0.04/30.00h and TPU 19.58/20.00h. Both quotas refresh at 2026-11-28 00:00 UTC / 07:00 Vietnam time. Kaggle exposes no queue ETA.
- At 2026-11-24 16:18 UTC, `kaggle kernels status` still reported version 3 as `QUEUED`; `kaggle quota` remained GPU 0.04/30.00h and TPU 19.58/20.00h. Both quotas refresh at 2026-11-28 00:00 UTC / 07:00 Vietnam time. Kaggle exposes no queue ETA.
- Keep this runtime smoke separate from competition evaluation. No evaluator task or competition score was produced.

## Evaluator integration gap

The existing `evals/kaggle_runtime.py` is NvidiaL4-specific: it installs the competition CUDA wheelhouse, requires `torch.cuda.device_count() >= 4`, selects vLLM GPU-memory settings and TP=4. Reuse its task and scoring setup only; a TPU probe needs a separate JAX server launch path and must keep the local TPU result distinct from NvidiaL4 comparisons.

## Recommendation

Wait for corrected kernel version 3 to leave the queue, then inspect its logs. If model load, text generation, and a parsed tool call all pass, run only the planned two-task evaluator integration probe and label its result as TPU-backend local evidence. If it fails again, use the new logs to decide whether the setup is repairable; do not spend the TPU allowance on a full task suite. A successful TPU smoke still does not establish comparability with NvidiaL4.

The competition's tested evaluation environment remains NvidiaL4/vLLM from its Python 3.12 wheelhouse; a successful TPU smoke does not establish score comparability or a competition submission result.
