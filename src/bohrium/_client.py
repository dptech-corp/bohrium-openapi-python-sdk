from __future__ import annotations

import os
from typing import Mapping, Optional, Union

from httpx import URL, Client, Response, Timeout
from typing_extensions import override

from . import _exceptions, resources
from ._base_client import DEFAULT_MAX_RETRIES, AsyncAPIClient, SyncAPIClient
from ._exceptions import APIStatusError, BohriumError
from ._version import __version__


class Bohrium(SyncAPIClient):
    job: resources.Job
    sigma_search: resources.SigmaSearch
    uni_parser: resources.UniParser
    knowledge_base: resources.KnowledgeBase
    paper: resources.Paper

    # client options
    access_key: str
    project_id: Optional[str]

    def __init__(
        self,
        access_key: Optional[str] = None,
        app_key: Optional[str] = None,
        base_url: Optional[Union[str, URL]] = None,
        project_id: Optional[str] = None,
        timeout: Optional[Union[float, Timeout]] = 30.0,
        max_retries: Optional[int] = DEFAULT_MAX_RETRIES,
        http_client: Optional[Client] = None,
    ) -> None:
        """Construct a new synchronous openai client instance."""
        if access_key is None:
            access_key = os.environ.get("BOHRIUM_ACCESS_KEY")
        if access_key is None:
            raise BohriumError(
                "The api_key client option must be set either by passing api_key to the client or by setting the ACCESS_KEY environment variable"
            )
        self.access_key = access_key
        self.app_key = app_key or os.environ.get("BOHRIUM_APP_KEY")
        self.params = {"accessKey": self.access_key}
        if project_id is None:
            project_id = os.environ.get("BOHRIUM_PROJECT_ID")

        self.project_id = project_id

        if base_url is None:
            base_url = os.environ.get("BOHRIUM_BASE_URL")

        if base_url is None:
            base_url = "https://openapi.dp.tech"

        super().__init__(
            _version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=self.default_headers,
        )

        self.job = resources.Job(self)
        self.sigma_search = resources.SigmaSearch(self)
        self.uni_parser = resources.UniParser(self)
        self.knowledge_base = resources.KnowledgeBase(self)
        self.paper = resources.Paper(self)

    @property
    @override
    def default_headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_key}",
            "x-app-key": self.app_key,
        }

    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: Response,
    ) -> APIStatusError:
        data = body.get("error", body) if isinstance(body, Mapping) else body
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=data)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(
                err_msg, response=response, body=data
            )

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(
                err_msg, response=response, body=data
            )

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=data)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=data)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(
                err_msg, response=response, body=data
            )

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=data)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(
                err_msg, response=response, body=data
            )
        return APIStatusError(err_msg, response=response, body=data)


class AsyncBohrium(AsyncAPIClient):
    pass
