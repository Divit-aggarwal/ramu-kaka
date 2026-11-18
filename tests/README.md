# tests/ — every phase

pytest tests. Run with `uv run pytest`.
Phase 0 has only an import check. Phase 2 adds tool/sandbox tests, and Phase 3 adds
harness tests that use a scripted mock model (hard rule 7).
