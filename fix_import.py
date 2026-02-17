with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# إضافة Notification في الاستيراد من models
old_import = "from models import db, User, Game, Category, ContactMessage, GameSite, ErrorLog, SiteSettings"
new_import = "from models import db, User, Game, Category, ContactMessage, GameSite, ErrorLog, SiteSettings, Notification"

if old_import in content:
    content = content.replace(old_import, new_import)
    print("✅ تم إضافة Notification في الاستيراد")
else:
    print("⚠️ لم يتم العثور على سطر الاستيراد، سأبحث عن بديل...")
    # محاولة أخرى إذا كان السطر مختلفاً قليلاً
    if "from models import" in content and "Notification" not in content:
        content = content.replace(
            "from models import db, User, Game, Category, ContactMessage, GameSite, ErrorLog, SiteSettings",
            "from models import db, User, Game, Category, ContactMessage, GameSite, ErrorLog, SiteSettings, Notification"
        )
        print("✅ تم إضافة Notification في الاستيراد (الطريقة الثانية)")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم حفظ الملف")
