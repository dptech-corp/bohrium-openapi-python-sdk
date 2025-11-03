常见问题 (FAQ)
==============

本文档回答了一些使用 Bohrium OpenAPI Python SDK 时的常见问题。

安装和配置
----------

如何安装SDK？
~~~~~~~~~~~~

使用 pip 安装：

.. code-block:: bash

   pip install bohrium-sdk

更多安装选项，请查看 :doc:`installation`。

如何配置API密钥？
~~~~~~~~~~~~~~~~~

有三种方式：

1. **环境变量（推荐）**：

   .. code-block:: bash

      export BOHRIUM_ACCESS_KEY="your_key"

2. **代码中直接传入**：

   .. code-block:: python

      client = Bohrium(access_key="your_key")

3. **混合使用**：参数会覆盖环境变量

更多信息，请查看 :doc:`quickstart`。

如何验证安装是否成功？
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   try:
       client = Bohrium()
       print("安装成功！")
   except ImportError as e:
       print(f"安装失败: {e}")

使用问题
--------

同步和异步客户端有什么区别？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **同步客户端 (Bohrium)**: 适用于大多数场景，代码更简单直观
* **异步客户端 (AsyncBohrium)**: 适用于需要并发处理的场景，性能更好

选择建议：
- 简单脚本或少量请求：使用同步客户端
- 需要处理大量并发请求：使用异步客户端

更多信息，请查看 :doc:`tutorial` 中的 :ref:`async-operations` 部分。

如何处理请求超时？
~~~~~~~~~~~~~~~~~~

可以在初始化客户端时设置超时时间：

.. code-block:: python

   client = Bohrium(
       access_key="your_key",
       timeout=120.0  # 120秒超时
   )

也可以自定义HTTP客户端来设置更细粒度的超时控制。

如何配置重试机制？
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   client = Bohrium(
       access_key="your_key",
       max_retries=5  # 最多重试5次
   )

SDK会自动处理临时性错误并重试。

错误处理
--------

常见的错误类型有哪些？
~~~~~~~~~~~~~~~~~~~~~~

主要错误类型包括：

* ``AuthenticationError``: 认证失败
* ``PermissionDeniedError``: 权限不足
* ``NotFoundError``: 资源不存在
* ``BadRequestError``: 请求参数错误
* ``RateLimitError``: 请求频率过高
* ``InternalServerError``: 服务器内部错误

如何处理限流错误？
~~~~~~~~~~~~~~~~~~

遇到限流时，SDK会自动重试。您也可以手动处理：

.. code-block:: python

   from bohrium._exceptions import RateLimitError
   import time
   
   try:
       result = client.job.retrieve(job_id="job_id")
   except RateLimitError as e:
       wait_time = getattr(e, 'retry_after', 60)
       print(f"遇到限流，等待 {wait_time} 秒")
       time.sleep(wait_time)
       # 重试操作

为什么会出现认证错误？
~~~~~~~~~~~~~~~~~~~~~~

可能的原因：

1. API密钥错误或过期
2. 未设置API密钥
3. 密钥格式不正确

检查步骤：

.. code-block:: python

   import os
   
   # 检查环境变量
   print(f"ACCESS_KEY: {os.environ.get('BOHRIUM_ACCESS_KEY', '未设置')}")
   
   # 或在代码中直接验证
   try:
       client = Bohrium(access_key="your_key")
       client.job.list()  # 尝试一个简单操作
   except AuthenticationError:
       print("认证失败，请检查密钥")

性能优化
--------

如何提高请求性能？
~~~~~~~~~~~~~~~~~~

1. **使用异步客户端**进行并发请求
2. **复用客户端实例**，避免频繁创建
3. **合理设置超时时间**，避免过长等待
4. **使用流式接口**处理大量数据

示例：

.. code-block:: python

   # 复用客户端
   client = Bohrium(access_key="your_key")
   
   # 并发请求（异步）
   import asyncio
   from bohrium import AsyncBohrium
   
   async def fetch_multiple():
       client = AsyncBohrium(access_key="your_key")
       results = await asyncio.gather(
           client.job.retrieve("id1"),
           client.job.retrieve("id2"),
           client.job.retrieve("id3"),
       )
       return results

如何处理大量数据的请求？
~~~~~~~~~~~~~~~~~~~~~~~~

对于大量数据，建议使用流式接口：

.. code-block:: python

   # 流式获取搜索结果
   for chunk in client.sigma_search.search_stream(query="query"):
       process_chunk(chunk)

功能问题
--------

支持哪些文件格式的解析？
~~~~~~~~~~~~~~~~~~~~~~~~

通用解析器支持多种格式，包括但不限于：

* PDF (.pdf)
* Word文档 (.doc, .docx)
* Excel (.xls, .xlsx)
* 图片文件 (.jpg, .png, 等)
* 文本文件 (.txt, .md)

具体支持的格式请参考API文档。

如何获取任务的实时状态？
~~~~~~~~~~~~~~~~~~~~~~~~

可以定期轮询任务状态：

.. code-block:: python

   import time
   
   while True:
       job = client.job.retrieve(job_id="job_id")
       print(f"状态: {job.status}")
       
       if job.status in ["completed", "failed"]:
           break
       
       time.sleep(5)  # 每5秒查询一次

其他问题
--------

SDK是否支持代理？
~~~~~~~~~~~~~~~~~

可以通过自定义HTTP客户端设置代理：

.. code-block:: python

   import httpx
   from bohrium import Bohrium
   
   proxy_client = httpx.Client(
       proxies="http://proxy.example.com:8080"
   )
   
   client = Bohrium(
       access_key="your_key",
       http_client=proxy_client
   )

如何在Docker中使用SDK？
~~~~~~~~~~~~~~~~~~~~~~~

在Docker容器中使用时，确保：

1. 通过环境变量传递API密钥
2. 设置适当的网络配置
3. 检查时区和时间设置

.. code-block:: dockerfile

   FROM python:3.9
   RUN pip install bohrium-sdk
   ENV BOHRIUM_ACCESS_KEY=your_key
   COPY app.py .
   CMD ["python", "app.py"]

如何获取帮助？
~~~~~~~~~~~~~

如果遇到问题：

1. 查看本文档的相应章节
2. 查看 :doc:`api/reference` 了解API详情
3. 查看 :doc:`examples` 查看示例代码
4. 在GitHub仓库提交Issue

仍然无法解决？
--------------

如果以上方法都无法解决您的问题，请：

1. 检查SDK版本是否为最新版本
2. 查看错误信息的详细信息
3. 在GitHub仓库提交Issue，并提供：
   * 错误信息和堆栈跟踪
   * 您的代码示例
   * SDK版本和Python版本
   * 操作系统信息

