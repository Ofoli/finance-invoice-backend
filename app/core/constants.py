import os

_BASE_APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR: str = os.path.join(_BASE_APP_DIR, "..", "logs")
FILES_DIR: str = os.path.join(_BASE_APP_DIR, "..", "files")


APP_LOGGER = "syslog"
JWT_SECRET = os.environ.get("JWT_SECRET", "")
WHITELISTED_IPS = os.environ.get("WHITELISTED_IPS", "")
