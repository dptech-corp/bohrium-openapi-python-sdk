import logging
from typing import Optional, List, Dict, Any, Union, Iterator
from pprint import pprint
import json
import httpx

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

        response = self._client.post("/openapi/v1/sigma-search/api/v2/ai_search/sessions", json=data)
        log.info(response.json())
        return APIResponse(response).json.get("data")

    def get_session(
        self,
        uuid: str,
        **kwargs
    ):
        """获取会话详情"""
        log.info(f"getting sigma search session: {uuid}")

        response = self._client.get(f"/openapi/v1/sigma-search/api/v1/ai_search/sessions_extended/{uuid}")
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

        try:
            # 使用专门的流式HTTP客户端
            import httpx
            
            # 创建专门的流式客户端，禁用缓冲
            stream_client = httpx.Client(
                timeout=httpx.Timeout(timeout=600.0, connect=10.0),
                limits=httpx.Limits(max_connections=1, max_keepalive_connections=1)
            )
            
            # 构建完整URL
            url = f"{self._client._base_url}/openapi/v1/sigma-search/api/v1/ai_search/questions/{query_id}/stream"
            
            # 添加access key参数
            params = {"accessKey": self._client.access_key}
            
            # 使用专门的流式请求头
            headers = {
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Cache-Control": "no-cache"
            }
            
            log.info("开始流式请求...")
            
            # 使用stream方法进行真正的流式请求
            with stream_client.stream(
                "GET", 
                url, 
                params=params, 
                headers=headers
            ) as response:
                log.info(f"流式响应状态: {response.status_code}")
                
                if response.status_code != 200:
                    log.error(f"流式请求失败: {response.status_code}")
                    return
                
                # 逐行读取流式数据
                for line in response.iter_lines():
                    if line:
                        log.debug(f"收到流式数据: {line[:100]}...")
                        yield line.encode('utf-8')
            
            stream_client.close()
        except Exception as e:
            log.error(f"Stream error: {e}")
            return

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