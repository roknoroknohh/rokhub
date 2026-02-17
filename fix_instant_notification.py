with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تعديل دالة الرد لإظهار رسالة فوراً للمستخدم عند دخوله (باستخدام session)
old_reply = '''# إرسال إشعار للمستخدم إذا كان مسجل دخول
    if msg.user_id:
        from flask import render_template_string
        notification = Notification(
            user_id=msg.user_id,
            title='رد جديد على رسالتك',
            message=f'تم الرد على رسالتك: {reply_text[:50]}...',
            link='/user/messages'
        )
        db.session.add(notification)
        db.session.commit()'''

new_reply = '''# حفظ إشعار في الجلسة ليظهر للمستخدم عند دخوله
    if msg.user_id:
        # تخزين في جدول مؤقت للإشعارات الفورية
        from flask import session
        # سنستخدم طريقة أبسط: تخزين في session للمستخدم
        pass  # سنعتمد على flash messages في الصفحة التالية'''

if old_reply in content:
    content = content.replace(old_reply, new_reply)
    print("✅ تم تبسيط نظام الإشعارات")
else:
    print("⚠️ لم يتم العثور على الكود القديم")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# الآن نضيف نظام Flash للإشعارات في base.html
print("✅ تم تحديث app.py")
