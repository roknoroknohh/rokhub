import os

# إنشاء ملف JavaScript للشروط
os.makedirs('static/js', exist_ok=True)

with open('static/js/terms-popup.js', 'w', encoding='utf-8') as f:
    f.write('''
// نافذة شروط الخدمة المنبثقة
document.addEventListener('DOMContentLoaded', function() {
    // التحقق إذا كان المستخدم وافق مسبقاً
    if (!localStorage.getItem('termsAccepted')) {
        showTermsModal();
    }
});

function showTermsModal() {
    // إنشاء النافذة المنبثقة
    const modal = document.createElement('div');
    modal.id = 'termsModal';
    modal.innerHTML = `
        <div style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 9999;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        ">
            <div style="
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                color: white;
                padding: 30px;
                border-radius: 15px;
                max-width: 500px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 20px 60px rgba(0,0,0,0.5);
                border: 2px solid rgba(255,255,255,0.1);
            ">
                <h2 style="text-align: center; margin-bottom: 20px; font-size: 24px;">
                    📜 شروط الخدمة و الخصوصية
                </h2>
                
                <div style="
                    background: rgba(255,255,255,0.1);
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 20px;
                    max-height: 300px;
                    overflow-y: auto;
                    line-height: 1.6;
                ">
                    <h3>شروط الاستخدام:</h3>
                    <ul style="padding-right: 20px;">
                        <li>الموقع مخصص للألعاب القانونية فقط</li>
                        <li>يمنع نشر أي محتوى غير لائق</li>
                        <li>المستخدم مسؤول عن حسابه الشخصي</li>
                        <li>نحتفظ بحق تعليق أي حساب مخالف</li>
                    </ul>
                    
                    <h3>سياسة الخصوصية:</h3>
                    <ul style="padding-right: 20px;">
                        <li>نجمع بيانات أساسية لتحسين الخدمة</li>
                        <li>لا نشارك بياناتك مع طرف ثالث</li>
                        <li>يمكنك حذف حسابك في أي وقت</li>
                        <li>نستخدم ملفات Cookies لتحسين التجربة</li>
                    </ul>
                </div>
                
                <div style="display: flex; gap: 10px; flex-direction: column;">
                    <button onclick="acceptTerms()" style="
                        background: #22c55e;
                        color: white;
                        border: none;
                        padding: 15px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 16px;
                        font-weight: bold;
                        transition: all 0.3s;
                    " onmouseover="this.style.background='#16a34a'" onmouseout="this.style.background='#22c55e'">
                        ✅ أوافق على الشروط والأحكام
                    </button>
                    
                    <button onclick="declineTerms()" style="
                        background: #ef4444;
                        color: white;
                        border: none;
                        padding: 12px;
                        border-radius: 8px;
                        cursor: pointer;
                        font-size: 14px;
                        transition: all 0.3s;
                    " onmouseover="this.style.background='#dc2626'" onmouseout="this.style.background='#ef4444'">
                        ❌ لا أوافق (سيتم إغلاق الموقع)
                    </button>
                </div>
                
                <p style="text-align: center; margin-top: 15px; font-size: 12px; opacity: 0.8;">
                    بالنقر على "أوافق"، فإنك توافق على <a href="/terms" style="color: #60a5fa;">شروط الخدمة</a> و <a href="/privacy" style="color: #60a5fa;">سياسة الخصوصية</a>
                </p>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden'; // منع التمرير
}

function acceptTerms() {
    localStorage.setItem('termsAccepted', 'true');
    localStorage.setItem('termsAcceptedDate', new Date().toISOString());
    document.getElementById('termsModal').remove();
    document.body.style.overflow = 'auto';
    
    // إظهار رسالة ترحيب
    showWelcomeMessage();
}

function declineTerms() {
    alert('يجب الموافقة على الشروط لاستخدام الموقع. سيتم إغلاق الصفحة.');
    window.close();
    // إذا لم يغلق المتصفح، نحوله لصفحة فارغة
    setTimeout(() => {
        document.body.innerHTML = '<div style="display:flex;justify-content:center;align-items:center;height:100vh;font-family:Arial;"><h2>❌ تم رفض الوصول</h2></div>';
    }, 1000);
}

function showWelcomeMessage() {
    const toast = document.createElement('div');
    toast.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #22c55e;
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 10000;
            animation: slideDown 0.5s ease;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        ">
            🎉 أهلاً بك في ROKhub! تم تفعيل حسابك بنجاح
        </div>
    `;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// CSS Animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from { transform: translate(-50%, -100%); opacity: 0; }
        to { transform: translate(-50%, 0); opacity: 1; }
    }
`;
document.head.appendChild(style);
''')

print("✅ تم إنشاء ملف terms-popup.js")

# تعديل base.html لإضافة الـ JS
if os.path.exists('templates/base.html'):
    with open('templates/base.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # إضافة script قبل نهاية body
    if 'terms-popup.js' not in content:
        content = content.replace('</body>', '<script src="{{ url_for(\'static\', filename=\'js/terms-popup.js\') }}"></script>\n</body>')
        
        with open('templates/base.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ تم ربط ملف JavaScript في base.html")
    else:
        print("⚠️ الملف مربوط مسبقاً")
else:
    print("❌ لم يتم العثور على base.html")
