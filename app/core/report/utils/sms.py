import logging

from typing import Callable, List, Optional

from app.core.clients.queries import ModelClient, Client
from app.core.constants import APP_LOGGER
from app.core.report.queries import Report
from app.core.utils.enums import ReportType, ClientType

ReportSaver = Callable[[List[dict]], None]

logger = logging.getLogger(APP_LOGGER)


def _save_reports(client_type: ClientType, report_type: ReportType) -> ReportSaver:
    client_service = Client(client_type.value)
    report_service = Report(report_type)

    def saver(reports: List[dict]) -> None:
        for data in reports:
            username = data.get("account")
            if username:
                user: Optional[ModelClient] = client_service.get_client_by_username(
                    username=username
                )
                if user is None:
                    key = f"Report<type={report_type.value}, username={username}>"
                    logger.error(f"user not found for {key}")
                    continue

                report_service.add(user_id=user.id, data=data)  # type: ignore

    return saver


save_esme_reports: ReportSaver = _save_reports(ClientType.ESME, ReportType.SMPP)
save_sms_api_reports: ReportSaver = _save_reports(ClientType.API, ReportType.SMSAPI)
save_sms_web_reports: ReportSaver = _save_reports(ClientType.BLAST, ReportType.SMSWEB)
