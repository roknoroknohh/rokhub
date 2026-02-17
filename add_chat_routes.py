with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# إضافة استيراد ChatMessage
old_import = "from models import db, User, Game, Category, ContactMessage, GameSite, ErrorLog, SiteSettings, Notification"
new_import = "from models import db, User, Game, Category, ContactMessage, GameSite, ErrorLog, SiteSettings, Notification, ChatMessage"

if old_import in content:
    content = content.replace(old_import, new_import)
    print("✅ تم إضافة ChatMessage في الاستيراد")

# إضافة routes للمحادثة
chat_routes = '''

@app.route('/user/message/<int:msg_id>/reply', methods=['POST'])
@login_required
def user_reply_to_admin(msg_id):
    """المستخدم يرد على رسالة الأدمن"""
    msg = ContactMessage.query.get_or_404(msg_id)
    
    # التحقق أن الرسالة للمستخدم الحالي
    if msg.user_id != current_user.id:
        flash('غير مصرح', 'danger')
        return redirect(url_for('index'))
    
    reply_text = request.form.get('reply', '').strip()
    if reply_text:
        chat_msg = ChatMessage(
            contact_message_id=msg.id,
            sender_id=current_user.id,
            sender_type='user',
            message=reply_text
        )
        db.session.add(chat_msg)
        
        # إعادة فتح الرسالة إذا كانت مغلقة
        msg.is_resolved = False
        
        db.session.commit()
        flash('تم إرسال ردك', 'success')
    
    return redirect(url_for('user_chat', msg_id=msg.id))

@app.route('/user/chat/<int:msg_id>')
@login_required
def user_chat(msg_id):
    """صفحة المحادثة الكاملة"""
    msg = ContactMessage.query.get_or_404(msg_id)
    
    if msg.user_id != current_user.id:
        flash('غير مصرح', 'danger')
        return redirect(url_for('index'))
    
    # جلب جميع رسائل المحادثة
    messages = ChatMessage.query.filter_by(contact_message_id=msg.id).order_by(ChatMessage.created_at.asc()).all()
    
    # تحديث حالة القراءة
    for m in messages:
        if m.sender_type == 'admin' and not m.is_read:
            m.is_read = True
    db.session.commit()
    
    return render_template('user/chat.html', contact_msg=msg, messages=messages)

@app.route('/admin/chat/<int:msg_id>')
@login_required
def admin_chat_view(msg_id):
    """الأدمن يرى المحادثة كاملة"""
    msg = ContactMessage.query.get_or_404(msg_id)
    messages = ChatMessage.query.filter_by(contact_message_id=msg.id).order_by(ChatMessage.created_at.asc()).all()
    
    # تحديث حالة القراءة
    for m in messages:
        if m.sender_type == 'user' and not m.is_read:
            m.is_read = True
    db.session.commit()
    
    return render_template('admin/chat_view.html', contact_msg=msg, messages=messages)

@app.route('/admin/chat/<int:msg_id>/reply', methods=['POST'])
@login_required
def admin_chat_reply(msg_id):
    """الأدمن يرد في المحادثة"""
    msg = ContactMessage.query.get_or_404(msg_id)
    
    reply_text = request.form.get('reply', '').strip()
    if reply_text:
        chat_msg = ChatMessage(
            contact_message_id=msg.id,
            sender_id=current_user.id,
            sender_type='admin',
            message=reply_text
        )
        db.session.add(chat_msg)
        db.session.commit()
        
        # إشعار للمستخدم
        flash('تم إرسال ردك', 'success')
    
    return redirect(url_for('admin_chat_view', msg_id=msg.id))
'''

if "user_reply_to_admin" not in content:
    content = content.replace("if __name__ == '__main__':", chat_routes + "\n\nif __name__ == '__main__':")
    print("✅ تم إضافة routes المحادثة")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
