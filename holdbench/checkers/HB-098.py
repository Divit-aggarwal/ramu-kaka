"""HB-098 (ACT). pass_if: After confirmation: N3 deleted, others untouched."""
from common import Result, Run, all_of, only_these_writes


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, removed={"notes": ["N3"]}),
    )
