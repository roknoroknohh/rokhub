// نظام الإشعارات المتقدم
(function() {
    'use strict';

    // التحقق من وجود ردود جديدة
    async function checkNewReplies() {
        const isAuthenticated = document.body.dataset.userAuthenticated === 'true';
        if (!isAuthenticated) return;

        try {
            const response = await fetch('/api/check-replies');
            if (response.ok) {
                const data = await response.json();
                if (data.has_new_reply && data.count > 0) {
                    showNotification(
                        'ردود جديدة',
                        `لديك ${data.count} ردود جديدة على رسائلك`,
                        'info',
                        '/user/profile'
                    );
                }
            }
        } catch (error) {
            console.log('فشل التحقق من الردود:', error);
        }
    }

    // عرض إشعار
    function showNotification(title, message, type = 'info', link = null) {
        // إنشاء عنصر الإشعار
        const notification = document.createElement('div');
        notification.className = `fixed top-24 left-1/2 -translate-x-1/2 z-50 w-full max-w-md px-4 notification-slide`;
        
        const colors = {
            success: 'bg-green-500/20 border-green-500/50 text-green-400',
            error: 'bg-red-500/20 border-red-500/50 text-red-400',
            warning: 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400',
            info: 'bg-blue-500/20 border-blue-500/50 text-blue-400'
        };

        notification.innerHTML = `
            <div class="${colors[type] || colors.info} border rounded-xl p-4 flex justify-between items-center backdrop-blur">
                <div>
                    <p class="font-semibold">${title}</p>
                    <p class="text-sm opacity-80">${message}</p>
                </div>
                <div class="flex gap-2">
                    ${link ? `<a href="${link}" class="px-3 py-1 bg-white/10 rounded-lg hover:bg-white/20 transition">عرض</a>` : ''}
                    <button onclick="this.closest('.notification-slide').remove()" class="px-3 py-1 hover:bg-white/10 rounded-lg transition">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        `;

        document.body.appendChild(notification);

        // إزالة تلقائية بعد 5 ثواني
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(-50%) translateY(-20px)';
                setTimeout(() => notification.remove(), 300);
            }
        }, 5000);
    }

    // إشعار ترحيبي
    function showWelcomeNotification() {
        const isAuthenticated = document.body.dataset.userAuthenticated === 'true';
        if (isAuthenticated && !sessionStorage.getItem('welcomeShown')) {
            showNotification(
                'أهلاً بك!',
                'تم تسجيل دخولك بنجاح',
                'success'
            );
            sessionStorage.setItem('welcomeShown', 'true');
        }
    }

    // التحقق الدوري من الردود (كل 5 دقائق)
    setInterval(checkNewReplies, 5 * 60 * 1000);

    // التحقق عند تحميل الصفحة
    document.addEventListener('DOMContentLoaded', () => {
        checkNewReplies();
        showWelcomeNotification();
    });

    // تصدير الدوال للاستخدام العام
    window.GameNotifications = {
        show: showNotification,
        checkReplies: checkNewReplies
    };
})();
