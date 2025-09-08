FROM python:3.12-slim
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
    
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN useradd -u 10001 -ms /bin/bash django || true \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R django:django /app

USER django

CMD ["bash", "-lc", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn true.wsgi:application -c gunicorn.conf.py"]
