import re

with open('utils.py', 'r', encoding='utf-8') as f:
    content = f.read()

# إضافة استيراد generate_password_hash في الأعلى إذا لم يكن موجوداً
if 'from werkzeug.security import generate_password_hash' not in content:
    content = content.replace(
        'from werkzeug.security import generate_password_hash, check_password_hash',
        'from werkzeug.security import generate_password_hash, check_password_hash'
    )

# تعديل دالة init_database لضمان إنشاء admin
old_init = '''    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@rokhub.com', is_admin=True)
        admin.password_hash = generate_password_hash(ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()
        logger.info(f"Admin created! Password: {ADMIN_PASSWORD}")
        print(f"\\n{'='*50}")
        print(f"🔥 ADMIN CREATED!")
        print(f"   Username: admin")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"{'='*50}\\n")'''

new_init = '''    # إنشاء حساب admin إذا لم يكن موجوداً
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@rokhub.com',
            password_hash=generate_password_hash(ADMIN_PASSWORD),
            is_admin=True,
            is_active=True,
            accepted_terms=True
        )
        db.session.add(admin)
        db.session.commit()
        logger.info(f"Admin created! Password: {ADMIN_PASSWORD}")
        print(f"\\n{'='*50}")
        print(f"🔥 ADMIN CREATED!")
        print(f"   Username: admin")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"{'='*50}\\n")
    else:
        # التأكد من أن admin لديه كلمة مرور صحيحة
        from werkzeug.security import check_password_hash
        if not check_password_hash(admin.password_hash, ADMIN_PASSWORD):
            admin.password_hash = generate_password_hash(ADMIN_PASSWORD)
            db.session.commit()
            print(f"✅ تم تحديث كلمة مرور admin")'''

content = content.replace(old_init, new_init)

with open('utils.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم تعديل utils.py بنجاح!")
