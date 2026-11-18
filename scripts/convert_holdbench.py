"""Convert holdbench/source/holdbench.xlsx into phone_state.json and one JSON file per task.

Usage: uv run python scripts/convert_holdbench.py
Tables are found by their title/header text, not by row number, so adding rows is safe.
Safe to re-run after the hidden split: hidden pairs (from HIDDEN_SET.md) go to tasks_hidden/.
"""

import re

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

from holdbench_common import (
    HIDDEN_DIR, PHONE_STATE, SOURCE_XLSX, TASKS_DIR, dump_json, read_hidden_set,
)

Cell = str | int | float | None
PHONE_TABLES = ["Contacts", "Notes", "Calendar", "Reminders", "Facts", "Files"]


def clean(value: object) -> Cell:
    """Strip text; blank cells become None. Anything else (e.g. a date object) fails loudly."""
    if isinstance(value, str):
        return value.strip() or None
    if value is None or isinstance(value, (int, float)):
        return value
    raise TypeError(f"Unexpected cell type {type(value).__name__}: {value!r}. Store it as text in the sheet.")


def stacked_tables(ws: Worksheet, titles: list[str]) -> dict[str, list[dict[str, Cell]]]:
    """Read tables stacked in one sheet: a title row, a header row, then data rows."""
    tables: dict[str, list[dict[str, Cell]]] = {}
    current: str | None = None
    header: dict[int, str] = {}
    for row in ws.iter_rows(values_only=True):
        cells = {i: clean(v) for i, v in enumerate(row) if clean(v) is not None}
        if not cells:
            continue
        values = list(cells.values())
        if len(values) == 1 and values[0] in titles:  # title row
            current, header = str(values[0]), {}
            tables[current] = []
        elif current and not header:  # header row right after the title
            header = {i: str(v) for i, v in cells.items()}
        elif current:
            tables[current].append({name: clean(row[i]) for i, name in header.items()})
    missing = [t for t in titles if t not in tables]
    if missing:
        raise SystemExit(f"Phone state tab is missing tables: {missing}")
    return tables


def phone_state(ws: Worksheet) -> dict[str, object]:
    t = stacked_tables(ws, PHONE_TABLES)
    return {
        "now": "2026-11-19T10:00",
        "timezone": "Asia/Kolkata",
        "contacts": [{"id": f"C{i}", "name": r["Name"], "phone": r["Phone"], "email": r["Email"]}
                     for i, r in enumerate(t["Contacts"], 1)],
        "notes": [{"id": r["ID"], "title": r["Title"], "text": r["Text"], "created": r["Created"]}
                  for r in t["Notes"]],
        "events": [{"id": f"E{i}", "title": r["Title"], "start": r["Start"], "end": r["End"]}
                   for i, r in enumerate(t["Calendar"], 1)],
        "reminders": [{"id": f"R{i}", "text": r["Text"], "time": r["Time"]}
                      for i, r in enumerate(t["Reminders"], 1)],
        "facts": [{"id": f"F{i}", "text": r["Fact"]} for i, r in enumerate(t["Facts"], 1)],
        "files": [{"id": f"D{i}", "name": r["Name"], "folder": r["Folder"], "downloaded": r["Downloaded"]}
                  for i, r in enumerate(t["Files"], 1)],
        "alarms": [],
        "timers": [],
        "drafts": [],
    }


FILLER_WORDS = {"none", "or", "optional", "declined", "correction", "allowed"}


def parse_tools(raw: str | None) -> list[str]:
    """'search_notes → delete_note ×2 (declined)' → ['search_notes', 'delete_note'].
    Keeps every lowercase word except known filler, so a misspelled tool name still reaches
    the validator (and fails there) instead of vanishing."""
    return [w for w in re.findall(r"[a-z][a-z_]*", raw or "") if w not in FILLER_WORDS]


def parse_simulated_user(raw: str | None) -> list[dict[str, str]]:
    """'the October one; Confirm: yes' → [answer 'the October one', confirm 'yes'].
    'then:' takes the kind of the part before it. 'yes (both)' / 'yes (both times)' means
    two separate confirm prompts, so it becomes two entries."""
    replies: list[dict[str, str]] = []
    kind = "answer"
    for part in (p.strip() for p in (raw or "").split(";")):
        if not part:
            continue
        if part.lower().startswith("confirm:"):
            kind, text = "confirm", part[len("confirm:"):].strip()
        elif part.lower().startswith("then:"):
            text = part[len("then:"):].strip()  # keeps the previous kind
        else:
            kind, text = "answer", part
        both = re.fullmatch(r"(.*?)\s*\(both(?: times)?\)", text)
        for t in [both.group(1)] * 2 if both else [text]:
            replies.append({"kind": kind, "text": t})
    return replies


def tasks(ws: Worksheet) -> list[dict[str, object]]:
    rows = list(ws.iter_rows(values_only=True))
    head_i = next(i for i, r in enumerate(rows) if "ID" in r and "Pair" in r)
    col = {str(name).strip(): i for i, name in enumerate(rows[head_i]) if name}
    out = []
    for r in rows[head_i + 1:]:
        task_id = clean(r[col["ID"]])
        if not (isinstance(task_id, str) and re.fullmatch(r"HB-\d{3}", task_id)):
            continue
        raw_tools = clean(r[col["Expected tools (in order)"]])
        raw_user = clean(r[col["Simulated user reply"]])
        out.append({
            "id": task_id,
            "pair": clean(r[col["Pair"]]),
            "type": clean(r[col["Type"]]),
            "request": clean(r[col["User request"]]),
            "expected_tools": parse_tools(raw_tools),
            "expected_tools_raw": raw_tools,
            "steps": clean(r[col["Steps"]]),
            "pass_if": clean(r[col["Pass if"]]),
            "simulated_user": parse_simulated_user(raw_user),
            "simulated_user_raw": raw_user,
            "why": clean(r[col["Why this task"]]),
            "expected_plan": clean(r[col["Expected plan (reasoning)"]]),
            "checks": None,  # machine-checkable pass_if: written in Phase 2 with the checkers
        })
    return out


def main() -> None:
    wb = openpyxl.load_workbook(SOURCE_XLSX)
    PHONE_STATE.write_text(dump_json(phone_state(wb["Phone state"])))

    hidden = read_hidden_set()
    hidden_pairs = hidden[0] if hidden else set()
    for d in (TASKS_DIR, HIDDEN_DIR):
        for old in d.glob("HB-*.json"):
            old.unlink()
    all_tasks = tasks(wb["HoldBench"])
    for task in all_tasks:
        folder = HIDDEN_DIR if task["pair"] in hidden_pairs else TASKS_DIR
        (folder / f"{task['id']}.json").write_text(dump_json(task))
    n_hidden = sum(t["pair"] in hidden_pairs for t in all_tasks)
    print(f"Wrote {PHONE_STATE.name} and {len(all_tasks)} tasks "
          f"({len(all_tasks) - n_hidden} in tasks/, {n_hidden} in tasks_hidden/).")


if __name__ == "__main__":
    main()
