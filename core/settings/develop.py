from .base import *  # noqa

DEBUG = True

STATICFILES_DIRS = (BASE_DIR / "static",)

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if env.bool("USE_POSTGRES", False):
# if env.bool("USE_POSTGRES", False):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.str("DB_NAME"),
            "USER": env.str("DB_USER"),
            "PASSWORD": env.str("DB_PASSWORD"),
            "HOST": env.str("DB_HOST"),
            "PORT": env.str("DB_PORT"),
            "ATOMIC_REQUESTS": False,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }