import logging
from datetime import datetime, timedelta

from ...clients.queries import Client
from ...utils.enums import ClientType
from ...constants import APP_LOGGER


logger = logging.getLogger(APP_LOGGER)


def _get_previous_month() -> str:
    current_date = datetime.now()
    previous_month = current_date.replace(day=1) - timedelta(days=1)
    return previous_month.strftime('%Y-%m')


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

    return {**payload, "date": _get_previous_month()}


def handle_s3_script_response(name: str, status: bool, data: str | dict) -> dict[str, str | dict]:
    if not status:
        logger.error(f"{name} report script initiation failed: {data}")
        # send email or sms alert
        return dict(error=data)

    logger.info(f"{name} report script initiated: {data}")
    return dict(data=data)
