import os
import re

# تعديل app.py - إصلاح حفظ user_id في رسالة الدعم
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# البحث عن دالة support وإضافة حفظ user_id
old_support = '''@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        msg = ContactMessage(
            name=request.form.get('name', ''),
            email=request.form.get('email', ''),
            msg_type=request.form.get('type', 'support'),
            message=request.form.get('message', '')
        )'''

new_support = '''@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        msg = ContactMessage(
            name=request.form.get('name', ''),
            email=request.form.get('email', ''),
            msg_type=request.form.get('type', 'support'),
            message=request.form.get('message', ''),
            user_id=current_user.id if current_user.is_authenticated else None
        )'''

if old_support in content:
    content = content.replace(old_support, new_support)
    print("✅ تم إصلاح حفظ user_id في رسائل الدعم")
else:
    print("⚠️ لم يتم العثور على الكود القديم")

# تعديل دالة الرد لإرسال إشعار للمستخدم
old_reply = '''@app.route('/admin/message/<int:msg_id>/reply', methods=['POST'])
@login_required
def admin_reply_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.admin_reply = request.form.get('reply')
    msg.is_resolved = True
    msg.resolved_at = datetime.utcnow()
    msg.resolved_by = current_user.id
    db.session.commit()
    flash('تم الرد', 'success')
    return redirect(url_for('admin_messages'))'''

new_reply = '''@app.route('/admin/message/<int:msg_id>/reply', methods=['POST'])
@login_required
def admin_reply_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    reply_text = request.form.get('reply')
    msg.admin_reply = reply_text
    msg.is_resolved = True
    msg.resolved_at = datetime.utcnow()
    msg.resolved_by = current_user.id
    db.session.commit()
    
    # إرسال إشعار للمستخدم إذا كان مسجل دخول
    if msg.user_id:
        from flask import render_template_string
        notification = Notification(
            user_id=msg.user_id,
            title='رد جديد على رسالتك',
            message=f'تم الرد على رسالتك: {reply_text[:50]}...',
            link='/user/messages'
        )
        db.session.add(notification)
        db.session.commit()
    
    flash('تم الرد وإرسال الإشعار للمستخدم', 'success')
    return redirect(url_for('admin_messages'))'''

if old_reply in content:
    content = content.replace(old_reply, new_reply)
    print("✅ تم إضافة نظام الإشعارات للردود")
else:
    print("⚠️ لم يتم العثور على دالة الرد القديمة")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم تحديث app.py")
