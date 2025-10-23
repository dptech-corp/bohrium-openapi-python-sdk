import logging
from typing import Optional, List, Dict, Any, Union, Iterator
from pprint import pprint
import json

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._response import APIResponse
from ...types.sigma_search.sigma_search import (
    CreateSessionRequest,
    SessionInfo,
    QuestionInfo,
    PaperInfo,
    FollowUpRequest,
    SearchHistoryResponse
)

log = logging.getLogger(__name__)


class SigmaSearch(SyncAPIResource):
    """Sigma搜索相关接口"""

    def create_session(
        self,
        query: str,
        model: str = "qwen",
        discipline: str = "All",
        resource_id_list: Optional[List[str]] = None,
        **kwargs
    ):
        """创建搜索会话"""
        log.info(f"creating sigma search session: {query}")

        data = {
            "query": query,
            "model": model,
            "discipline": discipline,
            "resource_id_list": resource_id_list or []
        }

        if kwargs:
            data.update(kwargs)

        response = self._client.post("/openapi/v1/sigma-search/api/v1/ai_search/sessions", json=data)
        log.info(response.json())
        return APIResponse(response).json.get("data")

    def get_session(
        self,
        uuid: str,
        **kwargs
    ):
        """获取会话详情"""
        log.info(f"getting sigma search session: {uuid}")

        response = self._client.get(f"/openapi/v1/sigma-search/api/v1/ai_search/sessions/{uuid}")
        log.info(response.json())
        return APIResponse(response).json.get("data")

    def get_papers(
        self,
        query_id: int,
        sort: str = "RelevanceScore",
        **kwargs
    ):
        """获取问题相关文献"""
        log.info(f"getting papers for query: {query_id}")

        params = {"sort": sort}
        if kwargs:
            params.update(kwargs)

        response = self._client.get(
            f"/openapi/v1/sigma-search/api/v1/ai_search/questions/{query_id}/papers",
            params=params
        )
        log.info(response.json())
        return APIResponse(response).json.get("data")

    def get_summary_stream(
        self,
        query_id: int,
        **kwargs
    ):
        """获取总结流式输出"""
        log.info(f"getting summary stream for query: {query_id}")

        response = self._client.get(
            f"/openapi/v1/sigma-search/api/v1/ai_search/questions/{query_id}/stream",
            stream=True
        )
        
        # 处理流式响应
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('event:data'):
                    continue
                elif line_str.startswith('data:'):
                    try:
                        data = json.loads(line_str[5:])  # 去掉 'data:' 前缀
                        yield data
                    except json.JSONDecodeError:
                        log.warning(f"Failed to parse JSON: {line_str}")
                        continue

    def get_summary_content(
        self,
        query_id: int,
        **kwargs
    ):
        """获取总结内容"""
        log.info(f"getting summary content for query: {query_id}")

        response = self._client.get(f"/openapi/v1/sigma-search/api/v1/ai_search/questions/{query_id}")
        log.info(response.json())
        return APIResponse(response).json.get("data")

    def follow_up_question(
        self,
        session_uuid: str,
        query: str,
        **kwargs
    ):
        """文献搜索追问"""
        log.info(f"follow up question in session: {session_uuid}")

        data = {"query": query}
        if kwargs:
            data.update(kwargs)

        response = self._client.post(
            f"/openapi/v1/sigma-search/api/v1/ai_search/sessions/{session_uuid}/questions",
            json=data
        )
        log.info(response.json())
        return APIResponse(response).json.get("data")

    def get_search_history(
        self,
        **kwargs
    ):
        """获取搜索历史记录"""
        log.info("getting sigma search history")

        response = self._client.get("/openapi/v1/sigma-search/api/v1/ai_search/sessions")
        log.info(response.json())
        return APIResponse(response).json.get("data")

    def search_with_request(
        self,
        request: Union[CreateSessionRequest, FollowUpRequest]
    ):
        """使用请求对象进行搜索"""
        if isinstance(request, CreateSessionRequest):
            return self.create_session(**request.to_dict())
        elif isinstance(request, FollowUpRequest):
            return self.follow_up_question(**request.to_dict())
        else:
            raise ValueError("request must be CreateSessionRequest or FollowUpRequest")


class AsyncSigmaSearch(AsyncAPIResource):
    """异步Sigma搜索相关接口"""
    pass