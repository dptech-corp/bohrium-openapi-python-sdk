import logging
from typing import Optional, List, Dict, Any, Union
from pprint import pprint

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._response import APIResponse
from ...types.knowledge_base.knowledge_base import (
    HybridRecallRequest,
    PaperRecallRequest,
    PaperInfo,
    ChunkSearchRequest
)

log = logging.getLogger(__name__)


class KnowledgeBase(SyncAPIResource):
    """知识库相关接口"""

    def hybrid_recall(
        self,
        knowledge_base_id: int,
        text: str,
        k: int = 200,
        keywords: Optional[Dict[str, float]] = None,
        **kwargs
    ):
        """知识库混合召回"""
        log.info(f"hybrid recall from knowledge base: {knowledge_base_id}")
        
        data = {
            "knowledge_base_id": knowledge_base_id,
            "text": text,
            "k": k
        }
        
        if keywords:
            data["keywords"] = keywords
        if kwargs:
            data.update(kwargs)
            
        response = self._client.post("/openapi/v1/knowledge/recall/hybrid", json=data)
        log.info(response.json())
        return APIResponse(response).json.get("data")

    def paper_recall(
        self,
        text: str,
        k: int,
        papers: List[Dict[str, str]],
        **kwargs
    ):
        """单篇论文召回"""
        log.info(f"paper recall: {len(papers)} papers")
        
        data = {
            "text": text,
            "k": k,
            "papers": papers
        }
        
        if kwargs:
            data.update(kwargs)
            
        response = self._client.post("/openapi/v1/knowledge/recall/papers", json=data)
        log.info(response.json())
        return APIResponse(response).json.get("data")

    def get_file_tree(
        self,
        folder_id: str,
        **kwargs
    ):
        """获取单篇切片文件树"""
        log.info(f"get file tree for folder: {folder_id}")
        
        params = {"folderId": folder_id}
        if kwargs:
            params.update(kwargs)
            
        response = self._client.get("/openapi/v1/knowledge/folder/file_tree", params=params)
        log.info(response.json())
        return APIResponse(response).json.get("data")

    def search_by_md5_paper_id(
        self,
        md5: str,
        paper_id: str = "",
        page_num: int = 0,
        page_size: int = 9999,
        **kwargs
    ):
        """根据md5和paper_id搜索chunk信息"""
        log.info(f"search chunk by md5: {md5}, paper_id: {paper_id}")
        
        data = {
            "md5": md5,
            "paper_id": paper_id,
            "page_num": page_num,
            "page_size": page_size
        }
        
        if kwargs:
            data.update(kwargs)
            
        response = self._client.post("/openapi/v1/knowledge/box/search_by_md5_paper_id", json=data)
        log.info(response.json())
        return APIResponse(response).json.get("data")



class AsyncKnowledgeBase(AsyncAPIResource):
    """异步知识库相关接口"""
    pass
