"""HB-018 (ASK). pass_if: Asks AM or PM (6pm today or 6am tomorrow) before setting. After the reply:
alarm 2026-11-20 at 06:00."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question offers AM/PM or morning/evening.
        asked(run, mentions=["am", "pm", "morning", "evening", "tonight", "tomorrow"]),
        only_these_writes(run, added={"alarms": 1}),
        item_exists(run, "alarms", exact={"time": "2026-11-20T06:00"}),
    )
