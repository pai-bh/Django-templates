from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Log setting
LOG_LEVEL = 'INFO'

LOGGING['handlers']['console']['level'] = LOG_LEVEL
LOGGING['handlers']['django.server']['level'] = LOG_LEVEL
LOGGING['loggers']['console']['level'] = LOG_LEVEL
LOGGING['loggers']['django.server']['level'] = LOG_LEVEL
