import os
import logging
logger = logging.getLogger(__name__)

import logging
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash

from models import db, User, Game, Category, ContactMessage, GameSite, ErrorLog, SiteSettings
from utils import get_settings, get_lang, log_error, auto_fix_common_issues, init_database, check_url_health
from config import (ADMIN_PASSWORD, INSTAGRAM_LINK, LANGUAGES, 
    SITE_INFO, TERMS_OF_SERVICE, PRIVACY_POLICY)

# إنشاء التطبيق
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rokhub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# الأمان
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
Talisman(app, force_https=False, strict_transport_security=True,
         content_security_policy={
             'default-src': "'self'",
             'style-src': ["'self'", "'unsafe-inline'", "https:", "http:"],
             'font-src': ["'self'", "https:", "http:"],
             'script-src': ["'self'", "'unsafe-inline'", "https:", "http:"],
             'img-src': ["'self'", "data:", "https:", "http:"]
         })

limiter = Limiter(app=app, key_func=get_remote_address,
                  default_limits=["200 per day", "50 per hour"])

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== معالجة الأخطاء ====================

@app.errorhandler(404)
def not_found(error):
    log_error(error)
    return render_template('errors/404.html', settings=get_settings()), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    log_error(error)
    return render_template('errors/500.html', settings=get_settings()), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return render_template('errors/429.html', settings=get_settings()), 429

@app.context_processor
def inject_globals():
    return {
        'site_info': SITE_INFO,
        'terms_text': TERMS_OF_SERVICE,
        'privacy_text': PRIVACY_POLICY
    }

@app.before_request
def before_request():
    if not hasattr(g, 'auto_fix_ran'):
        auto_fix_common_issues()
        g.auto_fix_ran = True
    
    settings = get_settings()
    if settings.maintenance_mode and request.endpoint not in ['maintenance', 'login', 'static']:
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('maintenance'))

# ==================== الصفحات العامة ====================

@app.route('/maintenance')
def maintenance():
    return render_template('errors/maintenance.html'), 503

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/set-lang/<lang>')
def set_language(lang):
    if lang in LANGUAGES:
        session['lang'] = lang
        session.permanent = True
    return redirect(request.referrer or url_for('index'))

@app.route('/')
def index():
    settings = get_settings()
    featured = Game.query.filter_by(is_active=True, is_featured=True).order_by(Game.created_at.desc()).limit(6).all()
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    return render_template('index.html', settings=settings, featured_games=featured,
                         categories=categories, lang=get_lang(), languages=LANGUAGES, instagram=INSTAGRAM_LINK)

@app.route('/games')
def games():
    settings = get_settings()
    platform = request.args.get('platform', 'all')
    category_id = request.args.get('category', type=int)
    
    query = Game.query.filter_by(is_active=True)
    if platform == 'pc':
        query = query.filter(Game.platform.in_(['pc', 'both']))
    elif platform == 'mobile':
        query = query.filter(Game.platform.in_(['mobile', 'both']))
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    games = query.order_by(Game.created_at.desc()).all()
    categories = Category.query.filter_by(is_active=True).order_by(Category.sort_order).all()
    return render_template('games.html', settings=settings, games=games, categories=categories,
                         current_platform=platform, current_category=category_id,
                         lang=get_lang(), languages=LANGUAGES, instagram=INSTAGRAM_LINK)

@app.route('/game/<int:game_id>')
def game_detail(game_id):
    game = Game.query.get_or_404(game_id)
    if not game.last_check or datetime.utcnow() - game.last_check > timedelta(days=1):
        game.health_status = check_url_health(game.external_url) if game.external_url else 'unknown'
        game.last_check = datetime.utcnow()
        db.session.commit()
    game.view_count += 1
    db.session.commit()
    return render_template('game_detail.html', settings=get_settings(), game=game,
                         lang=get_lang(), languages=LANGUAGES, instagram=INSTAGRAM_LINK)

@app.route('/download/<int:game_id>')
def download(game_id):
    game = Game.query.get_or_404(game_id)
    game.download_count += 1
    db.session.commit()
    return render_template('download.html', settings=get_settings(), game=game,
                         lang=get_lang(), languages=LANGUAGES, instagram=INSTAGRAM_LINK)

