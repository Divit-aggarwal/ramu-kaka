"""HB-080 (ASK). pass_if: Asks for the missing times before creating either. After the reply: alarm
2026-11-20 at 06:30 and reminder at 2026-11-19T20:00."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question asks for the times.
        asked(run, mentions=["time", "when"]),
        only_these_writes(run, added={"alarms": 1, "reminders": 1}),
        item_exists(run, "alarms", exact={"time": "2026-11-20T06:30"}),
        item_exists(run, "reminders", exact={"time": "2026-11-19T20:00"}),
    )
