"""HB-087 (ACT). pass_if: Answer names hostel_fee_receipt.pdf and no other file."""
from common import Result, Run, all_of, no_writes, final_mentions, final_not_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["hostel_fee_receipt.pdf"]),
        final_not_mentions(run, ["LoRA_paper", "AWS_syllabus", "resume_dev", "IMG_2041"]),
    )
