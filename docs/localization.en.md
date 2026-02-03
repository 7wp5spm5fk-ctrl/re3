# Localization (Chinese) Workflow

## Utils Tools Documentation

The following tools are located in `utils/` for handling Chinese font/text resources.

### utils/dat - Chinese.dat and Character Table Generation

- `dat_generator.py`: Extracts character sets from GXT text (single `.txt` or directory), generates `Chinese.dat` and `CHARACTERS.txt`.
- `build.sh`: Batch generation to `gamefiles/` and `local_gamefiles/`.

Example:

```bash
python utils/dat/dat_generator.py utils/gxt/chinese --table gamefiles/data/Chinese.dat --characters utils/dat/CHARACTERS.txt
```

### utils/fonts - Font Texture Generation

- `png_generator.py`: Reads `CHARACTERS.txt`, generates 4096x4096 `normal.png` and `slant.png` (64x64 grid).
- Dependencies: `pillow`, optional `pilmoji` (for emoji rendering), see `requirements.txt`.

Example:

```bash
python -m pip install -r utils/fonts/requirements.txt
python utils/fonts/png_generator.py --characters utils/dat/CHARACTERS.txt --output-dir utils/fonts
```

Optional parameters: `--normal-font` / `--slant-font` for specifying custom font files.

### utils/gxt - Text Packing/Unpacking and Translation Assistance

- `pack_gxt.py`: Packs `utils/gxt/chinese` or `utils/gxt/american` directory into `.gxt` (currently only supports VC).
- `unpack_gxt.py`: Unpacks `.gxt` into text directory.
- `compare_translations.py`: Compares `american/` and `chinese/`, outputs `missing_translations.txt` and `extra_translations.txt`.
- `apply_translation_diffs.py`: Writes missing/extra entries back to corresponding directories and sorts them.
- `build.sh`: Packs Chinese and English to `gamefiles/` and `local_gamefiles/`.
- `build_native.bat`: Uses `gxt` tool on Windows to generate `.gxt` files for other languages from `native/` text.

Example:

```bash
python utils/gxt/pack_gxt.py utils/gxt/chinese vc gamefiles/TEXT/chinese.gxt
python utils/gxt/unpack_gxt.py gamefiles/TEXT/chinese.gxt utils/gxt/chinese
python utils/gxt/compare_translations.py
python utils/gxt/apply_translation_diffs.py
```

## Steps

> The code already implements logic for mapping Chinese characters and rendering them through dat files.

1. Change directory to `utils/gxt/` and edit the Chinese translation text in the `chinese` directory.
2. Run `compare_translations.py` to check the translation keys between English and Chinese, identifying missing and extra translations.
3. Edit the translations that need to be added to Chinese or English in `missing_translations.txt` and `extra_translations.txt`, then run `apply_translation_diffs.py` to insert these translations. They will be automatically sorted in dictionary order during insertion.
4. Run `./build.sh` to pack the processed text into gxt files and output to `gamefiles/`.
5. Change working directory to `utils/dat` and run `./build.sh` to generate the character mapping dat files to `gamefiles/` and generate the corresponding plain text version txt file.
6. Change working directory to `utils/fonts`, prepare the required fonts, install the dependencies from `requirements.txt`, and run `png_generator.py` to generate Chinese character png images.
7. Use Magic.TXD to pack the Chinese character png images into a txd file and install it into the game files.
