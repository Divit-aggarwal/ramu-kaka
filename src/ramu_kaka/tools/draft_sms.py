"""draft_sms: open the SMS app with recipient and text filled in. The user presses send."""

from pydantic import Field, field_validator

from ramu_kaka.sandbox.state import Draft, PhoneState, Strict

NAME = "draft_sms"
DESCRIPTION = ("Prepare an SMS for one phone number. It opens in the SMS app and the user presses send; "
               "nothing is sent by you. Get the number from find_contact first.")
RISK = "Draft only"
VERSION = "v1"


class Args(Strict):
    phone: str = Field(pattern=r"^\+[\d ]+$",
                       description="Phone number from find_contact: + then 7-15 digits, e.g. +91 98100 44444.")
    text: str = Field(min_length=1, description="The message.")

    @field_validator("phone")
    @classmethod
    def _seven_to_fifteen_digits(cls, phone: str) -> str:
        digits = sum(c.isdigit() for c in phone)
        if not 7 <= digits <= 15:
            raise ValueError(f"must have 7-15 digits after the +, got {digits}")
        return phone


def run(state: PhoneState, args: Args) -> dict:
    draft = Draft(id=state.new_id("drafts"), kind="sms", to=args.phone, body=args.text)
    state.drafts.append(draft)
    return {"drafted": draft.model_dump(), "note": "Opened in the SMS app. Not sent: the user presses send."}
