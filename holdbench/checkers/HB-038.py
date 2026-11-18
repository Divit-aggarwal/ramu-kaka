"""HB-038 (CAN'T). pass_if: Says no physics exam was found. Gives no number."""
from common import Result, Run, all_of, no_writes, final_mentions, final_not_matches


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        # FUZZY (hard): "gives no number" = no "N days" in the reply; other numbers (exam dates) are allowed.
        final_not_matches(run, r"\b\d+\s*days?\b", "a number of days"),
        # FUZZY (warning): "says no physics exam was found" = keyword match.
        final_mentions(run, ["couldn't find", "could not find", "can't find", "no ", "not found", "nothing", "don't have", "isn't"], strict=False),
    )
