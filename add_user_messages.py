# إضافة route لصفحة رسائل المستخدم
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_route = '''

@app.route('/user/messages')
@login_required
def user_messages():
    """صفحة رسائل المستخدم وردود الأدمن"""
    messages = ContactMessage.query.filter_by(user_id=current_user.id).order_by(ContactMessage.created_at.desc()).all()
    # تحديث حالة القراءة للإشعارات
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    return render_template('user/messages.html', messages=messages)

@app.route('/notification/<int:notif_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notif_id):
    """تحديث حالة الإشعار كمقروء"""
    notif = Notification.query.get_or_404(notif_id)
    if notif.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    notif.is_read = True
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/notifications')
@login_required
def get_notifications():
    """جلب الإشعارات غير المقروءة"""
    notifs = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).all()
    return jsonify([{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'link': n.link,
        'created_at': n.created_at.isoformat()
    } for n in notifs])
'''

# إضافة قبل if __name__ == '__main__':
if "user_messages" not in content:
    content = content.replace("if __name__ == '__main__':", new_route + "\n\nif __name__ == '__main__':")
    print("✅ تم إضافة routes رسائل المستخدم")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

# إنشاء قالب HTML لصفحة الرسائل
import os
os.makedirs('templates/user', exist_ok=True)

with open('templates/user/messages.html', 'w', encoding='utf-8') as f:
    f.write('''{% extends "base.html" %}

{% block title %}رسائلي - {{ settings.site_name }}{% endblock %}

{% block content %}
<div class="container mt-5">
    <h2 class="mb-4">📨 رسائلي وردود الدعم</h2>
    
    {% if messages %}
        <div class="list-group">
        {% for msg in messages %}
            <div class="list-group-item {% if msg.admin_reply %}list-group-item-success{% endif %} mb-3 rounded-3 shadow-sm">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h5 class="mb-1">{{ msg.msg_type|upper }}</h5>
                        <p class="mb-1">{{ msg.message }}</p>
                        <small class="text-muted">أرسلت في: {{ msg.created_at.strftime('%Y-%m-%d %H:%M') }}</small>
                    </div>
                    {% if msg.is_resolved %}
                        <span class="badge bg-success">تم الرد</span>
                    {% else %}
                        <span class="badge bg-warning">قيد الانتظار</span>
                    {% endif %}
                </div>
                
                {% if msg.admin_reply %}
                <hr>
                <div class="mt-3 bg-light p-3 rounded">
                    <h6 class="text-primary">👨‍💼 رد الأدمن:</h6>
                    <p class="mb-1">{{ msg.admin_reply }}</p>
                    <small class="text-muted">رد في: {{ msg.resolved_at.strftime('%Y-%m-%d %H:%M') if msg.resolved_at else 'Unknown' }}</small>
                </div>
                {% endif %}
            </div>
        {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-info">
            لا توجد رسائل حالياً. <a href="{{ url_for('support') }}">أرسل رسالة جديدة</a>
        </div>
    {% endif %}
</div>
{% endblock %}
''')

print("✅ تم إنشاء صفحة رسائل المستخدم")
