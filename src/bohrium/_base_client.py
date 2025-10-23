import logging
import platform
import time
from functools import wraps
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    Literal,
    Mapping,
    Optional,
    TypeVar,
    Union,
    cast,
)
from urllib.parse import urljoin

import distro
import httpx
from httpx import URL, Limits, Timeout

from ._constants import DEFAULT_CONNECTION_LIMITS, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from ._utils import lru_cache

logger = logging.getLogger(__name__)

Arch = Union[Literal["x32", "x64", "arm", "arm64", "unknown"]]

Platform = Union[
    Literal[
        "MacOS",
        "Linux",
        "Windows",
        "FreeBSD",
        "OpenBSD",
        "iOS",
        "Android",
        "Unknown",
    ],
]


class _DefaultHttpxClient(httpx.Client):
    def __init__(self, **kwargs: Any) -> None:
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        kwargs.setdefault("limits", DEFAULT_CONNECTION_LIMITS)
        kwargs.setdefault("follow_redirects", True)
        super().__init__(**kwargs)


if TYPE_CHECKING:
    DefaultHttpxClient = httpx.Client
    """An alias to `httpx.Client` that provides the same defaults that this SDK
    uses internally.

    This is useful because overriding the `http_client` with your own instance of
    `httpx.Client` will result in httpx's defaults being used, not ours.
    """
else:
    DefaultHttpxClient = _DefaultHttpxClient

_HttpxClientT = TypeVar("_HttpxClientT", bound=Union[httpx.Client, httpx.AsyncClient])


class SyncHttpxClientWrapper(DefaultHttpxClient):
    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass


