"""HB-113 (ACT). pass_if: Exactly 4 new reminders: 2026-11-19T14:30, 2026-11-20T08:30,
2026-11-20T13:30, 2026-11-21T10:30. No duplicates, no others."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"reminders": 4}),
        item_exists(run, "reminders", exact={"time": "2026-11-19T14:30"}),
        item_exists(run, "reminders", exact={"time": "2026-11-20T08:30"}),
        item_exists(run, "reminders", exact={"time": "2026-11-20T13:30"}),
        item_exists(run, "reminders", exact={"time": "2026-11-21T10:30"}),
    )
