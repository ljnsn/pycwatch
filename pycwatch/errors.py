from typing import Any, Optional


class CryptowatchError(Exception):
    def __init__(
        self,
        message: Optional[str] = None,
        http_body: Optional[str] = None,
        http_status: Optional[int] = None,
        json_body: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}

    def __repr__(self) -> str:
        return "{}(message={}, http_status={})".format(
            self.__class__.__name__, self._message, self.http_status
        )


class APIResourceNotFoundError(CryptowatchError):
    pass


class APIRateLimitError(CryptowatchError):
    pass


class APIServerError(CryptowatchError):
    pass


class APIRequestError(CryptowatchError):
    pass


class APIKeyError(CryptowatchError):
    pass


class APIError(CryptowatchError):
    pass
