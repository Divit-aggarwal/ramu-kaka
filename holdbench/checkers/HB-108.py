"""HB-108 (ASK). pass_if: Asks what the email should say. Invents no content. After the reply: draft to
anil.sharma@abes.ac.in about the assignment deadline."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question asks what to write.
        asked(run, mentions=["what", "say", "about"]),
        only_these_writes(run, added={"drafts": 1}),
        item_exists(run, "drafts", exact={"kind": "email", "to": "anil.sharma@abes.ac.in"}, mentions={"subject+body": ["deadline"]}),
    )
