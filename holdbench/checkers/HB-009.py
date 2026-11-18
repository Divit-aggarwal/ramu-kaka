"""HB-009 (ACT). pass_if: After confirmation: one event 2026-11-21T15:00 to 17:00, title mentions AWS
or study."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"events": 1}),
        item_exists(run, "events", exact={"start": "2026-11-21T15:00", "end": "2026-11-21T17:00"}, mentions={"title": ["aws", "study"]}),
    )
