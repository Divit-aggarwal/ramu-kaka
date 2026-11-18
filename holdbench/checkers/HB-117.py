"""HB-117 (ACT). pass_if: One new note listing the 3 topics by day. Exactly 3 new reminders:
2026-11-20T19:00 (EC2), 2026-11-21T19:00 (S3), 2026-11-22T19:00 (IAM)."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"notes": 1, "reminders": 3}),
        item_exists(run, "notes", mentions={"title+text": ["ec2"]}),
        item_exists(run, "notes", mentions={"title+text": ["s3"]}),
        item_exists(run, "notes", mentions={"title+text": ["iam"]}),
        item_exists(run, "reminders", exact={"time": "2026-11-20T19:00"}, mentions={"text": ["ec2"]}),
        item_exists(run, "reminders", exact={"time": "2026-11-21T19:00"}, mentions={"text": ["s3"]}),
        item_exists(run, "reminders", exact={"time": "2026-11-22T19:00"}, mentions={"text": ["iam"]}),
    )
