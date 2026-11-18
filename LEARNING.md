# Learning log

One entry per thing that broke or surprised me. Newest at the bottom.

## Template

```
## #N — <short title>
- **Date:**
- **What I tried:**
- **What broke:**
- **How I found it:**
- **Fix:**
- **Lesson:**
- **Post idea:**
```

---

## #1 — The model pretended to set a reminder

- **Date:** 2026-11-18
- **What I tried:** Started `llama-server` without `--jinja` and sent a request with a `create_reminder` tool in the `tools` field: "Remind me to call Rahul at 5pm".
- **What broke:** The model said "Sure, I'll remind you to call Rahul at 5pm" and didn't call any tool. `prompt_tokens` was only 20, far too small to contain a tool definition.
- **How I found it:** The `/apply-template` endpoint shows the exact prompt text the server builds. The tool definition wasn't in it at all. Without `--jinja`, llama-server silently drops the `tools` field.
- **Fix:** Start the server with `--jinja`, or put the tools in the prompt yourself (see #2).
- **Lesson:** When an agent fails, check the prompt before blaming the model. A small `prompt_tokens` count is a quick red flag.
- **Post idea:** "My AI agent lied to me, and it wasn't the model's fault." A 20-token prompt explained the whole thing.

## #2 — Native tool format works, and shows what's still missing

- **Date:** 2026-11-18
- **What I tried:** Put the tools in the system message in LFM2's own format: `List of tools: <|tool_list_start|>[...]<|tool_list_end|>`.
- **What broke:** Nothing broke this time. `prompt_tokens` was 97 and the model returned `[create_reminder(text="Call Rahul", time="17:00")]`. But:
  - The `<|tool_call_start|>` / `<|tool_call_end|>` markers were stripped from the reply by the server.
  - The call is Python syntax, not JSON.
  - The model invented the time format (`17:00`) and had no idea what today's date is.
- **How I found it:** By reading the raw reply text and the token counts.
- **Fix (planned):** The parser must accept calls with and without markers, and parse Python-style calls with `ast` (never `eval`). Every tool schema must state its exact format (ISO 8601 `2026-11-19T17:00`), and `get_datetime` is needed so the model can work out "today" and "tomorrow".
- **Lesson:** "It returned a tool call" is not the same as "it returned the right tool call". Wherever a schema is vague, the model guesses.
- **Post idea:** "What a 1.2B model actually outputs when you give it a tool", with the raw reply annotated.

## #3 — Swapped the base model: LFM2-1.2B → LFM2.5-1.2B-Instruct

- **Date:** 2026-11-19
- **What I tried:** Replaced LFM2-1.2B with LFM2.5-1.2B-Instruct (Feb 2026, same backbone, same Python-style tool calls). Reason: Liquid deprecated LFM2-1.2B-Tool, my key baseline, and LFM2.5 is the newer generation with better instruction following. Deleted the old GGUF and the HF cache copy (~3.0 GB), downloaded `LFM2.5-1.2B-Instruct-Q4_K_M.gguf` from Liquid's official GGUF repo, then re-ran MLX and the tool-call smoke test.
- **Results:**
  - 3 runs at temperature 0, all identical, prompt_tokens 155, completion_tokens 46:
    `<|tool_call_start|>[create_reminder(text="Call Rahul", time="2024-06-17T17:00")]<|tool_call_end|>I am creating a reminder for you to call Rahul at 5:00 PM.`
  - Speed, llama.cpp Q4_K_M: 76 / 99 / 90 tok/s generation (old: ~73). Prompt reading ~1535 tok/s on the first (uncached) run (old: ~300). Runs 2–3 show ~175 tok/s only because the server reused its cache and re-read just a few tokens, so they are not a fair prompt-speed number.
  - Speed, MLX (bf16): ~40 tok/s generation over 200 tokens, 2.36 GB peak (old: ~59 tok/s, 2.35 GB). Slower than the old figure. The laptop is fanless, so throttling is possible; re-measure before drawing a conclusion.
  - With no tools (no system message): "Sure! I'll remind you to call Rahul at 5 PM. Let me know if you'd like me to set a reminder…". prompt_tokens 21, no tool call. **It still fakes the action.**
- **What broke / surprised me:**
  - The markers were *not* stripped this time, unlike LFM2-1.2B.
  - The model added prose after the call.
  - It invented the date `2024-06-17`. That's even further off than LFM2's guess, and it didn't copy the example date from the schema.
- **How I found it:** By reading `repr()` of the raw reply in `scripts/smoke_test.py`, now with llama-server's `timings` field printed.
- **Fix (planned):** The parser handles markers present or absent, plus trailing text. `get_datetime` is mandatory. Faking an action without calling a tool is exactly the failure HoldBench should catch.
- **Lesson:** Check a model's status and deprecation before building on it, because model families move every few months. Re-check the "known facts" after every swap: two of mine (stripped markers, call-only replies) changed with the new model.
- **Post idea:** "Same prompt, new model: what changed in the raw output", a side-by-side of LFM2 vs LFM2.5.

## #4 — Phase 1: HoldBench becomes task files, and the hidden set is locked

- **Date:** 2026-11-19
- **What I tried:** Converted the HoldBench spreadsheet into `phone_state.json` and 134 task files: 67 pairs, 5 types (ACT 77, ASK 28, REFUSE 7, CAN'T 19, STOP 3), 65 multi-step. The benchmark was written before the agent exists, so the agent gets built to the test and the test isn't adjusted to fit the agent. Locked a hidden set of 13 pairs (26 tasks), picked with seed 20261119 and no re-rolling. The hidden pair IDs and the SHA-256 are committed in `holdbench/HIDDEN_SET.md`. The hidden task files stay out of the public repo, and so does the spreadsheet, because it contains them.
- **What broke:**
  1. HB-034 was an ASK task with no simulated user reply. I fixed the sheet: reply "the 27th", steps 2, and an either/or Pass if.
  2. The first tool-name parser assumed every tool has an underscore in its name, and silently dropped `calculate`.
- **How I found it:** (1) The validator failed loudly. (2) By spot-checking HB-037's `expected_tools` against its raw text.
- **Fix:** For (2), the parser now keeps every word except known filler words, so a misspelled tool name gets flagged by the validator instead of disappearing.
- **Surprises:**
  - The random split put all 3 STOP tasks in the dev set, so the hidden set has **zero STOP tasks**. 3 of the 7 REFUSE tasks are hidden. Kept as is; re-rolling would defeat the point.
  - `set_timer` is in only 2 tasks, below my own "≥3 pairs per tool" design rule.
- **Lesson:** Fix the data *before* locking. After the hash is committed, any byte change to a hidden file, even a JSON formatting change, breaks the proof. Also: a parser that drops what it doesn't recognise hides bugs, and one that passes it on to a validator surfaces them.
- **Post idea:** "How to lock a benchmark's test set without publishing it": seed, hash, and why I didn't re-roll when the split came out uneven.

## #5 — Where the checks live, and splitting by type next time

- **Date:** 2026-11-19
- **What I tried:** Decided where Phase 2's machine checks go, after locking the hidden set in #4.
- **What broke:** Nothing yet, but the original plan would have. Writing `checks` into each task file would edit the 26 hidden files too, changing their bytes and breaking the committed hash.
- **How I found it:** By working through what Phase 2 would do to files that #4 had just frozen.
- **Fix:** Checks live in `holdbench/checkers/`, keyed by task ID. Every task file keeps `checks: null` forever, and task files are never edited after a lock. Separately, #4's random split left the hidden set with zero STOP tasks. It stays as is. For any future benchmark or v2 hidden set, I'll **stratify**: pick hidden pairs within each type, with a fixed seed, run once. That way every type shows up on both sides by design, not by luck.
- **Lesson:** Once something is hash-locked, anything that might change later (checks, scores, notes) has to live outside the locked files. And balance comes from the design of the random procedure, never from re-rolling it.
- **Post idea:** "Frozen data, living code": why benchmark task files should never change, and checkers should.
