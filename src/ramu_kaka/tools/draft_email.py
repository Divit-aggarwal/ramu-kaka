"""draft_email: open the email app with to, subject and body filled in. The user presses send."""

from pydantic import Field

from ramu_kaka.sandbox.state import Draft, PhoneState, Strict

NAME = "draft_email"
DESCRIPTION = ("Prepare an email to one address. It opens in the email app and the user presses send; "
               "nothing is sent by you. Get the address from find_contact first.")
RISK = "Draft only"
VERSION = "v1"


class Args(Strict):
    to: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$", description="Email address, e.g. anil.sharma@abes.ac.in.")
    subject: str = Field(min_length=1, description="Short subject line.")
    body: str = Field(min_length=1, description="The email text.")


def run(state: PhoneState, args: Args) -> dict:
    draft = Draft(id=state.new_id("drafts"), kind="email", to=args.to, subject=args.subject, body=args.body)
    state.drafts.append(draft)
    return {"drafted": draft.model_dump(), "note": "Opened in the email app. Not sent: the user presses send."}
