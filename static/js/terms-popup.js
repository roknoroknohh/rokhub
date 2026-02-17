// نظام النوافذ المنبثقة للشروط والأحكام
(function() {
    'use strict';

    // إنشاء نافذة منبثقة
    function createPopup(title, content, onAccept, onDecline) {
        // إزالة أي نوافذ منبثقة سابقة
        const existingPopup = document.getElementById('terms-popup');
        if (existingPopup) existingPopup.remove();

        const popup = document.createElement('div');
        popup.id = 'terms-popup';
        popup.className = 'fixed inset-0 z-50 flex items-center justify-center p-4';
        popup.innerHTML = `
            <div class="absolute inset-0 bg-black/70 backdrop-blur-sm" onclick="if('${onDecline ? 'decline' : ''}') window.TermsPopup.decline()"></div>
            <div class="relative bg-gray-900 rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-hidden border border-gray-700 shadow-2xl">
                <div class="p-6 border-b border-gray-800">
                    <h2 class="text-2xl font-bold">${title}</h2>
                </div>
                <div class="p-6 overflow-y-auto max-h-[50vh] text-gray-300 leading-relaxed">
                    ${content.replace(/\n/g, '<br>')}
                </div>
                <div class="p-6 border-t border-gray-800 flex gap-3 justify-end">
                    <button id="decline-btn" class="px-6 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition">
                        رفض
                    </button>
                    <button id="accept-btn" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg transition">
                        أوافق
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(popup);
        document.body.style.overflow = 'hidden';

        // أحداث الأزرار
        document.getElementById('accept-btn').addEventListener('click', () => {
            closePopup();
            if (onAccept) onAccept();
        });

        if (onDecline) {
            document.getElementById('decline-btn').addEventListener('click', () => {
                closePopup();
                onDecline();
            });
        } else {
            document.getElementById('decline-btn').style.display = 'none';
        }
    }

    function closePopup() {
        const popup = document.getElementById('terms-popup');
        if (popup) {
            popup.style.opacity = '0';
            setTimeout(() => {
                popup.remove();
                document.body.style.overflow = '';
            }, 200);
        }
    }

    // عرض شروط الخدمة
    function showTerms() {
        const termsText = document.querySelector('meta[name="terms-text"]')?.content || 
            `شروط استخدام الموقع:
            
1. الموقع مخصص للألعاب القانونية فقط
2. يمنع نشر أي محتوى غير لائق
3. المستخدم مسؤول عن حسابه الشخصي
4. نحتفظ بحق تعليق أي حساب مخالف
5. البيانات الشخصية محمية وفق سياسة الخصوصية`;

        createPopup('شروط الخدمة', termsText, 
            () => {
                localStorage.setItem('termsAccepted', 'true');
                localStorage.setItem('termsAcceptedDate', new Date().toISOString());
            },
            () => {
                window.location.href = '/';
            }
        );
    }

    // عرض سياسة الخصوصية
    function showPrivacy() {
        const privacyText = document.querySelector('meta[name="privacy-text"]')?.content ||
            `سياسة الخصوصية:
            
1. نجمع بيانات أساسية لتحسين الخدمة
2. لا نشارك بياناتك مع طرف ثالث
3. يمكنك حذف حسابك في أي وقت
4. نستخدم ملفات Cookies لتحسين التجربة`;

        createPopup('سياسة الخصوصية', privacyText, null, null);
    }

    // التحقق من قبول الشروط
    function checkTermsAccepted() {
        const termsAccepted = localStorage.getItem('termsAccepted');
        const acceptedDate = localStorage.getItem('termsAcceptedDate');
        
        // إعادة عرض الشروط كل 6 أشهر
        if (acceptedDate) {
            const sixMonthsAgo = new Date();
            sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);
            
            if (new Date(acceptedDate) < sixMonthsAgo) {
                localStorage.removeItem('termsAccepted');
                return false;
            }
        }
        
        return termsAccepted === 'true';
    }

    // تهيئة
    document.addEventListener('DOMContentLoaded', () => {
        // التحقق من قبول الشروط للمستخدمين المسجلين
        const isAuthenticated = document.body.dataset.userAuthenticated === 'true';
        if (isAuthenticated && !checkTermsAccepted()) {
            setTimeout(showTerms, 1000);
        }

        // أزرار عرض الشروط والخصوصية
        document.querySelectorAll('[data-show-terms]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                showTerms();
            });
        });

        document.querySelectorAll('[data-show-privacy]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                showPrivacy();
            });
        });
    });

    // تصدير الدوال
    window.TermsPopup = {
        show: createPopup,
        close: closePopup,
        showTerms: showTerms,
        showPrivacy: showPrivacy,
        decline: () => window.location.href = '/'
    };
})();
