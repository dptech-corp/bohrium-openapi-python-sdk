import logging
from typing import Optional, List, Dict, Any
from pprint import pprint

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._response import APIResponse
from ...types.paper.paper import PaperRAGRequest

log = logging.getLogger(__name__)


class Paper(SyncAPIResource):
    """论文相关接口"""

    def rag_pass_keyword(
        self,
        type: int,
        rerank: int,
        question: str,
        page_size: int,
        words: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        **kwargs
    ):
        """论文RAG关键词检索"""
        log.info(f"paper rag pass keyword: type={type}, rerank={rerank}")
        
        data = {
            "type": type,
            "rerank": rerank,
            "question": question,
            "pageSize": page_size
        }
        
        if words:
            data["words"] = words
        if start_time:
            data["startTime"] = start_time
        if end_time:
            data["endTime"] = end_time
        if kwargs:
            data.update(kwargs)
            
        response = self._client.post("/openapi/v1/paper/rag/pass/keyword", json=data)
        log.info(response.json())
        return APIResponse(response).json.get("data")


class AsyncPaper(AsyncAPIResource):
    """异步论文相关接口"""
    pass
