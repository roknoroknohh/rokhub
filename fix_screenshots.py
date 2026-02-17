import os

# استخدام لقطات شاشة حقيقية من المواقع (صور من Wikipedia/Wikimedia - مفتوحة المصدر)
with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# لقطات شاشة حقيقية من أرشيف الإنترنت أو صور توضيحية
new_sites = """GAME_SITES = [
    {
        'name': 'Y8 Games',
        'url': 'https://www.y8.com',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Y8.com_logo.png/800px-Y8.com_logo.png',
        'description': 'ألعاب فلاش وأونلاين مجانية',
        'color': '#ef4444'
    },
    {
        'name': 'Poki',
        'url': 'https://poki.com',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Poki_logo.png/800px-Poki_logo.png',
        'description': 'ألعاب مجانية للجميع',
        'color': '#22c55e'
    },
    {
        'name': 'Crazy Games',
        'url': 'https://www.crazygames.com',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Video_game_controller_icon_designed_by_Maico_Amorim.svg/1024px-Video_game_controller_icon_designed_by_Maico_Amorim.svg.png',
        'description': 'ألعاب مجنونة وممتعة',
        'color': '#a855f7'
    },
    {
        'name': 'Kizi',
        'url': 'https://kizi.com',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Video_game_development_icon.svg/1024px-Video_game_development_icon.svg.png',
        'description': 'ألعاب أطفال وعائلية',
        'color': '#3b82f6'
    },
    {
        'name': 'Friv',
        'url': 'https://www.friv.com',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Gamepad_icon.svg/1024px-Gamepad_icon.svg.png',
        'description': 'ألعاب بسيطة وسريعة',
        'color': '#f59e0b'
    }
]"""

# البحث عن GAME_SITES واستبدالها
import re
pattern = r'GAME_SITES = \[.*?\]'
if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, new_sites, content, flags=re.DOTALL)
    print("✅ تم تحديث GAME_SITES بالكامل")
else:
    print("⚠️ لم يتم العثور على GAME_SITES")

with open('config.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم حفظ config.py")
