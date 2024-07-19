from .base import *

# Override base settings here
DEBUG = True

# Media and Static files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "../", "media")
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "../", "static")

ALLOWED_HOSTS = ["*"]
