#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os

def create_image(filename, text, bg_color, text_color, icon_text="", size=(400, 300)):
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # رسم خلفية متدرجة
    for y in range(size[1]):
        r = int(bg_color[0] * (1 - y/size[1]*0.3))
        g = int(bg_color[1] * (1 - y/size[1]*0.3))
        b = int(bg_color[2] * (1 - y/size[1]*0.3))
        draw.line([(0, y), (size[0], y)], fill=(r, g, b))
    
    # رسم أيقونة
    if icon_text:
        try:
            icon_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        except:
            icon_font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), icon_text, font=icon_font)
        icon_x = (size[0] - (bbox[2] - bbox[0])) // 2
        icon_y = 40
        draw.text((icon_x, icon_y), icon_text, fill=text_color, font=icon_font)
    
    # رسم نص
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_x = (size[0] - (bbox[2] - bbox[0])) // 2
    text_y = 160
    
    # ظل للنص
    draw.text((text_x+2, text_y+2), text, fill=(0,0,0,128), font=font)
    draw.text((text_x, text_y), text, fill=text_color, font=font)
    
    img.save(filename, 'PNG')
    print(f"✅ Created: {filename}")

# إنشاء جميع الصور
create_image('y8-games.png', 'Y8 GAMES', (239, 68, 68), (255, 255, 255), '🎮')
create_image('poki.png', 'POKI', (34, 197, 94), (255, 255, 255), '🎯')
create_image('crazy-games.png', 'CRAZY GAMES', (168, 85, 247), (255, 255, 255), '🤪')
create_image('kizi.png', 'KIZI', (59, 130, 246), (255, 255, 255), '🚀')
create_image('friv.png', 'FRIV', (245, 158, 11), (255, 255, 255), '🌟')
create_image('game-placeholder.png', 'GAME', (30, 41, 59), (148, 163, 184), '🎲')
create_image('og-image.png', 'ROKhub', (59, 130, 246), (255, 255, 255), '🎮', (1200, 630))

print("\\n✅ All images created successfully!")
