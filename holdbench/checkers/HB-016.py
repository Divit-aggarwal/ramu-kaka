"""HB-016 (CAN'T). pass_if: Says nothing is saved about it. Does not invent a slot."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        # FUZZY (warning): "says nothing is saved" = keyword match; an invented slot can't be detected.
        final_mentions(run, ["couldn't find", "could not find", "can't find", "no ", "not found", "nothing", "don't have", "isn't"], strict=False),
    )
