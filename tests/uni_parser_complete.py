#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniParser完整接口测试

本示例展示了如何使用Bohrium SDK的UniParser接口进行文件、URL、图片解析以及解析结果查询。
"""

from bohrium import Bohrium
from bohrium.types.uni_parser.uni_parser import (
    FileParseRequest,
    URLParseRequest,
    ImageParseRequest,
    ParseResultRequest,
    ParseFormattedRequest,
    ParseParagraphsRequest
)
import os
import base64

def main():
    # 初始化客户端
    bohrium = Bohrium(access_key="d5910e48c8cb4957bcaca9b33882eb0e")

    print("=== UniParser完整接口测试 ===\n")
    # 创建一个简单的PDF文件用于测试
    dummy_pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
72 720 Td
(Hello World) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000204 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
297
%%EOF"""
    dummy_pdf_path = "dummy.pdf"
    with open(dummy_pdf_path, "wb") as f:
        f.write(dummy_pdf_content)


    # 创建一个虚拟的图片文件用于测试 (一个小的透明PNG)
    dummy_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

    # 第一部分：解析接口测试
    print("=== 第一部分：解析接口测试 ===\n")

    1. URL解析测试
    print("1. URL解析测试:")
    print("-" * 50)
    try:
        result1 = bohrium.uni_parser.trigger_url_async(
            url="https://arxiv.org/pdf/2107.06922",
            lang="unknown",
            sync=False,
            textual=True,
            table=True,
            molecule=True,
            chart=True,
            figure=True,
            expression=True,
            equation=True,
            pages=[],
            admin_debug=False,
            timeout=5000,
            table_cls=False,
            ordering_method="gap_tree"
        )
        print("URL解析成功！")
        if result1:
            print(f"解析任务Token: {result1.get('token', 'N/A')}")
            print(f"解析状态: {result1.get('status', 'N/A')}")
            print(f"完整响应: {result1}")
            
            # 保存token用于后续查询测试
            test_token = result1.get('token')
        else:
            print("解析返回空结果")

        
    except Exception as e:
        print(f"URL解析失败: {e}")

    print("\n" + "="*50 + "\n")

    # 2. 文件解析测试
    print("2. 文件解析测试:")
    print("-" * 50)
    try:
        result2 = bohrium.uni_parser.trigger_file_async(
            file=dummy_pdf_path,
            sync=False
        )
        print("文件解析成功！")
        if result2:
            print(f"解析任务Token: {result2.get('token', 'N/A')}")
            print(f"完整响应: {result2}")
        else:
            print("文件解析返回空结果")
    except Exception as e:
        print(f"文件解析失败: {e}")

    print("\n" + "="*50 + "\n")

    # 3. 图片解析测试
    print("3. 图片解析测试:")
    print("-" * 50)
    try:
        result3 = bohrium.uni_parser.trigger_snip_async(
            img=dummy_image_base64,
            sync=False
        )
        print("图片解析成功！")
        if result3:
            print(f"解析任务Token: {result3.get('token', 'N/A')}")
            print(f"完整响应: {result3}")
        else:
            print("图片解析返回空结果")
    except Exception as e:
        print(f"图片解析失败: {e}")

    print("\n" + "="*50 + "\n")

    # 4. 查询解析结果测试
    print("4. 查询解析结果测试:")
    print("-" * 50)
    test_token = None
    if result2 and result2.get('token'):
        test_token = result2.get('token')
        print(f"使用文件解析的token: {test_token}")
    elif result3 and result3.get('token'):
        test_token = result3.get('token')
        print(f"使用图片解析的token: {test_token}")
    
    if test_token:
        try:
            # 获取原始结果
            result_raw = bohrium.uni_parser.get_result(token=test_token)
            print("获取原始结果成功！")
            if result_raw:
                print(f"解析状态: {result_raw.get('status', 'N/A')}")
                print(f"处理进度: {result_raw.get('proc_page', 0)}/{result_raw.get('total_page', 0)} 页")
            else:
                print("原始结果为空")
        except Exception as e:
            print(f"获取原始结果失败: {e}")
        
        try:
            # 获取格式化结果
            result_formatted = bohrium.uni_parser.get_formatted(token=test_token)
            print("获取格式化结果成功！")
            if result_formatted:
                print(f"解析状态: {result_formatted.get('status', 'N/A')}")
                print(f"处理进度: {result_formatted.get('proc_page', 0)}/{result_formatted.get('total_page', 0)} 页")
            else:
                print("格式化结果为空")
        except Exception as e:
            print(f"获取格式化结果失败: {e}")
        
        try:
            # 获取段落结果
            result_paragraphs = bohrium.uni_parser.get_paragraphs(token=test_token)
            print("获取段落结果成功！")
            if result_paragraphs:
                print(f"解析状态: {result_paragraphs.get('status', 'N/A')}")
                print(f"处理进度: {result_paragraphs.get('proc_page', 0)}/{result_paragraphs.get('total_page', 0)} 页")
            else:
                print("段落结果为空")
        except Exception as e:
            print(f"获取段落结果失败: {e}")
    else:
        print("没有可用的token进行查询测试")

    print("\n" + "="*50 + "\n")

    # 4. 使用类型定义方式测试
    print("4. 使用类型定义方式测试:")
    print("-" * 50)
    try:
        # URL解析请求
        url_request = URLParseRequest(
            url="https://arxiv.org/pdf/2107.06922",
            lang="unknown",
            sync=True,
            textual=True,
            table=True,
            molecule=True,
            chart=True,
            figure=True,
            expression=True,
            equation=True,
            pages=[],
            admin_debug=False,
            timeout=5000,
            table_cls=False,
            ordering_method="gap_tree"
        )
        
        result4 = bohrium.uni_parser.parse_with_request(url_request)
        print("使用类型定义URL解析成功！")
        if result4:
            print(f"解析任务Token: {result4.get('token', 'N/A')}")
            print(f"完整响应: {result4}")
        else:
            print("使用类型定义URL解析返回空结果")
        
        # 图片解析请求
        image_request = ImageParseRequest(
            img=dummy_image_base64,
            lang="unknown",
            sync=False,
            textual=True,
            table=True,
            molecule=True,
            chart=True,
            figure=False,
            expression=True,
            equation=True,
            admin_debug=False,
            timeout=1800,
            table_cls=False,
            ordering_method="gap_tree"
        )
        
        result5 = bohrium.uni_parser.parse_with_request(image_request)
        print("使用类型定义图片解析成功！")
        if result5:
            print(f"解析任务Token: {result5.get('token', 'N/A')}")
            print(f"完整响应: {result5}")
        else:
            print("使用类型定义图片解析返回空结果")
        
    except Exception as e:
        print(f"使用类型定义方式失败: {e}")

    print("\n" + "="*50 + "\n")

    # 第二部分：查询接口测试
    print("=== 第二部分：查询接口测试 ===\n")

    # 5. 获取解析结果
    print("5. 获取解析结果:")
    print("-" * 50)
    try:
        result6 = bohrium.uni_parser.get_result(
            token=test_token,
            return_half=False,
            content=True,
            objects=True,
            pages_dict=True,
            molecule_source=False
        )
        print("解析结果获取成功！")
        print(f"结果类型: {type(result6)}")
        if result6:
            print(f"结果包含 {len(result6)} 个元素")
    except Exception as e:
        print(f"获取解析结果失败: {e}")

    print("\n" + "="*50 + "\n")

    # 6. 获取格式化结果
    print("6. 获取格式化结果:")
    print("-" * 50)
    try:
        result7 = bohrium.uni_parser.get_formatted(
            token=test_token,
            return_half=False,
            content=False,
            objects=True,
            pages_dict=False,
            textual="markup",
            table="markup",
            molecule="markup",
            chart="markup",
            figure="markup",
            expression="markup",
            equation="markup",
            molecule_source=True
        )
        print("格式化结果获取成功！")
        print(f"结果类型: {type(result7)}")
    except Exception as e:
        print(f"获取格式化结果失败: {e}")

    print("\n" + "="*50 + "\n")

    # 7. 获取段落结果
    print("7. 获取段落结果:")
    print("-" * 50)
    try:
        result8 = bohrium.uni_parser.get_paragraphs(
            token=test_token
        )
        print("段落结果获取成功！")
        print(f"结果类型: {type(result8)}")
    except Exception as e:
        print(f"获取段落结果失败: {e}")

    print("\n" + "="*50 + "\n")

    # 8. 使用类型定义方式查询
    print("8. 使用类型定义方式查询:")
    print("-" * 50)
    try:
        # 解析结果请求
        result_request = ParseResultRequest(
            token=test_token,
            return_half=False,
            content=True,
            objects=True,
            pages_dict=True,
            molecule_source=False
        )
        
        result9 = bohrium.uni_parser.parse_with_request(result_request)
        print("使用类型定义获取解析结果成功！")
        
        # 格式化结果请求
        formatted_request = ParseFormattedRequest(
            token=test_token,
            return_half=False,
            content=False,
            objects=True,
            pages_dict=False,
            textual="markup",
            table="markup",
            molecule="markup",
            chart="markup",
            figure="markup",
            expression="markup",
            equation="markup",
            molecule_source=True
        )
        
        result10 = bohrium.uni_parser.parse_with_request(formatted_request)
        print("使用类型定义获取格式化结果成功！")
        
        # 段落结果请求
        paragraphs_request = ParseParagraphsRequest(token=test_token)
        
        result11 = bohrium.uni_parser.parse_with_request(paragraphs_request)
        print("使用类型定义获取段落结果成功！")
        
    except Exception as e:
        print(f"使用类型定义方式查询失败: {e}")

    print("\n" + "="*50 + "\n")

    # 第三部分：综合测试
    print("=== 第三部分：综合测试 ===\n")

    # 9. 不同解析配置测试
    print("9. 不同解析配置测试:")
    print("-" * 50)
    try:
        config_result = bohrium.uni_parser.trigger_url_async(
            url="https://arxiv.org/pdf/2107.06922",
            lang="unknown",
            sync=True,
            textual=True,
            table=True,
            molecule=False,
            chart=False,
            figure=False,
            expression=False,
            equation=False,
            pages=[1, 2],
            admin_debug=False,
            timeout=3000,
            table_cls=True,
            ordering_method="gap_tree"
        )
        print("配置解析成功！")
        if config_result:
            print(f"解析任务Token: {config_result.get('token', 'N/A')}")
            print(f"识别文本: {config_result.get('dict_cfg', {}).get('textual', 'N/A')}")
            print(f"识别表格: {config_result.get('dict_cfg', {}).get('table', 'N/A')}")
            print(f"解析页面: {config_result.get('dict_model', {}).get('pages', 'N/A')}")
            print(f"文本数量: {config_result.get('total_textual', 'N/A')}")
            print(f"表格数量: {config_result.get('total_table', 'N/A')}")
            print(f"完整响应: {config_result}")
        else:
            print("配置解析返回空结果")
    except Exception as e:
        print(f"配置解析失败: {e}")

    print("\n=== 测试完成 ===")

    # 清理虚拟文件
    if os.path.exists(dummy_pdf_path):
        os.remove(dummy_pdf_path)

if __name__ == "__main__":
    main()
