from typing import List, Optional, Dict, Any, Union
from datetime import datetime


class CreateSessionRequest:
    """创建搜索会话请求"""

    def __init__(
        self,
        query: str,
        model: str = "qwen",
        discipline: str = "All",
        resource_id_list: Optional[List[str]] = None,
        **kwargs
    ):
        self.query = query
        self.model = model
        self.discipline = discipline
        self.resource_id_list = resource_id_list or []
        self.extra = kwargs

    def to_dict(self):
        data = {
            "query": self.query,
            "model": self.model,
            "discipline": self.discipline,
            "resource_id_list": self.resource_id_list
        }
        if self.extra:
            data.update(self.extra)
        return data


class FollowUpRequest:
    """追问请求"""

    def __init__(
        self,
        session_uuid: str,
        query: str,
        **kwargs
    ):
        self.session_uuid = session_uuid
        self.query = query
        self.extra = kwargs

    def to_dict(self):
        data = {
            "query": self.query
        }
        if self.extra:
            data.update(self.extra)
        return data


class SessionInfo:
    """会话信息"""

    def __init__(
        self,
        uuid: str = "",
        title: str = "",
        status: str = "",
        share: bool = False,
        share_link: str = "",
        model: str = "",
        model_type: str = "",
        questions: Optional[List[Dict[str, Any]]] = None,
        resources: Optional[Any] = None,
        create_time: str = "",
        permission: int = 0,
        discipline: str = "",
        **kwargs
    ):
        self.uuid = uuid
        self.title = title
        self.status = status
        self.share = share
        self.share_link = share_link
        self.model = model
        self.model_type = model_type
        self.questions = questions or []
        self.resources = resources
        self.create_time = create_time
        self.permission = permission
        self.discipline = discipline
        self.extra = kwargs

    def to_dict(self):
        data = {
            "uuid": self.uuid,
            "title": self.title,
            "status": self.status,
            "share": self.share,
            "shareLink": self.share_link,
            "model": self.model,
            "modelType": self.model_type,
            "questions": self.questions,
            "resources": self.resources,
            "createTime": self.create_time,
            "permission": self.permission,
            "discipline": self.discipline
        }
        if self.extra:
            data.update(self.extra)
        return data


class QuestionInfo:
    """问题信息"""

    def __init__(
        self,
        id: int = 0,
        query: str = "",
        status: str = "",
        last_answer_id: int = 0,
        **kwargs
    ):
        self.id = id
        self.query = query
        self.status = status
        self.last_answer_id = last_answer_id
        self.extra = kwargs

    def to_dict(self):
        data = {
            "id": self.id,
            "query": self.query,
            "status": self.status,
            "lastAnswerID": self.last_answer_id
        }
        if self.extra:
            data.update(self.extra)
        return data


class PaperInfo:
    """论文信息"""

    def __init__(
        self,
        sequence_id: int = 0,
        author: Optional[List[str]] = None,
        link: str = "",
        source: str = "",
        source_zh: str = "",
        abstract: str = "",
        abstract_zh: str = "",
        title: str = "",
        title_zh: str = "",
        seo_title: str = "",
        doi: str = "",
        bohrium_id: str = "",
        publication_id: int = 0,
        publication_cover: str = "",
        publication_date: str = "",
        journal: str = "",
        arxiv: str = "",
        ai_summarize: str = "",
        open_access: str = "",
        pdf_flag: bool = False,
        pieces: str = "",
        sort_score: float = 0.0,
        relevance_score: float = 0.0,
        publication_score: float = 0.0,
        impact_factor: float = 0.0,
        impact_factor_score: float = 0.0,
        citation_nums: int = 0,
        full_text: str = "",
        figures: Optional[Any] = None,
        **kwargs
    ):
        self.sequence_id = sequence_id
        self.author = author or []
        self.link = link
        self.source = source
        self.source_zh = source_zh
        self.abstract = abstract
        self.abstract_zh = abstract_zh
        self.title = title
        self.title_zh = title_zh
        self.seo_title = seo_title
        self.doi = doi
        self.bohrium_id = bohrium_id
        self.publication_id = publication_id
        self.publication_cover = publication_cover
        self.publication_date = publication_date
        self.journal = journal
        self.arxiv = arxiv
        self.ai_summarize = ai_summarize
        self.open_access = open_access
        self.pdf_flag = pdf_flag
        self.pieces = pieces
        self.sort_score = sort_score
        self.relevance_score = relevance_score
        self.publication_score = publication_score
        self.impact_factor = impact_factor
        self.impact_factor_score = impact_factor_score
        self.citation_nums = citation_nums
        self.full_text = full_text
        self.figures = figures
        self.extra = kwargs

    def to_dict(self):
        data = {
            "sequenceId": self.sequence_id,
            "author": self.author,
            "link": self.link,
            "source": self.source,
            "sourceZh": self.source_zh,
            "abstract": self.abstract,
            "abstractZh": self.abstract_zh,
            "title": self.title,
            "titleZh": self.title_zh,
            "seoTitle": self.seo_title,
            "doi": self.doi,
            "bohriumId": self.bohrium_id,
            "publicationId": self.publication_id,
            "publicationCover": self.publication_cover,
            "publicationDate": self.publication_date,
            "journal": self.journal,
            "arxiv": self.arxiv,
            "aiSummarize": self.ai_summarize,
            "openAccess": self.open_access,
            "pdfFlag": self.pdf_flag,
            "pieces": self.pieces,
            "sortScore": self.sort_score,
            "relevanceScore": self.relevance_score,
            "publicationScore": self.publication_score,
            "impactFactor": self.impact_factor,
            "impactFactorScore": self.impact_factor_score,
            "citationNums": self.citation_nums,
            "fullText": self.full_text,
            "figures": self.figures
        }
        if self.extra:
            data.update(self.extra)
        return data


class SearchHistoryResponse:
    """搜索历史响应"""

    def __init__(
        self,
        sessions: Optional[List[SessionInfo]] = None,
        **kwargs
    ):
        self.sessions = sessions or []
        self.extra = kwargs

    def to_dict(self):
        data = {
            "sessions": [session.to_dict() if isinstance(session, SessionInfo) else session for session in self.sessions]
        }
        if self.extra:
            data.update(self.extra)
        return data


class StreamData:
    """流式数据"""

    def __init__(
        self,
        content: Any = None,
        finish_reason: str = "",
        received_at: str = "",
        sended_at: str = "",
        type: str = "",
        **kwargs
    ):
        self.content = content
        self.finish_reason = finish_reason
        self.received_at = received_at
        self.sended_at = sended_at
        self.type = type
        self.extra = kwargs

    def to_dict(self):
        data = {
            "content": self.content,
            "finishReason": self.finish_reason,
            "receivedAt": self.received_at,
            "sendedAt": self.sended_at,
            "type": self.type
        }
        if self.extra:
            data.update(self.extra)
        return data