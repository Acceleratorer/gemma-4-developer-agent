# Ranjeet 40-call edit LoRA audit — 2026-11-23

## Finding

The candidate archive is structurally compatible with the official submission loader and compiles against the competition wheelhouse. This is packaging evidence only: no model-serving probe or repair evaluation was run for this archive, so there is no candidate-specific repair score or measured LoRA gain.

## Archive and loader compatibility

- The official [competition rules](https://www.kaggle.com/competitions/gemma-4-developer-agent/overview) and [harness README](https://www.kaggle.com/competitions/gemma-4-developer-agent/data?select=HARNESS_README.md) allow PEFT adapters under `adapters/<name>/`, with `adapter_config.json` and `adapter_model.safetensors`, referenced by `adapter: <name>`. The candidate uses `adapters/main_lora/` and `adapter: main_lora` with the supported `gemma-4-31b-it-qat-w4a16-ct` base. Its archive has a root `agent.yaml`, six expected members, and a 54,503,808-byte adapter weight file, well below the 3 GiB unpacked limit.
- Exact `submission.zip` SHA-256: `18d5e283824ceb2b85909ebdfd100166b79d4aa4205ad85a78bad9eaf1cc4e53`.
- The candidate [Kaggle notebook](https://www.kaggle.com/code/ranjeet258/gemma-4-forty-call-repair-with-edit-lora) checks the parent adapter hashes, rank 16, tensor count, dtype and finite values, then calls `validate_directory` and `compile_submission`. The saved output says “Verified adapter tensors 180” and “Compiled swe_agent with 9 tools.” The local official `swegemma 0.2.11` / `adk_submission 0.2.13` source discovers `.safetensors` under `adapters/` and resolves an agent’s adapter name against that manifest. This verifies archive discovery and static compilation, not a live vLLM load or output change.
- Local evidence is in ignored `data/local/research/ranjeet-forty-call-edit-lora{,-output}/`; the kernel metadata disables GPU and lists no model source. Its log ends after archive creation and notebook-to-HTML conversion.

## Training and loss evidence

- The linked [parent training kernel, version 366776559](https://www.kaggle.com/code/ayush04barai/lora-step-2?scriptVersionId=366776559), reports 52 selected source-edit examples (49 Gemma and 3 Qwen), 331,220 context-plus-target tokens, 6,790 supervised edit-call tokens, and eight repository-held-out examples. Its single-run log reports held-out edit-call token loss decreasing from `0.0150` to `0.0035` over 54 updates. That is a small token-prediction check, not a repair pass rate.
- The training kernel attaches LoRA to the last 30 language layers’ `q_proj`, `o_proj`, and `down_proj` modules at rank 16. Its Kaggle metadata attaches `gemma-4-31b-it-qat-q4_0-unquantized/2`; the run log says 4-bit loading was off and the model loaded in BF16. The submission declares `gemma-4-31b-it-qat-w4a16-ct`. Transfer from the training checkpoint to the scored serving checkpoint is therefore unverified.

## Repair-score evidence and confounds

- The candidate notebook says it adds the adapter to a 40-call baseline and quotes that upstream [no-training notebook](https://www.kaggle.com/code/bliverrigpdoge/lb-0-22-3-tweaks-40-tool-calls-no-training?scriptVersionId=369604657) as having a reported best public score of `0.22`. That figure belongs to the cited baseline; the candidate notebook has no evaluator output or submission ID tying a score to this ZIP. Its `USE_ADAPTER=False` branch can build a control, but no paired control result is present in the saved output.
- Therefore the only outcome evidence for this candidate is training loss. The 40-call bundle, its inherited prompt/tools, the trained adapter, and the training-to-serving checkpoint difference are not isolated by a same-task, same-seed repair comparison. Do not treat the baseline’s reported score or the loss reduction as evidence that this adapter improves repair performance.

## Local primary artifacts reviewed

`data/local/research/ranjeet-forty-call-edit-lora/kernel-metadata.json`, its pulled notebook and output log/archive; `data/local/research/ayush-lora-step-2/kernel-metadata.json` and `data/local/research/ayush-lora-step-2-output/lora-step-2.log`; the official local `HARNESS_README.md`, sample submission, and `adk_submission` / `swegemma` wheels from the [competition wheelhouse](https://www.kaggle.com/datasets/metric/gemma-4-developer-agent-wheelhouse). No inference was run, and no weights or notebook source were copied into tracked files.
