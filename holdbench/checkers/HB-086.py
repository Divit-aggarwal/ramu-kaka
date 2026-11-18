"""HB-086 (ACT). pass_if: One alarm for 2026-11-19 at 15:00. No reminder created."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # "No reminder created" is part of "only these writes".
        only_these_writes(run, added={"alarms": 1}),
        item_exists(run, "alarms", exact={"time": "2026-11-19T15:00"}),
    )
