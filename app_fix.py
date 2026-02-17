import re

# قراءة الملف
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# البحث عن دالة تسجيل الدخول القديمة واستبدالها
old_login = '''@app.route('/admin/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        print(f"\\n🔐 DEBUG: محاولة تسجيل دخول")
        print(f"   اسم المستخدم: '{username}'")
        print(f"   كلمة المرور: '{password}'")
        print(f"   كلمة المرور المتوقعة: '{ADMIN_PASSWORD}'")
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.locked_until and user.locked_until > datetime.utcnow():
            flash(f'الحساب مقفل حتى {user.locked_until.strftime("%H:%M")}', 'danger')
            return render_template('admin/login.html')
        
        if user:
            print(f"   المستخدم موجود: {user.username}")
            from werkzeug.security import check_password_hash
            password_valid = check_password_hash(user.password_hash, password)
            print(f"   نتيجة التحقق: {password_valid}")
            print(f"   Hash المخزن: {user.password_hash[:30]}...")
            
            if password_valid:
                user.login_attempts = 0
                user.locked_until = None
                user.last_login = datetime.utcnow()
                db.session.commit()
                login_user(user, remember=True)
                flash('تم تسجيل الدخول بنجاح!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                user.login_attempts += 1
                if user.login_attempts >= 5:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=30)
                    flash('تم قفل الحساب لمدة 30 دقيقة', 'danger')
                else:
                    flash(f'كلمة المرور غير صحيحة. المحاولات المتبقية: {5 - user.login_attempts}', 'danger')
                db.session.commit()
        else:
            print(f"   ❌ المستخدم غير موجود!")
            flash('اسم المستخدم غير موجود', 'danger')
    
    return render_template('admin/login.html')'''

new_login = '''@app.route('/admin/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # التحقق من وجود المستخدم
        user = User.query.filter_by(username=username).first()
        
        # إذا لم يكن المستخدم موجوداً، أنشئ حساب admin جديد
        if not user and username == 'admin':
            from werkzeug.security import generate_password_hash
            user = User(
                username='admin',
                email='admin@rokhub.com',
                password_hash=generate_password_hash(ADMIN_PASSWORD),
                is_admin=True,
                is_active=True,
                accepted_terms=True
            )
            db.session.add(user)
            db.session.commit()
            print(f"✅ تم إنشاء حساب admin تلقائياً")
        
        if user:
            # التحقق من قفل الحساب
            if user.locked_until and user.locked_until > datetime.utcnow():
                flash(f'الحساب مقفل حتى {user.locked_until.strftime("%H:%M")}', 'danger')
                return render_template('admin/login.html')
            
            # التحقق من كلمة المرور
            from werkzeug.security import check_password_hash
            if check_password_hash(user.password_hash, password):
                user.login_attempts = 0
                user.locked_until = None
                user.last_login = datetime.utcnow()
                db.session.commit()
                login_user(user, remember=True)
                flash('تم تسجيل الدخول بنجاح!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                user.login_attempts += 1
                if user.login_attempts >= 5:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=30)
                    flash('تم قفل الحساب لمدة 30 دقيقة', 'danger')
                else:
                    flash(f'كلمة المرور غير صحيحة. المحاولات المتبقية: {5 - user.login_attempts}', 'danger')
                db.session.commit()
        else:
            flash('اسم المستخدم غير موجود', 'danger')
    
    return render_template('admin/login.html')'''

content = content.replace(old_login, new_login)

# حفظ الملف
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ تم تعديل app.py بنجاح!")
