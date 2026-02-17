"""
اختبارات أساسية لـ ROKhub
"""
import unittest
import sys
import os

# إضافة المسار الرئيسي
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import User, Game, Category


class ROKhubTestCase(unittest.TestCase):
    """اختبارات أساسية للتطبيق"""
    
    def setUp(self):
        """إعداد قبل كل اختبار"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """تنظيف بعد كل اختبار"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_index_page(self):
        """اختبار الصفحة الرئيسية"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_games_page(self):
        """اختبار صفحة الألعاب"""
        response = self.client.get('/games')
        self.assertEqual(response.status_code, 200)
    
    def test_online_games_page(self):
        """اختبار صفحة الألعاب الأونلاين"""
        response = self.client.get('/online-games')
        self.assertEqual(response.status_code, 200)
    
    def test_support_page(self):
        """اختبار صفحة الدعم"""
        response = self.client.get('/support')
        self.assertEqual(response.status_code, 200)
    
    def test_terms_page(self):
        """اختبار صفحة الشروط"""
        response = self.client.get('/terms')
        self.assertEqual(response.status_code, 200)
    
    def test_privacy_page(self):
        """اختبار صفحة الخصوصية"""
        response = self.client.get('/privacy')
        self.assertEqual(response.status_code, 200)
    
    def test_health_check(self):
        """اختبار فحص الصحة"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)
    
    def test_api_stats(self):
        """اختبار API الإحصائيات"""
        response = self.client.get('/api/stats')
        self.assertEqual(response.status_code, 200)
    
    def test_sitemap(self):
        """اختبار خريطة الموقع"""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
    
    def test_robots_txt(self):
        """اختبار robots.txt"""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
    
    def test_404_page(self):
        """اختبار صفحة 404"""
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)


class UserModelTestCase(unittest.TestCase):
    """اختبارات نموذج المستخدم"""
    
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_user_creation(self):
        """اختبار إنشاء مستخدم"""
        with self.app.app_context():
            user = User(
                username='testuser',
                email='test@example.com',
                is_admin=False
            )
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
            
            self.assertIsNotNone(user.id)
            self.assertEqual(user.username, 'testuser')
            self.assertTrue(user.check_password('testpassword'))
            self.assertFalse(user.check_password('wrongpassword'))


if __name__ == '__main__':
    unittest.main()
