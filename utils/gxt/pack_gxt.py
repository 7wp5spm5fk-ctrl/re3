import struct
import os
import sys

# GTA GXT 专用的哈希算法 (用于 SA 版本)
def gxt_hash(string):
    string = string.upper()
    hash_val = 0
    for char in string:
        hash_val = (hash_val * 33 + ord(char)) & 0xFFFFFFFF
    return hash_val

def pack_gxt(input_dir, version, output_file):
    if version == 'vc':
        encoding = 'utf-16'
        key_size = 12
    elif version == 'sa':
        encoding = 'cp1252'
        key_size = 8
    elif version == 'sa-mobile':
        encoding = 'utf-16'
        key_size = 8
    else:
        print("不支持的版本")
        return

    tables_names = ['MAIN']
    other_tables = [d for d in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, d)) and d != 'MAIN']
    tables_names.extend(sorted(other_tables))

    table_data_blocks = []

    for table_name in tables_names:
        txt_path = os.path.join(input_dir, table_name, table_name + '.txt')
        if not os.path.exists(txt_path): continue

        entries = []
        with open(txt_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip('\n\r')
                if not line or '\t' not in line: 
                    # 尝试处理没有 Tab 但有空格的情况
                    parts = line.split(None, 1) 
                    if len(parts) < 2: continue
                    key, val = parts[0], parts[1]
                else:
                    key, val = line.split('\t', 1)
                
                entries.append((key.strip(), val))
        
        print(f"正在处理表 [{table_name}]，包含 {len(entries)} 条文本...")

        # 构建 TDAT
        tdat_payload = b''
        offsets = []
        for _, val in entries:
            offsets.append(len(tdat_payload))
            # 替换换行符 \n 为游戏识别的字符（可选）
            encoded_val = val.encode(encoding)
            tdat_payload += encoded_val + (b'\x00\x00' if 'utf-16' in encoding else b'\x00')

        # 构建 TKEY
        tkey_payload = b''
        for i, (key, _) in enumerate(entries):
            offset = offsets[i]
            if version == 'vc':
                key_bytes = key.encode('ascii')[:7].ljust(8, b'\x00')
                tkey_payload += struct.pack('I8s', offset, key_bytes)
            else:
                # SA 处理：如果是 0x 开头的十六进制则转换，否则计算哈希
                if key.startswith('0x'):
                    key_int = int(key, 16)
                else:
                    key_int = gxt_hash(key)
                tkey_payload += struct.pack('II', offset, key_int)

        block = b'TKEY' + struct.pack('I', len(tkey_payload)) + tkey_payload
        block += b'TDAT' + struct.pack('I', len(tdat_payload)) + tdat_payload
        table_data_blocks.append(block)

    with open(output_file, 'wb') as gxt:
        if len(tables_names) > 1 or version.startswith('sa'):
            gxt.write(b'TABL')
            tabl_size = len(tables_names) * 12
            gxt.write(struct.pack('I', tabl_size))
            current_offset = 8 + tabl_size
            for i, name in enumerate(tables_names):
                name_bytes = name.encode('ascii')[:7].ljust(8, b'\x00')
                gxt.write(struct.pack('8sI', name_bytes, current_offset))
                current_offset += len(table_data_blocks[i])
        
        for block in table_data_blocks:
            gxt.write(block)

    print(f"成功打包！总大小: {os.path.getsize(output_file)} 字节")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python pack_gxt.py <输入文件夹> <版本: vc|sa|sa-mobile> <输出文件名.gxt>")
    else:
        pack_gxt(sys.argv[1], sys.argv[2], sys.argv[3])