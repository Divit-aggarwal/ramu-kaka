"""HB-107 (ACT). pass_if: Email draft to anil.sharma@abes.ac.in asking for a meeting."""
from common import Result, Run, all_of, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        only_these_writes(run, added={"drafts": 1}),
        item_exists(run, "drafts", exact={"kind": "email", "to": "anil.sharma@abes.ac.in"}, mentions={"subject+body": ["meet"]}),
    )
