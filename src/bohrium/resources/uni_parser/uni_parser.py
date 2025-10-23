import logging
from typing import Optional, List, Dict, Any, Union, BinaryIO
from pprint import pprint
import base64
import os

from ..._resource import AsyncAPIResource, SyncAPIResource
from ..._response import APIResponse
from ...types.uni_parser.uni_parser import (
    FileParseRequest,
    URLParseRequest,
    ImageParseRequest,
    ParseResultRequest,
    ParseFormattedRequest,
    ParseParagraphsRequest
)

log = logging.getLogger(__name__)


class UniParser(SyncAPIResource):
    """通用解析器相关接口"""

    def trigger_file_async(
        self,
        file: Union[str, BinaryIO, bytes],
        lang: str = "unknown",
        sync: bool = False,
        textual: bool = True,
        table: bool = True,
        molecule: bool = True,
        chart: bool = True,
        figure: bool = False,
        expression: bool = True,
        equation: bool = True,
        pages: Optional[List[int]] = None,
        admin_debug: bool = False,
        timeout: int = 1800,
        table_cls: bool = False,
        ordering_method: str = "gap_tree",
        **kwargs
    ):
        """提交PDF文件进行异步/同步解析"""
        log.info(f"triggering file async parse: sync={sync}")
        
        # 准备文件数据
        if isinstance(file, str):
            # 文件路径
            if not os.path.exists(file):
                raise FileNotFoundError(f"File not found: {file}")
            files = {"file": (os.path.basename(file), open(file, "rb"), "application/pdf")}
        elif isinstance(file, bytes):
            files = {"file": ("upload.pdf", file, "application/pdf")}
        elif hasattr(file, 'read'):
            # 文件对象
            files = {"file": ("upload.pdf", file, "application/pdf")}
        else:
            raise ValueError("file must be a file path, file object, or bytes")
        # 将表单数据合并到files中
        form_data = {
            'lang': str(lang),
            'sync': str(sync).lower()
        }
        
        if kwargs:
            form_data.update({k: str(v) for k, v in kwargs.items()})
        
        # 将表单数据添加到files中
        files.update({k: (None, v) for k, v in form_data.items()})
            
        response = self._client.post("/openapi/v1/parse/trigger-file-async", files=files, params={"accessKey": self._client.access_key})
        log.info(response.json())
        return APIResponse(response).json

    def trigger_url_async(
        self,
        url: str,
        lang: str = "unknown",
        sync: bool = False,
        textual: bool = True,
        table: bool = True,
        molecule: bool = True,
        chart: bool = True,
        figure: bool = False,
        expression: bool = True,
        equation: bool = True,
        pages: Optional[List[int]] = None,
        admin_debug: bool = False,
        timeout: int = 1800,
        table_cls: bool = False,
        ordering_method: str = "gap_tree",
        **kwargs
    ):
        """提交PDF文件链接进行异步/同步解析"""
        log.info(f"triggering URL async parse: {url}, sync={sync}")
        
        data = {
            "url": url,
            "lang": lang,
            "sync": sync,
            "textual": textual,
            "table": table,
            "molecule": molecule,
            "chart": chart,
            "figure": figure,
            "expression": expression,
            "equation": equation,
            "admin_debug": admin_debug,
            "timeout": timeout,
            "table_cls": table_cls,
            "ordering_method": ordering_method
        }
        
        if pages is not None:
            data["pages"] = pages
        if kwargs:
            data.update(kwargs)
            
        response = self._client.post("/openapi/v1/parse/trigger-url-async", json=data)
        log.info(response.json())
        log.info(APIResponse(response).json)
        return APIResponse(response).json
    def trigger_snip_async(
        self,
        img: Union[str, bytes],
        lang: str = "unknown",
        sync: bool = False,
        textual: bool = True,
        table: bool = True,
        molecule: bool = True,
        chart: bool = True,
        figure: bool = False,
        expression: bool = True,
        equation: bool = True,
        pages: Optional[List[int]] = None,
        admin_debug: bool = False,
        timeout: int = 1800,
        table_cls: bool = False,
        ordering_method: str = "gap_tree",
        **kwargs
    ):
        """提交图片或截图进行异步/同步解析"""
        log.info(f"triggering snip async parse: sync={sync}")
        
        # 处理图片数据
        if isinstance(img, str):
            # 如果是base64字符串，直接使用
            if img.startswith('data:image'):
                img_data = img.split(',')[1]
            elif len(img) > 50 and not img.startswith('/') and not img.startswith('\\') and not img.startswith('C:'):
                # 如果字符串较长且不是路径，认为是base64数据
                img_data = img
            else:
                # 如果是文件路径，读取并编码
                with open(img, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode('utf-8')
        elif isinstance(img, bytes):
            img_data = base64.b64encode(img).decode('utf-8')
        else:
            raise ValueError("img must be a file path, base64 string, or bytes")
        
        # 准备表单数据，使用multipart/form-data格式
        form_data = {
            'lang': str(lang),
            'sync': str(sync).lower(),
            'textual': str(textual).lower(),
            'table': str(table).lower(),
            'molecule': str(molecule).lower(),
            'chart': str(chart).lower(),
            'figure': str(figure).lower(),
            'expression': str(expression).lower(),
            'equation': str(equation).lower(),
            'admin_debug': str(admin_debug).lower(),
            'timeout': str(timeout),
            'table_cls': str(table_cls).lower(),
            'ordering_method': str(ordering_method)
        }
        
        if pages is not None:
            if isinstance(pages, list) and len(pages) > 0:
                form_data['page'] = str(pages[0])
            else:
                form_data['page'] = str(pages)
        else:
            form_data['page'] = "-1"
        
        if kwargs:
            form_data.update({k: str(v) for k, v in kwargs.items()})
        
        # 将图片数据作为表单字段传递
        form_data['img'] = img_data
        
        # 将表单数据添加到files中
        files = {k: (None, v) for k, v in form_data.items()}
            
        response = self._client.post("/openapi/v1/parse/trigger-snip-async", files=files, params={"accessKey": self._client.access_key})
        log.info(response.json())
        return APIResponse(response).json

    def get_result(
        self,
        token: str,
        return_half: bool = False,
        content: bool = True,
        objects: bool = True,
        pages_dict: bool = True,
        molecule_source: bool = False,
        **kwargs
    ):
        """根据Token索引解析结果"""
        log.info(f"getting parse result for token: {token}")
        
        data = {
            "token": token,
            "return_half": return_half,
            "content": content,
            "objects": objects,
            "pages_dict": pages_dict,
            "molecule_source": molecule_source
        }
        
        if kwargs:
            data.update(kwargs)
            
        response = self._client.post("/openapi/v1/parse/get-result", json=data)
        log.info(response.json())
        # 检查响应是否包含data字段，如果没有则直接返回整个响应
        return APIResponse(response).json

    def get_formatted(
        self,
        token: str,
        return_half: bool = False,
        content: bool = False,
        objects: bool = True,
        pages_dict: bool = False,
        textual: str = "markup",
        table: str = "markup",
        molecule: str = "markup",
        chart: str = "markup",
        figure: str = "markup",
        expression: str = "markup",
        equation: str = "markup",
        molecule_source: bool = True,
        **kwargs
    ):
        """根据Token索引解析结果并进行指定格式化"""
        log.info(f"getting formatted parse result for token: {token}")
        
        data = {
            "token": token,
            "return_half": return_half,
            "content": content,
            "objects": objects,
            "pages_dict": pages_dict,
            "textual": textual,
            "table": table,
            "molecule": molecule,
            "chart": chart,
            "figure": figure,
            "expression": expression,
            "equation": equation,
            "molecule_source": molecule_source
        }
        
        if kwargs:
            data.update(kwargs)
            
        response = self._client.post("/openapi/v1/parse/get-formatted", json=data)
        log.info(response.json())
        return APIResponse(response).json

    def get_paragraphs(
        self,
        token: str,
        **kwargs
    ):
        """根据Token索引分段落的解析结果"""
        log.info(f"getting paragraphs for token: {token}")
        
        data = token
        if kwargs:
            data = {"token": token, **kwargs}
            
        response = self._client.post("/openapi/v1/parse/get-paragraphs", json=data)
        log.info(response.json())
        return APIResponse(response).json

    def parse_with_request(
        self,
        request: Union[FileParseRequest, URLParseRequest, ImageParseRequest, ParseResultRequest, ParseFormattedRequest, ParseParagraphsRequest]
    ):
        """使用请求对象进行解析或查询"""
        if isinstance(request, FileParseRequest):
            return self.trigger_file_async(**request.to_dict())
        elif isinstance(request, URLParseRequest):
            return self.trigger_url_async(**request.to_dict())
        elif isinstance(request, ImageParseRequest):
            return self.trigger_snip_async(**request.to_dict())
        elif isinstance(request, ParseResultRequest):
            return self.get_result(**request.to_dict())
        elif isinstance(request, ParseFormattedRequest):
            return self.get_formatted(**request.to_dict())
        elif isinstance(request, ParseParagraphsRequest):
            return self.get_paragraphs(**request.to_dict())
        else:
            raise ValueError("request must be one of the supported request types")


class AsyncUniParser(AsyncAPIResource):
    """异步通用解析器相关接口"""
    pass