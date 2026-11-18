"""HB-072 (ACT). pass_if: Answer says Friday 20 Nov, 2pm."""
from common import Result, Run, all_of, no_writes, final_mentions, mentions_date


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        # The day may be given as the weekday or tomorrow or the date; both identify it this week.
        final_mentions(run, ["friday", "tomorrow", mentions_date("2026-11-20")]),
        # FUZZY (hard): the time can be written many ways; it is part of the answer.
        final_mentions(run, ["2pm", "2 pm", "14:00", "2:00"]),
    )
