API参考
========

本文档提供了 Bohrium OpenAPI Python SDK 的完整API参考。

客户端类
--------

.. automodule:: bohrium
   :members:
   :undoc-members:
   :show-inheritance:

主客户端
~~~~~~~~

.. autoclass:: bohrium.Bohrium
   :members:
   :undoc-members:
   :show-inheritance:

异步客户端
~~~~~~~~~~

.. autoclass:: bohrium.AsyncBohrium
   :members:
   :undoc-members:
   :show-inheritance:

基础客户端类
~~~~~~~~~~~~

.. autoclass:: bohrium.SyncAPIClient
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.AsyncAPIClient
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.BaseClient
   :members:
   :undoc-members:
   :show-inheritance:

资源模块
--------

任务管理 (Job)
~~~~~~~~~~~~~~

.. automodule:: bohrium.resources.job
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.resources.job.Job
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.resources.job.AsyncJob
   :members:
   :undoc-members:
   :show-inheritance:

Sigma搜索
~~~~~~~~~

.. automodule:: bohrium.resources.sigma_search
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.resources.sigma_search.SigmaSearch
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.resources.sigma_search.AsyncSigmaSearch
   :members:
   :undoc-members:
   :show-inheritance:

通用解析器
~~~~~~~~~~

.. automodule:: bohrium.resources.uni_parser
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.resources.uni_parser.UniParser
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.resources.uni_parser.AsyncUniParser
   :members:
   :undoc-members:
   :show-inheritance:

知识库
~~~~~~

.. automodule:: bohrium.resources.knowledge_base
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.resources.knowledge_base.KnowledgeBase
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.resources.knowledge_base.AsyncKnowledgeBase
   :members:
   :undoc-members:
   :show-inheritance:

论文管理
~~~~~~~~

.. automodule:: bohrium.resources.paper
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.resources.paper.Paper
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: bohrium.resources.paper.AsyncPaper
   :members:
   :undoc-members:
   :show-inheritance:

类型定义
--------

任务类型
~~~~~~~~

.. automodule:: bohrium.types.job
   :members:
   :undoc-members:
   :show-inheritance:

Sigma搜索类型
~~~~~~~~~~~~~

.. automodule:: bohrium.types.sigma_search
   :members:
   :undoc-members:
   :show-inheritance:

通用解析器类型
~~~~~~~~~~~~~~

.. automodule:: bohrium.types.uni_parser
   :members:
   :undoc-members:
   :show-inheritance:

知识库类型
~~~~~~~~~~

.. automodule:: bohrium.types.knowledge_base
   :members:
   :undoc-members:
   :show-inheritance:

论文类型
~~~~~~~~

.. automodule:: bohrium.types.paper
   :members:
   :undoc-members:
   :show-inheritance:

异常类
------

.. automodule:: bohrium._exceptions
   :members:
   :undoc-members:
   :show-inheritance:

.. autoexception:: bohrium._exceptions.BohriumError
   :members:
   :undoc-members:

.. autoexception:: bohrium._exceptions.APIStatusError
   :members:
   :undoc-members:

工具函数
--------

.. automodule:: bohrium._utils._utils
   :members:
   :undoc-members:

.. automodule:: bohrium._utils._logs
   :members:
   :undoc-members:

.. automodule:: bohrium._utils._typing
   :members:
   :undoc-members:

