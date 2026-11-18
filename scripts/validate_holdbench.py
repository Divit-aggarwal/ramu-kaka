"""Validate HoldBench task files and the starting phone state. Exits 1 on any error.

Usage: uv run python scripts/validate_holdbench.py
Works before and after the hidden split, and on a fresh clone without tasks_hidden/ files.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

from holdbench_common import (
    HIDDEN_DIR, PHONE_STATE, TASKS_DIR, TYPES, V1_TOOLS, read_hidden_set, sha256_of,
)

N_TASKS, N_PAIRS = 134, 67
ALL_IDS = {f"HB-{i:03d}" for i in range(1, N_TASKS + 1)}
ALL_PAIRS = {f"P{i:02d}" for i in range(1, N_PAIRS + 1)}
EXPECTED_STATE_COUNTS = {"contacts": 6, "notes": 7, "events": 5, "reminders": 1, "facts": 2, "files": 5}
TASK_KEYS = ["id", "pair", "type", "request", "expected_tools", "expected_tools_raw", "steps",
             "pass_if", "simulated_user", "simulated_user_raw", "why", "expected_plan", "checks"]
VALUE_PATTERNS = {
    "phone": r"\+91 \d{5} \d{5}",
    "email": r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+",
    "note id": r"\bN\d+\b",
    "timestamp": r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}",
}


def load(folder: Path) -> list[dict]:
    return [json.loads(f.read_text()) | {"_file": f.stem} for f in sorted(folder.glob("HB-*.json"))]


def main() -> int:
    errors: list[str] = []
    state = json.loads(PHONE_STATE.read_text())
    dev, hidden_files = load(TASKS_DIR), load(HIDDEN_DIR)
    hidden = read_hidden_set()

    # --- Phone state ---
    for key, n in EXPECTED_STATE_COUNTS.items():
        if len(state[key]) != n:
            errors.append(f"phone_state: expected {n} {key}, found {len(state[key])}")
    for c in state["contacts"]:
        if c["phone"] is not None and not isinstance(c["phone"], str):
            errors.append(f"phone_state: {c['id']} phone is not a string: {c['phone']!r}")

    # --- Which tasks should exist, given the hidden split ---
    tasks = dev + hidden_files
    expected_pairs = ALL_PAIRS
    if hidden:
        hidden_pairs, digest = hidden
        leaked = sorted(t["id"] for t in dev if t["pair"] in hidden_pairs)
        if leaked:
            errors.append(f"hidden tasks found in tasks/ (public folder): {leaked}")
        stray = sorted(t["id"] for t in hidden_files if t["pair"] not in hidden_pairs)
        if stray:
            errors.append(f"tasks_hidden/ has tasks from non-hidden pairs: {stray}")
        if hidden_files:
            actual = sha256_of(list(HIDDEN_DIR.glob("HB-*.json")))
            if actual != digest:
                errors.append(f"hidden set hash mismatch: HIDDEN_SET.md says {digest}, files give {actual}")
        else:  # fresh clone: hidden files aren't in git
            expected_pairs = ALL_PAIRS - hidden_pairs
            print(f"(tasks_hidden/ is empty: checking the {len(dev)} public tasks only)")
    elif hidden_files:
        errors.append("tasks_hidden/ has files but HIDDEN_SET.md doesn't exist")

    # --- IDs and pairs ---
    ids = [t["id"] for t in tasks]
    expected_ids = ALL_IDS if expected_pairs == ALL_PAIRS else None
    dupes = [i for i, n in Counter(ids).items() if n > 1]
    if dupes:
        errors.append(f"duplicate IDs: {sorted(dupes)}")
    if expected_ids is not None and set(ids) != expected_ids:
        errors.append(f"IDs not continuous HB-001..HB-{N_TASKS}: missing {sorted(expected_ids - set(ids))}, "
                      f"extra {sorted(set(ids) - expected_ids)}")
    pair_counts = Counter(t["pair"] for t in tasks)
    bad_pairs = {p: n for p, n in pair_counts.items() if n != 2}
    if bad_pairs:
        errors.append(f"pairs without exactly 2 tasks: {bad_pairs}")
    if set(pair_counts) != expected_pairs:
        errors.append(f"pair IDs wrong: missing {sorted(expected_pairs - set(pair_counts))}, "
                      f"extra {sorted(set(pair_counts) - expected_pairs)}")
    if len(tasks) != 2 * len(expected_pairs):
        errors.append(f"expected {2 * len(expected_pairs)} tasks, found {len(tasks)}")

    # --- Per task ---
    for t in tasks:
        tid = t["id"]
        if tid != t["_file"]:
            errors.append(f"{t['_file']}.json contains id {tid}")
        missing = [k for k in TASK_KEYS if k not in t]
        if missing:
            errors.append(f"{tid}: missing keys {missing}")
            continue
        if t["type"] not in TYPES:
            errors.append(f"{tid}: unknown type {t['type']!r}")
        unknown = [x for x in t["expected_tools"] if x not in V1_TOOLS]
        if unknown:
            errors.append(f"{tid}: not v1 tools: {unknown}")
        if not isinstance(t["steps"], int):
            errors.append(f"{tid}: steps is not a whole number: {t['steps']!r}")
        if t["type"] in ("ASK", "STOP") and not t["simulated_user"]:
            errors.append(f"{tid}: {t['type']} task has no simulated user reply")
        if isinstance(t["steps"], int) and t["steps"] >= 3 and not t["expected_plan"]:
            errors.append(f"{tid}: steps={t['steps']} but expected_plan is empty")
        if not t["request"] or not t["pass_if"]:
            errors.append(f"{tid}: empty request or pass_if")

    # --- pass_if values not in the phone state (eyeball list, never an error) ---
    known = {c["phone"] for c in state["contacts"]} | {c["email"] for c in state["contacts"]}
    known |= {n["id"] for n in state["notes"]} | {r["time"] for r in state["reminders"]}
    known |= {e["start"] for e in state["events"]} | {e["end"] for e in state["events"]}
    eyeball_tasks = dev if hidden else tasks  # never print hidden pass_if content after the split
    print(f"\npass_if values not in phone_state.json ({len(eyeball_tasks)} public tasks; "
          f"usually new values the task creates):")
    for t in eyeball_tasks:
        new = [f"{kind} {v}" for kind, pat in VALUE_PATTERNS.items()
               for v in re.findall(pat, t.get("pass_if") or "") if v not in known]
        if new:
            print(f"  {t['id']} {t['type']:<6} {', '.join(new)}")

    # --- Summary ---
    print(f"\nTasks loaded: {len(tasks)} ({len(dev)} public, {len(hidden_files)} hidden)")
    types = Counter(t["type"] for t in tasks)
    print("By type:     " + "  ".join(f"{k} {types[k]}" for k in TYPES))
    multi = sum(isinstance(t["steps"], int) and t["steps"] >= 2 for t in tasks)
    print(f"Multi-step (steps >= 2): {multi} / {len(tasks)} ({multi / max(len(tasks), 1):.0%})")
    usage = Counter(tool for t in tasks for tool in set(t["expected_tools"]))
    print("Tool coverage (tasks using each tool):")
    for tool in V1_TOOLS:
        print(f"  {tool:<16} {usage[tool]:>3}{'   <-- unused' if not usage[tool] else ''}")

    if errors:
        print(f"\nFAILED with {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("\nOK: all checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
