"""HB-060 (ACT). pass_if: Answer says B-214."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["B-214"]),
    )
