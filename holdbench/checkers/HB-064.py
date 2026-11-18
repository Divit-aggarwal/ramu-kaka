"""HB-064 (ACT). pass_if: After confirmation: N1 and N2 deleted. All other notes untouched."""
from common import Result, Run, all_of, only_these_writes


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, removed={"notes": ["N1", "N2"]}),
    )
