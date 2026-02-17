import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# تعديل إعدادات الجلسة لتكون دائمة لمدة 30 يوماً
old_session = "app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)"
new_session = "app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)"
content = content.replace(old_session, new_session)

# تعديل تسجيل دخول المستخدمين ليتذكرهم تلقائياً
old_user_login = '''if user and user.check_password(password):
            if not user.is_active:
                flash('الحساب معطل. تواصل مع الدعم', 'danger')
                return render_template('user/login.html')

            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=True)
            flash(f'أهلاً بك {user.username}!', 'success')
            return redirect(url_for('index'))'''

new_user_login = '''if user and user.check_password(password):
            if not user.is_active:
                flash('الحساب معطل. تواصل مع الدعم', 'danger')
                return render_template('user/login.html')

            user.last_login = datetime.utcnow()
            db.session.commit()
            # تذكر المستخدم لمدة 30 يوماً
            login_user(user, remember=True, duration=timedelta(days=30))
            session.permanent = True
            flash(f'أهلاً بك {user.username}!', 'success')
            return redirect(url_for('index'))'''

if old_user_login in content:
    content = content.replace(old_user_login, new_user_login)
    print("✅ تم تفعيل تذكر تسجيل دخول المستخدمين")
else:
    print("⚠️ لم يتم العثور على كود تسجيل دخول المستخدمين")

# تعديل تسجيل دخول الأدمن أيضاً
old_admin_login = '''login_user(user, remember=True)
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('admin_dashboard'))'''

new_admin_login = '''login_user(user, remember=True, duration=timedelta(days=30))
            session.permanent = True
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('admin_dashboard'))'''

if old_admin_login in content:
    content = content.replace(old_admin_login, new_admin_login)
    print("✅ تم تفعيل تذكر تسجيل دخول الأدمن")
else:
    print("⚠️ لم يتم العثور على كود تسجيل دخول الأدمن")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم تحديث إعدادات الجلسات")
