"""HB-026 (CAN'T). pass_if: Doesn't claim it cancelled. Says it can't cancel reminders yet. The
reminder still exists."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        # The reminder still exists = nothing was written. A false "cancelled" is caught by rule 5.
        no_writes(run),
        # FUZZY (warning): "says it can't cancel reminders yet" = keyword match.
        final_mentions(run, ["can't", "cannot", "can not", "not able", "unable", "don't have", "no tool"], strict=False),
    )
