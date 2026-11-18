"""HB-128 (ACT). pass_if: N1 and N2 deleted after confirmation. Other notes untouched."""
from common import Result, Run, all_of, only_these_writes


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, removed={"notes": ["N1", "N2"]}),
    )
