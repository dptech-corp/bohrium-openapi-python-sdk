#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sigma Search接口测试

本示例展示了如何使用Bohrium SDK的Sigma Search接口进行智能搜索。
"""

from bohrium import Bohrium
from bohrium.types.sigma_search.sigma_search import (
    CreateSessionRequest,
    FollowUpRequest,
    SessionInfo,
    PaperInfo
)

def main():
    # 初始化客户端
    # 请替换为你的实际access_key
    bohrium = Bohrium(access_key="91eb9cdf3e434172ad8dba347b6471c4")

    print("=== Sigma Search接口测试 ===\n")

    # 1. 创建搜索会话
    print("1. 创建搜索会话:")
    print("-" * 50)
    try:
        session_result = bohrium.sigma_search.create_session(
            query="Transformer在视频处理中的应用",
            model="deepseek",
            discipline="All",
            resource_id_list=[]
        )
        print("会话创建成功！")
        print(f"会话UUID: {session_result.get('uuid')}")
        print(f"会话标题: {session_result.get('title')}")
        print(f"是否分享: {session_result.get('share')}")
        
        session_uuid = session_result.get('uuid')
        if not session_uuid:
            print("未获取到会话UUID，无法继续测试")
            return
            
    except Exception as e:
        print(f"创建会话失败: {e}")
        print("注意：这可能是由于使用了测试用的access_key导致的")
        print("请替换为真实的access_key后重新测试")
        return

    print("\n" + "="*50 + "\n")

    # 2. 获取会话详情
    print("2. 获取会话详情:")
    print("-" * 50)
    try:
        session_detail = bohrium.sigma_search.get_session(session_uuid)
        print("会话详情获取成功！")
        print(f"会话状态: {session_detail.get('status')}")
        print(f"模型类型: {session_detail.get('modelType')}")
        print(f"创建时间: {session_detail.get('createTime')}")
        print(f"权限级别: {session_detail.get('permission')}")
        print(f"学科领域: {session_detail.get('discipline')}")
        
        # 获取问题信息
        questions = session_detail.get('questions', [])
        if questions:
            question = questions[0]
            print(f"问题ID: {question.get('id')}")
            print(f"问题状态: {question.get('status')}")
            print(f"最后答案ID: {question.get('lastAnswerID')}")
            query_id = question.get('id')
        else:
            print("未找到问题信息")
            query_id = None
            
    except Exception as e:
        print(f"获取会话详情失败: {e}")
        query_id = None

    print("\n" + "="*50 + "\n")

    # # 3. 获取相关文献
    # print("3. 获取相关文献:")
    # print("-" * 50)
    # if query_id:
    #     try:
    #         papers_result = bohrium.sigma_search.get_papers(
    #             query_id=query_id,
    #             sort="RelevanceScore"
    #         )
    #         print("文献获取成功！")
    #         papers = papers_result.get('list', [])
    #         print(f"找到 {len(papers)} 篇相关文献")
            
    #         if papers:
    #             paper = papers[0]
    #             print(f"第一篇文献标题: {paper.get('title')}")
    #             print(f"第一篇文献作者: {', '.join(paper.get('author', [])[:3])}")
    #             print(f"第一篇文献期刊: {paper.get('journal')}")
    #             print(f"第一篇文献摘要: {paper.get('abstract', '')[:100]}...")
    #     except Exception as e:
    #         print(f"获取文献失败: {e}")
    # else:
    #     print("跳过文献获取测试（缺少query_id）")

    # print("\n" + "="*50 + "\n")

    # 4. 获取总结内容
    print("4. 获取总结内容:")
    print("-" * 50)
    if query_id:
        try:
            summary_result = bohrium.sigma_search.get_summary_content(query_id=query_id)
            print("总结内容获取成功！")
            print(f"问题状态: {summary_result.get('status')}")
            print(f"论文总数: {summary_result.get('paperTotal', 0)}")
            print(f"知识库总数: {summary_result.get('knowledgeBaseTotal', 0)}")
            
            # 显示部分总结内容
            summary = summary_result.get('summary', '')
            if summary:
                print(f"总结内容预览: {summary[:200]}...")
            
            # 显示相关问题
            related = summary_result.get('related', [])
            if related:
                print(f"相关问题数量: {len(related)}")
                for i, rel in enumerate(related[:3]):
                    print(f"  问题{i+1}: {rel.get('query', '')}")
                    
        except Exception as e:
            print(f"获取总结内容失败: {e}")
    else:
        print("跳过总结内容获取测试（缺少query_id）")

    print("\n" + "="*50 + "\n")

    # # 5. 追问测试
    # print("5. 追问测试:")
    # print("-" * 50)
    # try:
    #     follow_up_result = bohrium.sigma_search.follow_up_question(
    #         session_uuid=session_uuid,
    #         query="Transformer在音频处理中的应用"
    #     )
    #     print("追问成功！")
    #     print(f"新问题ID: {follow_up_result.get('id')}")
    #     print(f"新问题查询: {follow_up_result.get('query')}")
    #     print(f"最后答案ID: {follow_up_result.get('lastAnswerID')}")
    # except Exception as e:
    #     print(f"追问失败: {e}")

    # print("\n" + "="*50 + "\n")

    # # 6. 获取搜索历史
    # print("6. 获取搜索历史:")
    # print("-" * 50)
    # try:
    #     history_result = bohrium.sigma_search.get_search_history()
    #     print("搜索历史获取成功！")
    #     sessions = history_result.get('sessions', [])
    #     print(f"历史会话数量: {len(sessions)}")
        
    #     for i, session in enumerate(sessions[:3]):
    #         print(f"  会话{i+1}: {session.get('title')} ({session.get('uuid')})")
    #         print(f"    创建时间: {session.get('createTime')}")
    #         print(f"    状态: {session.get('status')}")
    # except Exception as e:
    #     print(f"获取搜索历史失败: {e}")

    # print("\n" + "="*50 + "\n")

    # # 7. 使用类型定义方式
    # print("7. 使用类型定义方式:")
    # print("-" * 50)
    # try:
    #     # 创建会话请求
    #     session_request = CreateSessionRequest(
    #         query="深度学习在医疗诊断中的应用",
    #         model="qwen",
    #         discipline="LS",  # 生命科学
    #         resource_id_list=[]
    #     )
        
    #     session_result2 = bohrium.sigma_search.search_with_request(session_request)
    #     print("使用类型定义创建会话成功！")
    #     print(f"会话UUID: {session_result2.get('uuid')}")
    #     print(f"会话标题: {session_result2.get('title')}")
        
    #     # 追问请求
    #     follow_up_request = FollowUpRequest(
    #         session_uuid=session_result2.get('uuid'),
    #         query="深度学习在医学影像分析中的具体应用"
    #     )
        
    #     follow_up_result2 = bohrium.sigma_search.search_with_request(follow_up_request)
    #     print("使用类型定义追问成功！")
    #     print(f"新问题ID: {follow_up_result2.get('id')}")
        
    # except Exception as e:
    #     print(f"使用类型定义方式失败: {e}")

    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()
