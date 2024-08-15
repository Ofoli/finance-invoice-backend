from flask import Blueprint
from flask_restful import Api

from ..models.report import ApiReport, BlastReport, EsmeReport
from .tasks import test_celery

report_bp = Blueprint("report", __name__)
api = Api(report_bp)
