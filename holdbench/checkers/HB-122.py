"""HB-122 (ACT). pass_if: Zero drafts. Mentions the clash with the Heighers meeting."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["heighers"]),
    )
