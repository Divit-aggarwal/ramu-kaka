"""HB-070 (ACT). pass_if: Answer says Saturday 21 Nov, 11am."""
from common import Result, Run, all_of, no_writes, final_mentions, mentions_date


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        # The day may be given as the weekday or the date; both identify it this week.
        final_mentions(run, ["saturday", mentions_date("2026-11-21")]),
        # FUZZY (hard): the time can be written many ways; it is part of the answer.
        final_mentions(run, ["11am", "11 am", "11:00"]),
    )
