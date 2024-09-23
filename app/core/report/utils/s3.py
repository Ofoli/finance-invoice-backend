import logging

from ...clients.queries import Client
from ...utils.enums import ClientType
from ...constants import APP_LOGGER
from ...utils.http import Request

from ..constants import (
    GET_USER_REPORT_URL,
    GET_S9_USER_REPORT,
    GET_RESELLER_USERS_URL,
    S3_CLIENT_AID,
)

from .misc import get_previous_month, get_report_period
from .s7 import fetch_user_rate


logger: logging.Logger = logging.getLogger(APP_LOGGER)


def get_initiate_fetch_payload() -> dict[str, list[str] | str]:
    payload = dict(esmes=[], apiusers=[], resellers=[])
    clients = Client.get_all()

    for client_type, data in clients.items():
        if client_type == ClientType.API.value:
            for client in data:
                if client.reseller_prefix:  # type: ignore
                    payload['resellers'].append(
                        client.reseller_prefix)  # type: ignore
                else:
                    payload['apiusers'].append(client.username)
        if client_type == ClientType.ESME.value:
            payload['esmes'] = [client.username for client in data]

    return {**payload, "date": get_previous_month()}


def handle_s3_script_response(name: str, status: bool, data: str | dict) -> dict[str, str | dict]:
    if not status:
        logger.error(f"{name} report script initiation failed: {data}")
        # send email or sms alert
        return dict(error=data)

    logger.info(f"{name} report script initiated: {data}")
    return dict(data=data)


def _fetch_report(url: str) -> list:
    status, data = Request.get(url)
    if status and not isinstance(data, str) and data.get("status"):
        return data["data"]

    logger.error(f"failed to fetch report with url:{url}")
    return []


def fetch_s3_user_report(username: str) -> list:
    logger.info(f"fetching report for user: {username}")
    url = f"{GET_USER_REPORT_URL}?username={username}"
    return report[0]["data"] if len(report := _fetch_report(url)) else []


def fetch_s9_user_report(aid: str) -> list:
    logger.info(f"fetching report for user: {aid}")
    sdt, edt = get_report_period()
    url = f"{GET_S9_USER_REPORT}/?aid={aid}&start_date={sdt}&end_date={edt}"
    return _fetch_report(url)


def fetch_reseller_users() -> list[str]:
    logger.info("fetching reseller users")
    return [_create_api_user(user[5:-1]) for user in _fetch_report(GET_RESELLER_USERS_URL) if bool(user)]


def _create_api_user(username: str) -> str:
    api_client = Client(ClientType.API.value)
    user = api_client.get_client_by_username(username)

    if user is None:
        logger.info("Attempting to create api client for {}".format(username))
        try:
            first, second, *_ = username.split("_")
            prefix = f"{first}_{second}"
            user = api_client.create(dict(
                username=username,
                aid=S3_CLIENT_AID,
                reseller_prefix=prefix,
                rate=fetch_user_rate(username)
            ))
        except Exception as e:
            logger.error(
                "failed to create s3 api user {} with error {}".format(username, e))
            return username
    return str(user.username)
