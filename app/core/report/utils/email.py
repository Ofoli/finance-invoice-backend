import logging
from typing import Optional

from app.core.clients.queries import Client, ModelClient
from app.core.utils.enums import ClientType, ReportType
from app.core.constants import APP_LOGGER

from app.core.report.constants import EMAIL_CLIENT_AID, DEFAULT_EMAIL_RATE
from app.core.report.queries import Report
from app.core.report.utils.misc import extract_reseller_prefix

logger: logging.Logger = logging.getLogger(APP_LOGGER)


def save_email_reports(reports: list[dict], client_type: ClientType) -> None:
    client_service = Client(client_type.value)
    report_service = Report(ReportType.EMAILAPI)

    for report in reports:
        username: str = report["username"]
        account: Optional[ModelClient] = client_service.get_client_by_username(username=username)

        if account is None:
            try:
                account = _create_email_client(username, client_type)
            except Exception as e:
                logger.error(f"failed to create email client for {username}, error:{e}")
                logger.error(f"Could not save email report for {username}, report:{report}")
                continue

        report_service.add(user_id=account.id, data=report)  # type: ignore


def _get_type_defaults(client_type: ClientType, username: str) -> dict:
    if client_type.value == ClientType.BLAST.value:
        return dict(key_id=EMAIL_CLIENT_AID)
    return dict(
        reseller_prefix=extract_reseller_prefix(username),
        aid=EMAIL_CLIENT_AID,
    )


def _fetch_email_rate(username: str) -> float:
    return DEFAULT_EMAIL_RATE


def _create_email_client(username: str, client_type: ClientType) -> ModelClient:
    return Client(client_type.value).create(
        dict(
            **_get_type_defaults(client_type, username),
            rate=_fetch_email_rate(username),
            username=username,
            has_email=True,
        )
    )
