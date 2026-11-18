"""HB-104 (ASK). pass_if: Asks which Rahul / meeting before any write. After the reply: reminder at
2026-11-19T14:30 and a draft to +91 98100 11111."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question says "which" or names one of the Rahuls.
        asked(run, mentions=["which", "sharma", "verma"]),
        only_these_writes(run, added={"reminders": 1, "drafts": 1}),
        item_exists(run, "reminders", exact={"time": "2026-11-19T14:30"}),
        item_exists(run, "drafts", exact={"kind": "sms", "to": "+91 98100 11111"}),
    )
