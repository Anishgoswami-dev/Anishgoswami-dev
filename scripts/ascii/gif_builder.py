"""Generate assets/ascii/portrait.gif from ASCII text frames and terminal styling."""
import os
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORK = HERE / "_work"
ASCII = WORK / "ascii"
OUT = ROOT / "assets" / "ascii"

base_lines = (ASCII / "base-dark.txt").read_text(encoding="utf-8").split("\n")
while base_lines and not base_lines[0].strip():
    base_lines.pop(0)
while base_lines and not base_lines[-1].strip():
    base_lines.pop()

W, H = 616, 738
BG = (13, 17, 23)
TEXT_COLOR = (139, 148, 158)
CYAN = (34, 211, 238)
PURPLE = (167, 139, 250)
GREEN = (46, 160, 67)
BORDER = (48, 54, 61)
WHITE = (240, 246, 252)

# Try loading monospace font, fallback to default
font = None
font_sm = None
font_bold = None
try:
    font = ImageFont.truetype("consolas.ttf", 10)
    font_sm = ImageFont.truetype("consolas.ttf", 9)
    font_bold = ImageFont.truetype("consolab.ttf", 10)
except Exception:
    try:
        font = ImageFont.truetype("cour.ttf", 10)
        font_sm = font
        font_bold = font
    except Exception:
        font = ImageFont.load_default()
        font_sm = font
        font_bold = font

frames = []
num_frames = 20
rnd = random.Random(42)

for frame_idx in range(num_frames):
    im = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(im)

    # Window border & header
    draw.rounded_rectangle([1, 1, W - 2, H - 2], radius=14, outline=BORDER, width=1)
    
    # 3 dots
    draw.ellipse([16, 14, 26, 24], fill=(237, 106, 94))
    draw.ellipse([34, 14, 44, 24], fill=(245, 192, 60))
    draw.ellipse([52, 14, 62, 24], fill=(97, 197, 84))
    
    # Title
    draw.text((W // 2 - 80, 14), "anish@msit ~/portrait", fill=TEXT_COLOR, font=font_sm)
    
    # Right pill
    draw.ellipse([W - 110, 18, W - 104, 24], fill=GREEN)
    draw.text((W - 98, 14), "ASCII  LIVE", fill=TEXT_COLOR, font=font_sm)

    # Command line
    draw.text((20, 52), "anish@msit:~$", fill=CYAN, font=font_bold)
    draw.text((115, 52), "./render --portrait", fill=WHITE, font=font)

    # Progress bar
    draw.rounded_rectangle([20, 72, 160, 78], radius=3, fill=PURPLE)
    draw.text((170, 70), "100% decoding 2679 glyphs", fill=TEXT_COLOR, font=font_sm)

    # Radar in top right
    cx, cy, rad = W - 60, 130, 36
    draw.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], outline=(40, 50, 65), width=1)
    draw.ellipse([cx - rad // 2, cy - rad // 2, cx + rad // 2, cy + rad // 2], outline=(40, 50, 65), width=1)
    draw.line([cx - rad, cy, cx + rad, cy], fill=(40, 50, 65), width=1)
    draw.line([cx, cy - rad, cx, cy + rad], fill=(40, 50, 65), width=1)
    # radar sweep
    angle_offset = (frame_idx / num_frames) * 360
    import math
    rad_angle = math.radians(angle_offset)
    ex = cx + rad * math.cos(rad_angle)
    ey = cy + rad * math.sin(rad_angle)
    draw.line([cx, cy, ex, ey], fill=CYAN, width=1)
    draw.ellipse([cx + 12, cy - 8, cx + 16, cy - 4], fill=GREEN)

    # Frame scan line y-pos
    scan_y = 100 + int((frame_idx / num_frames) * (H - 220))

    # Draw ASCII lines
    y_start = 100
    line_h = 9.8
    char_w = 6.0
    
    for row_i, line in enumerate(base_lines):
        curr_y = y_start + row_i * line_h
        if curr_y > H - 100:
            break
            
        # Check if scanline touches this row
        is_scanned = abs(curr_y - scan_y) < 16
        
        for col_j, ch in enumerate(line):
            if ch == ' ':
                continue
            x_pos = 20 + col_j * char_w
            
            # shimmer random characters
            color = TEXT_COLOR
            if is_scanned:
                color = CYAN
            elif rnd.random() < 0.015:
                color = CYAN if rnd.random() < 0.7 else PURPLE
                
            draw.text((x_pos, curr_y), ch, fill=color, font=font)

    # Terminal bottom status
    draw.text((20, H - 54), "> identity verified: Anish Goswami", fill=CYAN, font=font_bold)
    
    # Bottom prompt + blinking cursor
    draw.text((20, H - 32), "anish@msit:~$", fill=TEXT_COLOR, font=font)
    if (frame_idx // 3) % 2 == 0:
        draw.rectangle([112, H - 32, 119, H - 20], fill=CYAN)

    frames.append(im)

# Save animated GIF
OUT.mkdir(parents=True, exist_ok=True)
gif_path = OUT / "portrait.gif"
frames[0].save(
    gif_path,
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0,
    optimize=True
)
print(f"Saved {gif_path} ({gif_path.stat().st_size / 1024:.1f} KB)")
