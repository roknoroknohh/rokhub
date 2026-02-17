import os

# استخدام صور من مصادر موثوقة تعمل بالفعل
with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# استبدال بصور من ويكيبيديا/مصادر مفتوحة تعمل
old_sites = """GAME_SITES = [
    {
        'name': 'Y8 Games',
        'url': 'https://www.y8.com',
        'image': 'https://img.y8.com/assets/y8-logo-95e27c6c8a7c11867eb3e20d52f0d7a3.png',
        'description': 'ألعاب فلاش وأونلاين مجانية',
        'color': '#ef4444'
    },
    {
        'name': 'Poki',
        'url': 'https://poki.com',
        'image': 'https://poki.com/assets/images/poki-logo.png',
        'description': 'ألعاب مجانية للجميع',
        'color': '#22c55e'
    },
    {
        'name': 'Crazy Games',
        'url': 'https://www.crazygames.com',
        'image': 'https://images.crazygames.com/crazygames-logo.png',
        'description': 'ألعاب مجنونة وممتعة',
        'color': '#a855f7'
    },
    {
        'name': 'Kizi',
        'url': 'https://kizi.com',
        'image': 'https://kizi.com/assets/images/kizi-logo.png',
        'description': 'ألعاب أطفال وعائلية',
        'color': '#3b82f6'
    },
    {
        'name': 'Friv',
        'url': 'https://www.friv.com',
        'image': 'https://www.friv.com/images/friv-logo.png',
        'description': 'ألعاب بسيطة وسريعة',
        'color': '#f59e0b'
    }
]"""

# استخدام صور من Unsplash (صور مجانية مضمونة)
new_sites = """GAME_SITES = [
    {
        'name': 'Y8 Games',
        'url': 'https://www.y8.com',
        'image': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=200&fit=crop',
        'description': 'ألعاب فلاش وأونلاين مجانية',
        'color': '#ef4444'
    },
    {
        'name': 'Poki',
        'url': 'https://poki.com',
        'image': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400&h=200&fit=crop',
        'description': 'ألعاب مجانية للجميع',
        'color': '#22c55e'
    },
    {
        'name': 'Crazy Games',
        'url': 'https://www.crazygames.com',
        'image': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400&h=200&fit=crop',
        'description': 'ألعاب مجنونة وممتعة',
        'color': '#a855f7'
    },
    {
        'name': 'Kizi',
        'url': 'https://kizi.com',
        'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=200&fit=crop',
        'description': 'ألعاب أطفال وعائلية',
        'color': '#3b82f6'
    },
    {
        'name': 'Friv',
        'url': 'https://www.friv.com',
        'image': 'https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?w=400&h=200&fit=crop',
        'description': 'ألعاب بسيطة وسريعة',
        'color': '#f59e0b'
    }
]"""

if old_sites in content:
    content = content.replace(old_sites, new_sites)
else:
    # استبدال أي روابط صور أخرى
    content = content.replace(
        "'image': 'https://img.y8.com/assets/y8-logo-95e27c6c8a7c11867eb3e20d52f0d7a3.png'",
        "'image': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=200&fit=crop'"
    )
    content = content.replace(
        "'image': 'https://poki.com/assets/images/poki-logo.png'",
        "'image': 'https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400&h=200&fit=crop'"
    )
    content = content.replace(
        "'image': 'https://images.crazygames.com/crazygames-logo.png'",
        "'image': 'https://images.unsplash.com/photo-1538481199705-c710c4e965fc?w=400&h=200&fit=crop'"
    )
    content = content.replace(
        "'image': 'https://kizi.com/assets/images/kizi-logo.png'",
        "'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=200&fit=crop'"
    )
    content = content.replace(
        "'image': 'https://www.friv.com/images/friv-logo.png'",
        "'image': 'https://images.unsplash.com/photo-1493711662062-fa541adb3fc8?w=400&h=200&fit=crop'"
    )

with open('config.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم تحديث الصور إلى صور Unsplash تعمل")
