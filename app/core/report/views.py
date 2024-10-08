from typing import Any
from flask import request
from marshmallow import ValidationError
from http import HTTPStatus


from app.core.utils.auth import IsIPWhitelistedMixin
from app.core.utils.http import Response
from app.core.schemas.report import EmailReportCallbackDataSchema
from .tasks import handle_s3_report_callback, handle_email_report_callback


class S3ReportCallbackView(IsIPWhitelistedMixin):
    def get(self):
        res: Any = handle_s3_report_callback.delay()  # type: ignore
        return res.id


class EmailReportCallbackView(IsIPWhitelistedMixin):
    __schema = EmailReportCallbackDataSchema

    def post(self):
        try:
            validated_data = self.__schema().load(request.get_json())
            result = handle_email_report_callback(validated_data).delay()
            return result.id
        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)
