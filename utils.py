import os
import logging
import sys
import requests
from datetime import datetime, timedelta
from flask import request
from models import db, SiteSettings, Game, GameSite, ErrorLog, AutoFixLog, User
from config import ADMIN_PASSWORD, INSTAGRAM_LINK, LANGUAGES

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def get_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
    return settings

def get_lang():
    from flask import session
    return session.get('lang', 'ar')

def log_error(error, route=None):
    try:
        error_log = ErrorLog(
            error_type=type(error).__name__,
            error_message=str(error),
            route=route or request.endpoint,
            user_agent=request.user_agent.string[:500] if request.user_agent else None,
            ip_address=request.remote_addr
        )
        db.session.add(error_log)
        db.session.commit()
        logger.error(f"Error logged: {error} at {route}")
    except Exception as e:
        logger.critical(f"Failed to log error: {e}")

def check_url_health(url):
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return 'healthy' if response.status_code == 200 else 'broken'
    except:
        return 'broken'

def auto_fix_common_issues():
    fixes = []
    
    broken_games = Game.query.filter_by(health_status='broken').all()
    for game in broken_games:
        if game.external_url:
            new_status = check_url_health(game.external_url)
            if new_status == 'healthy':
                game.health_status = 'healthy'
                game.last_check = datetime.utcnow()
                fixes.append(f"Fixed game: {game.title}")
    
    sites = GameSite.query.filter(
        (GameSite.last_check < datetime.utcnow() - timedelta(hours=6)) | 
        (GameSite.last_check == None)
    ).all()
    for site in sites:
        site.health_status = check_url_health(site.url)
        site.last_check = datetime.utcnow()
    
    old_errors = ErrorLog.query.filter(
        ErrorLog.created_at < datetime.utcnow() - timedelta(days=30),
        ErrorLog.is_resolved == True
    ).all()
    for error in old_errors:
        db.session.delete(error)
    if old_errors:
        fixes.append(f"Cleaned {len(old_errors)} old errors")
    
    locked_users = User.query.filter(
        User.locked_until < datetime.utcnow(),
        User.login_attempts > 0
    ).all()
    for user in locked_users:
        user.login_attempts = 0
        user.locked_until = None
        fixes.append(f"Reset login: {user.username}")
    
    if fixes:
        db.session.commit()
        for fix in fixes:
            logger.info(f"Auto-fix: {fix}")
            log = AutoFixLog(issue_type='auto_fix', description=fix, action_taken='automatic', success=True)
            db.session.add(log)
        db.session.commit()
    
    return fixes

def init_database():
    from models import Category, GameSite
    from werkzeug.security import generate_password_hash
    
    db.create_all()
    # إنشاء المجلدات اللازمة بشكل مرن
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(base_dir, 'logs')
    uploads_dir = os.path.join(base_dir, 'uploads')
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(uploads_dir, exist_ok=True)
    
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@rokhub.com', is_admin=True)
        admin.password_hash = generate_password_hash(ADMIN_PASSWORD)
        db.session.add(admin)
        db.session.commit()
        logger.info(f"Admin created! Password: {ADMIN_PASSWORD}")
        print(f"\\n{'='*50}")
        print(f"✅ ADMIN CREATED!")
        print(f"   Username: admin")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"{'='*50}\\n")
    
    if not Category.query.first():
        categories = [
            Category(name='أكشن', icon='sword', color='#ef4444'),
            Category(name='مغامرة', icon='mountain', color='#22c55e'),
            Category(name='رياضة', icon='trophy', color='#3b82f6'),
            Category(name='سباق', icon='car', color='#f59e0b')
        ]
        db.session.add_all(categories)
    
    if not SiteSettings.query.first():
        db.session.add(SiteSettings())
    
    if not GameSite.query.first():
        from config import GAME_SITES
        sites = []
        for idx, site_data in enumerate(GAME_SITES[:5], 1):
            sites.append(GameSite(
                name=site_data['name'],
                url=site_data['url'],
                image_url=site_data.get('image', ''),
                description=site_data.get('description', ''),
                sort_order=idx
            ))
        db.session.add_all(sites)
    
    db.session.commit()
    return True


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
