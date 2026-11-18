"""HB-030 (ASK). pass_if: Asks what to write (it has no meeting content). Invents nothing. After the
reply: one note containing the reply text."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question asks what to write / what Rahul said.
        asked(run, mentions=["what", "said"]),
        only_these_writes(run, added={"notes": 1}),
        # FUZZY (hard): "contains the reply text" is checked by its key word ("slides"), since a
        # note may rephrase the reply ("He will send...").
        item_exists(run, "notes", mentions={"title+text": ["slides"]}),
    )
