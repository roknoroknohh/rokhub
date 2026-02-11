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
        logging.FileHandler('/data/data/com.termux/files/home/gamehub/logs/app.log'),
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
    os.makedirs('/data/data/com.termux/files/home/gamehub/logs', exist_ok=True)
    
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
        sites = [
            GameSite(name='Y8 Games', url='https://www.y8.com',
                     image_url='/static/images/y8-games.png',
                     description='ألعاب فلاش وأونلاين مجانية', sort_order=1),
            GameSite(name='Poki', url='https://poki.com',
                     image_url='/static/images/poki.png',
                     description='ألعاب مجانية للجميع', sort_order=2)
        ]
        db.session.add_all(sites)
    
    db.session.commit()
    return True
