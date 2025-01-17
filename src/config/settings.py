"""
Django settings for yodaspeak project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import json
import os
from distutils.util import strtobool
from pathlib import Path

from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if it exists
if os.path.exists(os.path.join(BASE_DIR, ".env")):
    load_dotenv()

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

DEBUG = bool(strtobool(os.getenv("DEBUG", "false")))

CACHE_ENABLED = bool(strtobool(os.getenv("CACHE_ENABLED", "false")))

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# https://docs.djangoproject.com/en/5.1/ref/settings/#std:setting-ALLOWED_HOSTS
ALLOWED_HOSTS = list(map(str.strip, os.getenv("ALLOWED_HOSTS").split(",")))

# Application definitions
INSTALLED_APPS = [
    "yodaspeak.apps.PagesConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.contrib.psutil",
    "health_check.contrib.redis",
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

if DEBUG:
    INSTALLED_APPS = ["whitenoise.runserver_nostatic", "django_extensions"] + INSTALLED_APPS
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

ROOT_URLCONF = "config.urls"

# Starting with Django 4.1+ we need to pick which template loaders to use
# based on our environment since 4.1+ will cache templates by default.
default_loaders = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

cached_loaders = [("django.template.loaders.cached.Loader", default_loaders)]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "yodaspeak/templates")],
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
            "loaders": default_loaders if DEBUG else cached_loaders,
            "debug": DEBUG,
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASE_ENGINES = {
    "SQLITE": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "yodaspeak.db",
    },
    "POSTGRES": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    },
}
DATABASES = {"default": DATABASE_ENGINES[os.getenv("DATABASE_ENGINE", "SQLITE")]}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]

# Sessions
# https://docs.djangoproject.com/en/5.1/ref/settings/#sessions
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

if CACHE_ENABLED:
    # Redis
    REDIS_URL = os.getenv("REDIS_URL")

    # Caching
    # https://docs.djangoproject.com/en/5.1/topics/cache/
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_L10N = False
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# App Settings
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

YODASPEAK_PROMPT = ""
with open(os.path.join(BASE_DIR, "config/yodaspeak_prompt.txt"), "r") as file:
    YODASPEAK_PROMPT = file.read().strip()

TRANSLATE_SAMPLES = {}
if TRANSLATE_SAMPLES_ENABLED := bool(strtobool(os.getenv("TRANSLATE_SAMPLES_ENABLED", "false"))):
    translate_samples_path = os.path.join(BASE_DIR, "config/translate_samples.json")
    if os.path.exists(translate_samples_path):
        with open(translate_samples_path, "r") as file:
            TRANSLATE_SAMPLES = json.load(file)
