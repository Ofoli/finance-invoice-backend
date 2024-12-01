import logging
from typing import Dict, List

from app.core.clients.queries import Client
from app.core.constants import APP_LOGGER
from app.core.report.constants import (
    GET_RESELLER_USERS_URL,
    GET_RUIDS_URL,
    GET_S9_USER_REPORT,
    GET_S9_USERS,
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

    logger.error({"action": "_fetch_report", "url": url})
    return []


def _fetch_new_s9_users(prefixes: list) -> list:
    key = "|".join(prefixes)
    return _fetch_report(f"{GET_S9_USERS}?prefixes={key}")


def _fetch_ruids(users: list) -> List[dict]:
    status, data = Request.post(GET_RUIDS_URL, data={"users": users})
    if status and not isinstance(data, str) and data.get("status"):
        return data["data"]

    logger.error({"action": "_fetch_ruids", "data": users, "details": data})
    return []


def fetch_s3_user_report(username: str) -> list:
    logger.info({"action": "fetch_s3_user_report", "username": username})
    url = f"{GET_USER_REPORT_URL}?username={username}"
    return report[0]["data"] if len(report := _fetch_report(url)) else []


def fetch_s9_user_report(aid: str) -> list:
    logger.info({"action": "fetch_s9_user_report", "aid": aid})
    sdt, edt = get_report_period()
    url = f"{GET_S9_USER_REPORT}/?aid={aid}&start_date={sdt}&end_date={edt}"
    return _fetch_report(url)


def fetch_reseller_users() -> List[str]:
    return [
        _create_api_user(user[5:-1]) for user in _fetch_report(GET_RESELLER_USERS_URL) if bool(user)
    ]


def fetch_s9_users(accounts: List[dict]) -> List[dict]:
    prefixes: List[str] = []
    usernames: List[str] = []
    s9_users: List[dict] = accounts[:]

    for account in accounts:
        prefixes.append(account["reseller"])
        usernames.append(account["username"])

    new_users: List[str] = [
        username
        for user in _fetch_new_s9_users(prefixes)
        if user and (username := user[5:-1]) not in usernames
    ]

    return s9_users + [
        {
            "username": _create_api_user(account["user"], aid=account["ruid"]),
            "aid": account["ruid"],
        }
        for account in _fetch_ruids(new_users)
    ]


def _create_api_user(username: str, aid: str = S3_CLIENT_AID) -> str:
    api_client = Client(ClientType.API.value)
    user = api_client.get_client_by_username(username)

    if user is None:
        logger.info({"action": "_create_api_user", "data": f"{username}_{aid}"})
        try:
            prefix: str = extract_reseller_prefix(username)
            user = api_client.create(
                dict(
                    aid=aid,
                    username=username,
                    reseller_prefix=prefix,
                    rate=fetch_user_rate(username),
                )
            )
            return username
        except Exception as e:
            logger.error({"action": "_create_api_user", "data": f"{username}_{aid}", "details": e})
            return username
    return str(user.username)
