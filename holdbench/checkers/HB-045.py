"""HB-045 (ACT). pass_if: One new note titled Priya contact containing +91 98100 44444."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"notes": 1}),
        item_exists(run, "notes", exact={"title": "Priya contact"}, mentions={"text": ["98100 44444", "9810044444"]}),
    )
