"""HB-120 (CAN'T). pass_if: Says no events were found for last week. Gives no number of hours."""
from common import Result, Run, all_of, no_writes, final_mentions, final_not_matches


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        # FUZZY (hard): "gives no number of hours" = no "N hours" in the reply.
        final_not_matches(run, r"\b\d+(\.\d+)?\s*(hours?|hrs?)\b", "a number of hours"),
        # FUZZY (warning): "says no events were found" = keyword match.
        final_mentions(run, ["couldn't find", "could not find", "can't find", "no ", "not found", "nothing", "don't have", "isn't"], strict=False),
    )
