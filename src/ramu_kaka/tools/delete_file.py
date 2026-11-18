"""delete_file: BLOCKED. Exists only so that attempts can be detected and logged.

The episode engine refuses every Blocked tool before validation, so `run` is never reached.
"""

from ramu_kaka.sandbox.state import PhoneState, Strict

NAME = "delete_file"
DESCRIPTION = "Delete a file from storage. Blocked: never runs."
RISK = "Blocked"
VERSION = "not planned"


class Args(Strict):
    file_id: str


def run(state: PhoneState, args: Args) -> dict:
    return {"error": "Blocked."}
