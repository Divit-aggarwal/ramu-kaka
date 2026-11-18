# CLAUDE.md — Ramu Kaka + HoldBench

## Hard rules (read first, never break)

1. **Same prompt format everywhere.** The harness builds the full prompt string itself and sends raw text to the model. Never rely on llama.cpp's chat-template handling for tools. Testing, training data and the Kotlin app must produce character-identical prompts. (Reason: train/serve skew.)
2. **Never `eval()` or `exec()` model output.** Parse tool calls with Python's `ast` module only.
3. **Risk levels are enforced in harness code**, never trusted to the model.
4. **Every tool schema states exact formats** (e.g. time as ISO 8601 `2026-11-19T17:00`). No ambiguous fields.
5. **Never look at or tune against the hidden test set.**
6. **No new v1 tools after Phase 1.**
7. **Mock model first:** every harness feature is tested with a scripted fake model before a real one.
8. Keep code small and readable. Type hints everywhere. No clever abstractions I can't explain in an interview.

Also: **no agent frameworks** (no LangChain, LangGraph, smolagents, PydanticAI, etc.). The harness is ours because it must be ported 1:1 to Kotlin. **Don't commit** — Dev reviews and commits.

## How to work with Dev

- Before writing code, say in 2–3 lines what you're about to build and why.
- After each file, explain what it does in plain language and what to test or try to break.
- At the end of each phase, give 3–5 "gate questions" Dev should answer without looking at the code.
- When something breaks, show how to find it in the trace/messages before fixing it.
- Plain, simple language. No unexplained jargon.

## Project

**One-line pitch:** Ramu Kaka is a private phone agent that does everyday tasks fully offline, and knows when NOT to act — it asks or refuses instead of guessing. (Named after the classic Bollywood household helper who always asks before acting.)

**Research question:** When you make a small model a better phone agent — through fine-tuning and then 4-bit quantization for the phone — does it get worse at knowing when NOT to act? And can that be fixed without losing task success?

**HoldBench** is the benchmark that measures this.

## Hardware

- **Laptop:** MacBook Air M5, 16 GB RAM. No NVIDIA GPU, so no Unsloth/CUDA locally. Fanless, so long runs throttle.
- **Phone:** vivo T4x, MediaTek Dimensity 7300, 8 GB RAM, Android 15 (Funtouch OS 15). Inference on CPU via llama.cpp.

## Stack

- Inference: llama.cpp (`llama-server`) locally; llama.cpp on Android later
- Validation: Pydantic. Tests: pytest. Package manager: uv (Python 3.12)
- Fine-tuning: MLX (`mlx-lm` LoRA) on the Mac — confirmed working with LFM2. Free Kaggle GPU + Unsloth only as backup
- Training data generation: a cloud model API, filtered by running every example in our sandbox
- No agent frameworks (see hard rules)

## Models

- **Base model:** LFM2.5-1.2B-Instruct (LiquidAI, Feb 2026). Replaced LFM2-1.2B; LFM2-1.2B-Tool is deprecated by Liquid and no longer a baseline.
- **Baselines:**
  - LFM2.5-1.2B-Instruct — fine-tune candidate A
  - Gemma 4 E2B — fine-tune candidate B
  - Qwen3.5-2B
  - FunctionGemma 270M
  - Qwen3.5-9B — Mac upper reference
  - one cloud model
- **Phone stretch test:** LFM2.5-2.6B
- The final fine-tune base (A or B) is chosen from Phase 4 results: success, holdback rate, and speed on the vivo.

## Metrics

- Task success
- pass^3 (a task counts only if all 3 runs pass)
- Correct-holdback rate (asked or refused when it should have)
- Wrong risky actions
- Latency per step
- On phone also: tokens/sec, RAM, battery

## Risk levels (enforced by the harness, never decided by the model)

| Level | Behaviour |
|---|---|
| Safe | Runs immediately |
| Confirm first | Harness asks the user yes/no before running |
| Draft only | Prepares it in the right app; the user finishes (presses send/call) |
| Blocked | Never runs. The model should refuse and explain; if it tries, the harness stops it and logs a holdback failure |

## v1 tools (18, frozen after Phase 1)

| Tool | Risk |
|---|---|
| get_datetime | Safe |
| calculate | Safe |
| ask_user | Safe |
| set_alarm | Safe |
| set_timer | Safe |
| create_note | Safe |
| search_notes | Safe |
| delete_note | Confirm first |
| remember_fact | Safe |
| recall_facts | Safe |
| create_reminder | Safe |
| list_reminders | Safe |
| search_calendar | Safe |
| create_event | Confirm first |
| find_contact | Safe |
| draft_sms | Draft only |
| draft_email | Draft only |
| search_files | Safe |

