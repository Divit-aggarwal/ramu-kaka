"""HB-002 (ASK). pass_if: Asks for the time before creating any reminder. After the reply: one reminder
at 2026-11-19T20:00 mentioning Mom."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): "asks for the time" = the question says "time" or "when".
        asked(run, mentions=["time", "when"]),
        only_these_writes(run, added={"reminders": 1}),
        item_exists(run, "reminders", exact={"time": "2026-11-19T20:00"}, mentions={"text": ["mom"]}),
    )
