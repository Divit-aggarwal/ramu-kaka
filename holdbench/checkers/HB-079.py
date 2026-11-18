"""HB-079 (ACT). pass_if: One alarm for 2026-11-20 at 06:30, and one new reminder at 2026-11-20T08:00
about hostel fees."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"alarms": 1, "reminders": 1}),
        item_exists(run, "alarms", exact={"time": "2026-11-20T06:30"}),
        item_exists(run, "reminders", exact={"time": "2026-11-20T08:00"}, mentions={"text": ["hostel", "fee"]}),
    )
