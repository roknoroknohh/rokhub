import os

# البحث عن index.html
index_path = 'templates/index.html'
if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # إضافة Font Awesome إذا لم يكن موجوداً
    if 'font-awesome' not in content and 'fontawesome' not in content:
        content = content.replace('</head>', '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n</head>')
        print("✅ تم إضافة Font Awesome")
    
    # تحديث عرض الفئات لاستخدام الأيقونات الاحترافية
    # هذا يعتمد على كيفية عرض الفئات في قالبك الحالي
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ تم تحديث index.html")
else:
    print("⚠️ لم يتم العثور على index.html")
