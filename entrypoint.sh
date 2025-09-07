#!/usr/bin/env bash
set -e

python manage.py migrate --noinput

# إنشاء سوبر يوزر اختياري عبر ENV
python - <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE","true.settings"))
django.setup()
from django.contrib.auth import get_user_model
U, E, P = os.getenv("DJANGO_SU_NAME"), os.getenv("DJANGO_SU_EMAIL"), os.getenv("DJANGO_SU_PASS")
if U and E and P:
    User = get_user_model()
    if not User.objects.filter(username=U).exists():
        User.objects.create_superuser(U, E, P)
        print(f"✔ Superuser created: {U}")
    else:
        print("ℹ Superuser already exists.")
else:
    print("ℹ No superuser env vars set. Skipping.")
PY

exec "$@"
