import os

BASE_APP_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_APP_DIR, "..", "logs")


APP_LOGGER = "syslog"
JWT_SECRET = os.environ.get("JWT_SECRET", "")
