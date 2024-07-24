from pathlib import Path

from split_settings.tools import include

from core.general.utils.pytest import is_pytest_running

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENVVAR_SETTINGS_PREFIX = "ECOMFULFIL_"

include(
    "base.py",
    "envvars.py",
    "logging.py",
    "rest_framework.py",
    "channels.py",
    "aws.py",
    "custom.py",
    "mail.py",
    "docker.py",
)

if not is_pytest_running():
    assert SECRET_KEY is not NotImplemented  # type: ignore # noqa: F821
