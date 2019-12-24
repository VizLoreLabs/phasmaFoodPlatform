from .base import *  # noqa
from .base import env

# DEBUG
# ----------------------------------------------------------------------------------------------------------------------
DEBUG = True

# SECURITY
# ----------------------------------------------------------------------------------------------------------------------
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="FSUQVk1VhM0eemFzaLDrJ7GkPyVSOsZXCccIUkFDrXFzzLoJbPAIGHKkuUQYDvQR",
)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# DATABASE
# ----------------------------------------------------------------------------------------------------------------------
MONGO_HOST = env("MONGO_DEV", default="localhost")

# CACHES
# ----------------------------------------------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

# EMAIL
# ----------------------------------------------------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025

# APPS
# ----------------------------------------------------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar", "django_extensions"]  # noqa F405
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]

# MIDDLEWARE
# ----------------------------------------------------------------------------------------------------------------------
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405
