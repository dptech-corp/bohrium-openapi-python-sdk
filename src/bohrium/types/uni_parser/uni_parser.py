from typing import List, Optional, Dict, Any, Union, BinaryIO


class FileParseRequest:
    """文件解析请求"""
    
    def __init__(
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
        self.file = file
        self.lang = lang
        self.sync = sync
        self.textual = textual
        self.table = table
        self.molecule = molecule
        self.chart = chart
        self.figure = figure
        self.expression = expression
        self.equation = equation
        self.pages = pages
        self.admin_debug = admin_debug
        self.timeout = timeout
        self.table_cls = table_cls
        self.ordering_method = ordering_method
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "file": self.file,
            "lang": self.lang,
            "sync": self.sync,
            "textual": self.textual,
            "table": self.table,
            "molecule": self.molecule,
            "chart": self.chart,
            "figure": self.figure,
            "expression": self.expression,
            "equation": self.equation,
            "admin_debug": self.admin_debug,
            "timeout": self.timeout,
            "table_cls": self.table_cls,
            "ordering_method": self.ordering_method
        }
        
        if self.pages is not None:
            data["pages"] = self.pages
        if self.extra:
            data.update(self.extra)
            
        return data


class ParseResultRequest:
    """解析结果查询请求"""
    
    def __init__(
        self,
        token: str,
        return_half: bool = False,
        content: bool = True,
        objects: bool = True,
        pages_dict: bool = True,
        molecule_source: bool = False,
        **kwargs
    ):
        self.token = token
        self.return_half = return_half
        self.content = content
        self.objects = objects
        self.pages_dict = pages_dict
        self.molecule_source = molecule_source
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "token": self.token,
            "return_half": self.return_half,
            "content": self.content,
            "objects": self.objects,
            "pages_dict": self.pages_dict,
            "molecule_source": self.molecule_source
        }
        
        if self.extra:
            data.update(self.extra)
            
        return data


class ParseFormattedRequest:
    """格式化解析结果查询请求"""
    
    def __init__(
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
        self.token = token
        self.return_half = return_half
        self.content = content
        self.objects = objects
        self.pages_dict = pages_dict
        self.textual = textual
        self.table = table
        self.molecule = molecule
        self.chart = chart
        self.figure = figure
        self.expression = expression
        self.equation = equation
        self.molecule_source = molecule_source
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "token": self.token,
            "return_half": self.return_half,
            "content": self.content,
            "objects": self.objects,
            "pages_dict": self.pages_dict,
            "textual": self.textual,
            "table": self.table,
            "molecule": self.molecule,
            "chart": self.chart,
            "figure": self.figure,
            "expression": self.expression,
            "equation": self.equation,
            "molecule_source": self.molecule_source
        }
        
        if self.extra:
            data.update(self.extra)
            
        return data


class ParseParagraphsRequest:
    """段落解析结果查询请求"""
    
    def __init__(
        self,
        token: str,
        **kwargs
    ):
        self.token = token
        self.extra = kwargs
    
    def to_dict(self):
        data = self.token
        if self.extra:
            data = {"token": self.token, **self.extra}
        return data


class URLParseRequest:
    """URL解析请求"""
    
    def __init__(
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
        self.url = url
        self.lang = lang
        self.sync = sync
        self.textual = textual
        self.table = table
        self.molecule = molecule
        self.chart = chart
        self.figure = figure
        self.expression = expression
        self.equation = equation
        self.pages = pages
        self.admin_debug = admin_debug
        self.timeout = timeout
        self.table_cls = table_cls
        self.ordering_method = ordering_method
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "url": self.url,
            "lang": self.lang,
            "sync": self.sync,
            "textual": self.textual,
            "table": self.table,
            "molecule": self.molecule,
            "chart": self.chart,
            "figure": self.figure,
            "expression": self.expression,
            "equation": self.equation,
            "admin_debug": self.admin_debug,
            "timeout": self.timeout,
            "table_cls": self.table_cls,
            "ordering_method": self.ordering_method
        }
        
        if self.pages is not None:
            data["pages"] = self.pages
        if self.extra:
            data.update(self.extra)
            
        return data


class ParseResultRequest:
    """解析结果查询请求"""
    
    def __init__(
        self,
        token: str,
        return_half: bool = False,
        content: bool = True,
        objects: bool = True,
        pages_dict: bool = True,
        molecule_source: bool = False,
        **kwargs
    ):
        self.token = token
        self.return_half = return_half
        self.content = content
        self.objects = objects
        self.pages_dict = pages_dict
        self.molecule_source = molecule_source
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "token": self.token,
            "return_half": self.return_half,
            "content": self.content,
            "objects": self.objects,
            "pages_dict": self.pages_dict,
            "molecule_source": self.molecule_source
        }
        
        if self.extra:
            data.update(self.extra)
            
        return data


