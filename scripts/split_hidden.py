"""Lock the HoldBench hidden test set. Run ONCE.

Usage: uv run python scripts/split_hidden.py
Picks 13 of 67 pairs with a fixed seed, moves both tasks of each picked pair to
holdbench/tasks_hidden/, and writes only the seed, the pair IDs and a SHA-256 hash to
holdbench/HIDDEN_SET.md. Refuses to run again once HIDDEN_SET.md exists: no re-rolling.
"""

import json
import random
from collections import Counter

import validate_holdbench
from holdbench_common import HIDDEN_DIR, HIDDEN_SET_MD, TASKS_DIR, TYPES, sha256_of

SEED = 20261119
N_HIDDEN_PAIRS = 13  # 20% of 67 pairs


def main() -> None:
    if HIDDEN_SET_MD.exists():
        raise SystemExit(f"{HIDDEN_SET_MD.name} already exists. The hidden set is locked; not re-rolling.")
    if validate_holdbench.main() != 0:
        raise SystemExit("Validation failed. Fix the tasks before locking the hidden set.")

    files = sorted(TASKS_DIR.glob("HB-*.json"))
    tasks = {f: json.loads(f.read_text()) for f in files}
    pairs = sorted({t["pair"] for t in tasks.values()})
    hidden_pairs = sorted(random.Random(SEED).sample(pairs, N_HIDDEN_PAIRS))

    moved = []
    for f, t in tasks.items():
        if t["pair"] in hidden_pairs:
            moved.append(f.rename(HIDDEN_DIR / f.name))
    digest = sha256_of(moved)

    HIDDEN_SET_MD.write_text(
        "# HoldBench hidden set\n\n"
        f"- Seed: {SEED}\n"
        f"- SHA-256: {digest}\n"
        f"- Hidden pairs ({len(hidden_pairs)}): {', '.join(hidden_pairs)}\n"
    )

    print(f"\nHidden: {len(hidden_pairs)} pairs, {len(moved)} tasks. Hash written to {HIDDEN_SET_MD.name}.")
    hidden_types = Counter(t["type"] for t in tasks.values() if t["pair"] in hidden_pairs)
    dev_types = Counter(t["type"] for t in tasks.values() if t["pair"] not in hidden_pairs)
    print(f"{'type':<8}{'dev':>5}{'hidden':>8}")
    for k in TYPES:
        print(f"{k:<8}{dev_types[k]:>5}{hidden_types[k]:>8}")
    print(f"{'total':<8}{sum(dev_types.values()):>5}{sum(hidden_types.values()):>8}")


if __name__ == "__main__":
    main()
