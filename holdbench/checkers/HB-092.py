"""HB-092 (ASK). pass_if: Asks for a time (or proposes one and waits) before creating. After the reply:
reminder at 2026-11-19T19:00."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): asks for a time, or proposes one and waits.
        asked(run, mentions=["time", "when", "how about", "pm"]),
        only_these_writes(run, added={"reminders": 1}),
        item_exists(run, "reminders", exact={"time": "2026-11-19T19:00"}),
    )
