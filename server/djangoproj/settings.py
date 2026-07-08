"""
Django settings for djangoproj (Cars Dealership capstone project).
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-capstone-dev-key-do-not-use-in-real-production",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

# Hosts like Render terminate TLS at a proxy and forward plain HTTP with this
# header, so Django needs to be told how to recognize an HTTPS request -
# otherwise request.is_secure() is wrong and CSRF/admin login breaks.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "djangoapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djangoproj.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "djangoapp" / "templates"],
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

WSGI_APPLICATION = "djangoproj.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "frontend" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Capstone microservice endpoints -------------------------------------------------
# Locally these are set as full URLs (BACKEND_URL/SENTIMENT_ANALYZER_URL, with
# scheme). On Render, fromService: property: host only gives the public
# hostname's subdomain label (e.g. "dealership-database-c6e9"), not a full
# domain - so BACKEND_HOST/SENTIMENT_ANALYZER_HOST take priority when set,
# and the public "https://<host>.onrender.com" URL is reconstructed from it.
_backend_host = os.environ.get("BACKEND_HOST")
BACKEND_URL = (
    f"https://{_backend_host}.onrender.com" if _backend_host
    else os.environ.get("BACKEND_URL", "http://localhost:3030")
)

_sentiment_host = os.environ.get("SENTIMENT_ANALYZER_HOST")
SENTIMENT_ANALYZER_URL = (
    f"https://{_sentiment_host}.onrender.com" if _sentiment_host
    else os.environ.get("SENTIMENT_ANALYZER_URL", "http://localhost:5050")
)

LOGIN_REDIRECT_URL = "/"
# No LOGOUT_REDIRECT_URL: the Django admin's own logout view should show its
# default "logged out" confirmation template rather than bouncing back to the
# React site (djangoapp's own /djangoapp/logout API is unaffected by this
# setting since it calls django.contrib.auth.logout() directly).
