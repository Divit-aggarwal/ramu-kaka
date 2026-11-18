"""HB-103 (ACT). pass_if: Reminder at 2026-11-20T13:30, plus an SMS draft to +91 98100 22222 confirming
the review."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"reminders": 1, "drafts": 1}),
        item_exists(run, "reminders", exact={"time": "2026-11-20T13:30"}),
        # FUZZY (warning): "confirming the review" = mentions review/confirm.
        item_exists(run, "drafts", exact={"kind": "sms", "to": "+91 98100 22222"}),
        item_exists(run, "drafts", exact={"kind": "sms"}, mentions={"body": ["review", "confirm"]}, strict=False),
    )
