"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os
from core.config import settings
from celery.beat import crontab
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = settings.SECRET_KEY

DEBUG = settings.DEBUG

ALLOWED_HOSTS = settings.ALLOWED_HOSTS.get_secret_value().split(",")


# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # libraris
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_yasg",
    "django_filters",
    # apps
    "applications.account",
    "applications.product",
    "applications.subscriptions",
    "applications.countries",
    "applications.comment",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.db.DB_NAME.get_secret_value(),
        "USER": settings.db.DB_USER.get_secret_value(),
        "PASSWORD": settings.db.DB_PASSWORD.get_secret_value(),
        "HOST": settings.db.DB_HOST,
        "PORT": settings.db.DB_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Bishkek"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "account.CustomUser"


CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "permissions.permissions.IsNotBlocked",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=500),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": settings.JWT_SECRET_KEY.get_secret_value(),
}

CACHE_MIDDLEWARE_SECONDS = 3


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # ログ出力フォーマットの設定
    "formatters": {
        "production": {
            "format": "%(asctime)s [%(levelname)s] %(process)d %(thread)d "
            "%(lineno)d %(message)s"
        },
    },
    # ハンドラの設定
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "production",
        },
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    # ロガーの設定
    "loggers": {
        # 自分で追加したアプリケーション全般のログを拾うロガー
        "": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
        # Django自身が出力するログ全般を拾うロガー
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

CELERY_BROKER_URL = settings.CELERY_BROKER_URL
CELERY_BROKER_TRANSPORT = settings.CELERY_BROKER_TRANSPORT

CELERY_BEAT_SCHEDULE = {
    "sample_task": {
        "task": "applications.countries.tasks.country_task",
        "schedule": crontab(minute="*/720"),
    },
    "lift-posts-every-minute": {
        "task": "applications.product.tasks.lift_posts",
        "schedule": crontab(minute="*/1"),
    },
}
