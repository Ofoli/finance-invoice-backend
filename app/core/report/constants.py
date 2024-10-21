import os
from app.core.constants import FILES_DIR

# FILES
ETZ_SENT_FILES_DIR = os.path.join(FILES_DIR, "etz", "sent_files")
ETZ_STAT_FILES_DIR = os.path.join(FILES_DIR, "etz", "stat_files")
ETZ_REPORT_FILES_DIR = os.path.join(FILES_DIR, "etz", "reports")

# URLS
_s3_BASE_URL = os.environ.get("S3_BASE_URL", "")
_s7_BASE_URL = os.environ.get("S7_BASE_URL", "")
_s9_BASE_URL = os.environ.get("S9_BASE_URL", "")

INITIATE_FETCH_URL = f"{_s3_BASE_URL}/initiate-fetch.php"
INITIATE_ETZ_URL = f"{_s3_BASE_URL}/initiate-etz-report.php"
GET_RESELLER_USERS_URL = f"{_s3_BASE_URL}/get-reseller-users.php"
GET_USER_REPORT_URL = f"{_s3_BASE_URL}/report.php"
GET_BLASTS_URL = f"{_s7_BASE_URL}/blast"
GET_USER_RATE_URL = f"{_s7_BASE_URL}/fetch-rates.php/"
GET_S9_USER_REPORT = f"{_s9_BASE_URL}/network-report"


# ENDPOINTS
S3_REPORT_CALLBACK_URL = "/s3-callback"
ETZ_REPORT_CALLBACK_URL = "/etz-callback"
EMAIL_REPORT_CALLBACK_URL = "/email-report-callback"
MONTHLY_REPORT_URL = "/monthly-report"
TOP5_CLIENTS_STATS = "/top-five-clients"
YEARLY_SERVICE_STATS = "/yearly-service-counts"


# VALUES
S3_CLIENT_AID = "s3000000"
EMAIL_CLIENT_AID = "00000000"
DEFAULT_RATE = 0.032
DEFAULT_EMAIL_RATE = 0.04
NETWORKS = {
    "GLO": "23323",
    "EXPRESS0": "23328",
    "VODAFONE": "23350|23320",
    "AIRTELTIGO": "23327|23357|23326|23356",
    "MTN": "23324|23325|23359|23355|23354|23353",
}
CSV_SPACE_ROW = {
    "account": "",
    "network": "",
    "total_pages": "",
}
