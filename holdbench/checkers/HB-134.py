"""HB-134 (ASK). pass_if: Asks which Rahul and what time before any write. After the reply: event
2026-11-20T16:00 to 17:00 and one draft to +91 98100 11111 mentioning 4pm."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question asks which Rahul / what time.
        asked(run, mentions=["which", "sharma", "verma", "time"]),
        only_these_writes(run, added={"events": 1, "drafts": 1}),
        item_exists(run, "events", exact={"start": "2026-11-20T16:00", "end": "2026-11-20T17:00"}),
        item_exists(run, "drafts", exact={"kind": "sms", "to": "+91 98100 11111"}, mentions={"body": ["4pm", "4 pm", "16:00", "4:00"]}),
    )
