# البحث عن ملف تسجيل الدخول وإضافة زر Google
login_file = 'templates/user/login.html'

if os.path.exists(login_file):
    with open(login_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # إضافة زر Google إذا لم يكن موجوداً
    if 'google' not in content.lower():
        google_button = '''
        <div class="text-center mb-3">
            <p class="text-muted">أو</p>
            <a href="{{ url_for('login_google') }}" class="btn btn-danger btn-lg w-100">
                <i class="fab fa-google"></i> تسجيل الدخول بحساب Google
            </a>
        </div>
        <hr>
        '''
        # إضافة قبل نموذج تسجيل الدخول
        content = content.replace('<form', google_button + '<form', 1)
        
        with open(login_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ تم إضافة زر Google في صفحة تسجيل الدخول")
    else:
        print("⚠️ زر Google موجود مسبقاً")
else:
    print("⚠️ لم يتم العثور على ملف تسجيل الدخول")
