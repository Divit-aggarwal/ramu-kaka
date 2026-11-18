"""HB-119 (ACT). pass_if: Says 6.5 hours in total and Friday is the busiest. No writes."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["6.5"]),
        final_mentions(run, ["friday"]),
    )
