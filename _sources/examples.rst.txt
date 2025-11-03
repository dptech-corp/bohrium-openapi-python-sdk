示例代码
========

本文档提供了各种实际使用场景的示例代码。

目录
----

* :ref:`基础示例 <basic-examples>`
* :ref:`任务管理示例 <job-examples>`
* :ref:`搜索示例 <search-examples>`
* :ref:`解析示例 <parser-examples>`
* :ref:`异步示例 <async-examples>`
* :ref:`错误处理示例 <error-handling-examples>`

.. _basic-examples:

基础示例
--------

简单初始化
~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   # 使用环境变量
   client = Bohrium()
   
   # 或直接传入密钥
   client = Bohrium(access_key="your_access_key")

检查连接
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   try:
       # 尝试获取任务列表来验证连接
       jobs = client.job.list(limit=1)
       print("连接成功！")
   except Exception as e:
       print(f"连接失败: {e}")

.. _job-examples:

任务管理示例
------------

完整任务生命周期
~~~~~~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 1. 创建任务
   job = client.job.create(
       # 任务参数
       name="我的任务",
       # ... 其他参数
   )
   print(f"任务已创建: {job.id}")
   
   # 2. 查询任务状态
   status = client.job.retrieve(job_id=job.id)
   print(f"任务状态: {status.status}")
   
   # 3. 等待任务完成
   import time
   while status.status not in ["completed", "failed"]:
       time.sleep(5)
       status = client.job.retrieve(job_id=job.id)
       print(f"当前状态: {status.status}")
   
   # 4. 获取结果
   if status.status == "completed":
       print(f"任务完成！结果: {status.result}")
   else:
       print(f"任务失败: {status.error}")
   
   # 5. 清理（可选）
   # client.job.delete(job_id=job.id)

批量处理任务
~~~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 批量创建任务
   task_configs = [
       {"name": "任务1", "config": {...}},
       {"name": "任务2", "config": {...}},
       {"name": "任务3", "config": {...}},
   ]
   
   jobs = []
   for config in task_configs:
       job = client.job.create(**config)
       jobs.append(job)
       print(f"已创建任务: {job.id}")
   
   # 批量查询状态
   for job in jobs:
       status = client.job.retrieve(job_id=job.id)
       print(f"任务 {job.id} 状态: {status.status}")

.. _search-examples:

搜索示例
--------

基本搜索
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 执行搜索
   results = client.sigma_search.search(
       query="机器学习算法",
       limit=20
   )
   
   for i, result in enumerate(results, 1):
       print(f"{i}. {result.title}")
       print(f"   相关性: {result.score}")
       print()

高级搜索
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 带过滤条件的搜索
   results = client.sigma_search.search(
       query="深度学习",
       filters={
           "category": "research",
           "year": 2024
       },
       sort_by="relevance",
       limit=50
   )

流式搜索
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   from tqdm import tqdm
   
   client = Bohrium(access_key="your_access_key")
   
   # 流式获取大量搜索结果
   all_results = []
   with tqdm(desc="搜索中...") as pbar:
       for chunk in client.sigma_search.search_stream(
           query="大规模数据处理",
           limit=1000
       ):
           all_results.extend(chunk.results)
           pbar.update(len(chunk.results))
   
   print(f"共找到 {len(all_results)} 个结果")

.. _parser-examples:

解析示例
--------

解析PDF文件
~~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   
   client = Bohrium(access_key="your_access_key")
   
   # 解析PDF
   result = client.uni_parser.parse(
       file_path="./document.pdf",
       parser_type="pdf"
   )
   
   print(f"文档标题: {result.title}")
   print(f"页数: {result.page_count}")
   print(f"内容预览:\n{result.content[:500]}")

