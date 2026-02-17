with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_api = '''
@app.route('/api/check-replies')
@login_required
def check_new_replies():
    """التحقق من وجود ردود جديدة على رسائل المستخدم"""
    # البحث عن رسائل تم الرد عليها منذ آخر دخول
    last_check = session.get('last_notification_check', datetime.utcnow() - timedelta(days=1))
    
    new_replies = ContactMessage.query.filter(
        ContactMessage.user_id == current_user.id,
        ContactMessage.is_resolved == True,
        ContactMessage.resolved_at > last_check
    ).count()
    
    session['last_notification_check'] = datetime.utcnow()
    
    return jsonify({
        'has_new_reply': new_replies > 0,
        'count': new_replies
    })
'''

# إضافة قبل if __name__ == '__main__':
if "check_new_replies" not in content:
    content = content.replace("if __name__ == '__main__':", new_api + "\n\nif __name__ == '__main__':")
    print("✅ تم إضافة API التحقق من الردود")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
