#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对比 american 文件夹和 chinese 文件夹中的翻译键，
输出缺失和多余的翻译
"""

import os
import re
from collections import defaultdict


def parse_american_directory(dir_path):
    """
    解析 american 目录结构的翻译文件
    
    格式：
    KEY\tvalue
    
    返回：{table_name: {key: value}}
    """
    gxt_data = defaultdict(dict)
    
    if not os.path.isdir(dir_path):
        print(f"目录不存在: {dir_path}")
        return {}
    
    # 按字母顺序处理，MAIN 优先
    table_dirs = sorted(os.listdir(dir_path))
    if 'MAIN' in table_dirs:
        table_dirs.remove('MAIN')
        table_dirs.insert(0, 'MAIN')
    
    for table_name in table_dirs:
        table_path = os.path.join(dir_path, table_name)
        if not os.path.isdir(table_path):
            continue
        
        txt_file = os.path.join(table_path, f"{table_name}.txt")
        if not os.path.exists(txt_file):
            continue
        
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.rstrip('\n\r')
                    if not line.strip():
                        continue
                    
                    # 按 TAB 分隔
                    if '\t' in line:
                        parts = line.split('\t', 1)
                        key = parts[0]
                        value = parts[1] if len(parts) > 1 else ""
                    else:
                        # 如果没有 TAB，可能按空格分隔
                        parts = line.split(None, 1)
                        if len(parts) < 2:
                            continue
                        key, value = parts[0], parts[1]
                    
                    gxt_data[table_name][key] = value
        
        except Exception as e:
            print(f"加载 {txt_file} 失败: {e}")
            continue
    
    return dict(gxt_data)


def parse_chinese_directory(dir_path):
    """
    解析 chinese 目录结构的翻译文件
    
    格式：
    KEY\tvalue
    
    返回：{table_name: {key: value}}
    """
    gxt_data = defaultdict(dict)
    
    if not os.path.isdir(dir_path):
        print(f"目录不存在: {dir_path}")
        return {}
    
    # 按字母顺序处理，MAIN 优先
    table_dirs = sorted(os.listdir(dir_path))
    if 'MAIN' in table_dirs:
        table_dirs.remove('MAIN')
        table_dirs.insert(0, 'MAIN')
    
    for table_name in table_dirs:
        table_path = os.path.join(dir_path, table_name)
        if not os.path.isdir(table_path):
            continue
        
        txt_file = os.path.join(table_path, f"{table_name}.txt")
        if not os.path.exists(txt_file):
            continue
        
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.rstrip('\n\r')
                    if not line.strip():
                        continue
                    
                    # 按 TAB 分隔
                    if '\t' in line:
                        parts = line.split('\t', 1)
                        key = parts[0]
                        value = parts[1] if len(parts) > 1 else ""
                    else:
                        # 如果没有 TAB，可能按空格分隔
                        parts = line.split(None, 1)
                        if len(parts) < 2:
                            continue
                        key, value = parts[0], parts[1]
                    
                    gxt_data[table_name][key] = value
        
        except Exception as e:
            print(f"加载 {txt_file} 失败: {e}")
            continue
    
    return dict(gxt_data)


def get_all_keys(gxt_data):
    """从 GXT 数据结构中提取所有键"""
    all_keys = set()
    for table_name, entries in gxt_data.items():
        for key in entries.keys():
            all_keys.add(key)
    return all_keys


def compare_translations(american_dir, chinese_dir):
    """
    对比两个翻译来源，找出缺失的翻译
    """
    print(f"正在解析 {american_dir}...")
    american_data = parse_american_directory(american_dir)
    american_keys = get_all_keys(american_data)
    print(f"  找到 {len(american_keys)} 个唯一的键")
    
    print(f"\n正在解析 {chinese_dir}...")
    chinese_data = parse_chinese_directory(chinese_dir)
    chinese_keys = get_all_keys(chinese_data)
    print(f"  找到 {len(chinese_keys)} 个唯一的键")
    
    # 找出缺失的键（american 中有但 chinese 中没有）
    missing_keys = american_keys - chinese_keys
    
    # 找出多余的键（chinese 中有但 american 中没有）
    extra_keys = chinese_keys - american_keys
    
    print(f"\n对比结果:")
    print(f"  总共键数量差异: {len(american_keys)} vs {len(chinese_keys)}")
    print(f"  缺失的翻译键: {len(missing_keys)}")
    print(f"  多余的翻译键: {len(extra_keys)}")
    
    return {
        'missing': missing_keys,
        'extra': extra_keys,
       'american_data': american_data,
        'chinese_data': chinese_data,
       'american_keys': american_keys,
        'chinese_keys': chinese_keys
    }


def output_missing_translations(comparison_result, output_file=None):
    """
    输出缺失的翻译
    """
    missing_keys = sorted(comparison_result['missing'])
    
    print(f"\n{'='*60}")
    print(f"缺失的翻译键列表 ({len(missing_keys)} 个)")
    print(f"{'='*60}\n")
    
    # 按表分组
    missing_by_table = defaultdict(list)
    for key in missing_keys:
            for table_name, entries in comparison_result['american_data'].items():
                if key in entries:
                    missing_by_table[table_name].append(key)
                    break
    
    output_lines = []
    
    for table_name in sorted(missing_by_table.keys()):
        keys = sorted(missing_by_table[table_name])
        output_lines.append(f"\n[{table_name}] 缺失 {len(keys)} 个键:")
        output_lines.append("-" * 40)
        
        for key in keys:
            value = comparison_result['american_data'].get(table_name, {}).get(key, "")
            # 为输出美化，截断长值
            if len(value) > 60:
                value = value[:60] + "..."
            output_lines.append(f"  {key:20s} = {value}")
    
    # 输出到控制台
    for line in output_lines:
        print(line)
    
    # 如果指定了输出文件，也保存到文件
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(output_lines))
            print(f"\n结果已保存到: {output_file}")
        except Exception as e:
            print(f"保存输出文件失败: {e}")


def output_extra_translations(comparison_result, output_file=None):
    """
    输出多余的翻译（在 chinese 中有但 native 中没有）
    """
    extra_keys = sorted(comparison_result['extra'])
    
    if not extra_keys:
        print(f"\n没有多余的翻译键")
        return
    
    print(f"\n{'='*60}")
    print(f"多余的翻译键列表 ({len(extra_keys)} 个)")
    print(f"  这些键在 chinese 中存在但在 american 中缺失")
    print(f"{'='*60}\n")
    
    # 按表分组
    extra_by_table = defaultdict(list)
    for key in extra_keys:
        for table_name, entries in comparison_result['chinese_data'].items():
            if key in entries:
                extra_by_table[table_name].append(key)
                break
    
    output_lines = []
    output_lines.append("多余的翻译键列表（chinese 中有但 american 中没有）\n")
    
    for table_name in sorted(extra_by_table.keys()):
        keys = sorted(extra_by_table[table_name])
        output_lines.append(f"\n[{table_name}] 多余 {len(keys)} 个键:")
        output_lines.append("-" * 40)
        
        for key in keys:
            value = comparison_result['chinese_data'].get(table_name, {}).get(key, "")
            if len(value) > 60:
                value = value[:60] + "..."
            output_lines.append(f"  {key:20s} = {value}")
    
    # 输出到控制台
    for line in output_lines:
        print(line)
    
    # 如果指定了输出文件，也保存到文件
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(output_lines))
            print(f"\n结果已保存到: {output_file}")
        except Exception as e:
            print(f"保存输出文件失败: {e}")


def main():
    """主函数"""
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定义路径
    american_dir = os.path.join(script_dir, 'american')
    chinese_dir = os.path.join(script_dir, 'chinese')
    
    # 检查目录是否存在
    if not os.path.isdir(american_dir):
        print(f"错误: 找不到目录 {american_dir}")
        return
    
    if not os.path.isdir(chinese_dir):
        print(f"错误: 找不到目录 {chinese_dir}")
        return
    
    # 执行对比
    result = compare_translations(american_dir, chinese_dir)
    
    # 输出缺失的翻译
    print()
    output_missing_translations(result, 'missing_translations.txt')
    
    # 输出多余的翻译
    output_extra_translations(result, 'extra_translations.txt')
    
    print(f"\n完成！")


if __name__ == '__main__':
    main()