批量解析
~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   import os
   
   client = Bohrium(access_key="your_access_key")
   
   # 批量解析目录中的所有PDF文件
   pdf_dir = "./documents"
   results = []
   
   for filename in os.listdir(pdf_dir):
       if filename.endswith(".pdf"):
           filepath = os.path.join(pdf_dir, filename)
           print(f"正在解析: {filename}")
           
           try:
               result = client.uni_parser.parse(
                   file_path=filepath,
                   parser_type="pdf"
               )
               results.append({
                   "file": filename,
                   "title": result.title,
                   "pages": result.page_count
               })
           except Exception as e:
               print(f"解析失败 {filename}: {e}")
   
   print(f"\n成功解析 {len(results)} 个文件")

.. _async-examples:

异步示例
--------

并发获取多个任务
~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from bohrium import AsyncBohrium
   
   async def get_job_status(job_id: str):
       client = AsyncBohrium(access_key="your_access_key")
       job = await client.job.retrieve(job_id=job_id)
       return job.status
   
   async def main():
       job_ids = ["job1", "job2", "job3", "job4", "job5"]
       
       # 并发获取所有任务状态
       statuses = await asyncio.gather(*[
           get_job_status(job_id) for job_id in job_ids
       ])
       
       for job_id, status in zip(job_ids, statuses):
           print(f"{job_id}: {status}")
   
   asyncio.run(main())

异步流式搜索
~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from bohrium import AsyncBohrium
   
   async def async_search():
       client = AsyncBohrium(access_key="your_access_key")
       
       async for chunk in client.sigma_search.search_stream(
           query="异步处理"
       ):
           print(f"收到 {len(chunk.results)} 个结果")
           for result in chunk.results:
               print(f"  - {result.title}")
   
   asyncio.run(async_search())

.. _error-handling-examples:

错误处理示例
------------

完整错误处理
~~~~~~~~~~~~

.. code-block:: python

   from bohrium import Bohrium
   from bohrium._exceptions import (
       AuthenticationError,
       PermissionDeniedError,
       NotFoundError,
       RateLimitError,
       BadRequestError,
       BohriumError,
   )
   import time
   
   client = Bohrium(access_key="your_access_key")
   
   def safe_operation(func, max_retries=3):
       """安全执行操作，带自动重试"""
       for attempt in range(max_retries):
           try:
               return func()
           except RateLimitError as e:
               if attempt < max_retries - 1:
                   wait_time = getattr(e, 'retry_after', 60)
                   print(f"遇到限流，等待 {wait_time} 秒后重试...")
                   time.sleep(wait_time)
               else:
                   raise
           except AuthenticationError:
               print("认证失败，请检查API密钥")
               raise
           except PermissionDeniedError:
               print("权限不足")
               raise
           except NotFoundError:
               print("资源不存在")
               raise
           except BadRequestError as e:
               print(f"请求参数错误: {e}")
               raise
           except BohriumError as e:
               print(f"SDK错误: {e}")
               raise
           except Exception as e:
               print(f"未知错误: {e}")
               raise
   
   # 使用示例
   try:
       job = safe_operation(
           lambda: client.job.retrieve(job_id="job_id")
       )
       print(f"任务状态: {job.status}")
   except Exception as e:
       print(f"操作失败: {e}")

重试装饰器
~~~~~~~~~~

.. code-block:: python

   import time
   from functools import wraps
   from bohrium._exceptions import RateLimitError
   
   def retry_on_rate_limit(max_retries=3, base_delay=1):
       """限流重试装饰器"""
       def decorator(func):
           @wraps(func)
           def wrapper(*args, **kwargs):
               for attempt in range(max_retries):
                   try:
                       return func(*args, **kwargs)
                   except RateLimitError as e:
                       if attempt < max_retries - 1:
                           delay = base_delay * (2 ** attempt)
                           print(f"限流，等待 {delay} 秒后重试...")
                           time.sleep(delay)
                       else:
                           raise
               return None
           return wrapper
       return decorator
   
   # 使用装饰器
   @retry_on_rate_limit(max_retries=5)
   def get_job(job_id):
       client = Bohrium(access_key="your_access_key")
       return client.job.retrieve(job_id=job_id)
   
   job = get_job("job_id")

更多示例
--------

您可以在项目的 `tests/ <https://github.com/dingzhaohan/bohrium-openapi-python-sdk/tree/main/tests>`_ 目录中找到更多测试和使用示例。

