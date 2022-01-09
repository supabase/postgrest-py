from typing import Dict


class APIError(Exception):
    """
    Base exception for all API errors.
    """

    _raw_error: Dict[str, str]
    message: str
    code: str
    hint: str
    details: str

    def __init__(self, error: Dict[str, str]) -> None:
        self._raw_error = error
        self.message = error["message"]
        self.code = error["code"]
        self.hint = error["hint"]
        self.details = error["details"]
        Exception.__init__(self, str(self))

    def __repr__(self) -> str:
        error_text = f"Error {self.code}:" if self.code else ""
        message_text = f"\nMessage: {self.message}" if self.message else ""
        hint_text = f"\nHint: {self.hint}" if self.hint else ""
        details_text = f"\nDetails: {self.details}" if self.details else ""
        complete_error_text = f"{error_text}{message_text}{hint_text}{details_text}"
        return complete_error_text or "Empty error"

    def json(self) -> Dict[str, str]:
        return self._raw_error
