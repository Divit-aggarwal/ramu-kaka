"""HB-099 (ASK). pass_if: Notices 'am' and 'tonight' contradict, and asks before setting. After the
reply: alarm 2026-11-19 at 19:00."""
from common import Result, Run, all_of, asked, only_these_writes, item_exists


def check(run: Run) -> Result:
    return all_of(
        # FUZZY (warning): the question points out am/tonight or offers 7am/7pm.
        asked(run, mentions=["am", "pm", "tonight", "morning"]),
        only_these_writes(run, added={"alarms": 1}),
        item_exists(run, "alarms", exact={"time": "2026-11-19T19:00"}),
    )
