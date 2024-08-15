import celery

from ..utils.http import Request

from .constants import INITIATE_FETCH_URL, INITIATE_ETZ_URL
from .utils.s3 import get_initiate_fetch_payload, handle_s3_script_response


@celery.shared_task(ignore_result=False)
def initiate_s3_fetch_script() -> dict:
    payload = get_initiate_fetch_payload()
    status, data = Request.post(INITIATE_FETCH_URL, payload)
    return handle_s3_script_response("S3", status, data)


@celery.shared_task(ignore_result=False)
def initiate_etz_report_script() -> dict:
    status, data = Request.post(INITIATE_ETZ_URL, {})
    return handle_s3_script_response("ETZ", status, data)


@celery.shared_task(ignore_result=False)
def test_celery() -> str:
    return "testing...."
