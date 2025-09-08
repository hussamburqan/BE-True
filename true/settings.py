"""
Django settings for true project (local-friendly + Docker/Railway/Render ready).
Django 5.1.x
"""
from pathlib import Path
from datetime import timedelta
import os
import dj_database_url

# =========================
# Helpers
# =========================
def env_bool(key: str, default: str = "0") -> bool:
    return str(os.getenv(key, default)).lower() in {"1", "true", "yes", "on"}

def env_list(key: str, default: str = "") -> list[str]:
    return [x.strip() for x in os.getenv(key, default).split(",") if x.strip()]

# =========================
# Paths
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Core security & debug
# =========================
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_FOR_DEV_ONLY")
DEBUG = env_bool("DEBUG", "1")  # تشغيل محلي: 1

ALLOWED_HOSTS = env_list(
    "ALLOWED_HOSTS",
    "*" if DEBUG else "localhost,127.0.0.1,.onrender.com,.up.railway.app"
)

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost,http://127.0.0.1,http://localhost:3000,http://127.0.0.1:3000,https://*.onrender.com,https://*.up.railway.app"
)

# خلف بروكسي Render/Railway
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# تشديد الإنتاج (تلقائيًا عند عدم وجود DEBUG)
SECURE_SSL_REDIRECT   = env_bool("SECURE_SSL_REDIRECT", "0" if DEBUG else "1")
SESSION_COOKIE_SECURE = env_bool("SESSION_COOKIE_SECURE", "0" if DEBUG else "1")
CSRF_COOKIE_SECURE    = env_bool("CSRF_COOKIE_SECURE", "0" if DEBUG else "1")
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
        "DIRS": [BASE_DIR / "templates"],
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
# Database (PostgreSQL via DATABASE_URL, else SQLite)
# =========================
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()

if DATABASE_URL:
    # SSL مطلوب فقط إذا لسنا في DEBUG (إلا لو أجبرت بـ DB_SSL_REQUIRE)
    ssl_req = env_bool("DB_SSL_REQUIRE", "0" if DEBUG else "1")
    db_config = dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=ssl_req)
    # إن كان SQLite لا داعي لخيارات SSL
    if db_config.get("ENGINE", "").endswith("sqlite3"):
        db_config.pop("OPTIONS", None)
    DATABASES = {"default": db_config}
else:
    # تشغيل محلي سريع بدون أي إعداد خارجي
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
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
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Hebron")
USE_I18N = True
USE_TZ = True

# =========================
# Static & Media
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# قيم افتراضية للـ media عند العمل محليًا
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Django 5 STORAGES — عرّفه أولًا
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# بدّل التخزين الافتراضي إلى Cloudinary إذا كان المتغيّر موجود
USE_CLOUDINARY = bool(
    os.getenv("CLOUDINARY_URL") or
    (
        os.getenv("CLOUDINARY_CLOUD_NAME") and
        os.getenv("CLOUDINARY_API_KEY") and
        os.getenv("CLOUDINARY_API_SECRET")
    )
)

if USE_CLOUDINARY:
    STORAGES["default"] = {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    }
    # CKEditor يرفع على Cloudinary أيضًا
    CKEDITOR_UPLOAD_PATH = "uploads/"
    CKEDITOR_STORAGE_BACKEND = "cloudinary_storage.storage.MediaCloudinaryStorage"
# =========================
# CORS
# =========================
# التطوير: اسمح للكل إن لم تُحدّد Origins
CORS_ALLOW_ALL_ORIGINS = env_bool("CORS_ALLOW_ALL", "1" if DEBUG else "0")
CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS", "")
CORS_ALLOW_CREDENTIALS = env_bool("CORS_ALLOW_CREDENTIALS", "1")
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
# Email (from env)
# =========================
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", "1")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# رابط الواجهة الأمامية (اختياري)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# إبقاءه لو احتجته لأغراض أخرى
PASSWORD_RESET_TIMEOUT = int(os.getenv("PASSWORD_RESET_TIMEOUT", "600"))

# =========================
# CKEditor
# =========================
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": "100%",
    }
}

# =========================
# Third-party (Lahza) – from env
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


INSTALLED_APPS += [
    "cloudinary",
    "cloudinary_storage",
]
