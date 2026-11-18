# holdbench/ — Phase 1 (tasks), Phase 2 (checkers)

The benchmark: ~110 tasks in should-act / should-hold-back pairs, ≥30% multi-step.

- `tasks/` — public tasks
- `tasks_hidden/` — the 20% hidden test set
- `checkers/` — code that decides pass/fail from the final `PhoneState` and trace
