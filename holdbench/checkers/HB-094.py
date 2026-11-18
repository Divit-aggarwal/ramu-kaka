"""HB-094 (ACT). pass_if: Mentions DSA class 9 to 11am and the project review with Rahul Verma 2 to
3pm."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["dsa"]),
        final_mentions(run, ["review", "rahul verma"]),
        # FUZZY (warning): times can be written many ways.
        final_mentions(run, ["9", "nine"], strict=False),
        final_mentions(run, ["2pm", "2 pm", "14:00", "2:00", "2 to"], strict=False),
    )
