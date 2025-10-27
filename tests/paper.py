from bohrium import Bohrium
from bohrium.types.paper.paper import PaperRAGRequest

# 初始化客户端
bohrium = Bohrium(access_key="d5910e48c8cb4957bcaca9b33882eb0e")

# 1. 直接传参数方式
result = bohrium.paper.rag_pass_keyword(
    type=1,
    rerank=0,
    words=["models", "Recent"],
    question="Recent developments in large models",
    start_time="2022-01-01",
    end_time="2024-01-01",
    page_size=10
)

print("直接传参数结果:")
print(result)

# 2. 使用类型定义方式
request = PaperRAGRequest(
    type=1,
    rerank=0,
    words=["models", "Recent"],
    question="Recent developments in large models",
    start_time="2022-01-01",
    end_time="2024-01-01",
    page_size=10
)

result2 = bohrium.paper.rag_pass_keyword(
    type=request.type,
    rerank=request.rerank,
    words=request.words,
    question=request.question,
    start_time=request.startTime,
    end_time=request.endTime,
    page_size=request.pageSize
)

print("\n使用类型定义结果:")
print(result2)
