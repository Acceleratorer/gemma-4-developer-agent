# Submission source

`agents/current/` is the active single-agent candidate. It starts without LoRA adapters so the base prompt and budget can be measured independently. The reference notebook configurations are retained locally under ignored `agents/reference-*` directories.

`build_submission.py` packages an agent directory into a deterministic Kaggle `submission.zip`. Model overrides update every declared agent model in the staged archive and are restricted to the four competition-supported quantized Gemma 4 variants.

The primary agent uses the complete competition tool set, including graph retrieval. It uses graph tools when a relevant symbol is known and falls back to repository search when graph retrieval does not return a useful match.