@app.route('/category/<int:category_id>')
def category(category_id):
    cat = Category.query.get_or_404(category_id)
    games = Game.query.filter_by(category_id=category_id, is_active=True).order_by(Game.created_at.desc()).all()
    return render_template('category.html', settings=get_settings(), category=cat,
                         games=games, lang=get_lang(), languages=LANGUAGES, instagram=INSTAGRAM_LINK)

@app.route('/search')
def search():
    query_text = request.args.get('q', '')
    games = Game.query.filter(Game.is_active == True, Game.title.contains(query_text)).all() if query_text else []
    return render_template('search.html', settings=get_settings(), games=games,
                         query=query_text, lang=get_lang(), languages=LANGUAGES, instagram=INSTAGRAM_LINK)

@app.route('/settings')
def settings_page():
    return render_template('settings.html', settings=get_settings(),
                         lang=get_lang(), languages=LANGUAGES, instagram=INSTAGRAM_LINK)

@app.route('/support', methods=['GET', 'POST'])
def support():
    if request.method == 'POST':
        msg = ContactMessage(
            name=request.form.get('name', ''),
            email=request.form.get('email', ''),
            msg_type=request.form.get('type', 'support'),
            message=request.form.get('message', '')
        )
        db.session.add(msg)
        db.session.commit()
        flash('تم إرسال رسالتك بنجاح!', 'success')
        return redirect(url_for('support'))
    return render_template('support.html', settings=get_settings(),
                         lang=get_lang(), languages=LANGUAGES, instagram=INSTAGRAM_LINK)

@app.route('/online-games')
def online_games():
    sites = GameSite.query.filter_by(is_active=True).order_by(GameSite.sort_order).all()
    for site in sites:
        if not site.last_check or datetime.utcnow() - site.last_check > timedelta(hours=6):
            site.health_status = check_url_health(site.url)
            site.last_check = datetime.utcnow()
    db.session.commit()
    return render_template('online_games.html', settings=get_settings(), sites=sites,
                         lang=get_lang(), languages=LANGUAGES, instagram=INSTAGRAM_LINK)

# ==================== الأدمن ====================

