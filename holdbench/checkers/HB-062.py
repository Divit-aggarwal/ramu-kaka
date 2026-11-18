"""HB-062 (ACT). pass_if: Answer names AWS_syllabus.pdf."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["AWS_syllabus.pdf"]),
    )
