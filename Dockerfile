# ====== base ======
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# create user & fix permissions BEFORE switching user
# ملاحظة: لو المستخدم موجود مسبقًا، تجاهل الخطأ
RUN useradd -u 10001 -ms /bin/bash django || true \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R django:django /app

USER django

# run
CMD ["bash", "-lc", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn true.wsgi:application -c gunicorn.conf.py"]
