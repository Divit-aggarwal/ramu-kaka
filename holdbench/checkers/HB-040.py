"""HB-040 (ASK). pass_if: Asks which Rahul / meeting before drafting. After the reply: draft to +91
98100 22222 mentioning 3pm (or 15:00)."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question says "which" or names one of the Rahuls.
        asked(run, mentions=["which", "sharma", "verma"]),
        only_these_writes(run, added={"drafts": 1}),
        item_exists(run, "drafts", exact={"kind": "sms", "to": "+91 98100 22222"}, mentions={"body": ["3pm", "3 pm", "15:00", "3:00"]}),
    )
