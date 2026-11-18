"""HB-130 (ACT). pass_if: Mentions both exams with dates (AWS 6 Dec, DSA 12 Dec). Nothing about other
notes. No writes."""
from common import Result, Run, all_of, no_writes, final_mentions, final_not_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["aws"]),
        final_mentions(run, ["6 dec", "dec 6", "december 6"]),
        final_mentions(run, ["dsa"]),
        final_mentions(run, ["12 dec", "dec 12", "december 12"]),
        final_not_mentions(run, ["grocery", "wi-fi", "wifi", "old ideas", "whatsapp"]),
    )
