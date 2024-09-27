from flask import Blueprint
from flask_restful import Api

# from .tasks import initiate_s3_fetch_script
from .views import S3ReportCallbackView, EmailReportCallbackView, EtzReportCallbackView
from .constants import S3_REPORT_CALLBACK_URL, EMAIL_REPORT_CALLBACK_URL, ETZ_REPORT_CALLBACK_URL

report_bp = Blueprint("report", __name__)
api = Api(report_bp)

api.add_resource(S3ReportCallbackView, S3_REPORT_CALLBACK_URL)
api.add_resource(EmailReportCallbackView, EMAIL_REPORT_CALLBACK_URL)
api.add_resource(EtzReportCallbackView, ETZ_REPORT_CALLBACK_URL)
