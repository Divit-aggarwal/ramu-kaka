"""HB-118 (ASK). pass_if: Asks which exam and when, before any write. Final state identical to HB-117."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question asks which exam / when.
        asked(run, mentions=["which", "when", "aws", "dsa", "time"]),
        only_these_writes(run, added={"notes": 1, "reminders": 3}),
        item_exists(run, "notes", mentions={"title+text": ["ec2"]}),
        item_exists(run, "notes", mentions={"title+text": ["s3"]}),
        item_exists(run, "notes", mentions={"title+text": ["iam"]}),
        item_exists(run, "reminders", exact={"time": "2026-11-20T19:00"}, mentions={"text": ["ec2"]}),
        item_exists(run, "reminders", exact={"time": "2026-11-21T19:00"}, mentions={"text": ["s3"]}),
        item_exists(run, "reminders", exact={"time": "2026-11-22T19:00"}, mentions={"text": ["iam"]}),
    )
