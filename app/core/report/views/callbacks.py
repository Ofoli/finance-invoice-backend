from flask import request
from marshmallow import ValidationError
from http import HTTPStatus
from werkzeug.datastructures.file_storage import FileStorage


from app.core.utils.auth import IsIPWhitelistedMixin
from app.core.utils.http import Response
from app.core.schemas.report import EmailReportCallbackDataSchema
from app.core.report.tasks import (
    handle_s3_report_callback,
    handle_email_report_callback,
    handle_etz_report_callback,
)
from app.core.report.utils.etz import save_etz_file


class S3ReportCallbackView(IsIPWhitelistedMixin):
    def get(self):
        task = handle_s3_report_callback.delay()  # type: ignore
        return Response().success(task.id)


class EtzReportCallbackView(IsIPWhitelistedMixin):
    def get(self):
        task = handle_etz_report_callback.delay()  # type: ignore
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
        try:
            validated_data = self.__schema().load(request.get_json())
            task = handle_email_report_callback.delay(validated_data)  # type: ignore
            return Response().success(task.id)
        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)
