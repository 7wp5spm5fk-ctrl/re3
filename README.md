# reVC

**Languages:** [English] | [中文 (Chinese)](docs/README.zh_CN.md)

<img src="res/images/logo.svg" width="128px"></img>

## Introduction

This repository makes the following changes to the original re3 repository:

- Removed canon build
- Added nix flake build and packaging
- Fixed workflows to make them work properly

For easy installation and running on NixOS, a Nix wrapper has been written in [re3-flake](https://github.com/gujial/re3-flake).

> The wrapper can automatically configure re3, reVC, reLCS, but you still need the original game files. By default, it uses Steam's default installation path to find the original game files (except for reLCS).

Compared to other branches, the reVC branch has made more changes:

- Built-in Chinese support
- Added related tools for unpacking, translating, and packing text
- Added tool for automatically generating character tables
- Added tool for generating Chinese font texture maps based on character tables and custom fonts
- Support for rendering Emoji
- Enabled Japanese and Polish settings options, but not yet fully implemented
- Modified the poster when exiting

The following tools/code were used during game modification, thanks to:

- Chinese text is based on the Unnamed Chinese patch (WMHHZ) 1.0 official version, modified, adapted and supplemented
- Chinese text rendering code comes from [Ova1122/Revc_Chs](https://github.com/Ova1122/Revc_Chs)
- Chinese mapping table generator `dat_generator` referred to the code of Unnamed Chinese group [WMHHZ/VC.SA.Plugin](https://github.com/WMHHZ/VC.SA.Plugin/blob/master/VCGXTBuilder/VCGXT.cpp)
- GXT file packing and unpacking tools used modules from [Lzh102938/III.VC.SAGXTExtracter](https://github.com/Lzh102938/III.VC.SAGXTExtracter/blob/main/builder/VCGXT.PY)
- Used [Magic.TXD](https://www.gtagarage.com/mods/show.php?id=27862) when packing Chinese character png files into txd files
- Used pillow and pilmoji modules to render Chinese character png files
- Used wqy-zenhei and tegaki_zatsu_normal as Chinese fonts. May be changed later.

Subsequent modifications will continue to focus on the miami branch.

## Installation

### For non-NixOS systems

Prepare the original game files, then find the required version archive in Actions, and copy all files to the original game folder.

### For NixOS and other systems using Nix package manager

Refer to [re3-flake](https://github.com/gujial/re3-flake) for installation, binaries have been uploaded to Nix Cache.

## Mods

Current compatibility is the same as the original reVC, may consider extending the script system in the future.

## Building from Source  

> Building with Nix Flakes is recommended. Wiki links need to be accessed through the Internet Archive.

When using premake, you may want to point GTA_VC_RE_DIR environment variable to GTA Vice City root folder if you want the executable to be moved there via post-build script.

Clone the repository with `git clone --recursive -b miami https://github.com/GTAmodding/re3.git reVC`. Then `cd reVC` into the cloned repository.

<details><summary>Linux</summary>

1. Ensure you have the required dependencies installed
2. Run premake to generate build files:
   ```bash
   ./premake5Linux --with-librw gmake2
   ```
3. Build the project (choose one):
   ```bash
   cd build
   make -j5 config=debug_linux-amd64-librw_gl3_glfw-oal     # Debug build
   make -j5 config=release_linux-amd64-librw_gl3_glfw-oal   # Release build
   ```

For detailed setup instructions, see: [Building on Linux](https://github.com/GTAmodding/re3/wiki/Building-on-Linux)

</details>

<details><summary>macOS</summary>

1. Ensure you have the required dependencies installed
2. Run premake to generate build files:
   ```bash
   premake5 --with-librw gmake2
   ```
3. Build the project (choose one):
   ```bash
   cd build
   make -j5 config=debug_macosx-amd64-librw_gl3_glfw-oal     # Debug build
   make -j5 config=release_macosx-amd64-librw_gl3_glfw-oal   # Release build
   ```

For detailed setup instructions, see: [Building on macOS](https://github.com/GTAmodding/re3/wiki/Building-on-MacOS)

</details>

<details><summary>Nix/NixOS</summary>

reVC provides a `flake.nix` for building with Nix. You have two options:

**Option 1: Build in a development shell:**
```bash
nix flake update  # Update flake inputs if needed
nix develop       # Enter development shell with all dependencies
# Then run the build commands as described in Linux section above
```

**Option 2: Build directly with Nix flakes:**
```bash
nix build .#re3-vc       # Build GTA Vice City (miami branch)
```

The built binaries will be in `./result/bin/`

</details>

### Quick Build Reference

**Linux Debug:**
```bash
./premake5Linux --with-librw gmake2 && cd build && make -j5 config=debug_linux-amd64-librw_gl3_glfw-oal verbose=1
```

**Linux Release:**
```bash
./premake5Linux --with-librw gmake2 && cd build && make -j5 config=release_linux-amd64-librw_gl3_glfw-oal verbose=1
```

**macOS Debug:**
```bash
premake5 --with-librw gmake2 && cd build && make -j5 config=debug_macosx-amd64-librw_gl3_glfw-oal verbose=1
```

**macOS Release:**
```bash
premake5 --with-librw gmake2 && cd build && make -j5 config=release_macosx-amd64-librw_gl3_glfw-oal verbose=1
```

### Build Options

> :information_source: premake has an `--with-lto` option if you want the project to be compiled with Link Time Optimization.

> :information_source: There are various settings in [config.h](https://github.com/GTAmodding/re3/tree/miami/src/core/config.h), you may want to take a look there.

> :information_source: reVC uses completely homebrew RenderWare-replacement rendering engine; [librw](https://github.com/aap/librw/). librw comes as submodule of re3, but you also can use LIBRW environment variable to specify path to your own librw.

If you feel the need, you can also use CodeWarrior 7 to compile reVC using the supplied codewarrior/reVC.mcp project - this requires the original RW34 libraries, and the DX8 SDK. The build is unstable compared to the MSVC builds though, and is mostly meant to serve as a reference.

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

## Contributing

This repository is dedicated to improving the original game experience and implementing cross-platform synchronization. It can also serve as a base version for modified games. Compared to the original re3 repository, the requirements for contributions are lower.

## License

Keeping the requirements of the original re3 repository, no license is used. The code is for educational, documentation and modification purposes only. Piracy and commercial use are not supported.

## Additional Documentation

- [Original Repository README](docs/README.origin.md)
- [Chinese Localization Workflow](docs/chs.zh_CN.md)
