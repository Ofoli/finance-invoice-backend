from flask import request
from marshmallow import ValidationError
from http import HTTPStatus
from typing import cast

from app.core.schemas.report import MonthlyReportSchema, validate_client_service
from app.core.utils.auth import IsAuthedUserMixin
from app.core.utils.http import Response

from report.queries import Report, Statistics


class MonthlyReportView(IsAuthedUserMixin):
    schema = MonthlyReportSchema

    def get(self):
        try:
            params = cast(dict, self.schema().load(request.args.to_dict()))
            report = Report(report_type=params["service"]).query(params)
            return Response().success(report)
        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)


class TopFiveStatsView(IsAuthedUserMixin):
    def get(self):
        stats = Statistics().get_top5_clients_stats()
        return Response().success(stats)


class PastYearReportStats(IsAuthedUserMixin):
    def get(self):
        service = request.args.to_dict().get("service")
        if service and validate_client_service(service):
            stats = Statistics().get_service_yearly_stats(service)
            return Response().success(stats)
        return Response(HTTPStatus.BAD_REQUEST).failed("Invalid Service")
