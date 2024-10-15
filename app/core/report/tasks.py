from typing import Dict, List, Literal
import celery

from ..utils.http import Request
from ..utils.enums import ClientType
from ..clients.queries import Client, ModelClient

from .constants import INITIATE_FETCH_URL, INITIATE_ETZ_URL
from .utils.s3 import get_initiate_fetch_payload, handle_s3_script_response
from .utils.email import save_email_reports
from .utils.sms import save_sms_api_reports, save_sms_web_reports, save_esme_reports
from .utils.etz import save_etz_network_report, generate_dump_report
from .utils.misc import get_previous_month, create_csv_report, zip_blast_reports, send_report_email
from .utils.processors import fetch_alerts, fetch_esme_counts, fetch_blasts


@celery.shared_task(ignore_result=False)
def initiate_s3_fetch_script() -> dict:
    payload: Dict[str, List[str] | str] = get_initiate_fetch_payload()
    payload: Dict[str, List[str] | str] = get_initiate_fetch_payload()
    status, data = Request.post(INITIATE_FETCH_URL, payload)
    return handle_s3_script_response("S3", status, data)


@celery.shared_task(ignore_result=False)
def initiate_etz_report_script() -> Dict:
    status, data = Request.post(INITIATE_ETZ_URL, {})
    return handle_s3_script_response("ETZ", status, data)


@celery.shared_task(ignore_result=True)
def handle_s3_report_callback() -> Literal[True]:
    month: str = get_previous_month()
    clients: Dict[str, List[ModelClient]] = Client.get_all()

    alerts: List[Dict] = fetch_alerts(clients[ClientType.API.value])
    alerts_filename: str = create_csv_report(alerts, f"alerts_{month}.csv")
    save_sms_api_reports(alerts, month)

    esme_counts: List[Dict] = fetch_esme_counts(clients[ClientType.ESME.value])
    esme_filename: str = create_csv_report(esme_counts, f"esmes_{month}.csv")
    save_esme_reports(esme_counts, month)

    blasts: List[Dict] = fetch_blasts(clients[ClientType.BLAST.value])
    blast_filenames: List[str] = [
        dst_path
        for blast in blasts
        if (dst_path := create_csv_report(blast["report"], f"blast_{blast['account']}.csv"))
    ]
    blasts_filename = zip_blast_reports(blast_filenames, f"blasts_{month}.zip")
    save_sms_web_reports(blasts, month)

    send_report_email([alerts_filename, esme_filename, blasts_filename])
    return True


@celery.shared_task(ignore_result=True)
def handle_etz_report_callback() -> Literal[True]:
    dump_report_file_path, network_report = generate_dump_report()
    save_etz_network_report(network_report)
    send_report_email([dump_report_file_path])
    return True


@celery.shared_task(ignore_result=True)
def handle_email_report_callback(callback_data: dict) -> Literal[True]:
    month: str = callback_data["month"]
    api_reports: list[dict] = callback_data["api_reports"]
    web_reports: list[dict] = callback_data["web_reports"]

    save_email_reports(api_reports, ClientType.API, month)
    save_email_reports(web_reports, ClientType.BLAST, month)

    api_report_filename = create_csv_report(api_reports, f"api_email_{month}.csv")
    web_report_filename = create_csv_report(web_reports, f"web_email_{month}.csv")

    send_report_email([api_report_filename, web_report_filename])
    return True
