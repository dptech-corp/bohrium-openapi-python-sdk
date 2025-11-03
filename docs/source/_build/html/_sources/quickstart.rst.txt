快速开始
=========

本指南将帮助您快速上手使用 Bohrium OpenAPI Python SDK。

配置API密钥
-----------

使用SDK前，您需要配置API密钥。有三种方式：

方式1: 环境变量（推荐）
~~~~~~~~~~~~~~~~~~~~~~~

设置环境变量是最安全的方式：

.. code-block:: bash

   # Linux/Mac
   export BOHRIUM_ACCESS_KEY="your_access_key_here"
   export BOHRIUM_APP_KEY="your_app_key_here"  # 可选
   export BOHRIUM_PROJECT_ID="your_project_id"  # 可选

   # Windows PowerShell
   $env:BOHRIUM_ACCESS_KEY="your_access_key_here"
   $env:BOHRIUM_APP_KEY="your_app_key_here"
   $env:BOHRIUM_PROJECT_ID="your_project_id"

   # Windows CMD
   set BOHRIUM_ACCESS_KEY=your_access_key_here
   set BOHRIUM_APP_KEY=your_app_key_here
   set BOHRIUM_PROJECT_ID=your_project_id

方式2: 直接传入参数
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(
       access_key="your_access_key_here",
       app_key="your_app_key_here",  # 可选
       project_id="your_project_id"  # 可选
   )

方式3: 混合使用
~~~~~~~~~~~~~~~

可以同时使用环境变量和参数，参数会覆盖环境变量：

.. code-block:: python

   from bohrium import Bohrium
   
   # access_key从环境变量读取，其他参数直接传入
   client = Bohrium(
       app_key="your_app_key_here",
       project_id="your_project_id"
   )

初始化客户端
------------

同步客户端
~~~~~~~~~~

大多数情况下，使用同步客户端即可：

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")

异步客户端
~~~~~~~~~~

对于需要并发处理的场景，可以使用异步客户端：

.. code-block:: python

   import asyncio
   from bohrium import AsyncBohrium
   
   async def main():
       client = AsyncBohrium(access_key="your_access_key")
       # 使用异步方法
       result = await client.job.list()
       return result
   
   # 运行异步代码
   result = asyncio.run(main())

基本使用示例
------------

任务管理
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 列出所有任务
   jobs = client.job.list()
   
   # 获取特定任务
   job = client.job.retrieve(job_id="job_id_here")

Sigma搜索
~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 执行搜索
   results = client.sigma_search.search(
       query="your_search_query",
       # 其他参数...
   )

通用解析器
~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 解析文件
   result = client.uni_parser.parse(
       file_path="path/to/file",
       # 其他参数...
   )

知识库
~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 列出知识库
   knowledge_bases = client.knowledge_base.list()

论文管理
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 列出论文
   papers = client.paper.list()

错误处理
--------

SDK提供了详细的错误类型：

.. code-block:: python

   from bohrium import Bohrium
   from bohrium._exceptions import (
       AuthenticationError,
       PermissionDeniedError,
       NotFoundError,
       RateLimitError,
   )
   
   client = Bohrium(access_key="your_access_key")
   
   try:
       result = client.job.retrieve(job_id="invalid_id")
   except AuthenticationError:
       print("认证失败，请检查API密钥")
   except PermissionDeniedError:
       print("权限不足")
   except NotFoundError:
       print("资源不存在")
   except RateLimitError:
       print("请求频率过高，请稍后重试")
   except Exception as e:
       print(f"其他错误: {e}")

配置选项
--------

客户端支持多种配置选项：

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(
       access_key="your_access_key",
       base_url="https://openapi.dp.tech",  # 自定义API地址
       timeout=60.0,  # 请求超时时间（秒）
       max_retries=3,  # 最大重试次数
   )

下一步
------

* 查看 :doc:`tutorial` 了解更多详细用法
* 查看 :doc:`api/reference` 了解完整的API参考
* 查看 :doc:`examples` 查看更多示例代码

