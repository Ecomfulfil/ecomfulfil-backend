DEBUG = True
SECRET_KEY = "django-insecure-@+a^w04ry+6=9n@7_yp2xe)0g^07*7hp&t=v8ve0w&brwe09e#"

LOGGING["formatters"]["colored"] = {  # type: ignore
    "()": "colorlog.ColoredFormatter",
    "format": "%(log_color)s%(asctime)s %(levelname)s %(name)s %(bold_white)s%(message)s",
}
LOGGING["loggers"]["core"]["level"] = "DEBUG"  # type: ignore
LOGGING["handlers"]["console"]["level"] = "DEBUG"  # type: ignore
LOGGING["handlers"]["console"]["formatter"] = "colored"  # type: ignore
