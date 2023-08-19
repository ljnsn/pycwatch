"""Pycwatch exceptions."""


class PycwatchError(Exception):
    """Base exception for pycwatch."""


class ResponseStructureError(PycwatchError):
    """Raised when the response could not be structured."""
