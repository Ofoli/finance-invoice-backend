from ..constants import NETWORKS, ALERTS_SPACE_ROW

from .s3 import fetch_reseller_users, fetch_s3_user_report, fetch_s9_user_report
from .misc import is_s3_client


def _get_network(network: str) -> str:
    item = [name for name in NETWORKS.keys() if network.upper() in name]
    return item.pop() if bool(len(item)) else "FOREIGN"


def _format_report(username: str, report: list[dict]) -> list[dict]:
    formatted_report: dict[str, dict] = {}

    for record in report:
        network = _get_network(record["network"])
        if not network in formatted_report:
            formatted_report[network] = {
                "account": username,
                "network": network,
                "count": record["count"],
                "page_count": record["page_count"]
            }
            continue
        # this is to aggregate foreign network counts as one
        formatted_report[network]["count"] += record["count"]
        formatted_report[network]["page_count"] += record["page_count"]

    return list(formatted_report.values()) + [ALERTS_SPACE_ROW, ALERTS_SPACE_ROW]


def fetch_alerts(api_clients: list) -> list[dict]:
    reseller_users: list[str] = fetch_reseller_users()
    s9_users: list[dict] = []
    s3_users: list[str] = []
    alerts: list[dict] = []

    for client in api_clients:
        if is_s3_client(client.aid):
            s3_users.append(client.username)
        else:
            s9_users.append({"aid": client.aid, "username": client.username})

    for username in sorted(reseller_users + s3_users, key=lambda x: x):
        response: dict = fetch_s3_user_report(username)
        report: list = response.get("data", [])
        alerts += _format_report(username, report)

    for user in sorted(s9_users, key=lambda x: x["username"]):
        report: list = fetch_s9_user_report(user["aid"])
        alerts += _format_report(user["username"], report)

    return alerts


def fetch_esme_counts(esme_clients: list) -> list[dict]:
    return []
