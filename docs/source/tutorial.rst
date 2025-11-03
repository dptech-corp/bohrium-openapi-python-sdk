教程
====

本教程将详细介绍如何使用 Bohrium OpenAPI Python SDK 的各项功能。

目录
----

* :ref:`身份验证 <authentication>`
* :ref:`任务管理 <job-management>`
* :ref:`Sigma搜索 <sigma-search>`
* :ref:`通用解析器 <uni-parser>`
* :ref:`知识库 <knowledge-base>`
* :ref:`论文管理 <paper-management>`
* :ref:`异步操作 <async-operations>`
* :ref:`高级配置 <advanced-configuration>`

.. _authentication:

身份验证
--------

SDK支持多种身份验证方式。最基本的方式是提供 `access_key`：

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")

如果您的应用需要额外的应用密钥，可以同时提供 `app_key`：

.. code-block:: python

   client = Bohrium(
       access_key="your_access_key",
       app_key="your_app_key"
   )

对于多项目场景，可以指定 `project_id`：

.. code-block:: python

   client = Bohrium(
       access_key="your_access_key",
       project_id="your_project_id"
   )

.. _job-management:

任务管理
--------

任务管理是SDK的核心功能之一。以下是一些常见操作：

创建任务
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 创建新任务
   job = client.job.create(
       # 任务参数...
   )

列出任务
~~~~~~~~

.. code-block:: python

   # 列出所有任务
   jobs = client.job.list()
   
   # 带分页
   jobs = client.job.list(limit=10, offset=0)
   
   for job in jobs:
       print(f"任务ID: {job.id}, 状态: {job.status}")

获取任务详情
~~~~~~~~~~~~

.. code-block:: python

   # 获取特定任务
   job = client.job.retrieve(job_id="job_id_here")
   print(f"任务状态: {job.status}")
   print(f"创建时间: {job.created_at}")

更新任务
~~~~~~~~

.. code-block:: python

   # 更新任务
   updated_job = client.job.update(
       job_id="job_id_here",
       # 更新参数...
   )

删除任务
~~~~~~~~

.. code-block:: python

   # 删除任务
   client.job.delete(job_id="job_id_here")

.. _sigma-search:

Sigma搜索
---------

Sigma搜索提供了高性能的搜索功能：

基本搜索
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 执行搜索
   results = client.sigma_search.search(
       query="your_search_query",
       limit=10
   )
   
   for result in results:
       print(result)

流式搜索
~~~~~~~~

对于大量数据的搜索，可以使用流式方式：

.. code-block:: python

   # 流式获取搜索结果
   for chunk in client.sigma_search.search_stream(query="your_query"):
       print(chunk)

.. _uni-parser:

通用解析器
----------

通用解析器可以帮助您解析各种格式的文件：

解析文件
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 解析文件
   result = client.uni_parser.parse(
       file_path="path/to/file.pdf",
       parser_type="pdf"
   )
   
   print(result.content)

支持的格式
~~~~~~~~~~

通用解析器支持多种文件格式，包括：

* PDF文件
* Word文档
* Excel表格
* 图片文件
* 等等...

.. _knowledge-base:

知识库
------

知识库功能允许您管理和检索知识库内容：

列出知识库
~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 列出所有知识库
   knowledge_bases = client.knowledge_base.list()
   
   for kb in knowledge_bases:
       print(f"知识库名称: {kb.name}")

创建知识库
~~~~~~~~~~

.. code-block:: python

   # 创建新知识库
   kb = client.knowledge_base.create(
       name="我的知识库",
       description="知识库描述"
   )

检索知识库
~~~~~~~~~~

.. code-block:: python

   # 从知识库检索信息
   results = client.knowledge_base.retrieve(
       knowledge_base_id="kb_id",
       query="查询内容"
   )

.. _paper-management:

论文管理
--------

论文管理功能提供了论文相关的操作：

列出论文
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 列出论文
   papers = client.paper.list()
   
   for paper in papers:
       print(f"论文标题: {paper.title}")

获取论文详情
~~~~~~~~~~~~

.. code-block:: python

   # 获取论文详情
   paper = client.paper.retrieve(paper_id="paper_id")
   print(f"标题: {paper.title}")
   print(f"作者: {paper.authors}")

.. _async-operations:

异步操作
--------

SDK提供了完整的异步支持，适合需要并发处理的场景：

基本异步使用
~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from bohrium import AsyncBohrium
   
   async def fetch_jobs():
       client = AsyncBohrium(access_key="your_access_key")
       jobs = await client.job.list()
       return jobs
   
   # 运行
   jobs = asyncio.run(fetch_jobs())

并发请求
~~~~~~~~

.. code-block:: python

   import asyncio
   from bohrium import AsyncBohrium
   
   async def fetch_multiple():
       client = AsyncBohrium(access_key="your_access_key")
       
       # 并发获取多个任务
       tasks = [
           client.job.retrieve(job_id="id1"),
           client.job.retrieve(job_id="id2"),
           client.job.retrieve(job_id="id3"),
       ]
       
       results = await asyncio.gather(*tasks)
       return results
   
   results = asyncio.run(fetch_multiple())

.. _advanced-configuration:

高级配置
--------

自定义超时和重试
~~~~~~~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(
       access_key="your_access_key",
       timeout=120.0,  # 120秒超时
       max_retries=5   # 最多重试5次
   )

自定义HTTP客户端
~~~~~~~~~~~~~~~~

.. code-block:: python

   import httpx
   from bohrium import Bohrium
   
   # 创建自定义HTTP客户端
   custom_client = httpx.Client(
       timeout=60.0,
       verify=True
   )
   
   client = Bohrium(
       access_key="your_access_key",
       http_client=custom_client
   )

自定义Base URL
~~~~~~~~~~~~~~

如果需要使用不同的API端点：

.. code-block:: python

   client = Bohrium(
       access_key="your_access_key",
       base_url="https://custom-api.example.com"
   )

错误处理最佳实践
~~~~~~~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   from bohrium._exceptions import (
       BohriumError,
       APIStatusError,
       RateLimitError,
   )
   
   client = Bohrium(access_key="your_access_key")
   
   try:
       result = client.job.retrieve(job_id="job_id")
   except RateLimitError as e:
       # 处理限流，可以等待后重试
       print(f"遇到限流，等待 {e.retry_after} 秒")
   except APIStatusError as e:
       # 处理API错误
       print(f"API错误: {e.status_code} - {e.message}")
   except BohriumError as e:
       # 处理其他SDK错误
       print(f"SDK错误: {e}")

下一步
------

* 查看 :doc:`api/reference` 了解完整的API参考
* 查看 :doc:`examples` 查看更多实际使用示例
* 查看 :doc:`faq` 了解常见问题

