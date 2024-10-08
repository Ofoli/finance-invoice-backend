from typing import List, Dict
from sqlalchemy import and_

from app.config.extensions import db
from app.core.models.report import ApiReport, BlastReport, EsmeReport, ApiEmailReport, WebEmailReport
from app.core.utils.enums import ReportType


class Report:
    def __init__(self, report_type: ReportType) -> None:
        self.__set_model(report_type=report_type)

    def __set_model(self, report_type: ReportType) -> None:
        models = {
            ReportType.SMPP.value: EsmeReport,
            ReportType.SMSAPI.value: ApiReport,
            ReportType.SMSWEB.value: BlastReport,
            ReportType.EMAILAPI.value: ApiEmailReport,
            ReportType.EMAILWEB.value: WebEmailReport,
        }
        model = models.get(report_type.value)
        if model is None:
            raise ValueError(f"{report_type} is not a valid report type")

        self._model = model

    def __to_internal_format(self, user_id: int, month: str, data: dict) -> dict:
        internal_format = dict(user_id=user_id, month=month)
        key_mapping = {
            EsmeReport: ["network"],
            ApiReport: ["network", "page_count"],
            BlastReport: ["sent_date", "sender", "message", "total_pages"],
        }
        required_keys = key_mapping.get(self._model, [])
        for key in required_keys:
            internal_format[key] = data[key]

        return internal_format

    def add(self, user_id: int, month: str, data: dict) -> None:
        formatted_data: dict = self.__to_internal_format(user_id, month, data)
        report = self._model(**formatted_data)
        report.save()

    def query(self, filters: Dict[str, str]) -> List[dict]:
        return (
            db.session.query(self._model)
            .filter(
                and_(
                    self._model.month >= filters["start_date"],
                    self._model.month <= filters["end_date"],
                    self._model.user_id == filters["user"],
                )
            )
            .all()
        )
