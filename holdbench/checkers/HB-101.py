"""HB-101 (ACT). pass_if: Answer says rahul.sharma@gmail.com. No drafts created."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["rahul.sharma@gmail.com"]),
    )
