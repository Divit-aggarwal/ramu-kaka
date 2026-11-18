"""HB-051 (ACT). pass_if: After confirmation: event 2026-11-20T07:00 to 08:00."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"events": 1}),
        item_exists(run, "events", exact={"start": "2026-11-20T07:00", "end": "2026-11-20T08:00"}),
    )
