# URLS
_S3_BASE_URL = "http://5.9.79.123/eomreport/invoice/api"
_s7_BASE_URL = "https://api.nalosolutions.com:8888/lmensah"

INITIATE_FETCH_URL = f"{_S3_BASE_URL}/initiate-fetch.php"
INITIATE_ETZ_URL = f"{_S3_BASE_URL}/initiate-etz-report.php"
GET_RESELLER_USERS_URL = f"{_S3_BASE_URL}/get-reseller-users.php"
GET_USER_REPORT_URL = f"{_S3_BASE_URL}/report.php"
GET_S9_USER_REPORT = "http://95.217.203.30:6610/reports/network-report"


GET_BLASTS_URL = f"{_s7_BASE_URL}/blast"
GET_USER_RATE_URL = f"{_s7_BASE_URL}/fetch-rates.php/"


# ENDPOINTS
S3_REPORT_CALLBACK_URL = "/s3-callback"
ETZ_REPORT_CALLBACK_URL = "/etz-callback"


# VALUES
S3_CLIENT_AID = "s3clientaid"
DEFAULT_RATE = 0.032
NETWORKS = {
    "GLO": "23323",
    "EXPRESS0": "23328",
    "VODAFONE": "23350|23320",
    "AIRTELTIGO": "23327|23357|23326|23356",
    "MTN": "23324|23325|23359|23355|23354|23353"
}
ESME_SPACE_ROW = {
    "account": "",
    "network": "",
    "count": "",
}
ALERTS_SPACE_ROW = {**ESME_SPACE_ROW, "page_count": ""}
