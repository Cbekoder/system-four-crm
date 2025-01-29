from .base import *  # noqa


DEBUG = False

# Database

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": env.str("DB_NAME"),
#         "USER": env.str("DB_USER"),
#         "PASSWORD": env.str("DB_PASSWORD"),
#         "HOST": env.str("DB_HOST"),
#         "PORT": env.str("DB_PORT"),
#         "ATOMIC_REQUESTS": False,
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]