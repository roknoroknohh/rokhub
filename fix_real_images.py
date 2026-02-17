import os

# تحديث config.py لاستخدام روابط صور حقيقية من الإنترنت
with open('config.py', 'r', encoding='utf-8') as f:
    content = f.read()

# استبدال صور PNG/SVG بروابط صور حقيقية من الإنترنت
old_sites = """GAME_SITES = [
    {
        'name': 'Y8 Games',
        'url': 'https://www.y8.com',
        'image': '/static/images/y8-games.png',
        'description': 'ألعاب فلاش وأونلاين مجانية',
        'color': '#ef4444'
    },
    {
        'name': 'Poki',
        'url': 'https://poki.com',
        'image': '/static/images/poki.png',
        'description': 'ألعاب مجانية للجميع',
        'color': '#22c55e'
    },
    {
        'name': 'Crazy Games',
        'url': 'https://www.crazygames.com',
        'image': '/static/images/crazy-games.png',
        'description': 'ألعاب مجنونة وممتعة',
        'color': '#a855f7'
    },
    {
        'name': 'Kizi',
        'url': 'https://kizi.com',
        'image': '/static/images/kizi.png',
        'description': 'ألعاب أطفال وعائلية',
        'color': '#3b82f6'
    },
    {
        'name': 'Friv',
        'url': 'https://www.friv.com',
        'image': '/static/images/friv.png',
        'description': 'ألعاب بسيطة وسريعة',
        'color': '#f59e0b'
    }
]"""

new_sites = """GAME_SITES = [
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

if old_sites in content:
    content = content.replace(old_sites, new_sites)
    print("✅ تم تحديث روابط الصور إلى صور حقيقية")
else:
    print("⚠️ لم يتم العثور على الكود القديم، سأحاول طريقة أخرى...")
    # محاولة استبدال عام
    content = content.replace("'image': '/static/images/y8-games.png'", "'image': 'https://img.y8.com/assets/y8-logo-95e27c6c8a7c11867eb3e20d52f0d7a3.png'")
    content = content.replace("'image': '/static/images/poki.png'", "'image': 'https://poki.com/assets/images/poki-logo.png'")
    content = content.replace("'image': '/static/images/crazy-games.png'", "'image': 'https://images.crazygames.com/crazygames-logo.png'")
    content = content.replace("'image': '/static/images/kizi.png'", "'image': 'https://kizi.com/assets/images/kizi-logo.png'")
    content = content.replace("'image': '/static/images/friv.png'", "'image': 'https://www.friv.com/images/friv-logo.png'")
    content = content.replace("'image': '/static/images/y8-games.svg'", "'image': 'https://img.y8.com/assets/y8-logo-95e27c6c8a7c11867eb3e20d52f0d7a3.png'")
    content = content.replace("'image': '/static/images/poki.svg'", "'image': 'https://poki.com/assets/images/poki-logo.png'")
    content = content.replace("'image': '/static/images/crazy-games.svg'", "'image': 'https://images.crazygames.com/crazygames-logo.png'")
    content = content.replace("'image': '/static/images/kizi.svg'", "'image': 'https://kizi.com/assets/images/kizi-logo.png'")
    content = content.replace("'image': '/static/images/friv.svg'", "'image': 'https://www.friv.com/images/friv-logo.png'")
    print("✅ تم تحديث روابط الصور (الطريقة الثانية)")

with open('config.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم حفظ config.py")
