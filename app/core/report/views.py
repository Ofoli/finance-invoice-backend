from http import HTTPStatus
from typing import List, Any
from flask import request, abort
from marshmallow import ValidationError
from flask_restful import Resource


from .tasks import handle_s3_report_callback


class S3ReportCallbackView(Resource):
    def get(self):
        res = handle_s3_report_callback.delay()  # type: ignore
        return res.id