def retry(max_retries_func, delay=1, exceptions=(Exception,)):
    """
    Decorator for retrying a function upon exception.

    max_retries: The maximum number of retries before giving up.
    delay: Initial delay between retries in seconds.
    backoff: Multiplier applied to delay between retries (e.g., for exponential backoff).
    exceptions: Tuple of exceptions to catch. Defaults to base Exception class.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]
            max_retries = max_retries_func(self)
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if retries >= max_retries:
                        logger.error(
                            f"Exhausted all retries. Raising the last caught exception: {e}"
                        )
                        raise e
                    else:
                        logger.warning(
                            f"Retry {retries} due to error: {e}. Retrying in {delay} seconds..."
                        )
                        time.sleep(delay)
                    retries += 1

        return wrapper

    return decorator


class BaseClient(Generic[_HttpxClientT]):
    _client: _HttpxClientT
    _base_url: URL
    max_retries: int
    timeout: Union[float, Timeout, None]
    _limits: httpx.Limits
    _version: Union[str, None]

    def __init__(
        self,
        *,
        _version: Optional[str] = None,
        base_url: Union[str, URL],
        limits: httpx.Limits,
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: Optional[Union[float, httpx.Timeout]] = DEFAULT_TIMEOUT,
        custom_headers: Optional[Mapping[str, str]] = None,
    ):
        self._base_url = self._enforce_trailing_slash(URL(base_url))
        self._version = _version
        self.max_retries = max_retries
        self.timeout = timeout
        self._limits = limits
        self._custom_headers = custom_headers or {}
        self.backoff_base = 2

    def _enforce_trailing_slash(self, url: URL) -> URL:
        if url.raw_path.endswith(b"/"):
            return url
        return url.copy_with(raw_path=url.raw_path + b"/")

    def _build_headers(self, custom_headers) -> httpx.Headers:
        headers_dict = _merge_mappings(
            self.default_headers, self._custom_headers, custom_headers
        )
        # 过滤掉 value 为 None 的 header
        headers_dict = {k: v for k, v in headers_dict.items() if v is not None}
        headers = httpx.Headers(headers_dict)
        return headers or dict()

    def _build_params(self, custom_params) -> dict[str, str]:
        params = _merge_mappings(self.default_params, custom_params)
        return params

    @property
    def custom_auth(self) -> Union[httpx.Auth, None]:
        return None

    @property
    def auth_headers(self) -> dict[str, str]:
        return {}

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @property
    def default_params(self) -> dict[str, str]:
        return {"accessKey": self.access_key}

    def platform_headers(self) -> Dict[str, str]:
        return platform_headers(self._version)

    @retry(
        max_retries_func=lambda self: self.max_retries,
        exceptions=(httpx.RequestError,),
    )
    def _request(
        self, method: str, path: str, json=None, headers=None, data=None, **kwargs
    ) -> httpx.Response:
        url = urljoin(str(self._base_url), path)
        logger.info(f"Requesting {method} {url}")
        merged_headers = self._build_headers(headers)
        merged_params = self._build_params(kwargs.get("params"))
        
        # 处理文件上传
        request_kwargs = {
            "method": method.upper(),
            "url": url,
            "params": merged_params,
        }
        
        if json is not None:
            request_kwargs["json"] = json
            request_kwargs["headers"] = merged_headers
        elif "files" in kwargs:
            # 当有files参数时，不使用json参数，而是使用files和data
            # 不设置headers，让httpx自动处理multipart/form-data
            request_kwargs["files"] = kwargs["files"]
            if "data" in kwargs:
                request_kwargs["data"] = kwargs["data"]
        elif "data" in kwargs:
            request_kwargs["data"] = kwargs["data"]
            request_kwargs["headers"] = merged_headers
        else:
            request_kwargs["headers"] = merged_headers
            
        try:
            return self._client.request(
                method.upper(),
                url,
                json=json,
                data=data,
                headers=merged_headers,
                params=merged_params,
            )
        except httpx.TransportError as e:
            logger.error(f"Transport error: {e}.")
            raise e
        except httpx.RequestError as e:
            logger.error(f"Request failed with error: {e}.")

    def get(self, path: str, headers=None, **kwargs) -> httpx.Response:
        """Make a GET request."""
        return self._request("GET", path, headers=headers, **kwargs)

    def post(self, path: str, json=None, headers=None, **kwargs) -> httpx.Response:
        """Make a POST request."""
        return self._request("POST", path, json=json, headers=headers, **kwargs)

    def patch(self, path: str, json=None, headers=None, **kwargs) -> httpx.Response:
        """Make a PATCH request."""
        return self._request("PATCH", path, json=json, headers=headers, **kwargs)

    def put(self, path: str, json=None, headers=None, **kwargs) -> httpx.Response:
        """Make a PUT request."""
        return self._request("PUT", path, json=json, headers=headers, **kwargs)

    def delete(self, path: str, headers=None, **kwargs) -> httpx.Response:
        """Make a DELETE request."""
        return self._request("DELETE", path, headers=headers, **kwargs)

    def close(self):
        """Close the underlying HTTPX client."""
        self.client.close()


class SyncAPIClient(BaseClient[httpx.Client]):
    _client: httpx.Client

    def __init__(
        self,
        base_url: Union[str, httpx.URL],
        max_retries: int = DEFAULT_MAX_RETRIES,
        timeout: Union[float, Timeout, None] = DEFAULT_TIMEOUT,
        limits: Limits = DEFAULT_CONNECTION_LIMITS,
        _version: Optional[str] = None,
        http_client: Optional[httpx.Client] = None,
        custom_headers: Optional[Mapping[str, str]] = None,
    ) -> None:

        if http_client is not None and not isinstance(
            http_client, httpx.Client
        ):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"Invalid `http_client` argument; Expected an instance of `httpx.Client` but got {type(http_client)}"
            )
        print(timeout)
        super().__init__(
            _version=_version,
            limits=limits,
            # cast to a valid type because mypy doesn't understand our type narrowing
            timeout=cast(Timeout, timeout),
            base_url=base_url,
            max_retries=max_retries,
            custom_headers=custom_headers,
        )
        self._client = http_client or SyncHttpxClientWrapper(
            base_url=base_url,
            # cast to a valid type because mypy doesn't understand our type narrowing
            timeout=cast(Timeout, timeout),
            limits=limits,
            follow_redirects=True,
        )

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


def _merge_mappings(*mappings):
    merged = {}
    for mapping in mappings:
        if mapping:
            merged.update(mapping)
    return merged


class AsyncAPIClient(BaseClient[httpx.AsyncClient]):
    pass


@lru_cache(maxsize=None)
def get_platform() -> Platform:
    try:
        system = platform.system().lower()
        platform_name = platform.platform().lower()
    except Exception:
        return "Unknown"

    if "iphone" in platform_name or "ipad" in platform_name:
        # Tested using Python3IDE on an iPhone 11 and Pythonista on an iPad 7
        # system is Darwin and platform_name is a string like:
        # - Darwin-21.6.0-iPhone12,1-64bit
        # - Darwin-21.6.0-iPad7,11-64bit
        return "iOS"

    if system == "darwin":
        return "MacOS"

    if system == "windows":
        return "Windows"

    if "android" in platform_name:
        # Tested using Pydroid 3
        # system is Linux and platform_name is a string like 'Linux-5.10.81-android12-9-00001-geba40aecb3b7-ab8534902-aarch64-with-libc'
        return "Android"

    if system == "linux":
        # https://distro.readthedocs.io/en/latest/#distro.id
        distro_id = distro.id()
        if distro_id == "freebsd":
            return "FreeBSD"

        if distro_id == "openbsd":
            return "OpenBSD"

        return "Linux"

    return "Unknown"


def platform_headers(version: str) -> Dict[str, str]:
    return {
        "X-Stainless-Lang": "python",
        "X-Stainless-Package-Version": version,
        "X-Stainless-OS": str(get_platform()),
        "X-Stainless-Arch": str(get_architecture()),
        "X-Stainless-Runtime": get_python_runtime(),
        "X-Stainless-Runtime-Version": get_python_version(),
    }


def get_architecture() -> Arch:
    try:
        python_bitness, _ = platform.architecture()
        machine = platform.machine().lower()
    except Exception:
        return "unknown"

    if machine in ("arm64", "aarch64"):
        return "arm64"

    # TODO: untested
    if machine == "arm":
        return "arm"

    if machine == "x86_64":
        return "x64"

    # TODO: untested
    if python_bitness == "32bit":
        return "x32"

    return "unknown"


def get_python_runtime() -> str:
    try:
        return platform.python_implementation()
    except Exception:
        return "unknown"


def get_python_version() -> str:
    try:
        return platform.python_version()
    except Exception:
        return "unknown"
