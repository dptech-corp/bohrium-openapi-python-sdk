安装指南
=========

本页面将指导您安装 Bohrium OpenAPI Python SDK。

系统要求
--------

* Python 3.7 或更高版本
* pip 包管理器

安装方法
--------

使用 pip 安装（推荐）
~~~~~~~~~~~~~~~~~~~~

最简单的方式是使用 pip 直接从 PyPI 安装：

.. code-block:: bash

   pip install bohrium-sdk

如果您使用的是 Python 3，可能需要使用 pip3：

.. code-block:: bash

   pip3 install bohrium-sdk

从源码安装
~~~~~~~~~~

如果您想从源码安装最新版本或进行开发，可以按以下步骤操作：

.. code-block:: bash

   # 克隆仓库
   git clone https://github.com/dingzhaohan/bohrium-openapi-python-sdk.git
   cd bohrium-openapi-python-sdk
   
   # 安装依赖
   pip install -r requirements.txt
   
   # 安装SDK
   pip install -e .

开发模式安装
~~~~~~~~~~~~

如果您想参与SDK的开发，建议使用开发模式安装：

.. code-block:: bash

   git clone https://github.com/dingzhaohan/bohrium-openapi-python-sdk.git
   cd bohrium-openapi-python-sdk
   pip install -e ".[dev]"

验证安装
--------

安装完成后，您可以验证安装是否成功：

.. code-block:: python

   python -c "import bohrium; print(bohrium.__version__)"

或者：

.. code-block:: bash

   python -c "from bohrium import Bohrium; print('安装成功!')"

依赖包
------

SDK主要依赖以下包：

* `httpx <https://www.python-httpx.org/>`_ - 用于HTTP请求
* `pyhumps <https://github.com/nficano/pyhumps>`_ - 用于命名转换
* `typing_extensions <https://pypi.org/project/typing-extensions/>`_ - 类型扩展支持
* `anyio <https://anyio.readthedocs.io/>`_ - 异步IO支持
* `requests <https://requests.readthedocs.io/>`_ - HTTP库
* `tqdm <https://tqdm.github.io/>`_ - 进度条显示
* `distro <https://github.com/python-distro/distro>`_ - 系统信息

这些依赖会在安装SDK时自动安装。

故障排除
--------

常见问题
~~~~~~~~

**问题**: 安装时出现权限错误

**解决方案**: 使用 ``--user`` 标志安装到用户目录：

.. code-block:: bash

   pip install --user bohrium-sdk

**问题**: Python版本不兼容

**解决方案**: 确保您的Python版本 >= 3.7。可以使用以下命令检查：

.. code-block:: bash

   python --version

**问题**: 依赖包冲突

**解决方案**: 建议使用虚拟环境：

.. code-block:: bash

   # 创建虚拟环境
   python -m venv venv
   
   # 激活虚拟环境 (Windows)
   venv\Scripts\activate
   
   # 激活虚拟环境 (Linux/Mac)
   source venv/bin/activate
   
   # 安装SDK
   pip install bohrium-sdk

下一步
------

安装完成后，请继续阅读 :doc:`quickstart` 开始使用SDK。

