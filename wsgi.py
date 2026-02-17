"""
WSGI entry point for ROKhub
استخدام: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
"""

from app import app

if __name__ == "__main__":
    app.run()
