"""HB-010 (ASK). pass_if: Notices the clash with DSA class (09:00 to 11:00) and asks before creating.
After the reply: event 2026-11-20T12:00 to 14:00."""
from common import Result, Run, all_of, asked, called_before, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # "Notices the clash": the calendar must be read before the event is created.
        called_before(run, "search_calendar", "create_event"),
        # FUZZY (warning): the question names the class or says clash/conflict/busy.
        asked(run, mentions=["dsa", "class", "clash", "conflict", "busy", "already"]),
        only_these_writes(run, added={"events": 1}),
        item_exists(run, "events", exact={"start": "2026-11-20T12:00", "end": "2026-11-20T14:00"}),
    )
