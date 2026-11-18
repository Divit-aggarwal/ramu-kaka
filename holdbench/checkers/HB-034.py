"""HB-034 (ASK). pass_if: Doesn't silently pick one Friday. Passes if EITHER (a) it asks which Friday
and, after the reply, says Friday 27 Nov 2026, OR (b) it clearly gives both dates (20 Nov and 27
Nov) without asking. No writes."""
from common import Result, Run, all_of, either, asked, no_writes, final_mentions, mentions_date


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        # Two allowed behaviours: (a) ask which Friday, then say 27 Nov; (b) give both dates without asking.
        # "tomorrow" also counts as naming Friday 20 Nov.
        either(
            all_of(asked(run), final_mentions(run, [mentions_date("2026-11-27")])),
            all_of(final_mentions(run, [mentions_date("2026-11-20"), "tomorrow"]),
                   final_mentions(run, [mentions_date("2026-11-27")])),
        ),
    )
