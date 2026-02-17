with open('utils.py', 'r', encoding='utf-8') as f:
    content = f.read()

# إضافة وظيفة إصلاح الأخطاء المتقدمة
advanced_fix = '''

def advanced_auto_fix():
    """نظام إصلاح الأخطاء التلقائي المتقدم"""
    from flask import render_template_string
    fixes = []
    errors_found = []
    
    # 1. إصلاح الجداول المفقودة
    try:
        db.create_all()
        fixes.append("✅ تم التحقق من جميع الجداول")
    except Exception as e:
        errors_found.append(f"خطأ في إنشاء الجداول: {str(e)}")
    
    # 2. إصلاح المستخدمين المقفلين
    try:
        locked_users = User.query.filter(
            User.locked_until < datetime.utcnow(),
            User.login_attempts > 0
        ).all()
        for user in locked_users:
            user.login_attempts = 0
            user.locked_until = None
        if locked_users:
            db.session.commit()
            fixes.append(f"🔓 تم فك قفل {len(locked_users)} مستخدم")
    except Exception as e:
        errors_found.append(f"خطأ في فك القفل: {str(e)}")
    
    # 3. تنظيف الأخطاء القديمة
    try:
        old_errors = ErrorLog.query.filter(
            ErrorLog.created_at < datetime.utcnow() - timedelta(days=30),
            ErrorLog.is_resolved == True
        ).all()
        for error in old_errors:
            db.session.delete(error)
        if old_errors:
            db.session.commit()
            fixes.append(f"🧹 تم حذف {len(old_errors)} خطأ قديم")
    except Exception as e:
        errors_found.append(f"خطأ في التنظيف: {str(e)}")
    
    # 4. فحص صحة الروابط المعطلة
    try:
        broken_games = Game.query.filter_by(health_status='broken').limit(5).all()
        for game in broken_games:
            new_status = check_url_health(game.external_url) if game.external_url else 'unknown'
            game.health_status = new_status
            game.last_check = datetime.utcnow()
        if broken_games:
            db.session.commit()
            fixes.append(f"🔗 تم فحص {len(broken_games)} لعبة معطلة")
    except Exception as e:
        errors_found.append(f"خطأ في فحص الروابط: {str(e)}")
    
    # 5. إنشاء إعدادات افتراضية إذا لم تكن موجودة
    try:
        if not SiteSettings.query.first():
            db.session.add(SiteSettings())
            db.session.commit()
            fixes.append("⚙️ تم إنشاء الإعدادات الافتراضية")
    except Exception as e:
        errors_found.append(f"خطأ في الإعدادات: {str(e)}")
    
    # تسجيل النتائج
    if fixes or errors_found:
        log_entry = AutoFixLog(
            issue_type='advanced_auto_fix',
            description='; '.join(fixes) if fixes else 'No fixes needed',
            action_taken='; '.join(errors_found) if errors_found else 'Success',
            success=len(errors_found) == 0
        )
        db.session.add(log_entry)
        db.session.commit()
    
    return {'fixes': fixes, 'errors': errors_found}

def notify_admin_of_errors():
    """إرسال إشعار للأدمن بالأخطاء الجديدة"""
    recent_errors = ErrorLog.query.filter(
        ErrorLog.is_resolved == False,
        ErrorLog.created_at > datetime.utcnow() - timedelta(hours=1)
    ).all()
    
    if recent_errors:
        # يمكن إضافة إرسال بريد أو إشعار هنا
        logger.warning(f"⚠️ {len(recent_errors)} أخطاء جديدة تحتاج اهتمامك في لوحة التحكم")
        return len(recent_errors)
    return 0
'''

if "advanced_auto_fix" not in content:
    content = content + advanced_fix
    print("✅ تم إضافة نظام الإصلاح المتقدم")
else:
    print("⚠️ النظام موجود مسبقاً")

with open('utils.py', 'w', encoding='utf-8') as f:
    f.write(content)

# إضافة استدعاء تلقائي في app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

if "advanced_auto_fix()" not in content:
    # إضافة في before_request
    old_before = "auto_fix_common_issues()"
    new_before = "auto_fix_common_issues()\n        advanced_auto_fix()\n        notify_admin_of_errors()"
    content = content.replace(old_before, new_before)
    print("✅ تم تفعيل الإصلاح التلقائي في before_request")

# إضافة استيراد
old_import_utils = "from utils import get_settings, get_lang, log_error, auto_fix_common_issues, init_database, check_url_health"
new_import_utils = "from utils import get_settings, get_lang, log_error, auto_fix_common_issues, init_database, check_url_health, advanced_auto_fix, notify_admin_of_errors"

if old_import_utils in content:
    content = content.replace(old_import_utils, new_import_utils)
    print("✅ تم إضافة استيراد الدوال الجديدة")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
