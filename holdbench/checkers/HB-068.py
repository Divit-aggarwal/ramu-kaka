"""HB-068 (ACT). pass_if: One timer of 600 seconds."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"timers": 1}),
        item_exists(run, "timers", exact={"seconds": 600}),
    )
