# training/ — Phase 6

Training data generation and MLX LoRA fine-tuning of the chosen base (LFM2.5-1.2B-Instruct or Gemma 4 E2B).
Examples come from a cloud model, are kept only if they pass in our sandbox, and include
deliberate ask/refuse examples. Prompts must be character-identical to the harness (hard rule 1).
Adapters and raw data are git-ignored.
