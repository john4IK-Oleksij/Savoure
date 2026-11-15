"""
Django settings for Savoure Restaurant project.
Production-ready template aligned with senior engineering roadmap.
"""

import os
from pathlib import Path
from typing import Any, cast

import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# Security settings
SECRET_KEY: str = os.getenv(
    "SECRET_KEY",
    "django-insecure-savoure-restaurant-secret-key-development-2026",
)

DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

_allowed_hosts: str = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,testserver")
ALLOWED_HOSTS: list[str] = [h.strip() for h in _allowed_hosts.split(",") if h.strip()]
if DEBUG and "testserver" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("testserver")

_csrf_trusted: str = os.getenv("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS: list[str] = [
    origin.strip() for origin in _csrf_trusted.split(",") if origin.strip()
]


# Application definition
INSTALLED_APPS: list[str] = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Savoure domain apps
    "core.apps.CoreConfig",
    "menu.apps.MenuConfig",
    "reservations.apps.ReservationsConfig",
    "blog.apps.BlogConfig",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF: str = "config.urls"

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION: str = "config.wsgi.application"


# Database
# If DATABASE_URL, MYSQL_URL, or MYSQLHOST is set (e.g. on Railway), use MySQL.
# Otherwise, fall back to local SQLite for development.
db_url: str = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL") or ""

if not db_url and os.getenv("MYSQLHOST"):
    mysql_user: str = os.getenv("MYSQLUSER", "root")
    mysql_password: str = os.getenv("MYSQLPASSWORD", "")
    mysql_host: str = os.getenv("MYSQLHOST", "localhost")
    mysql_port: str = os.getenv("MYSQLPORT", "3306")
    mysql_db: str = os.getenv("MYSQLDATABASE", "railway")
    db_url = f"mysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}"

_default_db: dict[str, Any] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

if db_url:
    _default_db = cast(
        dict[str, Any],
        dj_database_url.parse(
            db_url,
            conn_max_age=600,
            conn_health_checks=True,
        ),
    )

DATABASES: dict[str, dict[str, Any]] = {
    "default": _default_db,
}


# Password validation
AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization & Localization
LANGUAGE_CODE: str = "uk"
TIME_ZONE: str = "Europe/Kyiv"
USE_I18N: bool = True
USE_TZ: bool = True


# Static files (CSS, JavaScript, Images)
STATIC_URL: str = "static/"
STATICFILES_DIRS: list[Path] = [BASE_DIR / "static"]
STATIC_ROOT: Path = BASE_DIR / "staticfiles"

STORAGES: dict[str, dict[str, Any]] = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
WHITENOISE_MANIFEST_STRICT: bool = False

# Media files (User & Admin uploads)
MEDIA_URL: str = "media/"
MEDIA_ROOT: Path = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

# Production security headers
if not DEBUG:
    SECURE_PROXY_SSL_HEADER: tuple[str, str] = ("HTTP_X_FORWARDED_PROTO", "https")
    _ssl_redirect = os.getenv("SECURE_SSL_REDIRECT", "True").lower()
    SECURE_SSL_REDIRECT: bool = _ssl_redirect in ("true", "1", "yes")
    SECURE_BROWSER_XSS_FILTER: bool = True
    SECURE_CONTENT_TYPE_NOSNIFF: bool = True
    X_FRAME_OPTIONS: str = "DENY"
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    CSRF_COOKIE_SECURE: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"
    CSRF_COOKIE_SAMESITE: str = "Lax"
    SECURE_HSTS_SECONDS: int = 31536000  # 1 year HSTS
    SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = True
    SECURE_HSTS_PRELOAD: bool = True

    if SECRET_KEY.startswith("django-insecure-"):
        import warnings
        warnings.warn(
            "CRITICAL SECURITY WARNING: Production is running with default/insecure SECRET_KEY! "
            "Please set a strong SECRET_KEY in your Railway Variables.",
            stacklevel=2,
        )
