class APIError(Exception):
    """
    Base exception for all API errors.
    """

    _raw_error: dict[str, str]
    message: str
    code: str
    hint: str
    details: str

    def __init__(self, error: dict[str, str]) -> None:
        self._raw_error = error
        self.message = error["message"]
        self.code = error["code"]
        self.hint = error["hint"]
        self.details = error["details"]
        super().__init__(str(self))

    def __str__(self):
        error_text = f"Error {self.code}:" if self.code else ""
        message_text = f"\nMessage: {self.message}" if self.message else ""
        hint_text = f"\nHint: {self.hint}" if self.hint else ""
        details_text = f"\nDetails: {self.details}" if self.details else ""
        complete_error_text = f"{error_text}{message_text}{hint_text}{details_text}"
        return complete_error_text or "Empty error"

    def json(self):
        return self._raw_error
