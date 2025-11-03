Bohrium OpenAPI Python SDK 文档
=====================================

欢迎使用 Bohrium OpenAPI Python SDK！本SDK提供了与Bohrium平台交互的Python接口。

.. toctree::
   :maxdepth: 2
   :caption: 内容目录:
   
   installation
   quickstart
   tutorial
   api/reference
   examples
   faq

.. toctree::
   :hidden:
   
   api/reference

简介
----

Bohrium OpenAPI Python SDK 是一个功能强大的Python库，用于与Bohrium平台的各种服务进行交互。SDK支持同步和异步两种操作模式，并提供以下核心功能：

* **任务管理 (Job)**: 提交、查询和管理计算任务
* **Sigma搜索**: 高性能搜索服务
* **通用解析器 (UniParser)**: 文件解析和处理
* **知识库 (KnowledgeBase)**: 知识库管理和检索
* **论文管理 (Paper)**: 论文相关操作

特性
----

* ✅ 完整的类型提示支持
* ✅ 同步和异步API
* ✅ 自动重试机制
* ✅ 详细的错误处理
* ✅ 简洁的API设计

快速开始
--------

最简单的使用方式：

.. code-block:: python

   from bohrium import Bohrium
   
   # 初始化客户端
   client = Bohrium(access_key="your_access_key")
   
   # 使用某个功能
   result = client.job.list()

更多详细信息，请查看 :doc:`快速开始 <quickstart>` 和 :doc:`教程 <tutorial>`。

索引和表格
==========

* :ref:`genindex` - 完整索引（所有术语、函数、类等）
* :ref:`modindex` - 模块索引（所有Python模块列表）

.. note::
   您可以使用页面左侧的搜索框快速查找文档内容。

