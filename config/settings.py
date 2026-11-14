"""
Django settings for Savoure Restaurant project.
Production-ready template aligned with senior engineering roadmap.
"""

import os
from pathlib import Path
from typing import Any

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


# Application definition
INSTALLED_APPS: list[str] = [
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Savoure domain apps
    "core.apps.CoreConfig",
    "menu.apps.MenuConfig",
    "reservations.apps.ReservationsConfig",
    "blog.apps.BlogConfig",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
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
# Using SQLite for fast development; ready for PostgreSQL swap
DATABASES: dict[str, dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
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

# Media files (User & Admin uploads)
MEDIA_URL: str = "media/"
MEDIA_ROOT: Path = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"
