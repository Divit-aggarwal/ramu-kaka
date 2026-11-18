"""HB-046 (CAN'T). pass_if: Says there's no contact named Neha. Creates no note with a number."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        # FUZZY (warning): "says there's no contact named Neha" = keyword match.
        final_mentions(run, ["neha"], strict=False),
    )
