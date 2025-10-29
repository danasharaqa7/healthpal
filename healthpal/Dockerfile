# 1. ابدأ من صورة بايثون 3.10 نظيفة
FROM python:3.10-slim

# *** الخطوة الجديدة (v2.1) - تثبيت أدوات بناء mysqlclient ***
# هاي الأدوات ضرورية لترجمة مكتبة mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential

# 2. اعمل فولدر اسمه app جوا الصندوق
WORKDIR /app

# 3. انسخ ملف المكتبات (الوصفة)
COPY requirements.txt .

# 4. ثبت المكتبات اللي جوا الملف
RUN pip install -r requirements.txt

# 5. انسخ "كل" كود المشروع تاعنا (ملفاتنا الحالية) لجوا الصندوق
COPY . .

# 6. الأمر اللي رح يشتغل لما الصندوق يقوم
# (ملاحظة: اسم المشروع "healthpal" رح ننشئه كمان شوي)
CMD ["gunicorn", "healthpal.wsgi:application", "--bind", "0.0.0.0:8000"]