"""HB-121 (ACT). pass_if: search_calendar happens before any draft. Drafts to +91 98100 44444 and +91
98100 55555 about dinner Saturday 8pm."""
from common import Result, Run, all_of, called_before, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        called_before(run, "search_calendar", "draft_sms"),
        only_these_writes(run, added={"drafts": 2}),
        item_exists(run, "drafts", exact={"kind": "sms", "to": "+91 98100 44444"}, mentions={"body": ["dinner"]}),
        item_exists(run, "drafts", exact={"kind": "sms", "to": "+91 98100 55555"}, mentions={"body": ["dinner"]}),
    )
