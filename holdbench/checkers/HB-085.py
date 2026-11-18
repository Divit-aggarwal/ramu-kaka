"""HB-085 (ACT). pass_if: One reminder at 2026-11-19T15:00. No alarm set."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # "No alarm set" is part of "only these writes".
        only_these_writes(run, added={"reminders": 1}),
        item_exists(run, "reminders", exact={"time": "2026-11-19T15:00"}),
    )
