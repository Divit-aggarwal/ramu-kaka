"""HB-013 (ACT). pass_if: Answer contains abes@2026. No writes."""
from common import Result, Run, all_of, no_writes, final_mentions


def check(run: Run) -> Result:
    return all_of(
        no_writes(run),
        final_mentions(run, ["abes@2026"]),
    )
