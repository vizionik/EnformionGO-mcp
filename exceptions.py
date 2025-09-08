"""Custom exceptions for the EnformionGO API wrapper."""

class EnformionGOException(Exception):
    """Base exception for the EnformionGO API wrapper."""

    def __init__(self, detail: str):
        """Initializes the exception.

        Args:
            detail: The detail of the exception.
        """
        self.detail = detail
        super().__init__(self.detail)


class APIConnectionError(EnformionGOException):
    """Raised when there is an error connecting to the EnformionGO API."""


class InvalidRequestError(EnformionGOException):
    """Raised when the request to the EnformionGO API is invalid."""
