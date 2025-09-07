"""
Django settings for true project (Railway + Docker + Postgres ready).
Django 5.1.x
"""
from pathlib import Path
from datetime import timedelta
import os
import dj_database_url

# =========================
# Paths & basics
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Core security & debug
# =========================
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_FOR_DEV_ONLY")
DEBUG = os.getenv("DEBUG", "0") == "1"

ALLOWED_HOSTS = [h.strip() for h in os.getenv(
    "ALLOWED_HOSTS",
    ".up.railway.app,localhost,127.0.0.1"
).split(",") if h.strip()]

CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://*.up.railway.app,https://localhost"
).split(",") if o.strip()]

# Running behind Railway proxy
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Extra production hardening (auto when not DEBUG)
SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "1") == "1" and not DEBUG
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "1") == "1" and not DEBUG
CSRF_COOKIE_SECURE = os.getenv("CSRF_COOKIE_SECURE", "1") == "1" and not DEBUG
X_FRAME_OPTIONS = "DENY"

# =========================
# Installed apps
# =========================
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "ckeditor",
    "ckeditor_uploader",

    # Local apps
    "authentiocation",
    "blog",
    "courses",
    "companies",
    "partners",
    "testimonials",
    "services",
    "portfolio",
    "team",
    "audit",
    "careers",
    "enrollments",
]

# =========================
# Middleware (WhiteNoise + CORS)
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # static files
    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "true.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # إن احتجت قوالب
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "true.wsgi.application"

# =========================
# Database (PostgreSQL via DATABASE_URL)
# =========================
# مثال لقيمة DATABASE_URL من Railway:
# postgres://user:pass@host:port/dbname
DATABASES = {
    "default": dj_database_url.config(
        env="DATABASE_URL",
        default=None,  
        conn_max_age=600,
        ssl_require=True,
    )
}
# =========================
# Auth / User Model
# =========================
AUTH_USER_MODEL = "authentiocation.User"

# =========================
# Password validation
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================
# Internationalization
# =========================
LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en-us")
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Hebron")  # افتراضيًا حسب منطقتك
USE_I18N = True
USE_TZ = True

# =========================
# Static & Media (WhiteNoise)
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Django 5 STORAGES (WhiteNoise for static)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# =========================
# CORS
# =========================
# للإنتاج، يفضّل تحديد CORS_ALLOWED_ORIGINS بدل السماح للكل
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL", "0") == "1"
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()]
CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "1") == "1"
CORS_ALLOW_HEADERS = [
    "authorization",
    "content-type",
    "x-is-admin",
]

# =========================
# DRF & JWT
# =========================
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.getenv("PAGE_SIZE", "10")),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_LIFETIME_MIN", "120"))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=int(os.getenv("REFRESH_TOKEN_LIFETIME_DAYS", "90"))
    ),
    "BLACKLIST_AFTER_ROTATION": True,
}

# =========================
# Email (all from env)
# =========================
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "1") == "1"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# في حال استعملته بمكان: رابط الواجهة الأمامية (اختياري)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:4200")

# إبقاءه لو بتحتاجه لأغراض ثانية (حتى لو لغينا مسارات نسيان كلمة المرور)
PASSWORD_RESET_TIMEOUT = int(os.getenv("PASSWORD_RESET_TIMEOUT", "600"))

# =========================
# CKEditor
# =========================
CKEDITOR_UPLOAD_PATH = "uploads/"
# مثال إعدادات (اختياري):
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
    }
}

# =========================
# Third-party (Lahza) – من env
# =========================
LAHZA_SECRET_KEY = os.getenv("LAHZA_SECRET_KEY", "")
LAHZA_PUBLIC_KEY = os.getenv("LAHZA_PUBLIC_KEY", "")
LAHZA_API_BASE = os.getenv("LAHZA_API_BASE", "https://api.lahza.io")
LAHZA_CALLBACK_URL = os.getenv("LAHZA_CALLBACK_URL", "http://127.0.0.1:8000/payments/callback/")

# =========================
# Audit retention
# =========================
AUDITLOG_RETENTION_DAYS = int(os.getenv("AUDITLOG_RETENTION_DAYS", "7"))

# =========================
# Default PK field
# =========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# Logging (console)
# =========================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "django.request": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
    },
}
