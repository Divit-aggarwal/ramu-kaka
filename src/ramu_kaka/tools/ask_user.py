"""ask_user: ask the user a question and wait for the answer.

The episode engine handles this tool itself (it owns the simulated user), so `run` is never reached.
"""

from ramu_kaka.sandbox.episode import AskUserArgs
from ramu_kaka.sandbox.state import PhoneState

NAME = "ask_user"
DESCRIPTION = ("Ask the user a question and wait for the answer. Use it when the request is unclear, "
               "info is missing, or more than one item matches. Optionally give short answer options.")
RISK = "Safe"
VERSION = "v1"
Args = AskUserArgs


def run(state: PhoneState, args: AskUserArgs) -> dict:
    return {"error": "ask_user is handled by the episode engine."}
