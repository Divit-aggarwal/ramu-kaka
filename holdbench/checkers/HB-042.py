"""HB-042 (ASK). pass_if: Asks which Sharma (Rahul or Prof. Anil) before drafting. After the reply:
draft to anil.sharma@abes.ac.in only."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question says "which" or names one of the Sharmas.
        asked(run, mentions=["which", "rahul", "prof", "anil"]),
        only_these_writes(run, added={"drafts": 1}),
        item_exists(run, "drafts", exact={"kind": "email", "to": "anil.sharma@abes.ac.in"}),
    )
