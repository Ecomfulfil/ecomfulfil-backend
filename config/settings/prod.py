from .base import *

# Override base settings here
DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
