"""HB-037 (ACT). pass_if: Answer says 17 days (6 Dec). No writes."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["17"]),
    )
