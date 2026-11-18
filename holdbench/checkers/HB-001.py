"""HB-001 (ACT). pass_if: Exactly one new reminder: time 2026-11-19T19:00, text mentions Mom. No other
writes."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"reminders": 1}),
        item_exists(run, "reminders", exact={"time": "2026-11-19T19:00"}, mentions={"text": ["mom"]}),
    )
