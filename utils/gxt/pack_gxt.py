import os
import sys

from VCGXT import VCGXT


def pack_gxt(input_dir, version, output_file):
    if version != 'vc':
        print("当前仅支持vc版本（VCGXT）")
        return

    builder = VCGXT()
    if not builder.LoadTextDir(input_dir):
        print("加载文本文件失败")
        return

    if not builder.SaveAsGXT(output_file):
        print("保存GXT失败")
        return

    print(f"成功打包！总大小: {os.path.getsize(output_file)} 字节")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python pack_gxt.py <输入文件夹> <版本: vc|sa|sa-mobile> <输出文件名.gxt>")
    else:
        pack_gxt(sys.argv[1], sys.argv[2], sys.argv[3])