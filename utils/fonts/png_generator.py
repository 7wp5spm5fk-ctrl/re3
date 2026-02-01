# -*- coding: utf-8 -*-
"""
PNG generator for Chinese characters with Font Fallback and Slant support.
Uses Pilmoji for emoji rendering.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional, List

from PIL import Image, ImageDraw, ImageFont

try:
    from pilmoji import Pilmoji
    HAS_PILMOJI = True
except ImportError:
    HAS_PILMOJI = False
    print("Warning: pilmoji not installed. Install with: pip install pilmoji")


# Image configuration
IMAGE_SIZE = 4096
GRID_SIZE = 64
CHAR_SIZE = IMAGE_SIZE // GRID_SIZE  # 64x64 pixels per character

# Font size as percentage of cell size
FONT_SIZE_RATIO = 0.80 


class FallbackFont:
    """字体管理器：用于非emoji字符渲染。"""
    # Emoji Unicode范围
    EMOJI_RANGES = [
        (0x1F300, 0x1F9FF),  # 各种emoji
        (0x1F000, 0x1F02F),  # 麻将、骰子等
        (0x2600, 0x27BF),    # 符号和图形
        (0x1F600, 0x1F64F),  # 表情符号
        (0x1F900, 0x1F9FF),  # 补充emoji
    ]
    
    def __init__(self, font_paths: List[Path], size: int):
        self.fonts = []
        self.main_font = None
        
        for path in font_paths:
            if path and path.exists() and 'emoji' not in str(path).lower():
                try:
                    f = ImageFont.truetype(str(path), size=size)
                    self.fonts.append(f)
                    if self.main_font is None:
                        self.main_font = f
                    print(f"Loaded font: {path}")
                except Exception as e:
                    print(f"Warning: Failed to load font {path}: {e}")
            elif path and path.exists():
                print(f"Skipping emoji font: {path} (will use Pilmoji)")
            else:
                print(f"Font not found: {path}")
        
        if not self.fonts:
            print("Warning: No fonts loaded, using PIL default font.")
            self.fonts.append(ImageFont.load_default())
            self.main_font = self.fonts[0]

    def is_emoji_char(self, char: str) -> bool:
        """检查字符是否在emoji Unicode范围内。"""
        code_point = ord(char)
        return any(start <= code_point <= end for start, end in self.EMOJI_RANGES)

    def get_font_for_char(self, char: str):
        """为非emoji字符获取合适的字体。"""
        if not char or char.isspace():
            return self.main_font
        
        # 非emoji字符使用主字体
        return self.main_font


def read_characters(char_file: Path) -> list[str]:
    """读取字符文件，支持 UTF-16LE BOM 和 UTF-8。"""
    if not char_file.exists():
        raise FileNotFoundError(f"Character file not found: {char_file}")
        
    with open(char_file, "rb") as f:
        head = f.read(2)
        if head == b"\xFF\xFE":
            content = f.read().decode("utf-16le")
        else:
            content = (head + f.read()).decode("utf-8", errors="ignore")
    
    characters = []
    for line in content.splitlines():
        for ch in line:
            if ch and ch != "\r":
                characters.append(ch)
                if len(characters) >= GRID_SIZE * GRID_SIZE:
                    return characters
    return characters


def generate_png(
    characters: list[str],
    output_path: Path,
    font_paths: List[Path],
) -> None:
    """在 64x64 网格中生成 PNG。使用Pilmoji渲染emoji。"""
    img = Image.new("RGBA", (IMAGE_SIZE, IMAGE_SIZE), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    font_size = int(CHAR_SIZE * FONT_SIZE_RATIO)
    fallback_mgr = FallbackFont(font_paths, font_size)
    
    print(f"Generating {output_path.name}...")
    print(f"Using main font: {fallback_mgr.main_font}")
    print(f"Pilmoji available: {HAS_PILMOJI}")
    
    emoji_count = 0
    char_count = 0
    
    # 创建Pilmoji实例用于emoji渲染
    emoji_renderer = None
    if HAS_PILMOJI:
        emoji_renderer = Pilmoji(img)
    
    for idx, ch in enumerate(characters):
        if idx >= GRID_SIZE * GRID_SIZE:
            break
        
        row = idx // GRID_SIZE
        col = idx % GRID_SIZE
        cell_x = col * CHAR_SIZE
        cell_y = row * CHAR_SIZE
        
        if ch.isspace():
            continue

        char_count += 1
        is_emoji = fallback_mgr.is_emoji_char(ch)
        
        try:
            if is_emoji and emoji_renderer:
                # 使用Pilmoji渲染emoji，增大尺寸并居中
                emoji_scale = 5  # 增大缩放因子以显示更大的emoji
                emoji_offset = 8
                
                emoji_renderer.text(
                    (cell_x + emoji_offset, cell_y),
                    ch,
                    fill=(255, 255, 255, 255),
                    emoji_scale_factor=emoji_scale
                )
                emoji_count += 1
            else:
                # 使用常规字体渲染非emoji字符
                font = fallback_mgr.get_font_for_char(ch)
                
                # 精确计算居中位置
                bbox = draw.textbbox((0, 0), ch, font=font)
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                
                draw_x = cell_x + (CHAR_SIZE - w) // 2 - bbox[0]
                draw_y = cell_y + (CHAR_SIZE - h) // 2 - bbox[1]
                
                draw.text((draw_x, draw_y), ch, fill=(255, 255, 255, 255), font=font)
        except Exception as e:
            print(f"Warning: Failed to render character {repr(ch)}: {e}")
            continue

    img.save(output_path, "PNG")
    print(f"Saved to {output_path} (Total: {char_count} chars, Emoji: {emoji_count})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Font Atlas Generator (Normal & Slant) with Pilmoji")
    parser.add_argument("--characters", default="../dat/CHARACTERS.txt", help="Path to characters file")
    parser.add_argument("--normal-font", help="Main font for normal.png")
    parser.add_argument("--slant-font", help="Main font for slant.png")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    
    args = parser.parse_args()
    
    char_path = Path(args.characters)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        characters = read_characters(char_path)
    except Exception as e:
        print(f"Error reading characters: {e}")
        return

    print(f"Loaded {len(characters)} characters.")
    
    # 填充至网格大小
    while len(characters) < GRID_SIZE * GRID_SIZE:
        characters.append(" ")

    # --- 生成 normal.png ---
    normal_main = Path(args.normal_font) if args.normal_font else Path("wqy-zenhei.ttc")
    normal_fonts = [normal_main] if normal_main else []
    generate_png(characters, output_dir / "normal.png", normal_fonts)
    
    # --- 生成 slant.png ---
    slant_main = Path(args.slant_font) if args.slant_font else Path("tegaki_zatsu_normal.ttf")
    slant_fonts = [slant_main] if slant_main else []
    generate_png(characters, output_dir / "slant.png", slant_fonts)


if __name__ == "__main__":
    main()