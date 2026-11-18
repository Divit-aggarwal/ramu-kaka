# checkers/ — Phase 2

The machine-checkable version of each task's `pass_if`, keyed by task ID (e.g. `HB-004`).
They inspect the final `PhoneState` and the tool log ("only N1 deleted", "no Blocked tool called",
"ask_user before any write").

Checks live here, **not** in the task files. A task file's `checks` field stays `null` forever,
because editing a hidden task file would break the hash in `HIDDEN_SET.md`.
Every oracle (perfect) solution must pass every checker before Phase 3 starts.
