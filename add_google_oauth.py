# إضافة في requirements.txt أولاً
with open('requirements.txt', 'r', encoding='utf-8') as f:
    req_content = f.read()

if 'flask-oauthlib' not in req_content and 'authlib' not in req_content:
    with open('requirements.txt', 'a') as f:
        f.write('\nauthlib>=1.0.0\nrequests>=2.28.0')
    print("✅ تم إضافة مكتبات OAuth")

# إضافة في app.py
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# إضافة الإعدادات
oauth_setup = '''
# إعدادات Google OAuth
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', 'your-client-id.apps.googleusercontent.com')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', 'your-client-secret')

from authlib.integrations.flask_client import OAuth
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

'''

if "oauth = OAuth(app)" not in content:
    # إضافة بعد إنشاء التطبيق
    content = content.replace(
        "db.init_app(app)",
        oauth_setup + "\ndb.init_app(app)"
    )
    print("✅ تم إضافة إعدادات Google OAuth")

# إضافة routes للـ OAuth
oauth_routes = '''

@app.route('/login/google')
def login_google():
    """تسجيل دخول بجوجل"""
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/callback')
def authorize_google():
    """استقبال بيانات جوجل"""
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()
        
        # البحث عن المستخدم أو إنشاؤه
        user = User.query.filter_by(email=user_info['email']).first()
        
        if not user:
            # إنشاء مستخدم جديد
            user = User(
                username=user_info['email'].split('@')[0],
                email=user_info['email'],
                is_active=True,
                accepted_terms=True
            )
            # كلمة مرور عشوائية (لن يستخدمها)
            import secrets
            user.set_password(secrets.token_urlsafe(32))
            db.session.add(user)
            db.session.commit()
            flash('تم إنشاء حسابك بنجاح!', 'success')
        else:
            flash('أهلاً بعودتك!', 'success')
        
        # تسجيل الدخول
        login_user(user, remember=True, duration=timedelta(days=30))
        session.permanent = True
        
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'خطأ في تسجيل الدخول: {str(e)}', 'danger')
        return redirect(url_for('user_login'))

'''

if "login_google" not in content:
    content = content.replace("if __name__ == '__main__':", oauth_routes + "\n\nif __name__ == '__main__':")
    print("✅ تم إضافة routes Google OAuth")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
