import logging
from typing import Dict, List

from app.core.clients.queries import Client
from app.core.constants import APP_LOGGER
from app.core.report.constants import (
    GET_RESELLER_USERS_URL,
    GET_S9_USER_REPORT,
    GET_USER_REPORT_URL,
    S3_CLIENT_AID,
)
from app.core.report.utils.misc import (
    extract_reseller_prefix,
    get_previous_month,
    get_report_period,
    is_nalo_reseller,
    is_s3_client,
)
from app.core.report.utils.s7 import fetch_user_rate
from app.core.utils.enums import ClientType
from app.core.utils.http import Request

logger: logging.Logger = logging.getLogger(APP_LOGGER)


def get_initiate_fetch_payload() -> Dict[str, list[str] | str]:
    resellers = set()
    payload = dict(esmes=[], apiusers=[], resellers=[])

    for client in Client.get_api_clients():
        if bool(client.reseller_prefix) and not is_nalo_reseller(client.reseller_prefix):
            resellers.add(client.reseller_prefix)
        elif is_s3_client(str(client.aid)):
            payload["apiusers"].append(client.username)

    payload["resellers"] = list(resellers)
    payload["esmes"] = [client.username for client in Client.get_esme_clients()]
    return {**payload, "date": get_previous_month()}


def handle_s3_script_response(name: str, status: bool, data: str | dict) -> Dict[str, str | dict]:
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


def fetch_reseller_users() -> List[str]:
    logger.info("fetching reseller users")
    return [
        _create_api_user(user[5:-1]) for user in _fetch_report(GET_RESELLER_USERS_URL) if bool(user)
    ]


def _create_api_user(username: str) -> str:
    api_client = Client(ClientType.API.value)
    user = api_client.get_client_by_username(username)

    if user is None:
        logger.info("Attempting to create api client for {}".format(username))
        try:
            prefix: str = extract_reseller_prefix(username)
            user = api_client.create(
                dict(
                    username=username,
                    aid=S3_CLIENT_AID,
                    reseller_prefix=prefix,
                    rate=fetch_user_rate(username),
                )
            )
            return username
        except Exception as e:
            logger.error("failed to create s3 api user {} with error {}".format(username, e))
            return username
    return str(user.username)
