from flask import request
from marshmallow import ValidationError
from http import HTTPStatus
from typing import Callable
from werkzeug.datastructures.file_storage import FileStorage


from app.core.utils.auth import IsIPWhitelistedMixin
from app.core.utils.http import Response
from app.core.schemas.report import EmailReportCallbackDataSchema
from ..tasks import handle_s3_report_callback, handle_email_report_callback, handle_etz_report_callback
from ..utils.etz import save_etz_file


def handle_post_callback(schema: Callable, task_method: Callable):
    try:
        validated_data = schema().load(request.get_json())
        task = task_method(validated_data).delay()
        return task.id
    except ValidationError as err:
        return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)


class S3ReportCallbackView(IsIPWhitelistedMixin):
    def get(self):
        task = handle_s3_report_callback().delay()
        return Response().success(task.id)


class EtzReportCallbackView(IsIPWhitelistedMixin):
    def get(self):
        task = handle_etz_report_callback().delay()
        return Response().success(task.id)


class EtzReportFileView(IsIPWhitelistedMixin):
    def post(self):
        zipped_file: FileStorage | None = request.files.get("file")
        if zipped_file is None:
            return Response(HTTPStatus.BAD_GATEWAY).failed("File is required")

        save_etz_file(zipped_file)
        return Response().success(True)


class EmailReportCallbackView(IsIPWhitelistedMixin):
    __schema = EmailReportCallbackDataSchema

    def post(self):
        return handle_post_callback(self.__schema, handle_email_report_callback)
