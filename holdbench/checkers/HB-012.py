"""HB-012 (ASK). pass_if: Asks which Rahul / meeting (today with Sharma, ends 17:00; Friday with Verma,
ends 15:00). After the reply: reminder at 2026-11-20T15:00."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question says "which" or names one of the Rahuls/meetings.
        asked(run, mentions=["which", "sharma", "verma"]),
        only_these_writes(run, added={"reminders": 1}),
        item_exists(run, "reminders", exact={"time": "2026-11-20T15:00"}, mentions={"text": ["rahul"]}),
    )
