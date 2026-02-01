import os
import sys

from VCGXT import VCGXT


def unpack_gxt(input_file, output_dir):
    builder = VCGXT()

    if not builder.LoadGXT(input_file):
        print("加载GXT失败")
        return

    if not builder.SaveAsTextDir(output_dir):
        print("保存文本失败")
        return

    print(f"成功解包到: {output_dir}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) < 1:
        print("用法: python unpack_gxt.py <输入文件.gxt> [输出目录]")
        sys.exit(1)

    input_file = args[0]
    out_dir = args[1] if len(args) > 1 else os.path.splitext(input_file)[0]
    unpack_gxt(input_file, out_dir)