class ParseFormattedRequest:
    """格式化解析结果查询请求"""
    
    def __init__(
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
        self.token = token
        self.return_half = return_half
        self.content = content
        self.objects = objects
        self.pages_dict = pages_dict
        self.textual = textual
        self.table = table
        self.molecule = molecule
        self.chart = chart
        self.figure = figure
        self.expression = expression
        self.equation = equation
        self.molecule_source = molecule_source
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "token": self.token,
            "return_half": self.return_half,
            "content": self.content,
            "objects": self.objects,
            "pages_dict": self.pages_dict,
            "textual": self.textual,
            "table": self.table,
            "molecule": self.molecule,
            "chart": self.chart,
            "figure": self.figure,
            "expression": self.expression,
            "equation": self.equation,
            "molecule_source": self.molecule_source
        }
        
        if self.extra:
            data.update(self.extra)
            
        return data


class ParseParagraphsRequest:
    """段落解析结果查询请求"""
    
    def __init__(
        self,
        token: str,
        **kwargs
    ):
        self.token = token
        self.extra = kwargs
    
    def to_dict(self):
        data = self.token
        if self.extra:
            data = {"token": self.token, **self.extra}
        return data


class ImageParseRequest:
    """图片解析请求"""
    
    def __init__(
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
        self.img = img
        self.lang = lang
        self.sync = sync
        self.textual = textual
        self.table = table
        self.molecule = molecule
        self.chart = chart
        self.figure = figure
        self.expression = expression
        self.equation = equation
        self.pages = pages
        self.admin_debug = admin_debug
        self.timeout = timeout
        self.table_cls = table_cls
        self.ordering_method = ordering_method
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "img": self.img,
            "lang": self.lang,
            "sync": self.sync,
            "textual": self.textual,
            "table": self.table,
            "molecule": self.molecule,
            "chart": self.chart,
            "figure": self.figure,
            "expression": self.expression,
            "equation": self.equation,
            "admin_debug": self.admin_debug,
            "timeout": self.timeout,
            "table_cls": self.table_cls,
            "ordering_method": self.ordering_method
        }
        
        if self.pages is not None:
            data["pages"] = self.pages
        if self.extra:
            data.update(self.extra)
            
        return data


class ParseResultRequest:
    """解析结果查询请求"""
    
    def __init__(
        self,
        token: str,
        return_half: bool = False,
        content: bool = True,
        objects: bool = True,
        pages_dict: bool = True,
        molecule_source: bool = False,
        **kwargs
    ):
        self.token = token
        self.return_half = return_half
        self.content = content
        self.objects = objects
        self.pages_dict = pages_dict
        self.molecule_source = molecule_source
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "token": self.token,
            "return_half": self.return_half,
            "content": self.content,
            "objects": self.objects,
            "pages_dict": self.pages_dict,
            "molecule_source": self.molecule_source
        }
        
        if self.extra:
            data.update(self.extra)
            
        return data


class ParseFormattedRequest:
    """格式化解析结果查询请求"""
    
    def __init__(
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
        self.token = token
        self.return_half = return_half
        self.content = content
        self.objects = objects
        self.pages_dict = pages_dict
        self.textual = textual
        self.table = table
        self.molecule = molecule
        self.chart = chart
        self.figure = figure
        self.expression = expression
        self.equation = equation
        self.molecule_source = molecule_source
        self.extra = kwargs
    
    def to_dict(self):
        data = {
            "token": self.token,
            "return_half": self.return_half,
            "content": self.content,
            "objects": self.objects,
            "pages_dict": self.pages_dict,
            "textual": self.textual,
            "table": self.table,
            "molecule": self.molecule,
            "chart": self.chart,
            "figure": self.figure,
            "expression": self.expression,
            "equation": self.equation,
            "molecule_source": self.molecule_source
        }
        
        if self.extra:
            data.update(self.extra)
            
        return data


class ParseParagraphsRequest:
    """段落解析结果查询请求"""
    
    def __init__(
        self,
        token: str,
        **kwargs
    ):
        self.token = token
        self.extra = kwargs
    
    def to_dict(self):
        data = self.token
        if self.extra:
            data = {"token": self.token, **self.extra}
        return data