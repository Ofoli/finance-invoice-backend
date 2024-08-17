from typing import Dict, List, Literal
import celery

from ..utils.http import Request
from ..utils.enums import ClientType
from ..clients.queries import Client, ModelClient

from .constants import INITIATE_FETCH_URL, INITIATE_ETZ_URL
from .utils.s3 import get_initiate_fetch_payload, handle_s3_script_response
from .utils.misc import get_previous_month, create_csv_report
from .utils.processors import fetch_alerts, fetch_esme_counts


@celery.shared_task(ignore_result=False)
def initiate_s3_fetch_script() -> dict:
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
    alerts_filename: str = f"alerts_{month}.csv"
    create_csv_report(alerts, alerts_filename)

    esme_counts: List[Dict] = fetch_esme_counts(clients[ClientType.ESME.value])
    esme_filename: str = f"esmes_{month}.csv"
    create_csv_report(esme_counts, esme_filename)

    return True

    # send_report_email
