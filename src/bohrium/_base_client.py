import logging
import time
from typing import Generic, Mapping, TypeVar, Union, cast

import httpx
from httpx import URL, Limits, Timeout

from ._constants import DEFAULT_CONNECTION_LIMITS, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT

log: logging.Logger = logging.getLogger(__name__)

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx.Client, httpx.AsyncClient])


class BaseClient(Generic[_HttpxClientT]):
    _client: _HttpxClientT
    _base_url: URL
    max_retries: int
    timeout: Union[float, Timeout, None]
    _limits: httpx.Limits

    def __init__(
        self,
        base_url: str | URL,
        limits: httpx.Limits,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: float | Timeout | None = DEFAULT_TIMEOUT,
        custom_headers: Mapping[str, str] | None = None,
    ):
        self._base_url = self._enforce_trailing_slash(URL(base_url))
        self.max_retries = max_retries
        self.timeout = timeout
        self._limits = limits
        self._custom_headers = custom_headers or {}

    def _enforce_trailing_slash(self, url: URL) -> URL:
        if url.raw_path.endswith(b"/"):
            return url
        return url.copy_with(raw_path=url.raw_path + b"/")

    def request(
        self, method: str, path: str, json=None, headers=None, **kwargs
    ) -> httpx.Response:
        url = self.base_url + path
        merged_headers = {**self.default_headers, **(headers or {})}
        retries_left = self.retries
        delay = self.backoff_base

        while retries_left > 0:
            try:
                return self.client.request(
                    method.upper(), url, json=json, headers=merged_headers, **kwargs
                )
            except httpx.RequestError as e:
                log.error(f"Request failed with error: {e}. Retrying...")
                retries_left -= 1
                if retries_left > 0:
                    time.sleep(delay)
                    delay *= self.backoff_base  # Exponential backoff
        raise Exception(f"Request failed after {self.retries} retries.")

    def get(self, path: str, headers=None, **kwargs) -> httpx.Response:
        """Make a GET request."""
        url = self.base_url + path
        return self.request("GET", url, headers=headers, **kwargs)

    def post(self, path: str, json=None, headers=None, **kwargs) -> httpx.Response:
        """Make a POST request."""
        url = self.base_url + path
        return self.request("POST", url, json=json, headers=headers, **kwargs)

    def patch(self, path: str, json=None, headers=None, **kwargs) -> httpx.Response:
        """Make a PATCH request."""
        url = self.base_url + path
        return self.request("PATCH", url, json=json, headers=headers, **kwargs)

    def put(self, path: str, json=None, headers=None, **kwargs) -> httpx.Response:
        """Make a PUT request."""
        url = self.base_url + path
        return self.request("PUT", url, json=json, headers=headers, **kwargs)

    def delete(self, path: str, headers=None, **kwargs) -> httpx.Response:
        """Make a DELETE request."""
        url = self.base_url + path
        return self.request("DELETE", url, headers=headers, **kwargs)

    def close(self):
        """Close the underlying HTTPX client."""
        self.client.close()


class SyncAPIClient(BaseClient[httpx.Client]):
    _client: httpx.Client

    def __init__(
        self,
        *,
        version: str,
        base_url: str | URL,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: float | Timeout,
        limits: Limits | None = None,
        http_client: httpx.Client | None = None,
        custom_headers: Mapping[str, str] | None = None,
        custom_query: Mapping[str, object] | None = None,
        _strict_response_validation: bool,
    ) -> None:
        if limits is not None:
            log.warn(
                "The `connection_pool_limits` argument is deprecated. The `http_client` argument should be passed instead",
                category=DeprecationWarning,
                stacklevel=3,
            )
            if http_client is not None:
                raise ValueError(
                    "The `http_client` argument is mutually exclusive with `connection_pool_limits`"
                )
        else:
            limits = DEFAULT_CONNECTION_LIMITS

        if not timeout:
            timeout = DEFAULT_TIMEOUT

        if http_client is not None and not isinstance(
            http_client, httpx.Client
        ):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"Invalid `http_client` argument; Expected an instance of `httpx.Client` but got {type(http_client)}"
            )

        super().__init__(
            version=version,
            limits=limits,
            # cast to a valid type because mypy doesn't understand our type narrowing
            timeout=cast(Timeout, timeout),
            base_url=base_url,
            max_retries=max_retries,
            custom_query=custom_query,
            custom_headers=custom_headers,
        )
        self._client = http_client

    def is_closed(self) -> bool:
        return self._client.is_closed

    def close(self) -> None:
        """Close the underlying HTTPX client.

        The client will *not* be usable after this.
        """
        # If an error is thrown while constructing a client, self._client
        # may not be present
        if hasattr(self, "_client"):
            self._client.close()

    def _prepare_request(
        self,
        request: httpx.Request,  # noqa: ARG002
    ) -> None:
        """This method is used as a callback for mutating the `Request` object
        after it has been constructed.
        This is useful for cases where you want to add certain headers based off of
        the request properties, e.g. `url`, `method` etc.
        """
        return None
