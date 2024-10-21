from typing import List, Dict, Tuple, Union
from sqlalchemy import and_, desc, func
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
from app.core.utils.enums import ReportType, ClientType

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

    def __to_internal_format(self, user_id: int, month: str, data: dict) -> dict:
        internal_format = dict(user_id=user_id, month=month)
        key_mapping = {
            EsmeReport: ["network"],
            ApiReport: ["network", "total_pages"],
            BlastReport: ["sent_date", "sender", "message", "total_pages"],
        }
        required_keys = key_mapping.get(self.__model, [])
        for key in required_keys:
            internal_format[key] = data[key]

        return internal_format

    def add(self, user_id: int, month: str, data: dict) -> None:
        formatted_data: dict = self.__to_internal_format(user_id, month, data)
        report = self.__model(**formatted_data)
        report.save()

    def query(self, filters: Dict[str, str]) -> List[Dict[str, str]]:
        return (
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


class Statistics:
    __model_mapping: dict = {
        Client(ClientType.API.value): ApiReport,
        Client(ClientType.BLAST.value): BlastReport,
        Client(ClientType.ESME.value): EsmeReport,
    }

    def get_top5_clients_stats(self) -> List[dict]:
        client_stats = [
            {
                "id": user_id,
                "username": client_service.get_client(user_id).username,
                "total_pages": total_pages,
            }
            for client_service, report_model in self.__model_mapping.items()
            for user_id, total_pages in self.__get_top5_stats_per_model(report_model)
        ]
        client_stats.sort(key=lambda report: report["total_pages"])
        return client_stats[-5:]

    def get_service_yearly_stats(self, service: str) -> List[dict]:
        model = self.__model_mapping.get(Client(service))
        if model is None:
            return []
        return [
            {"month": month, "total_pages": total_pages}
            for month, total_pages in self.__get_year_stats_per_model(model)
        ]

    def __get_top5_stats_per_model(self, model: SMSReportModel) -> List[Row[Tuple[int, int]]]:
        total_pages_sum = func.sum(model.total_pages)
        return (
            db.session.query(model.user_id, total_pages_sum.label("total_pages_sum"))
            .filter(model.month > "2023-01-01", model.month < "2024-02-01")
            .group_by(model.user_id)
            .order_by(desc("total_pages_sum"))
            .limit(5)
            .all()
        )

    def __get_year_stats_per_model(self, model: SMSReportModel):
        total_pages_sum = func.sum(model.total_pages)
        return (
            db.session.query(model.month, total_pages_sum.label("total_pages_sum"))
            .filter(model.month > "2023-01-01", model.month < "2024-02-01")
            .group_by(model.month)
        ).all()
