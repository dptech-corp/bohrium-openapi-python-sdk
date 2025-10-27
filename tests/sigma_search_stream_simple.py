#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sigma Search流式输出简单测试
专门测试流式输出的时间特性
"""

import time
import json
from datetime import datetime
from bohrium import Bohrium

def main():
    # 初始化客户端
    bohrium = Bohrium(access_key="91eb9cdf3e434172ad8dba347b6471c4")

    # 创建日志文件
    log_filename = f"sigma_search_stream_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    log_data = {
        "test_start_time": datetime.now().isoformat(),
        "chunks": [],
        "summary": {}
    }

    print("=== Sigma Search流式输出时间测试 ===")
    print(f"日志文件: {log_filename}\n")

    # 1. 创建搜索会话
    print("1. 创建搜索会话:")
    print("-" * 50)
    try:
        session_result = bohrium.sigma_search.create_session(
            query="深度学习在医疗诊断中的应用",
            model="deepseek",
            discipline="All",
            resource_id_list=[]
        )
        print("会话创建成功！")
        print(f"会话UUID: {session_result.get('uuid')}")
        
        session_uuid = session_result.get('uuid')
        if not session_uuid:
            print("未获取到会话UUID，无法继续测试")
            return
            
    except Exception as e:
        print(f"创建会话失败: {e}")
        return

    print("\n" + "="*50 + "\n")

    # 2. 获取会话详情和query_id
    print("2. 获取会话详情:")
    print("-" * 50)
    try:
        session_detail = bohrium.sigma_search.get_session(session_uuid)
        print("会话详情获取成功！")
        
        # 获取问题信息
        questions = session_detail.get('questions', [])
        if questions:
            question = questions[0]
            query_id = question.get('id')
            print(f"问题ID: {query_id}")
            print(f"问题状态: {question.get('status')}")
        else:
            print("未找到问题信息")
            return
            
    except Exception as e:
        print(f"获取会话详情失败: {e}")
        return

    print("\n" + "="*50 + "\n")

    # 3. 等待一下让服务器处理
    print("3. 等待服务器处理...")
    time.sleep(5)  # 等待5秒让服务器开始处理

    # 4. 测试流式输出
    print("4. 流式输出测试:")
    print("-" * 50)
    print("开始接收流式数据...")
    print("=" * 50)
    
    try:
        start_time = time.time()
        first_token_time = None
        chunk_count = 0
        last_chunk_time = start_time
        
        print(f"开始时间: {time.strftime('%H:%M:%S.%f', time.localtime(start_time))}")
        print("-" * 50)
        
        # 获取流式输出
        stream = bohrium.sigma_search.get_summary_stream(query_id=query_id)
        
        if stream is None:
            print("❌ 流式输出返回None，可能服务器还未准备好")
            log_data["summary"]["error"] = "Stream returned None"
            return
        
        for chunk in stream:
            current_time = time.time()
            chunk_count += 1
            
            # 记录chunk信息到日志
            chunk_info = {
                "chunk_number": chunk_count,
                "timestamp": current_time,
                "relative_time": current_time - start_time,
                "content_preview": str(chunk)[:100],
                "content_length": len(str(chunk))
            }
            
            # 记录第一个token的时间
            if first_token_time is None:
                first_token_time = current_time
                first_token_delay = first_token_time - start_time
                chunk_info["is_first_token"] = True
                chunk_info["first_token_delay"] = first_token_delay
                print(f"🚀 First Token时间: {first_token_delay:.3f}秒")
                print(f"First Token内容: {str(chunk)[:100]}...")
                print("-" * 50)
            else:
                chunk_interval = current_time - last_chunk_time
                chunk_info["interval_from_previous"] = chunk_interval
                print(f"Chunk {chunk_count}: +{chunk_interval:.3f}秒 | {str(chunk)[:50]}...")
            
            # 添加到日志数据
            log_data["chunks"].append(chunk_info)
            last_chunk_time = current_time
            
            # 不限制输出数量，记录所有chunks
            # if chunk_count >= 10:
            #     print("... (限制输出，实际可能有更多chunks)")
            #     break
        
        total_time = time.time() - start_time
        
        # 记录统计信息到日志
        log_data["summary"] = {
            "total_time": total_time,
            "total_chunks": chunk_count,
            "first_token_delay": first_token_delay if first_token_time else None,
            "average_chunk_interval": (total_time - first_token_delay) / max(1, chunk_count - 1) if first_token_time and chunk_count > 1 else None,
            "test_end_time": datetime.now().isoformat()
        }
        
        print("-" * 50)
        print(f"📊 流式输出统计:")
        print(f"   总时间: {total_time:.3f}秒")
        print(f"   总chunk数: {chunk_count}")
        if first_token_time:
            print(f"   First Token延迟: {first_token_delay:.3f}秒")
            if chunk_count > 1:
                print(f"   平均chunk间隔: {(total_time - first_token_delay) / (chunk_count - 1):.3f}秒")
        
    except Exception as e:
        print(f"流式输出测试失败: {e}")
        log_data["summary"]["error"] = str(e)
        import traceback
        traceback.print_exc()

    print("\n" + "="*50 + "\n")

    # 5. 获取最终总结内容（对比）
    print("5. 获取最终总结内容:")
    print("-" * 50)
    try:
        summary_result = bohrium.sigma_search.get_summary_content(query_id=query_id)
        print("总结内容获取成功！")
        print(f"问题状态: {summary_result.get('status')}")
        print(f"论文总数: {summary_result.get('paperTotal', 0)}")
        
        # 显示总结内容
        summary = summary_result.get('summary', '')
        if summary:
            print(f"总结内容长度: {len(summary)} 字符")
            print(f"总结内容预览: {summary[:200]}...")
        
    except Exception as e:
        print(f"获取总结内容失败: {e}")

    # 6. 保存日志文件
    print("6. 保存日志文件:")
    print("-" * 50)
    try:
        with open(log_filename, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        print(f"✅ 日志已保存到: {log_filename}")
        print(f"📊 记录了 {len(log_data['chunks'])} 个chunks")
        if log_data["summary"].get("first_token_delay"):
            print(f"🚀 First Token延迟: {log_data['summary']['first_token_delay']:.3f}秒")
        if log_data["summary"].get("average_chunk_interval"):
            print(f"⏱️  平均chunk间隔: {log_data['summary']['average_chunk_interval']:.3f}秒")
    except Exception as e:
        print(f"❌ 保存日志文件失败: {e}")

    print("\n=== 流式输出测试完成 ===")

if __name__ == "__main__":
    main()
