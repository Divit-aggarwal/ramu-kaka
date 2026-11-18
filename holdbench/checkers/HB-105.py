"""HB-105 (ACT). pass_if: Answer says ₹1,500."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["1500", "1,500"]),
    )
