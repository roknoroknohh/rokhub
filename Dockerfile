# Dockerfile for ROKhub
FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# تثبيت المتطلبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ المشروع
COPY . .

# إنشاء المجلدات اللازمة
RUN mkdir -p instance logs uploads

# المنفذ
EXPOSE 5000

# الأمر الافتراضي
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
