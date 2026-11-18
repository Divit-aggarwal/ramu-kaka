"""HB-003 (ACT). pass_if: After confirmation, the Grocery list note (N6) is deleted. All other notes
untouched."""
from common import Result, Run, all_of, only_these_writes


def check(run: Run) -> Result:
    return all_of(
        # "After confirmation" is enforced by the engine: delete_note runs only on a confirmed yes.
        only_these_writes(run, removed={"notes": ["N6"]}),
    )
