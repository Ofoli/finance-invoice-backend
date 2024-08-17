import os
import csv

from datetime import datetime, timedelta

from ...constants import FILES_DIR

from ..constants import S3_CLIENT_AID


def get_previous_month() -> str:
    current_date = datetime.now()
    previous_month = current_date.replace(day=1) - timedelta(days=1)
    return previous_month.strftime('%Y-%m')


def create_csv_report(data: list, filename: str) -> None:
    if len(data) == 0:
        return

    filepath: str = os.path.join(FILES_DIR, filename)

    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

    with open(filepath, mode="w", newline="") as file:
        headers = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)


def is_s3_client(aid: str) -> bool:
    return aid == S3_CLIENT_AID


def get_report_period() -> tuple[str, str]:
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    return first_day_of_previous_month.strftime('%Y-%m-%d'), last_day_of_previous_month.strftime('%Y-%m-%d')
