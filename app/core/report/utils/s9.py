import logging

from app.core.clients.queries import Client
from app.core.models.user import ApiClient, BlastClient, ESMEClient
from app.core.utils.enums import ClientType
from app.core.constants import APP_LOGGER

from ..constants import EMAIL_CLIENT_AID, DEFAULT_EMAIL_RATE
from .misc import extract_reseller_prefix

logger: logging.Logger = logging.getLogger(APP_LOGGER)


def save_email_report(reports: list[dict], client_type: ClientType, month: str) -> None:
    client = Client(client_type.value)

    for report in reports:
        username: str = report["username"]
        account = client.get_client_by_username(username=username)

        if account is None:
            try:
                account = _create_email_client(username, client_type)
            except Exception as e:
                logger.error("failed to create email client for {}, error:{}".format(username, e))
                logger.error("Could not save email report for {}, report:{}".format(username, report))
                continue
        # update save report in db
        logger.info("saving report for id {}, report:{}".format(account.id, report))


def _get_type_defaults(client_type: ClientType, username: str) -> dict:
    if client_type.value == ClientType.API.value:
        return dict(reseller_prefix=extract_reseller_prefix(username))
    return dict(is_reseller=False, user_id=EMAIL_CLIENT_AID, reseller_id=EMAIL_CLIENT_AID)


def _fetch_email_rate(username: str) -> float:
    return DEFAULT_EMAIL_RATE


def _create_email_client(username: str, client_type: ClientType) -> ApiClient | BlastClient | ESMEClient:
    return Client(client_type.value).create(
        dict(
            **_get_type_defaults(client_type, username),
            rate=_fetch_email_rate(username),
            aid=EMAIL_CLIENT_AID,
            username=username,
            has_email=True,
        )
    )
