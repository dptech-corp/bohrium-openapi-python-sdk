from typing import List, Optional, Dict, Any, Union
from datetime import datetime


class HybridRecallRequest:
    """知识库混合召回请求"""
    
    def __init__(
        self,
        knowledge_base_id: int,
        text: str,
        k: int = 200,
        keywords: Optional[Dict[str, float]] = None,
        **kwargs
    ):
        self.knowledge_base_id = knowledge_base_id
        self.text = text
        self.k = k
        self.keywords = keywords or {}
    
    def to_dict(self):
        return {
            "knowledge_base_id": self.knowledge_base_id,
            "text": self.text,
            "k": self.k,
            "keywords": self.keywords
        }


class PaperRecallRequest:
    """单篇论文召回请求"""
    
    def __init__(
        self,
        text: str,
        k: int,
        papers: List[Dict[str, str]],
        **kwargs
    ):
        self.text = text
        self.k = k
        self.papers = papers
    
    def to_dict(self):
        return {
            "text": self.text,
            "k": self.k,
            "papers": self.papers
        }


class PaperInfo:
    """论文信息"""
    
    def __init__(
        self,
        paper_id: str = "",
        md5: str = "",
        **kwargs
    ):
        self.paperId = paper_id
        self.md5 = md5
    
    def to_dict(self):
        return {
            "paperId": self.paperId,
            "md5": self.md5
        }


class ChunkSearchRequest:
    """根据md5和paper_id搜索chunk请求"""
    
    def __init__(
        self,
        md5: str,
        paper_id: str = "",
        page_num: int = 0,
        page_size: int = 9999,
        **kwargs
    ):
        self.md5 = md5
        self.paper_id = paper_id
        self.page_num = page_num
        self.page_size = page_size
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "md5": self.md5,
            "paper_id": self.paper_id,
            "page_num": self.page_num,
            "page_size": self.page_size
        }
        if self.extra:
            data.update(self.extra)
        return data


