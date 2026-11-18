"""HB-125 (ACT). pass_if: One reminder at 2026-11-20T15:15."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"reminders": 1}),
        item_exists(run, "reminders", exact={"time": "2026-11-20T15:15"}),
    )
