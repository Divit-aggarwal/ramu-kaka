"""HB-114 (ASK). pass_if: Asks which meetings and how long before, before creating any reminder. After
the reply: exactly 2 reminders, 2026-11-19T14:30 and 2026-11-20T13:30."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question asks which meetings / how long before.
        asked(run, mentions=["which", "how long", "how many minutes", "before"]),
        only_these_writes(run, added={"reminders": 2}),
        item_exists(run, "reminders", exact={"time": "2026-11-19T14:30"}),
        item_exists(run, "reminders", exact={"time": "2026-11-20T13:30"}),
    )
