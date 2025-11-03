# 文档构建说明

本文档目录包含 Bohrium OpenAPI Python SDK 的完整文档。

## 本地构建

### 前置要求

1. Python 3.7 或更高版本
2. 安装文档依赖：

```bash
pip install -r docs/requirements.txt
```

### 构建HTML文档

```bash
cd docs
make html
```

构建完成后，文档将在 `docs/build/html/index.html`

### 查看文档

在浏览器中打开 `docs/build/html/index.html` 即可查看本地构建的文档。

### 其他构建选项

- `make clean` - 清理构建文件
- `make html` - 构建HTML文档
- `make latexpdf` - 构建PDF文档（需要LaTeX）
- `make help` - 查看所有可用命令

## 自动部署

文档会在推送到 `main` 分支时自动通过 GitHub Actions 构建并部署到 GitHub Pages。

## 文档结构

```
docs/
├── source/          # 文档源文件
│   ├── conf.py     # Sphinx配置
│   ├── index.rst   # 文档首页
│   ├── installation.rst
│   ├── quickstart.rst
│   ├── tutorial.rst
│   ├── examples.rst
│   ├── faq.rst
│   ├── api/        # API参考文档
│   ├── _static/    # 静态文件
│   └── _templates/ # 自定义模板
├── build/          # 构建输出（不纳入版本控制）
├── Makefile        # 构建命令
└── requirements.txt # 文档依赖
```

## 开发建议

1. 使用 `make html` 构建后立即在浏览器中查看，确保格式正确
2. 修改文档后重新构建查看效果
3. 遵循 reStructuredText 格式规范
4. API参考文档通过 `autodoc` 自动从代码生成

