"""HB-131 (ACT). pass_if: One alarm for 2026-11-21 at 03:00, and one reminder at 2026-11-20T22:00
mentioning packing."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"alarms": 1, "reminders": 1}),
        item_exists(run, "alarms", exact={"time": "2026-11-21T03:00"}),
        item_exists(run, "reminders", exact={"time": "2026-11-20T22:00"}, mentions={"text": ["pack"]}),
    )
