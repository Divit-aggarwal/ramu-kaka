"""HB-015 (ACT). pass_if: One new fact containing P-17."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"facts": 1}),
        item_exists(run, "facts", mentions={"text": ["p-17"]}),
    )
