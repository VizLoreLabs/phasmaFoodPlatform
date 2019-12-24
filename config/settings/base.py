"""
Base settings to build other settings files upon.
"""

import datetime
import environ

# PATHS
# ----------------------------------------------------------------------------------------------------------------------
ROOT_DIR = (environ.Path(__file__) - 3)
APPS_DIR = ROOT_DIR.path("phasma_food_v2")

# ENVIRONMENTAL VARIABLES
# ----------------------------------------------------------------------------------------------------------------------
env = environ.Env()
env.read_env(str(ROOT_DIR.path(".env")))


# TIMEZONE
# ----------------------------------------------------------------------------------------------------------------------
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True


# DATABASES
# ----------------------------------------------------------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL", default="postgres:///phasma_food_v2")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
MONGO_DEFAULT_DB = env("MONGO_DEFAULT_DB", None)
MONGO_DEFAULT_COLLECTION = env("MONGO_DEFAULT_COLLECTION", None)

# APPS
# ----------------------------------------------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
]
THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_auth",
    "rest_auth.registration",
    "django_celery_beat",
    "fcm_django",
    "corsheaders",
    "drf_yasg"
]
LOCAL_APPS = [
    "phasma_food_v2.users.apps.UsersConfig",
    "phasma_food_v2.statistic.apps.StatisticConfig",
    "phasma_food_v2.measurements.apps.MeasurementsConfig",
    "phasma_food_v2.devices.apps.DevicesConfig",
    "phasma_food_v2.dashboard.apps.DashboardConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATION
# ----------------------------------------------------------------------------------------------------------------------
MIGRATION_MODULES = {"sites": "phasma_food_v2.contrib.sites.migrations"}

# USER
# ----------------------------------------------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
AUTH_USER_MODEL = "users.User"
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
JWT_AUTH = {
    "JWT_ENCODE_HANDLER":
    "rest_framework_jwt.utils.jwt_encode_handler",

    "JWT_DECODE_HANDLER":
    "rest_framework_jwt.utils.jwt_decode_handler",

    "JWT_PAYLOAD_HANDLER":
    "rest_framework_jwt.utils.jwt_payload_handler",

    "JWT_PAYLOAD_GET_USER_ID_HANDLER":
    "rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler",

    "JWT_RESPONSE_PAYLOAD_HANDLER":
    "rest_framework_jwt.utils.jwt_response_payload_handler",

    "JWT_SECRET_KEY": env.str(
        "DJANGO_SECRET_KEY",
        default="FSUQVk1VhM0eemFzaLDrJ7GkPyVSOsZXCccIUkFDrXFzzLoJbPAIGHKkuUQYDvQR"
    ),
    "JWT_GET_USER_SECRET_KEY": None,
    "JWT_PUBLIC_KEY": None,
    "JWT_PRIVATE_KEY": None,
    "JWT_ALGORITHM": "HS256",
    "JWT_VERIFY": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LEEWAY": 0,
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=60*60*24),
    "JWT_AUDIENCE": None,
    "JWT_ISSUER": None,
    "JWT_ALLOW_REFRESH": True,
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=30),
    "JWT_AUTH_HEADER_PREFIX": "JWT",
    "JWT_AUTH_COOKIE": None,
}
ACCOUNT_ADAPTER = "phasma_food_v2.users.adapters.AccountAdapter"
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[PhasmaFood Team] "
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
REST_USE_JWT = True
REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "phasma_food_v2.users.serializers.UserDetailsSerializer",
    "LOGIN_SERIALIZER": "phasma_food_v2.users.serializers.UserLoginSerializer"

}
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'phasma_food_v2.users.serializers.UserRegisterSerializer',
}

# MIDDLEWARE
# ----------------------------------------------------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# STATIC
# ----------------------------------------------------------------------------------------------------------------------
STATIC_ROOT = str(ROOT_DIR("staticfiles"))
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(APPS_DIR.path("static"))]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ----------------------------------------------------------------------------------------------------------------------
MEDIA_ROOT = str(APPS_DIR("media"))
MEDIA_URL = "/media/"

# TEMPLATES
# ----------------------------------------------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "phasma_food_v2.utils.context_processors.settings_context",
            ],
        },
    }
]

# SECURITY
# ----------------------------------------------------------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
CORS_ORIGIN_ALLOW_ALL = True

# EMAIL
# ----------------------------------------------------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_TIMEOUT = 5

# ADMIN
# ----------------------------------------------------------------------------------------------------------------------
ADMIN_URL = "admin/"
ADMINS = [("""Predrag Orelj""", "predrag.orelj@vizlore.com")]
MANAGERS = ADMINS

# REST
# ----------------------------------------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
}

# LOGGING
# ----------------------------------------------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# CELERY
# ----------------------------------------------------------------------------------------------------------------------
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 60 * 60 * 12
CELERY_TASK_SOFT_TIME_LIMIT = 60 * 60 * 24
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# FIREBASE
# ----------------------------------------------------------------------------------------------------------------------
FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "Firebase",
    "FCM_SERVER_KEY": env.str("FCM_API_KEY"),
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
}

# DOCS
# ----------------------------------------------------------------------------------------------------------------------
DRF_YASG_EXCLUDE_VIEWS = []
