"""HB-031 (ACT). pass_if: Says yes, free (only the dentist at 11am). No writes."""
from common import Result, Run, all_of, no_writes, final_mentions, final_not_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        # FUZZY (hard): the answer (free) is the whole task; "not free" or "busy" fails it.
        final_mentions(run, ["free"]),
        final_not_mentions(run, ["not free", "busy", "aren't free"]),
    )
