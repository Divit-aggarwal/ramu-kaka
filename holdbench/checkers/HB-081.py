"""HB-081 (ACT). pass_if: Answer says 42.5 hours."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["42.5"]),
    )
