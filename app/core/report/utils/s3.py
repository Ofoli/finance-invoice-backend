from datetime import datetime, timedelta

from ...clients.queries import Client
from ...utils.enums import ClientType
from ...schemas.user import ApiClientSchema, EsmeClientSchema


def _get_previous_month() -> str:
    current_date = datetime.now()
    previous_month = current_date.replace(day=1) - timedelta(days=1)
    return previous_month.strftime('%Y-%m')

# dict[str, list[str] | str]


def get_initiate_fetch_payload():
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
