# reVC-Improved

**Languages:** [English](README.md) | [中文 (Chinese)]

<img src="../res/images/logo.svg" width="128px"></img>

## 简介

本仓库在 re3 原仓库上做出以下改动：

- 移除了 canon 构建
- 增加了 nix flake 构建和打包
- 修复 workflows 使它们可以正常工作

为了方便在 NixOS 上安装和运行游戏，在 [re3-falke](https://github.com/gujial/re3-flake) 中编写了对应的 Nix 包装器。

> 包装器可以做到自动配置 re3、reVC、reLCS，但仍然需要有原版游戏文件，默认使用 Steam 的默认安装路径寻找原版游戏文件（除reLCS之外）。

相比其他分支，reVC 分支做出了更多改动：

- 内置的中文支持
- 添加了用于解包、翻译、打包文本的相关工具
- 添加了用于自动生成字符表的工具
- 添加了基于字符表和自定义字体生成中文字体贴图的工具
- 支持渲染 Emoji
- 启用了日文和波兰文的设置选项，但是并未实装
- 修改了退出时的海报
- 修复一些错误
   - wayland 下使用分数缩放比例时鼠标位置不正确
   - Linux 下无法删除存档
- 一些新功能
   - 在暂停菜单中保存游戏
   - 任务完成后自动保存存档到单独的自动保存槽位
   - 按下 `F10` 启用或关闭帧数限制
   - 减小第一人称鼠标灵敏度，倍率在设置中调整
   - 接听电话后再次按下跳过电话
- 一些改进
   - 统一水平和垂直灵敏度
   - 增加载具内自由视角跟随速度

> 在任务中或在载具中无法保存，自动保存会等待汤米离开载具后执行。

> 相比 reVC 分支，reVC-Improved 改动了游戏脚本文件 `main.scm`，不兼容原版存档。

修改游戏的过程中使用到了以下工具/代码，在此致谢：

- 中文文本基于无名汉化补丁 1.0 正式版修改、适配和补充
- 中文文字渲染代码来自 [Ova1122/Revc_Chs](https://github.com/Ova1122/Revc_Chs)
- 中文映射表生成器`dat_generator`实现时参考了无名汉化组 [WMHHZ/VC.SA.Plugin](https://github.com/WMHHZ/VC.SA.Plugin/blob/master/VCGXTBuilder/VCGXT.cpp) 的代码
- GXT 文件打包和解包工具实现时使用了 [Lzh102938/III.VC.SAGXTExtracter](https://github.com/Lzh102938/III.VC.SAGXTExtracter/blob/main/builder/VCGXT.PY) 的模块
- 将中文字符 png 文件打包为 txd 文件时使用了 [Magic.TXD](https://www.gtagarage.com/mods/show.php?id=27862)
- 渲染中文字符 png 文件使用了 pillow 和 pilmoji 模块
- 中文字体暂时使用的是 wqy-zenhei 和 tegaki_zatsu_normal，后续可能会调整

后续的修改依然集中于 miami 分支。

## 安装

### 非 Nixos 的情况

准备好原版游戏文件，之后在 Actions 中找到需要的版本压缩包，将全部文件覆盖到原版游戏文件夹。

### Nixos 和其他使用 Nix 软件包管理器的情况

参考 [re3-falke](https://github.com/gujial/re3-flake) 安装，二进制文件已上传至 Nix Cache。

## 模组

目前兼容情况与原版 reVC 相同，后续可能考虑扩展脚本系统。

## 从源代码构建  

> 推荐使用 Nix Flakes 构建。Wiki 链接需要通过互联网档案馆访问。

使用 premake 时，如果要将可执行文件通过后构建脚本移动到那里，您可能希望将 GTA_VC_RE_DIR 环境变量指向 GTA Vice City 根文件夹。

使用 `git clone --recursive -b miami https://github.com/GTAmodding/re3.git reVC` 克隆仓库。然后 `cd reVC` 进入克隆的仓库。

<details><summary>Linux</summary>

1. 确保已安装所需的依赖项
2. 运行 premake 以生成构建文件：
   ```bash
   ./premake5Linux --with-librw gmake2
   ```
3. 构建项目（选择其中之一）：
   ```bash
   cd build
   make -j5 config=debug_linux-amd64-librw_gl3_glfw-oal     # 调试构建
   make -j5 config=release_linux-amd64-librw_gl3_glfw-oal   # 发布构建
   ```

有关详细的设置说明，请参阅：[在 Linux 上构建](https://github.com/GTAmodding/re3/wiki/Building-on-Linux)

</details>

<details><summary>macOS</summary>

1. 确保已安装所需的依赖项
2. 运行 premake 以生成构建文件：
   ```bash
   premake5 --with-librw gmake2
   ```
3. 构建项目（选择其中之一）：
   ```bash
   cd build
   make -j5 config=debug_macosx-amd64-librw_gl3_glfw-oal     # 调试构建
   make -j5 config=release_macosx-amd64-librw_gl3_glfw-oal   # 发布构建
   ```

有关详细的设置说明，请参阅：[在 macOS 上构建](https://github.com/GTAmodding/re3/wiki/Building-on-MacOS)

</details>

<details><summary>Nix/NixOS</summary>

reVC 提供了 `flake.nix` 用于使用 Nix 进行构建。您有两个选项：

**选项 1：在开发 shell 中构建：**
```bash
nix flake update  # 如果需要，更新 flake 输入
nix develop       # 进入开发 shell，包含所有依赖项
# 然后运行上面 Linux 部分中描述的构建命令
```

**选项 2：直接使用 Nix flakes 构建：**
```bash
nix build .#re3-vc       # 构建 GTA Vice City（miami 分支）
```

构建的二进制文件将在 `./result/bin/` 中

</details>

### 快速构建参考

**Linux 调试版本：**
```bash
./premake5Linux --with-librw gmake2 && cd build && make -j5 config=debug_linux-amd64-librw_gl3_glfw-oal verbose=1
```

**Linux 发布版本：**
```bash
./premake5Linux --with-librw gmake2 && cd build && make -j5 config=release_linux-amd64-librw_gl3_glfw-oal verbose=1
```

**macOS 调试版本：**
```bash
premake5 --with-librw gmake2 && cd build && make -j5 config=debug_macosx-amd64-librw_gl3_glfw-oal verbose=1
```

**macOS 发布版本：**
```bash
premake5 --with-librw gmake2 && cd build && make -j5 config=release_macosx-amd64-librw_gl3_glfw-oal verbose=1
```

### 构建选项

> :information_source: premake 有一个 `--with-lto` 选项，如果您想用链接时优化编译项目。

> :information_source: [config.h](https://github.com/GTAmodding/re3/tree/miami/src/core/config.h) 中有各种设置，您可能想查看一下。

> :information_source: reVC 使用完全自制的 RenderWare 替代渲染引擎；[librw](https://github.com/aap/librw/)。librw 作为 re3 的子模块提供，但您也可以使用 LIBRW 环境变量来指定您自己的 librw 路径。

如果您愿意，您也可以使用 CodeWarrior 7 使用提供的 codewarrior/reVC.mcp 项目来编译 reVC - 这需要原始的 RW34 库和 DX8 SDK。与 MSVC 构建相比，此构建不稳定，主要用作参考。

## 贡献

本仓库致力于完善原版游戏体验，并实现多平台同步，也可作为改版游戏的基础版本，相比于原 re3 仓库对贡献的要求更低。

## 许可证

保留原 re3 仓库的要求，不使用许可证，代码仅用于教育、文档和修改目的，不支持盗版和商业使用。

## 文档补充

- [原仓库自述文件](./README.origin.md)
- [本地化工作流程](./localization.zh_CN.md)