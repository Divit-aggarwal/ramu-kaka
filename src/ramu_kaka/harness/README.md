# harness/ — Phase 3

The agent loop: builds the exact prompt string, parses tool calls with `ast` (with and without
LFM2's markers), validates arguments with Pydantic (one retry), enforces risk levels, runs the
simulated user for `ask_user`, applies a step limit and writes a JSONL trace.
Tested against a scripted mock model before any real model.
