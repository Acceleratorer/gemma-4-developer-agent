# Gemma 4 E4B distilled LoRA candidate

Separate small-model experiment; it does not replace the active 31B V5 candidate.

- Base: `gemma-4-e4b-it-qat-w4a16-ct`.
- Adapter: Omallo's [Gemma 4 E4B SWE-agent LoRA](https://www.kaggle.com/models/omallo/gemma4-e4b-swe-agent-lora-from-31b), Transformers variation `peft-lora-scale-1`, version 1.
- Adapter configuration: rank 16, served LoRA scale 1.0. Kaggle lists the model under Apache 2.0.
- The system prompt is reproduced from the traces in the companion [dataset](https://www.kaggle.com/datasets/omallo/gemma4-swe-agent-lora-distillation), released under CC BY 4.0; see `NOTICE.txt`.

The author's three-run means were 19.7/47 on held-out SWE-rebench, 12.7/49 on large repositories, and 10.3/50 on SWE-bench Verified. Plain E4B scored 9.7/47, 8.3/49, and 11.3/50. This supports a targeted small-model trial, not promotion to the 31B track. The adapter was trained on 60 public competition-task trajectories, so local scores on the public training pool are not independent evidence; use the Kaggle public score as the initial check and the private leaderboard for final placement.

The 69,839,856-byte `adapters/main_lora/adapter_model.safetensors` is downloaded locally from model version 1 and excluded from Git. SHA-256: `E7D5F6AFED8F5A6C2E3B031646D95ACCD94749289366696039F4641BAB396015`.

## Rebuild the submission archive

Download the pinned Kaggle model version into `adapters/main_lora/`, verify the weight hash above, then build the ZIP from the repository root:

```powershell
kaggle models instances versions download omallo/gemma4-e4b-swe-agent-lora-from-31b/transformers/peft-lora-scale-1/1 --path module/agents/e4b-31b-distilled-lora-v1/adapters/main_lora --untar
Get-FileHash module/agents/e4b-31b-distilled-lora-v1/adapters/main_lora/adapter_model.safetensors -Algorithm SHA256
py -3.12 module/build_submission.py --agent e4b-31b-distilled-lora-v1 --output dist/e4b-31b-distilled-lora-v1/submission.zip
```

The uploaded trial's archive SHA-256 and submission status are recorded in `/log/experiment-log.csv`.
