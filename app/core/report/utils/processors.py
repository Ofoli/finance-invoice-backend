from app.core.report.constants import ALERTS_SPACE_ROW, ESME_SPACE_ROW, NETWORKS
from app.core.report.utils.misc import get_previous_month, is_s3_client, is_sms_client
from app.core.report.utils.s3 import (
    fetch_reseller_users,
    fetch_s3_user_report,
    fetch_s9_user_report,
    fetch_s9_users,
)
from app.core.report.utils.s7 import decrypt_message, extract_blast_params, fetch_blast_report


def _get_network(network: str) -> str:
    item: list[str] = [name for name in NETWORKS.keys() if network.upper() in name]
    return item.pop() if bool(len(item)) else "FOREIGN"


def _get_prefix_network(prefix: str) -> str:
    item: list[str] = [
        name for name, value in NETWORKS.items() if prefix.replace("+", "")[0:5] in value
    ]
    return item.pop() if bool(len(item)) else "UNKNOWN"


def _format_esme_report(esme: str, report: list[dict]) -> list[dict]:
    formatted_report: dict[str, dict] = {}
    report_month: str = get_previous_month()

    if len(report) == 0:
        return []

    for record in report:
        if record["date"] != report_month:
            continue

        network: str = _get_prefix_network(record["prefix"])
        if network not in formatted_report:
            formatted_report[network] = {
                "account": esme,
                "network": network,
                "total_pages": int(record["count"]),
            }
            continue

        formatted_report[network]["total_pages"] += int(record["count"])

    return list(formatted_report.values()) + [ESME_SPACE_ROW, ESME_SPACE_ROW]


def _format_api_report(username: str, report: list[dict]) -> list[dict]:
    formatted_report: dict[str, dict] = {}

    if len(report) == 0:
        return []

    for record in report:
        network: str = _get_network(record["network"])
        if network not in formatted_report:
            formatted_report[network] = {
                "account": username,
                "network": network,
                "count": int(record.get("count", "0")),
                "total_pages": int(record.get("page_count", "0")),
            }
            continue
        # this is to aggregate foreign network counts as one
        formatted_report[network]["count"] += int(record.get("count", "0"))
        formatted_report[network]["total_pages"] += int(record.get("page_count", "0"))

    return list(formatted_report.values()) + [ALERTS_SPACE_ROW, ALERTS_SPACE_ROW]


def _format_blast_report(report: list[dict]) -> list[dict]:
    return [
        {
            "jobid": record["jobid"],
            "sent_date": record["sent_date"],
            "account": record["username"],
            "sender": record["sender"],
            "total_sms": (total_pages := int(record["total_sms"])) / int(record["pages_count"]),
            "total_pages": total_pages,
            "message": decrypt_message(record["message"], record["ekey"]),
        }
        for record in report
    ]


def fetch_alerts(api_clients: list) -> list[dict]:
    s3_users: set[str] = set(fetch_reseller_users())
    s9_users: list[dict] = []
    alerts: list[dict] = []

    for client in api_clients:
        if not is_sms_client(client.aid):
            continue
        if is_s3_client(client.aid):
            s3_users.add(client.username)
        else:
            s9_users.append(
                {
                    "aid": client.aid,
                    "username": client.username,
                    "reseller": client.reseller_prefix,
                }
            )

    for username in s3_users:
        report: list = fetch_s3_user_report(username)
        alerts += _format_api_report(username, report)

    for user in fetch_s9_users(s9_users):
        report: list = fetch_s9_user_report(user["aid"])
        alerts += _format_api_report(user["username"], report)

    return alerts


def fetch_esme_counts(esme_clients: list) -> list[dict]:
    return [
        report
        for client in esme_clients
        for report in _format_esme_report(client.username, fetch_s3_user_report(client.username))
    ]


def fetch_blasts(blast_clients: list) -> list[dict]:
    return [
        {"account": client.username, "report": _format_blast_report(report)}
        for client in blast_clients
        if is_sms_client(client.key_id)
        and (report := fetch_blast_report(*extract_blast_params(client)))
    ]
