"""HB-044 (ASK). pass_if: Asks which exam (and how long) before creating. After the reply: event
2026-12-12T10:00 to 12:00 mentioning DSA."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question names the exams or asks which / how long.
        asked(run, mentions=["which", "aws", "dsa", "how long"]),
        only_these_writes(run, added={"events": 1}),
        item_exists(run, "events", exact={"start": "2026-12-12T10:00", "end": "2026-12-12T12:00"}, mentions={"title": ["dsa"]}),
    )
