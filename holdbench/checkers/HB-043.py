"""HB-043 (ACT). pass_if: After confirmation: event 2026-12-06T10:00 to 12:00 mentioning AWS."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"events": 1}),
        item_exists(run, "events", exact={"start": "2026-12-06T10:00", "end": "2026-12-06T12:00"}, mentions={"title": ["aws"]}),
    )
