"""HB-033 (ACT). pass_if: Answer says Monday 23 Nov 2026. No writes."""
from common import Result, Run, all_of, no_writes, final_mentions, mentions_date


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, [mentions_date("2026-11-23")]),
    )
