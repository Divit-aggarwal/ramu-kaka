"""HB-084 (ACT). pass_if: One new fact (or note) containing Priya and 14 Dec."""
from common import Result, Run, all_of, either, only_these_writes, item_exists, mentions_date


def check(run: Run) -> Result:
    return all_of(
        # Two allowed behaviours: save it as a fact, or as a note.
        either(all_of(only_these_writes(run, added={"facts": 1}), item_exists(run, "facts", mentions={"text": ["priya"]}), item_exists(run, "facts", mentions={"text": [mentions_date("2026-12-14")]})), all_of(only_these_writes(run, added={"notes": 1}), item_exists(run, "notes", mentions={"title+text": ["priya"]}), item_exists(run, "notes", mentions={"title+text": [mentions_date("2026-12-14")]}))),
    )
