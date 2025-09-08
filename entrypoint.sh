#!/usr/bin/env bash
set -e

python manage.py migrate --noinput

# ===== Superuser creation (works with custom user model) =====
python - <<'PY'
import os, django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "true.settings")
)
django.setup()
from django.contrib.auth import get_user_model

User = get_user_model()
username_field = getattr(User, "USERNAME_FIELD", "username")  # غالبًا 'email'
identifier = (
    os.getenv("DJANGO_SU_IDENTIFIER")
    or os.getenv("DJANGO_SU_EMAIL")
    or os.getenv("DJANGO_SU_NAME")
)
password = os.getenv("DJANGO_SU_PASS")
email = os.getenv("DJANGO_SU_EMAIL")
name = os.getenv("DJANGO_SU_NAME")

if identifier and password:
    # هل يوجد بالفعل؟
    exists = User.objects.filter(**{username_field: identifier}).exists()
    if exists:
        print(f"ℹ Superuser already exists ({username_field}={identifier}).")
    else:
        kwargs = {username_field: identifier}
        # لو في حقل email إضافي (وأحيانًا USERNAME_FIELD نفسه هو email)
        if email:
            kwargs.setdefault("email", email)
        # لو عندك حقل name في المودل
        if name and hasattr(User, "name"):
            kwargs.setdefault("name", name)
        # أنشئ السوبر يوزر
        u = User.objects.create_superuser(password=password, **kwargs)
        print(f"✔ Superuser created with {username_field}={identifier}")
else:
    print("ℹ Missing DJANGO_SU_IDENTIFIER/EMAIL/NAME or DJANGO_SU_PASS; skipping.")
PY

exec "$@"
