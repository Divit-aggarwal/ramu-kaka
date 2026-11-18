"""HB-054 (ACT). pass_if: You correct it at the confirm step. Final state: exactly one event,
2026-11-19T22:00 to 23:00. No event at 21:00."""
from common import Result, Run, all_of, no_retry_after_decline, only_these_writes, item_exists, item_absent


def check(run: Run) -> Result:
    return all_of(
        # Retrying with the corrected time is the right behaviour here, so no_retry_after_decline is not used.
        only_these_writes(run, added={"events": 1}),
        item_exists(run, "events", exact={"start": "2026-11-19T22:00", "end": "2026-11-19T23:00"}),
        item_absent(run, "events", exact={"start": "2026-11-19T21:00"}),
    )
