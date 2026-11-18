"""Every oracle passes its checker, every mutation fails, and hidden checkers never leak."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from holdbench_common import HOLDBENCH, read_hidden_set  # noqa: E402


def test_all_oracles_pass_and_all_mutations_fail() -> None:
    # --all = every task file present. On a fresh clone tasks_hidden/ is empty, so only the 108
    # public tasks run; locally the 26 hidden ones run too (from the git-ignored *_hidden folders).
    result = subprocess.run([sys.executable, str(ROOT / "scripts" / "run_oracles.py"), "--all"],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout[-3000:] + result.stderr


def test_no_hidden_checker_or_oracle_in_public_folders() -> None:
    hidden = read_hidden_set()
    assert hidden, "HIDDEN_SET.md is missing"
    import json
    leaked = []
    for folder in ("checkers", "oracles"):
        for f in (HOLDBENCH / folder).glob("HB-*"):
            task_id = f.name[:6]
            task_file = HOLDBENCH / "tasks" / f"{task_id}.json"
            if not task_file.exists() or json.loads(task_file.read_text())["pair"] in hidden[0]:
                leaked.append(f.name)
    assert leaked == []
