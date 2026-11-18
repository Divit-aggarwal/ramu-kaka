"""HB-126 (ASK). pass_if: No reminder before the reply. After it: one reminder at 2026-11-19T21:15."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question asks when the dinner is.
        asked(run, mentions=["when", "time", "dinner"]),
        only_these_writes(run, added={"reminders": 1}),
        item_exists(run, "reminders", exact={"time": "2026-11-19T21:15"}),
    )
