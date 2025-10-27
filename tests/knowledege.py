from bohrium import Bohrium

# 初始化客户端
bohrium = Bohrium(access_key="91eb9cdf3e434172ad8dba347b6471c4")

# 1. 知识库混合召回
result = bohrium.knowledge_base.hybrid_recall(
    knowledge_base_id=7494441,
    text="曹操的伟绩",
    k=10,
    keywords={"曹操": 1.0, "伟绩": 1.0}
)

# 2. 单篇论文召回
papers = [{"paperId": "", "md5": "0002a2d5d0c3c70deedab01811a5a765"}]
result = bohrium.knowledge_base.paper_recall(
    text="曹操", k=10, papers=papers
)

# 3. 获取文件树
file_tree = bohrium.knowledge_base.get_file_tree(folder_id="7494441")

# 4. 获取某个文献的全部chunk
chunk_result = bohrium.knowledge_base.search_by_md5_paper_id(
            md5="0002a2d5d0c3c70deedab01811a5a765",
            paper_id="",
            page_num=0,
            page_size=10
        )
