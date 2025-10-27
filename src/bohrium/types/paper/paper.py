from typing import List, Optional, Dict, Any


class PaperRAGRequest:
    """论文RAG检索请求"""
    
    def __init__(
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
        self.type = type  # 0=关键词检索，1=关键词语义检索
        self.rerank = rerank  # 0=不重排序，1=重排序
        self.question = question  # 提问的问题，英文版本
        self.pageSize = page_size  # 页大小
        self.words = words or []  # 搜索关键词
        self.startTime = start_time  # 检索文献的起始时间
        self.endTime = end_time  # 检索文献的末尾时间
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "type": self.type,
            "rerank": self.rerank,
            "question": self.question,
            "pageSize": self.pageSize
        }
        
        if self.words:
            data["words"] = self.words
        if self.startTime:
            data["startTime"] = self.startTime
        if self.endTime:
            data["endTime"] = self.endTime
        if self.extra:
            data.update(self.extra)
            
        return data
