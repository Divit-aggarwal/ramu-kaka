"""HB-028 (ASK). pass_if: Asks which exam (AWS on 6 Dec or DSA on 12 Dec) and the time before creating.
After the reply: reminder at 2026-12-11T20:00."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question names the exams or asks which/what time.
        asked(run, mentions=["which", "aws", "dsa", "time"]),
        only_these_writes(run, added={"reminders": 1}),
        item_exists(run, "reminders", exact={"time": "2026-12-11T20:00"}),
    )
