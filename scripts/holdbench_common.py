"""Shared constants and helpers for the HoldBench scripts (convert, validate, split)."""

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOLDBENCH = ROOT / "holdbench"
SOURCE_XLSX = HOLDBENCH / "source" / "holdbench.xlsx"
PHONE_STATE = HOLDBENCH / "phone_state.json"
TASKS_DIR = HOLDBENCH / "tasks"
HIDDEN_DIR = HOLDBENCH / "tasks_hidden"
HIDDEN_SET_MD = HOLDBENCH / "HIDDEN_SET.md"

TYPES = ["ACT", "ASK", "REFUSE", "CAN'T", "STOP"]

# The 18 frozen v1 tools (CLAUDE.md). Phase 2's tools/ package will replace this list.
V1_TOOLS = [
    "get_datetime", "calculate", "ask_user", "set_alarm", "set_timer", "create_note",
    "search_notes", "delete_note", "remember_fact", "recall_facts", "create_reminder",
    "list_reminders", "search_calendar", "create_event", "find_contact", "draft_sms",
    "draft_email", "search_files",
]


def dump_json(obj: object) -> str:
    """One fixed JSON format. The hidden-set hash depends on these exact bytes."""
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def sha256_of(files: list[Path]) -> str:
    """SHA-256 over the files' contents, concatenated in filename order."""
    h = hashlib.sha256()
    for f in sorted(files, key=lambda p: p.name):
        h.update(f.read_bytes())
    return h.hexdigest()


def read_hidden_set() -> tuple[set[str], str] | None:
    """(hidden pair IDs, hash) from HIDDEN_SET.md, or None if the split hasn't happened."""
    if not HIDDEN_SET_MD.exists():
        return None
    text = HIDDEN_SET_MD.read_text()
    pairs = set(re.findall(r"\bP\d{2}\b", text))
    digest = re.search(r"\b[0-9a-f]{64}\b", text)
    if not pairs or not digest:
        raise SystemExit(f"{HIDDEN_SET_MD} exists but has no pair IDs or no hash.")
    return pairs, digest.group(0)
