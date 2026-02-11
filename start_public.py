import os
import time

print("🚀 تشغيل الموقع + ngrok...")
print("=" * 40)

# تشغيل Flask في الخلفية
os.system("python app.py &")

# انتظر قليلاً
time.sleep(3)

# تشغيل ngrok
print("🌐 تشغيل ngrok...")
os.system("ngrok http 5000")

