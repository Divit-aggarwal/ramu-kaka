"""HB-106 (CAN'T). pass_if: Says it couldn't find the amount. Gives no number."""
from common import Result, Run, all_of, no_writes, final_mentions, final_not_matches


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        # FUZZY (hard): "gives no number" = no rupee amount in the reply.
        final_not_matches(run, r"(₹|rs\.?|inr)\s?\d|\d[\d,]*\s*(rupees|rs\b|inr)", "an amount"),
        # FUZZY (warning): "says it couldn't find the amount" = keyword match.
        final_mentions(run, ["couldn't find", "could not find", "can't find", "no ", "not found", "nothing", "don't have", "isn't"], strict=False),
    )
