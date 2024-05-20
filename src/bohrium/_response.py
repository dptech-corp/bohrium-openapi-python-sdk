import httpx
from typing import Any, Optional, Dict


class APIErrorResponse:
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        return {"error": self.message, "status_code": self.status_code}

    def __repr__(self) -> str:
        return f"<APIErrorResponse(status_code={self.status_code}, message='{self.message}')>"


class APIResponse:
    def __init__(self, response: httpx.Response):
        self._response = response
        self.status_code = response.status_code
        self.headers = response.headers
        self._json = self._parse_json(response)

    def _parse_json(self, response: httpx.Response) -> Optional[Any]:
        """Parses the JSON content of the response."""
        try:
            return response.json()
        except ValueError:
            return APIErrorResponse("Invalid JSON response", response.status_code)

    @property
    def json(self) -> Optional[Any]:
        """Returns the JSON content of the response or an APIErrorResponse if parsing fails."""
        return self._json

    def is_success(self) -> bool:
        """Returns True if the response status code indicates success."""
        return 200 <= self.status_code < 300

    def raise_for_status(self):
        """Raises an HTTPError if the response status code indicates an error."""
        if not self.is_success():
            raise httpx.HTTPStatusError(
                f"HTTP Error {self.status_code} for url {self._response.url}",
                request=self._response.request,
                response=self._response,
            )

    def __repr__(self) -> str:
        return (
            f"<APIResponse(status_code={self.status_code}, "
            f"headers={dict(self.headers)}, "
            f"json={self._json})>"
        )
