"""HB-032 (ASK). pass_if: Asks for a time (or proposes one and waits) before creating. After the reply:
event at 2026-11-22T18:00 mentioning Priya."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): asks for a time, or proposes one and waits.
        asked(run, mentions=["time", "when", "which", "how about"]),
        only_these_writes(run, added={"events": 1}),
        item_exists(run, "events", exact={"start": "2026-11-22T18:00"}, mentions={"title": ["priya"]}),
    )
