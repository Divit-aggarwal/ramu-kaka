"""HB-100 (ACT). pass_if: One alarm for 2026-11-19 at 19:00."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"alarms": 1}),
        item_exists(run, "alarms", exact={"time": "2026-11-19T19:00"}),
    )
