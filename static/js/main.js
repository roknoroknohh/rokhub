// الملف الرئيسي لوظائف الموقع
(function() {
    'use strict';

    // ==================== الوضع المظلم ====================
    const ThemeManager = {
        init() {
            const savedTheme = localStorage.getItem('theme') || 'dark';
            this.setTheme(savedTheme);
            this.setupToggle();
        },

        setTheme(theme) {
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            
            // تحديث أيقونة الزر
            const toggleBtn = document.getElementById('theme-toggle');
            if (toggleBtn) {
                const icon = theme === 'dark' ? 'fa-sun' : 'fa-moon';
                toggleBtn.innerHTML = `<i class="fas ${icon}"></i>`;
            }
        },

        toggle() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            this.setTheme(newTheme);
        },

        setupToggle() {
            const toggleBtn = document.getElementById('theme-toggle');
            if (toggleBtn) {
                toggleBtn.addEventListener('click', () => this.toggle());
            }
        }
    };

    // ==================== البحث المباشر ====================
    const SearchManager = {
        init() {
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                let debounceTimer;
                searchInput.addEventListener('input', (e) => {
                    clearTimeout(debounceTimer);
                    debounceTimer = setTimeout(() => {
                        this.performSearch(e.target.value);
                    }, 300);
                });
            }
        },

        async performSearch(query) {
            if (query.length < 2) return;
            
            try {
                const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
                if (response.ok) {
                    // إعادة توجيه لصفحة البحث
                    window.location.href = `/search?q=${encodeURIComponent(query)}`;
                }
            } catch (error) {
                console.error('خطأ في البحث:', error);
            }
        }
    };

    // ==================== تأثيرات التمرير ====================
    const ScrollEffects = {
        init() {
            this.setupScrollToTop();
            this.setupNavbarScroll();
            this.setupFadeInOnScroll();
        },

        setupScrollToTop() {
            const btn = document.getElementById('scroll-to-top');
            if (!btn) return;

            window.addEventListener('scroll', () => {
                if (window.scrollY > 300) {
                    btn.classList.remove('opacity-0', 'pointer-events-none');
                } else {
                    btn.classList.add('opacity-0', 'pointer-events-none');
                }
            });

            btn.addEventListener('click', () => {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
        },

        setupNavbarScroll() {
            const navbar = document.querySelector('nav');
            if (!navbar) return;

            let lastScroll = 0;
            window.addEventListener('scroll', () => {
                const currentScroll = window.scrollY;
                
                if (currentScroll > 100) {
                    navbar.classList.add('shadow-lg');
                } else {
                    navbar.classList.remove('shadow-lg');
                }
                
                lastScroll = currentScroll;
            });
        },

        setupFadeInOnScroll() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in-visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.1 });

            document.querySelectorAll('.fade-in').forEach(el => {
                observer.observe(el);
            });
        }
    };

    // ==================== تحميل الصور ====================
    const ImageLoader = {
        init() {
            this.setupLazyLoading();
            this.setupImageErrorHandling();
        },

        setupLazyLoading() {
            if ('IntersectionObserver' in window) {
                const imageObserver = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            const img = entry.target;
                            img.src = img.dataset.src || img.src;
                            img.classList.remove('lazy');
                            imageObserver.unobserve(img);
                        }
                    });
                });

                document.querySelectorAll('img.lazy').forEach(img => {
                    imageObserver.observe(img);
                });
            }
        },

        setupImageErrorHandling() {
            document.querySelectorAll('img').forEach(img => {
                img.addEventListener('error', () => {
                    img.src = '/static/images/placeholder-game.png';
                    img.classList.add('image-error');
                });
            });
        }
    };

    // ==================== نسخ الروابط ====================
    const ClipboardManager = {
        init() {
            document.querySelectorAll('[data-copy]').forEach(btn => {
                btn.addEventListener('click', async (e) => {
                    const text = e.currentTarget.dataset.copy;
                    try {
                        await navigator.clipboard.writeText(text);
                        this.showToast('تم النسخ!');
                    } catch (err) {
                        this.showToast('فشل النسخ', 'error');
                    }
                });
            });
        },

        showToast(message, type = 'success') {
            const toast = document.createElement('div');
            toast.className = `fixed bottom-4 left-1/2 -translate-x-1/2 px-6 py-3 rounded-lg z-50 ${
                type === 'success' ? 'bg-green-600' : 'bg-red-600'
            } text-white`;
            toast.textContent = message;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 300);
            }, 2000);
        }
    };

    // ==================== عدادات الإحصائيات ====================
    const StatsCounter = {
        init() {
            document.querySelectorAll('[data-count]').forEach(el => {
                this.animateCounter(el);
            });
        },

        animateCounter(el) {
            const target = parseInt(el.dataset.count);
            const duration = 2000;
            const step = target / (duration / 16);
            let current = 0;

            const timer = setInterval(() => {
                current += step;
                if (current >= target) {
                    el.textContent = target.toLocaleString();
                    clearInterval(timer);
                } else {
                    el.textContent = Math.floor(current).toLocaleString();
                }
            }, 16);
        }
    };

    // ==================== تأكيد الحذف ====================
    const ConfirmManager = {
        init() {
            document.querySelectorAll('[data-confirm]').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const message = btn.dataset.confirm || 'هل أنت متأكد؟';
                    if (!confirm(message)) {
                        e.preventDefault();
                    }
                });
            });
        }
    };

    // ==================== تهيئة ====================
    document.addEventListener('DOMContentLoaded', () => {
        ThemeManager.init();
        SearchManager.init();
        ScrollEffects.init();
        ImageLoader.init();
        ClipboardManager.init();
        StatsCounter.init();
        ConfirmManager.init();
    });

    // ==================== تصدير ====================
    window.GameHub = {
        ThemeManager,
        SearchManager,
        ScrollEffects,
        ImageLoader,
        ClipboardManager,
        StatsCounter,
        ConfirmManager
    };
})();
