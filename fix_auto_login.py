with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تعديل دالة التسجيل لتسجيل الدخول مباشرة
old_register = '''flash('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول', 'success')
        return redirect(url_for('user_login'))'''

new_register = '''# تسجيل الدخول تلقائياً بعد إنشاء الحساب
        login_user(user, remember=True, duration=timedelta(days=30))
        session.permanent = True
        flash(f'أهلاً بك {user.username}! تم إنشاء حسابك وتسجيل دخولك تلقائياً', 'success')
        return redirect(url_for('index'))'''

if old_register in content:
    content = content.replace(old_register, new_register)
    print("✅ تم تفعيل تسجيل الدخول التلقائي بعد التسجيل")
else:
    print("⚠️ لم يتم العثور على كود التسجيل القديم")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
