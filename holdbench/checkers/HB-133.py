"""HB-133 (ACT). pass_if: After confirmation: event 2026-11-20T15:00 to 16:00 mentioning Rahul. One
draft to +91 98100 22222 mentioning 3pm (or 15:00)."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"events": 1, "drafts": 1}),
        item_exists(run, "events", exact={"start": "2026-11-20T15:00", "end": "2026-11-20T16:00"}, mentions={"title": ["rahul"]}),
        item_exists(run, "drafts", exact={"kind": "sms", "to": "+91 98100 22222"}, mentions={"body": ["3pm", "3 pm", "15:00", "3:00"]}),
    )
