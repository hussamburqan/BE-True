#!/usr/bin/env bash
set -e

python manage.py migrate --noinput

# ===== Superuser creation that respects USERNAME_FIELD & REQUIRED_FIELDS =====
python - <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE","true.settings"))
django.setup()
from django.contrib.auth import get_user_model

User = get_user_model()
username_field   = getattr(User, "USERNAME_FIELD", "username")     # غالبًا 'email'
required_fields  = list(getattr(User, "REQUIRED_FIELDS", []))       # عندك فيها tel_number على الأغلب

def env_for(field):
    return os.getenv(f"DJANGO_SU_{field.upper()}")  # مثال: DJANGO_SU_TEL_NUMBER

identifier = (
    os.getenv("DJANGO_SU_IDENTIFIER")               # يفضّل تحط الإيميل هون
    or env_for(username_field)
    or os.getenv("DJANGO_SU_EMAIL")
    or os.getenv("DJANGO_SU_NAME")
)
password = os.getenv("DJANGO_SU_PASS")

missing = []
if not identifier: missing.append(username_field)
if not password:   missing.append("password")

kwargs = {}
if identifier: kwargs[username_field] = identifier

# مرّر كل الحقول المطلوبة من REQUIRED_FIELDS (مثل tel_number)
for f in required_fields:
    val = env_for(f)
    if val: kwargs[f] = val
    else:   missing.append(f)

if missing:
    print("ℹ Skipping superuser creation; missing:", ", ".join(missing))
else:
    if User.objects.filter(**{username_field: identifier}).exists():
        print(f"ℹ Superuser already exists ({username_field}={identifier}).")
    else:
        User.objects.create_superuser(password=password, **kwargs)
        print(f"✔ Superuser created ({username_field}={identifier})")
PY

exec "$@"
