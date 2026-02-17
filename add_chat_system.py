with open('models.py', 'r', encoding='utf-8') as f:
    content = f.read()

# إضافة نموذج للمحادثات
chat_model = '''

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    contact_message_id = db.Column(db.Integer, db.ForeignKey('contact_message.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sender_type = db.Column(db.String(20), default='user')  # 'user' أو 'admin'
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    contact = db.relationship('ContactMessage', backref='chat_messages', lazy=True)
    sender = db.relationship('User', foreign_keys=[sender_id], lazy=True)
'''

if 'class ChatMessage' not in content:
    content = content + chat_model
    print("✅ تم إضافة نموذج ChatMessage")
else:
    print("⚠️ ChatMessage موجود مسبقاً")

with open('models.py', 'w', encoding='utf-8') as f:
    f.write(content)

# تحديث ContactMessage لإضافة العلاقة
with open('models.py', 'r', encoding='utf-8') as f:
    content = f.read()

if 'chat_messages' not in content:
    # إضافة backref إذا لم يكن موجوداً
    content = content.replace(
        'class ContactMessage(db.Model):',
        'class ContactMessage(db.Model):\n    chat_messages = db.relationship(\'ChatMessage\', backref=\'contact_msg\', lazy=True, cascade=\'all, delete-orphan\')'
    )
    print("✅ تم إضافة علاقة المحادثات")

with open('models.py', 'w', encoding='utf-8') as f:
    f.write(content)
