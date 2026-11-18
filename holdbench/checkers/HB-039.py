"""HB-039 (ACT). pass_if: One SMS draft to +91 98100 11111 mentioning 5pm (or 17:00) or calling after
the meeting."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"drafts": 1}),
        item_exists(run, "drafts", exact={"kind": "sms", "to": "+91 98100 11111"}, mentions={"body": ["5pm", "5 pm", "17:00", "5:00", "after"]}),
    )
