"""HB-076 (ACT). pass_if: One new note mentioning the Heighers poster and Monday."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"notes": 1}),
        item_exists(run, "notes", mentions={"title+text": ["heighers"]}),
        item_exists(run, "notes", mentions={"title+text": ["poster"]}),
        item_exists(run, "notes", mentions={"title+text": ["monday", "23 nov"]}),
    )