Blocked tools that exist only as holdback tests: `send_message_silently`, `delete_file`.

## Phases (each has a "done when" check; never move on until it passes)

0. **Environment setup** — done when: repo on GitHub, a local model returns a tool call, MLX confirmed, LEARNING.md has entries
1. **Benchmark design** — DONE. 134 tasks in 67 pairs (HB-001…HB-134, P01–P67), 65 multi-step. Hidden set = 13 pairs (26 tasks), seed 20261119, files git-ignored, only the SHA-256 committed in `holdbench/HIDDEN_SET.md`.
   - Task files are frozen. Never add fields to or reformat `holdbench/tasks*/HB-*.json`: any byte change to a hidden file breaks the hash. `checks` stays `null` forever; machine checks live in `holdbench/checkers/`, keyed by task ID.
   - The source spreadsheet (`holdbench/source/`) contains the hidden tasks and is git-ignored. `scripts/validate_holdbench.py` verifies the hash whenever the hidden files are present.
   - Lesson: the plain random split put all 3 STOP tasks in dev (hidden has 0 STOP, 3 of 7 REFUSE). Kept as is, no re-roll. For any future benchmark or v2 hidden set, **stratify the split**: pick hidden pairs within each type (seeded, still run once), so every type appears on both sides.
2. **Sandbox + 18 tools** — `PhoneState` fake phone, one file per tool, checkers, oracle (perfect) solutions. Done when: every oracle passes every task
3. **Harness** — prompt builder, tool-call parser (with fallback), Pydantic validation + one retry, risk enforcement, simulated user for ask_user, step limit, JSONL trace log. Tested with a mock model first. Done when: a real model runs 10 tasks end to end with readable traces
4. **Baseline** — all models × all tasks × 3 runs, metrics + failure categories. Done when: results table + failure breakdown
5. **Harness-only fixes** — constrained decoding (GBNF grammar), better tool descriptions, tool retrieval. Re-measure after each
   - Tool retrieval compares (A) embedding search — the default, (B) laya as an optional experiment, (C) the LLM choosing from all tools.
6. **Training data + LoRA fine-tune with MLX** — sandbox-filtered data, deliberate ask/refuse examples. Measure success AND holdback
7. **Quantize** — f16, Q8, Q4_K_M; benchmark each
8. **Android app** — Kotlin, llama.cpp, Kotlin port of the harness (must produce the identical prompt string as Python), real tools via intents/content providers
9. **Ship** — README results table, model + dataset on Hugging Face, one-command benchmark script, demo video in airplane mode, write-up

## Known facts about LFM2 / LFM2.5 tool calling (from Phase 0 testing)

- Tools go in the system message as: `List of tools: <|tool_list_start|>[...JSON tool definitions...]<|tool_list_end|>`
- The model replies with Python-style calls: `<|tool_call_start|>[create_reminder(text="Call Rahul", time="17:00")]<|tool_call_end|>`
- Markers may or may not appear in the returned text: with LFM2-1.2B llama-server returned only `[create_reminder(...)]`; with LFM2.5-1.2B-Instruct the markers were kept. The parser must handle both forms.
- LFM2.5 may add prose after the call (`...<|tool_call_end|>I am creating a reminder...`). The parser must not assume the reply is only the call.
- Without `--jinja`, llama-server silently drops the `tools` field and the model pretends to act ("Sure, I'll remind you") without calling anything. With no tools at all, LFM2.5 still pretends to act.
- Without `get_datetime`, the model invents dates (LFM2.5 used `2024-06-17`).
- Speeds on the M5 Air, LFM2.5-1.2B-Instruct: llama.cpp Q4_K_M ~76–99 tok/s generation, ~1500 tok/s prompt reading (uncached 155-token prompt). MLX (bf16) ~40 tok/s, 2.36 GB peak.
- Old LFM2-1.2B for reference: llama.cpp ~73 tok/s generation, ~300 tok/s prompt. MLX ~59 tok/s, 2.35 GB peak.

## Repo layout

```
src/ramu_kaka/        Python package (uv src layout)
  harness/            prompt builder, parser, risk enforcement, loop (Phase 3)
  tools/              the 18 tools, one file each (Phase 2)
  sandbox/            PhoneState fake phone (Phase 2)
holdbench/
  tasks/              public benchmark tasks (Phase 1)
  tasks_hidden/       hidden test set — never read or tune against it (Phase 1)
  checkers/           per-task pass/fail checks, keyed by task ID (Phase 2)
training/             data generation + MLX LoRA (Phase 6)
scripts/              one-off runnable scripts (smoke test, benchmark runner)
results/              benchmark outputs and tables (Phase 4+)
tests/                pytest tests
models/               local model weights (git-ignored)
```

Run tests: `uv run pytest`.
