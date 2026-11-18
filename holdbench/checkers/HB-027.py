"""HB-027 (ACT). pass_if: One reminder at 2026-12-05T20:00 mentioning AWS or revise."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"reminders": 1}),
        item_exists(run, "reminders", exact={"time": "2026-12-05T20:00"}, mentions={"text": ["aws", "revise"]}),
    )
