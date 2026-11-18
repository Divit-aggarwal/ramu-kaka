# Ramu Kaka

*An offline phone agent that asks before it breaks anything.*

In many classic Bollywood films, "Ramu Kaka" is the old family helper: trusted, quietly
capable and always polite. He doesn't do anything drastic without first checking with the
family. That's the behaviour this project is after: an assistant that does everyday tasks
for you, and stops to ask (or says no) when acting on a guess could cause harm.

## Research question

When you make a small model a better phone agent, first by fine-tuning it and then by
squeezing it to 4-bit so it fits on a phone, does it get worse at knowing when **not** to act?
And can that be fixed without losing task success?

## Status: building in public

Nothing is measured yet. This table will fill in as the phases are finished.

| Model | Task success | pass^3 | Correct holdback | Wrong risky actions | Latency / step |
|---|---|---|---|---|---|
| LFM2.5-1.2B-Instruct | — | — | — | — | — |
| Gemma 4 E2B | — | — | — | — | — |
| Qwen3.5-2B | — | — | — | — | — |
| FunctionGemma 270M | — | — | — | — | — |
| Qwen3.5-9B (Mac reference) | — | — | — | — | — |
| Cloud model | — | — | — | — | — |
| Ramu Kaka (LoRA, f16) | — | — | — | — | — |
| Ramu Kaka (LoRA, Q4_K_M) | — | — | — | — | — |

- **pass^3**: a task counts only if all 3 runs pass.
- **Correct holdback**: the agent asked or refused in cases where it should have.

## What it does

Ramu Kaka runs a small language model fully on the phone, with no internet. The current
candidate is LFM2.5-1.2B-Instruct. The final base model will be picked from the baseline results.
It gets 18 tools: alarms, timers, notes, reminders, calendar, contacts, files, and drafting
SMS and email. It uses them to carry out requests like "remind me to call Rahul at 5".

## What makes it different: holdback

Most agent benchmarks reward doing things. Ramu Kaka is also scored on **not** doing things:

- **Asking** when the request is unclear ("which Rahul?").
- **Refusing** when the action is not allowed (silently sending a message, deleting files).

The model never decides how risky an action is. Each tool has a fixed risk level, and the
harness code enforces it:

| Risk level | What happens |
|---|---|
| Safe | Runs immediately |
| Confirm first | The user is asked yes/no before it runs |
| Draft only | It's prepared in the right app, and the user presses send/call |
| Blocked | Never runs, and the attempt is logged as a failure |

The harness is written from scratch, with no agent framework, so it can be ported line for
line to Kotlin for the Android app.

## HoldBench

HoldBench is the benchmark built alongside the agent. It has 134 tasks (67 pairs) that run
against a fake phone (a sandbox), arranged as pairs: in one task of each pair the agent
should act, and in the other it should hold back. At least 30% of the tasks need more than
one step. 20% are a hidden test set, locked at the start by publishing a hash of it
(a fingerprint that would change if the set were edited). Every model is run 3 times on
every task.

## Roadmap

- [x] **0. Environment setup**: repo, local model returns a tool call, MLX confirmed
- [x] **1. Benchmark design**: 134 tasks in 67 act/hold-back pairs, hidden set hash-locked
- [ ] **2. Sandbox + 18 tools**: fake phone, checkers, perfect reference solutions
- [ ] **3. Harness**: prompt builder, parser, validation, risk enforcement, traces
- [ ] **4. Baseline**: all models × all tasks × 3 runs
- [ ] **5. Harness-only fixes**: grammar-constrained output, better tool descriptions
- [ ] **6. Fine-tune**: LoRA with MLX on sandbox-checked data
- [ ] **7. Quantize**: f16, Q8, Q4_K_M, each benchmarked
- [ ] **8. Android app**: Kotlin + llama.cpp, same prompts as Python
- [ ] **9. Ship**: results, model and dataset on Hugging Face, airplane-mode demo

## Hardware

- Laptop: MacBook Air M5, 16 GB RAM
- Phone: vivo T4x (Dimensity 7300, 8 GB RAM, Android 15), running on the CPU through llama.cpp

## Notes

What broke, and what I learned from it, is logged in [LEARNING.md](LEARNING.md).

## License

MIT, see [LICENSE](LICENSE).
