from flask import Blueprint
from flask_restful import Api

from .tasks import test_celery, initiate_s3_fetch_script

report_bp = Blueprint("report", __name__)
api = Api(report_bp)
