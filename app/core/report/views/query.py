from flask import request
from marshmallow import ValidationError
from http import HTTPStatus
from typing import cast

from app.core.schemas.report import MonthlyReportSchema
from app.core.utils.auth import IsAuthedUserMixin
from app.core.utils.http import Response

from report.queries import Report


class MonthlyReportView(IsAuthedUserMixin):
    schema = MonthlyReportSchema

    def get(self):
        try:
            params = cast(dict, self.schema().load(request.args.to_dict()))
            report = Report(report_type=params["service"]).query(params)
            return Response().success(report)
        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)
