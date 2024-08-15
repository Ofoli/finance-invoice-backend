import celery
import logging

from ..utils.http import Request
from ..constants import APP_LOGGER

from .constants import INITIATE_FETCH_URL
from .utils.s3 import get_initiate_fetch_payload

logger = logging.getLogger(APP_LOGGER)


@celery.shared_task(ignore_result=False)
def initiate_s3_fetch_script():
    payload = get_initiate_fetch_payload()
    status, data = Request.post(INITIATE_FETCH_URL, payload)
    logger.info(payload)

    if not status:
        logger.error(f"S3 report script initiation failed: {data}")
        # send email or sms alert
        return {"error": str(data)}

    logger.info(f"S3 report script initiated: {data}")
    return data


@celery.shared_task(ignore_result=False)
def test_celery() -> str:
    return "testing...."