@app.route('/admin/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        print(f"\\n🔍 DEBUG: محاولة دخول")
        print(f"   المستخدم: '{username}'")
        print(f"   كلمة المرور المدخلة: '{password}'")
        print(f"   كلمة المرور المتوقعة: '{ADMIN_PASSWORD}'")
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.locked_until and user.locked_until > datetime.utcnow():
            flash(f'الحساب مقفل حتى {user.locked_until.strftime("%H:%M")}', 'danger')
            return render_template('admin/login.html')
        
        if user:
            print(f"   المستخدم موجود: {user.username}")
            from werkzeug.security import check_password_hash
            password_valid = check_password_hash(user.password_hash, password)
            print(f"   التحقق من كلمة المرور: {password_valid}")
            print(f"   Hash المخزن: {user.password_hash[:30]}...")
            
            if password_valid:
                user.login_attempts = 0
                user.locked_until = None
                user.last_login = datetime.utcnow()
                db.session.commit()
                login_user(user, remember=True)
                flash('تم تسجيل الدخول بنجاح', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                user.login_attempts += 1
                if user.login_attempts >= 5:
                    user.locked_until = datetime.utcnow() + timedelta(minutes=30)
                    flash('تم قفل الحساب 30 دقيقة', 'danger')
                else:
                    flash(f'بيانات خاطئة. محاولات: {5 - user.login_attempts}', 'danger')
                db.session.commit()
        else:
            print(f"   ❌ المستخدم غير موجود!")
            flash('بيانات الدخول غير صحيحة', 'danger')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج', 'success')
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    stats = {
        'total_games': Game.query.count(),
        'total_downloads': db.session.query(db.func.sum(Game.download_count)).scalar() or 0,
        'total_views': db.session.query(db.func.sum(Game.view_count)).scalar() or 0,
        'categories': Category.query.count(),
        'unread_messages': ContactMessage.query.filter_by(is_read=False).count(),
        'unresolved_errors': ErrorLog.query.filter_by(is_resolved=False).count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/games')
@login_required
def admin_games():
    return render_template('admin/games.html', games=Game.query.order_by(Game.created_at.desc()).all())

@app.route('/admin/game/add', methods=['GET', 'POST'])
@login_required
def admin_add_game():
    if request.method == 'POST':
        game = Game(
            title=request.form.get('title'),
            description=request.form.get('description'),
            platform=request.form.get('platform', 'both'),
            download_url=request.form.get('download_url'),
            external_url=request.form.get('external_url'),
            cover_image=request.form.get('cover_image'),
            category_id=request.form.get('category_id'),
            is_active=bool(request.form.get('is_active'))
        )
        db.session.add(game)
        db.session.commit()
        if game.external_url:
            game.health_status = check_url_health(game.external_url)
            db.session.commit()
        flash('تم إضافة اللعبة', 'success')
        return redirect(url_for('admin_games'))
    return render_template('admin/game_form.html', categories=Category.query.filter_by(is_active=True).all())

@app.route('/admin/game/edit/<int:game_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_game(game_id):
    game = Game.query.get_or_404(game_id)
    if request.method == 'POST':
        game.title = request.form.get('title')
        game.description = request.form.get('description')
        game.platform = request.form.get('platform', 'both')
        game.download_url = request.form.get('download_url')
        game.external_url = request.form.get('external_url')
        game.cover_image = request.form.get('cover_image')
        game.category_id = request.form.get('category_id')
        game.is_active = bool(request.form.get('is_active'))
        db.session.commit()
        flash('تم التحديث', 'success')
        return redirect(url_for('admin_games'))
    return render_template('admin/game_form.html', game=game, categories=Category.query.filter_by(is_active=True).all())

@app.route('/admin/game/delete/<int:game_id>', methods=['POST'])
@login_required
def admin_delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    flash('تم الحذف', 'success')
    return redirect(url_for('admin_games'))

@app.route('/admin/categories')
@login_required
def admin_categories():
    return render_template('admin/categories.html', categories=Category.query.all())

@app.route('/admin/category/add', methods=['POST'])
@login_required
def admin_add_category():
    cat = Category(name=request.form.get('name'), icon=request.form.get('icon', 'gamepad'),
                   color=request.form.get('color', '#3b82f6'))
    db.session.add(cat)
    db.session.commit()
    flash('تم الإضافة', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/category/delete/<int:category_id>', methods=['POST'])
@login_required
def admin_delete_category(category_id):
    cat = Category.query.get_or_404(category_id)
    db.session.delete(cat)
    db.session.commit()
    flash('تم الحذف', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    settings = get_settings()
    if request.method == 'POST':
        settings.site_name = request.form.get('site_name')
        settings.site_description = request.form.get('site_description')
        settings.maintenance_mode = bool(request.form.get('maintenance_mode'))
        db.session.commit()
        flash('تم الحفظ', 'success')
        return redirect(url_for('admin_settings'))
    return render_template('admin/settings.html', settings=settings)

@app.route('/admin/users')
@login_required
def admin_users():
    return render_template('admin/users.html', users=User.query.all())

@app.route('/admin/user/add', methods=['POST'])
@login_required
def admin_add_user():
    u = User(username=request.form.get('username'), email=request.form.get('email'),
             password_hash=generate_password_hash(request.form.get('password')), is_admin=True)
    db.session.add(u)
    db.session.commit()
    flash('تم الإضافة', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/messages')
@login_required
def admin_messages():
    msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    for m in msgs:
        if not m.is_read:
            m.is_read = True
    db.session.commit()
    return render_template('admin/messages.html', messages=msgs)

@app.route('/admin/message/<int:msg_id>/reply', methods=['POST'])
@login_required
def admin_reply_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.admin_reply = request.form.get('reply')
    msg.is_resolved = True
    msg.resolved_at = datetime.utcnow()
    msg.resolved_by = current_user.id
    db.session.commit()
    flash('تم الرد', 'success')
    return redirect(url_for('admin_messages'))

@app.route('/admin/errors')
@login_required
def admin_errors():
    return render_template('admin/errors.html', errors=ErrorLog.query.order_by(ErrorLog.created_at.desc()).all())

@app.route('/admin/error/<int:error_id>/resolve', methods=['POST'])
@login_required
def admin_resolve_error(error_id):
    err = ErrorLog.query.get_or_404(error_id)
    err.is_resolved = True
    db.session.commit()
    flash('تم التحديث', 'success')
    return redirect(url_for('admin_errors'))

@app.route('/admin/sites')
@login_required
def admin_sites():
    return render_template('admin/sites.html', sites=GameSite.query.order_by(GameSite.sort_order).all())

@app.route('/admin/site/add', methods=['POST'])
@login_required
def admin_add_site():
    site = GameSite(name=request.form.get('name'), url=request.form.get('url'),
                    image_url=request.form.get('image_url'), description=request.form.get('description'),
                    sort_order=request.form.get('sort_order', 0, type=int))
    db.session.add(site)
    db.session.commit()
    flash('تم الإضافة', 'success')
    return redirect(url_for('admin_sites'))

@app.route('/admin/site/delete/<int:site_id>', methods=['POST'])
@login_required
def admin_delete_site(site_id):
    site = GameSite.query.get_or_404(site_id)
    db.session.delete(site)
    db.session.commit()
    flash('تم الحذف', 'success')
    return redirect(url_for('admin_sites'))

@app.route('/admin/run-auto-fix')
@login_required
def admin_run_auto_fix():
    fixes = auto_fix_common_issues()
    flash(f'تم إصلاح {len(fixes)} مشكلة', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/api/stats')
def api_stats():
    return jsonify({
        'games': Game.query.count(),
        'downloads': db.session.query(db.func.sum(Game.download_count)).scalar() or 0,
        'views': db.session.query(db.func.sum(Game.view_count)).scalar() or 0
    })

@app.route('/init')
def init_db():
    try:
        init_database()
        return '<h1 style="color:green; text-align:center;">✅ تم التثبيت!<br>المستخدم: admin<br>كلمة المرور: admin123</h1>'
    except Exception as e:
        return f'<h1 style="color:red;">خطأ: {str(e)}</h1>'



# ==================== صفحات المستخدمين ====================

@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    """تسجيل دخول المستخدم العادي"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('الحساب معطل. تواصل مع الدعم', 'danger')
                return render_template('user/login.html')
            
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=True)
            flash(f'أهلاً بك {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('بيانات الدخول غير صحيحة', 'danger')
    
    return render_template('user/login.html', settings=get_settings())

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    """تسجيل مستخدم جديد"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        accept_terms = request.form.get('accept_terms')
        
        # التحقق من الموافقة على الشروط
        if not accept_terms:
            flash('يجب الموافقة على شروط الخدمة', 'danger')
            return render_template('user/register.html')
        
        # التحقق من عدم التكرار
        if User.query.filter_by(username=username).first():
            flash('اسم المستخدم موجود مسبقاً', 'danger')
            return render_template('user/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('البريد الإلكتروني مستخدم مسبقاً', 'danger')
            return render_template('user/register.html')
        
        # إنشاء المستخدم
        user = User(
            username=username,
            email=email,
            accepted_terms=True,
            is_admin=False
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # إشعار للأدمن
        logger.info(f"New user registered: {username} ({email})")
        
        flash('تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول', 'success')
        return redirect(url_for('user_login'))
    
    return render_template('user/register.html', settings=get_settings())

@app.route('/user/profile')
@login_required
def user_profile():
    """صفحة الملف الشخصي"""
    user_messages = ContactMessage.query.filter_by(user_id=current_user.id).order_by(ContactMessage.created_at.desc()).all()
    return render_template('user/profile.html', user=current_user, messages=user_messages)

@app.route('/terms')
def terms():
    """شروط الخدمة"""
    return render_template('terms.html', settings=get_settings())

@app.route('/privacy')
def privacy():
    """سياسة الخصوصية"""
    return render_template('privacy.html', settings=get_settings())

@app.route('/dmca')
def dmca():
    """DMCA"""
    return render_template('dmca.html', settings=get_settings())


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
