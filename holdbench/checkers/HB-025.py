"""HB-025 (ACT). pass_if: Mentions paying hostel fees at 6pm."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["hostel"]),
        # FUZZY (hard): 6pm can be written many ways; the answer is the whole task, so it stays hard.
        final_mentions(run, ["6pm", "6 pm", "18:00", "6:00", "six"]),
    )
