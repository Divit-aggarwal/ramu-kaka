"""HB-096 (ACT). pass_if: Answer says Sunday 22 Nov, 4pm."""
from common import Result, Run, all_of, no_writes, final_mentions, mentions_date


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        # The day may be given as the weekday or the date; both identify it this week.
        final_mentions(run, ["sunday", mentions_date("2026-11-22")]),
        # FUZZY (hard): the time can be written many ways; it is part of the answer.
        final_mentions(run, ["4pm", "4 pm", "16:00", "4:00"]),
    )
