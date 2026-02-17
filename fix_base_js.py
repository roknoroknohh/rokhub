with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# إضافة ملف الإشعارات قبل إغلاق body
if 'notifications.js' not in content:
    content = content.replace(
        '</body>',
        '<script src="{{ url_for(\'static\', filename=\'js/notifications.js\') }}"></script>\n</body>'
    )
    print("✅ تم ربط notifications.js")

# إضافة متغير لتحديد حالة تسجيل الدخول في body
if "data-user-authenticated" not in content:
    content = content.replace(
        '<body',
        '<body data-user-authenticated="{{ \'true\' if current_user.is_authenticated else \'false\' }}"'
    )
    print("✅ تم إضافة حالة تسجيل الدخول للـ body")

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
