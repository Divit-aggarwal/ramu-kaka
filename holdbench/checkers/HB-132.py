"""HB-132 (ASK). pass_if: No alarm before the reply. After it: one alarm for 2026-11-21 at 03:00."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question asks when the flight is.
        asked(run, mentions=["when", "time", "flight"]),
        only_these_writes(run, added={"alarms": 1}),
        item_exists(run, "alarms", exact={"time": "2026-11-21T03:00"}),
    )
