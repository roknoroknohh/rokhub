with open('utils.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تحديث init_database لاستخدام الصور من GAME_SITES
old_init = """if not GameSite.query.first():
        sites = [
            GameSite(name='Y8 Games', url='https://www.y8.com',
                     image_url='/static/images/y8-games.png',
                     description='ألعاب فلاش وأونلاين مجانية', sort_order=1),
            GameSite(name='Poki', url='https://poki.com',
                     image_url='/static/images/poki.png',
                     description='ألعاب مجانية للجميع', sort_order=2)
        ]"""

new_init = """if not GameSite.query.first():
        from config import GAME_SITES
        sites = []
        for idx, site_data in enumerate(GAME_SITES[:5], 1):
            sites.append(GameSite(
                name=site_data['name'],
                url=site_data['url'],
                image_url=site_data.get('image', ''),
                description=site_data.get('description', ''),
                sort_order=idx
            ))"""

if old_init in content:
    content = content.replace(old_init, new_init)
    print("✅ تم تحديث init_database لاستخدام الصور من GAME_SITES")
else:
    print("⚠️ لم يتم العثور على الكود القديم")
    # محاولة استبدال عام
    content = content.replace("image_url='/static/images/y8-games.png'", "image_url='https://img.y8.com/assets/y8-logo-95e27c6c8a7c11867eb3e20d52f0d7a3.png'")
    content = content.replace("image_url='/static/images/poki.png'", "image_url='https://poki.com/assets/images/poki-logo.png'")
    print("✅ تم تحديث الصور مباشرة")

with open('utils.py', 'w', encoding='utf-8') as f:
    f.write(content)
