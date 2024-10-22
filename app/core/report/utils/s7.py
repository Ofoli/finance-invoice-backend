import logging
from cryptography.fernet import Fernet


from ...models.user import BlastClient
from ...utils.enums import BlastClientLevel
from ...constants import APP_LOGGER
from ...utils.http import Request

from ..constants import DEFAULT_RATE, GET_USER_RATE_URL, GET_BLASTS_URL

from .misc import get_blast_period

logger: logging.Logger = logging.getLogger(APP_LOGGER)


def extract_blast_params(client: BlastClient) -> tuple[str, str]:
    level = BlastClientLevel.USER.value
    if client.is_reseller is True:
        level = BlastClientLevel.RESELLER.value
    return str(client.key_id), level


def fetch_blast_report(uid: str, level: str) -> list[dict]:
    sdt, edt = get_blast_period()
    params = f"id={uid}&type={level}&start_date={sdt}&end_date={edt}"
    _, data = Request.get(f"{GET_BLASTS_URL}?{params}")

    if isinstance(data, dict):
        return data["data"]

    logger.error(f"failed to fetch blast report for {uid}, error:{data}")
    return []


def fetch_user_rate(username: str) -> float:
    status, data = Request.get(f"{GET_USER_RATE_URL}/?username={username}")
    if not status:
        return DEFAULT_RATE
    return data.get("local_sms_cost", DEFAULT_RATE)  # type: ignore


def decrypt_message(message: str, key: str) -> str:
    try:
        f = Fernet(bytes(key, "utf-8"))
        return f.decrypt(bytes(message, "utf-8")).decode()
    except Exception as e:
        logger.error(f"error occured decrypting. Error:{e}")
        return message
