#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكربت إصلاح مشاكل ROKhub
يصلح: Safari CSP + تسجيل الدخول + مشاكل أخرى
"""

import os
import shutil
from datetime import datetime

# المسار الرئيسي
BASE_DIR = "/data/data/com.termux/files/home/gamehub"
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
ADMIN_DIR = os.path.join(TEMPLATES_DIR, "admin")

def backup_file(filepath):
    """إنشاء نسخة احتياطية"""
    if os.path.exists(filepath):
        backup_path = f"{filepath}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(filepath, backup_path)
        print(f"✅ نسخ احتياطي: {backup_path}")
        return True
    return False

def fix_base_html():
    """إصلاح base.html - إضافة CSP لـ Safari"""
    filepath = os.path.join(TEMPLATES_DIR, "base.html")
    
    if not os.path.exists(filepath):
        print(f"❌ لم يُعثر على: {filepath}")
        return False
    
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # التحقق إذا كان CSP موجوداً مسبقاً
    if "Content-Security-Policy" in content:
        print("⚠️ CSP موجود مسبقاً في base.html")
        return True
    
    # إضافة CSP بعد viewport meta tag
    csp_meta = '''    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://fonts.googleapis.com https://cdnjs.cloudflare.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; img-src 'self' data: https: http:;">'''
    
    content = content.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' + csp_meta
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ تم إصلاح base.html - إضافة CSP")
    return True

def fix_login_html():
    """إصلاح login.html - إضافة Font Awesome"""
    filepath = os.path.join(ADMIN_DIR, "login.html")
    
    if not os.path.exists(filepath):
        print(f"❌ لم يُعثر على: {filepath}")
        return False
    
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # التحقق من وجود Font Awesome
    if "font-awesome" in content:
        print("⚠️ Font Awesome موجود مسبقاً في login.html")
    else:
        # إضافة Font Awesome بعد Google Fonts
        fa_link = '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">'
        
        content = content.replace(
            "<link href=\"https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&display=swap\" rel=\"stylesheet\">",
            "<link href=\"https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&display=swap\" rel=\"stylesheet\">\n" + fa_link
        )
        print("✅ تم إضافة Font Awesome لـ login.html")
    
    # إضافة أيقونة القفل إذا كانت مفقودة
    if "fas fa-lock" in content and "<i class=\"fas fa-lock" in content:
        print("✅ أيقونة القفل موجودة")
    elif "fas fa-lock" in content:
        # استبدال النص بأيقونة حقيقية
        content = content.replace(
            '<i class="fas fa-lock text-2xl"></i>',
            '<i class="fas fa-lock text-2xl" style="color: white;"></i>'
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ تم إصلاح login.html")
    return True

def fix_app_py():
    """إصلاح app.py - تحسين تسجيل الدخول"""
    filepath = os.path.join(BASE_DIR, "app.py")
    
    if not os.path.exists(filepath):
        print(f"❌ لم يُعثر على: {filepath}")
        return False
    
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # البحث عن دالة login واستبدالها
    old_login = '''@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and check_password_hash(user.password_hash, request.form.get('password')):
            login_user(user)
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('بيانات الدخول غير صحيحة', 'danger')
    return render_template('admin/login.html')'''
    
    new_login = '''@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # طباعة للتصحيح (تظهر في termux)
        print(f"\\n[*] محاولة تسجيل دخول:")
        print(f"    المستخدم: {username}")
        print(f"    طول كلمة المرور: {len(password)}")
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"    المستخدم موجود: {user.email}")
            if check_password_hash(user.password_hash, password):
                login_user(user)
                flash('تم تسجيل الدخول بنجاح', 'success')
                print(f"    [+] نجح تسجيل الدخول!")
                return redirect(url_for('admin_dashboard'))
            else:
                print(f"    [-] كلمة المرور خاطئة")
        else:
            print(f"    [-] المستخدم غير موجود")
        
        flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
    
    return render_template('admin/login.html')'''
    
    if old_login in content:
        content = content.replace(old_login, new_login)
        print("✅ تم تحديث دالة login في app.py")
    else:
        print("⚠️ لم يُعثر على نص دالة login القديم - ربما تم تعديلها مسبقاً")
    
    # إضافة secret key أقوى إذا كان ضعيفاً
    if "rokhub-secret-key-2024" in content:
        import secrets
        new_secret = secrets.token_hex(32)
        content = content.replace(
            "app.config['SECRET_KEY'] = 'rokhub-secret-key-2024'",
            f"app.config['SECRET_KEY'] = '{new_secret}'"
        )
        print(f"✅ تم تحديث SECRET_KEY")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ تم إصلاح app.py")
    return True

def fix_admin_base_html():
    """إصلاح base_admin.html - إضافة CSP"""
    filepath = os.path.join(ADMIN_DIR, "base_admin.html")
    
    if not os.path.exists(filepath):
        print(f"❌ لم يُعثر على: {filepath}")
        return False
    
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "Content-Security-Policy" in content:
        print("⚠️ CSP موجود مسبقاً في base_admin.html")
        return True
    
    csp_meta = '''    <meta http-equiv="Content-Security-Policy" content="default-src 'self'; style-src 'self' 'unsafe-inline' https:; font-src 'self' https:; script-src 'self' 'unsafe-inline' https:; img-src 'self' data: https: http:;">'''
    
    content = content.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n' + csp_meta
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ تم إصلاح base_admin.html")
    return True

def clean_duplicate_files():
    """حذف الملفات المكررة"""
    duplicates = [
        os.path.join(ADMIN_DIR, "games(1).html"),
        os.path.join(ADMIN_DIR, "settings(1).html")
    ]
    
    for dup in duplicates:
        if os.path.exists(dup):
            backup_file(dup)
            os.remove(dup)
            print(f"✅ تم حذف الملف المكرر: {os.path.basename(dup)}")

def create_test_user():
    """إنشاء مستخدم test للتجربة"""
    print("\\n📊 لإنشاء مستخدم جديد، شغل هذا الأمر في Termux:")
    print("   python3 -c \"from app import app, db, User; from werkzeug.security import generate_password_hash; with app.app_context(): db.create_all(); u = User(username='test', email='test@test.com', password_hash=generate_password_hash('123456'), is_admin=True); db.session.add(u); db.session.commit(); print('تم إنشاء المستخدم')\"")
    print("\\n   بيانات الدخول:")
    print("   المستخدم: test")
    print("   كلمة المرور: 123456")

def main():
    """الدالة الرئيسية"""
    print("=" * 50)
    print("🔧 سكربت إصلاح ROKhub")
    print("=" * 50)
    print(f"📁 المسار: {BASE_DIR}")
    print()
    
    # التحقق من وجود المجلدات
    if not os.path.exists(BASE_DIR):
        print(f"❌ خطأ: المجلد غير موجود: {BASE_DIR}")
        return
    
    if not os.path.exists(TEMPLATES_DIR):
        print(f"❌ خطأ: مجلد templates غير موجود")
        return
    
    # تنفيذ الإصلاحات
    print("🔹 المرحلة 1: إصلاح القوالب...")
    fix_base_html()
    fix_admin_base_html()
    fix_login_html()
    
    print("\\n🔹 المرحلة 2: إصلاح التطبيق...")
    fix_app_py()
    
    print("\\n🔹 المرحلة 3: تنظيف الملفات...")
    clean_duplicate_files()
    
    print("\\n" + "=" * 50)
    print("✅ تم الانتهاء من الإصلاحات!")
    print("=" * 50)
    print("\\n📋 الخطوات التالية:")
    print("   1. cd /data/data/com.termux/files/home/gamehub")
    print("   2. python app.py")
    print("   3. افتح Safari وادخل على: http://localhost:5000")
    print("   4. للأدمن: http://localhost:5000/admin/login")
    print("\\n🔑 بيانات الدخول الافتراضية:")
    print("   المستخدم: admin")
    print("   كلمة المرور: server server15935713467906401593571346790640server server")
    print("\\n⚠️ إذا لم تنجح، جرب إنشاء مستخدم جديد (أنظر أعلاه)")
    
    create_test_user()

if __name__ == "__main__":
    main()
