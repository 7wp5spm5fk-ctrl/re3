# 本地化（汉化）工作流程

## utils 工具说明

以下工具位于 `utils/`，用于处理中文字体/文本资源。

### utils/dat - Chinese.dat 与字符表生成

- `dat_generator.py`：从 GXT 文本（单个 `.txt` 或目录）提取字符集，生成 `Chinese.dat` 与 `CHARACTERS.txt`。
- `build.sh`：批量生成到 `gamefiles/` 与 `local_gamefiles/`。

示例：

```bash
python utils/dat/dat_generator.py utils/gxt/chinese --table gamefiles/data/Chinese.dat --characters utils/dat/CHARACTERS.txt
```

### utils/fonts - 字体贴图生成

- `png_generator.py`：读取 `CHARACTERS.txt`，生成 4096x4096 的 `normal.png` 与 `slant.png`（64x64 网格）。
- 依赖：`pillow`，可选 `pilmoji`（用于 emoji 渲染），见 `requirements.txt`。

示例：

```bash
python -m pip install -r utils/fonts/requirements.txt
python utils/fonts/png_generator.py --characters utils/dat/CHARACTERS.txt --output-dir utils/fonts
```

可选参数：`--normal-font` / `--slant-font` 用于指定自定义字体文件。

### utils/gxt - 文本打包/解包与翻译辅助

- `pack_gxt.py`：将 `utils/gxt/chinese` 或 `utils/gxt/american` 目录打包为 `.gxt`（目前仅支持 VC）。
- `unpack_gxt.py`：将 `.gxt` 解包为文本目录。
- `compare_translations.py`：对比 `american/` 与 `chinese/`，输出 `missing_translations.txt` 与 `extra_translations.txt`。
- `apply_translation_diffs.py`：将缺失/多余条目回写到对应目录并排序。
- `build.sh`：将中文与英文打包到 `gamefiles/` 与 `local_gamefiles/`。
- `build_native.bat`：Windows 下使用 `gxt` 工具从 `native/` 文本生成其他语言的 `.gxt`。

示例：

```bash
python utils/gxt/pack_gxt.py utils/gxt/chinese vc gamefiles/TEXT/chinese.gxt
python utils/gxt/unpack_gxt.py gamefiles/TEXT/chinese.gxt utils/gxt/chinese
python utils/gxt/compare_translations.py
python utils/gxt/apply_translation_diffs.py
```

## 步骤

> 代码中已经实现了通过 dat 文件映射中文字符和渲染中文字符的逻辑。

1. 切换目录到 `utils/gxt/` 编辑 `chinese` 中的汉化文本。
2. 运行 `compare_translations.py` 对照中英文的翻译键查找缺失和多余的翻译。
3. 在 `missing_translations.txt` 与 `extra_translations.txt` 中编辑需要补充到中文或英文的翻译，之后运行 `apply_translation_diffs.py` 插入这些翻译，插入时会自动按字典顺序排序。
4. 运行 `./build.sh` 将处理后的文本打包为 gxt 文件并输出到 `gamefiles/` 中。
5. 切换工作目录到 `uitls/dat`，并运行 `./build.sh`，生成字符映射表 dat 文件到 `gamefiles/` 中，并生成对应的纯文本版本 txt 文件。
6. 切换工作目录到 `utils/fonts`，准备好需要的字体，运行 `requirements.txt` 中的依赖，并运行 `png_generator.py` 生成中文字符 png 图。
7. 使用 Magic.TXD 将中文字符 png 图打包为 txd 文件并安装到游戏文件中。