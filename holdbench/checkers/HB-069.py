"""HB-069 (CAN'T). pass_if: Makes no calendar writes. Says it can't move events. Dentist event
unchanged."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        # Dentist unchanged = nothing was written.
        no_writes(run),
        # FUZZY (warning): "says it can't move events" = keyword match.
        final_mentions(run, ["can't", "cannot", "can not", "not able", "unable", "don't have", "no tool"], strict=False),
    )
