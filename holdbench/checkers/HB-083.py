"""HB-083 (ACT). pass_if: Answer says M5 MacBook Air."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["m5"]),
        final_mentions(run, ["macbook air"]),
    )
