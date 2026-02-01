#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 missing_translations.txt 中的翻译插入到 chinese 目录，
将 extra_translations.txt 中的翻译插入到 american 目录。
"""

import os
import re
from collections import defaultdict


def parse_diff_file(path):
    """解析 missing/extra 的文本格式，返回 {table: {key: value}}"""
    data = defaultdict(dict)
    current_table = None

    if not os.path.isfile(path):
        return {}

    table_re = re.compile(r'^\[([0-9A-Z_]{1,7})\]')
    kv_re = re.compile(r'^\s*([0-9A-Z_]{1,7})\s*=\s*(.*)$')

    with open(path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.strip('\n\r')
            if not line.strip():
                continue
            m_table = table_re.match(line.strip())
            if m_table:
                current_table = m_table.group(1)
                continue
            m_kv = kv_re.match(line)
            if m_kv and current_table:
                key = m_kv.group(1)
                value = m_kv.group(2)
                data[current_table][key] = value

    return dict(data)


def load_existing_map(txt_path):
    """读取已有键值对，返回 dict"""
    if not os.path.isfile(txt_path):
        return {}

    data = {}
    with open(txt_path, 'r', encoding='utf-8') as f:
        for raw in f:
            line = raw.rstrip('\n\r')
            if not line.strip():
                continue
            if '\t' in line:
                key, value = line.split('\t', 1)
            else:
                parts = line.split(None, 1)
                if len(parts) < 2:
                    continue
                key, value = parts[0], parts[1]
            key = key.strip()
            if key:
                data[key] = value
    return data


def apply_to_directory(diff_data, target_dir):
    """将 diff_data 写入 target_dir，按键字典序排序，返回插入数量"""
    inserted = 0
    for table, entries in diff_data.items():
        table_dir = os.path.join(target_dir, table)
        os.makedirs(table_dir, exist_ok=True)
        txt_path = os.path.join(table_dir, f"{table}.txt")

        existing_map = load_existing_map(txt_path)

        for key, value in entries.items():
            if key in existing_map:
                continue
            existing_map[key] = value
            inserted += 1

        sorted_keys = sorted(existing_map.keys())
        lines = [f"{key}\t{existing_map[key]}" for key in sorted_keys]

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
            if lines:
                f.write("\n")
    return inserted


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    missing_path = os.path.join(script_dir, 'missing_translations.txt')
    extra_path = os.path.join(script_dir, 'extra_translations.txt')

    chinese_dir = os.path.join(script_dir, 'chinese')
    american_dir = os.path.join(script_dir, 'american')

    if not os.path.isdir(chinese_dir):
        print(f"错误: 找不到目录 {chinese_dir}")
        return
    if not os.path.isdir(american_dir):
        print(f"错误: 找不到目录 {american_dir}")
        return

    missing_data = parse_diff_file(missing_path)
    extra_data = parse_diff_file(extra_path)

    if not missing_data:
        print(f"提示: 未找到或无法解析 {missing_path}")
    if not extra_data:
        print(f"提示: 未找到或无法解析 {extra_path}")

    inserted_chs = apply_to_directory(missing_data, chinese_dir) if missing_data else 0
    inserted_ame = apply_to_directory(extra_data, american_dir) if extra_data else 0

    print(f"已插入到 chinese: {inserted_chs} 条")
    print(f"已插入到 american: {inserted_ame} 条")


if __name__ == '__main__':
    main()
