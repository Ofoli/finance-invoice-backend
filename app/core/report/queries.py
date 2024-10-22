from typing import List, Dict, Tuple, Union
from sqlalchemy import and_, desc, func, cast, String
from sqlalchemy.engine.row import Row

from app.config.extensions import db
from app.core.clients.queries import Client
from app.core.models.report import (
    ApiReport,
    BlastReport,
    EsmeReport,
    ApiEmailReport,
    WebEmailReport,
)
from app.core.schemas.report import ReportQuerySchema
from app.core.utils.enums import ReportType, ClientType
from app.core.report.utils.misc import get_report_period, get_year_period

Reports = List[Dict[str, str]]
SMSReportModel = Union[EsmeReport, ApiReport, BlastReport]


class Report:
    def __init__(self, report_type: int) -> None:
        self.__set_model(report_type=report_type)

    def __set_model(self, report_type: int) -> None:
        models = {
            ReportType.SMPP.value: EsmeReport,
            ReportType.SMSAPI.value: ApiReport,
            ReportType.SMSWEB.value: BlastReport,
            ReportType.EMAILAPI.value: ApiEmailReport,
            ReportType.EMAILWEB.value: WebEmailReport,
        }
        model = models.get(report_type)
        if model is None:
            raise ValueError(f"{report_type} is not a valid report type")

        self.__model = model

    def __to_internal_format(self, user_id: int, data: dict) -> dict:
        internal_format = dict(user_id=user_id)
        key_mapping = {
            EsmeReport: ["network", "total_pages"],
            ApiReport: ["network", "total_pages"],
            BlastReport: ["sent_date", "sender", "message", "total_pages"],
        }
        required_keys = key_mapping.get(self.__model, [])
        for key in required_keys:
            internal_format[key] = data[key]

        return internal_format

    def add(self, user_id: int, data: dict) -> None:
        formatted_data: dict = self.__to_internal_format(user_id, data)
        report = self.__model(**formatted_data)
        report.save()

    def query(self, filters: Dict[str, str]) -> List[Dict[str, str]]:
        report = (
            db.session.query(self.__model)
            .filter(
                and_(
                    self.__model.month >= filters["start_date"],
                    self.__model.month <= filters["end_date"],
                    self.__model.user_id == filters["user"],
                )
            )
            .all()
        )
        schema = ReportQuerySchema.create(self.__model)
        return schema(many=True).dump(report)


class Statistics:
    __model_mapping: dict = {
        ClientType.API.value: ApiReport,
        ClientType.BLAST.value: BlastReport,
        ClientType.ESME.value: EsmeReport,
    }

    def get_top5_clients_stats(self) -> List[dict]:
        client_stats = [
            {
                "id": user_id,
                "username": Client(client_type).get_client(user_id).username,
                "total_pages": total_pages,
            }
            for client_type, report_model in self.__model_mapping.items()
            for user_id, total_pages in self.__get_top5_stats_per_model(report_model)
        ]
        client_stats.sort(key=lambda report: report["total_pages"])
        return client_stats[-5:]

    def get_service_yearly_stats(self, service: str) -> List[dict]:
        model = self.__model_mapping.get(service)
        if model is None:
            return []
        return [
            {"month": month, "total_pages": total_pages}
            for month, total_pages in self.__get_year_stats_per_model(model)
        ]

    def __get_top5_stats_per_model(self, model: SMSReportModel) -> List[Row[Tuple[int, int]]]:
        total_pages_sum = func.sum(model.total_pages)
        start_date, end_date = get_report_period()
        return (
            db.session.query(model.user_id, total_pages_sum.label("total_pages_sum"))
            .filter(model.month > start_date, model.month <= end_date)
            .group_by(model.user_id)
            .order_by(desc("total_pages_sum"))
            .limit(5)
            .all()
        )

    def __get_year_stats_per_model(self, model: SMSReportModel):
        start_date, end_date = get_year_period()
        total_pages_sum = func.sum(model.total_pages)
        month_substr = func.substr(cast(model.month, String), 1, 7)
        return (
            db.session.query(month_substr, total_pages_sum.label("total_pages_sum"))
            .filter(model.month > start_date, model.month <= end_date)
            .group_by(month_substr)
        ).all()
