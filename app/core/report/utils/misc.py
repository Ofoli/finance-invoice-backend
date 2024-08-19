import os
import csv
import zipfile

from datetime import datetime, timedelta

from ...constants import FILES_DIR

from ..constants import S3_CLIENT_AID


def get_previous_month() -> str:
    current_date = datetime.now()
    previous_month = current_date.replace(day=1) - timedelta(days=1)
    return previous_month.strftime('%Y-%m')


def create_csv_report(data: list, filename: str) -> str:
    if len(data) == 0:
        return ""

    filepath: str = os.path.join(FILES_DIR, filename)

    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

    with open(filepath, mode="w", newline="") as file:
        headers = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    return filepath


def zip_blast_reports(src_files: list[str], dst_file: str) -> str:
    if len(src_files) == 0:
        return ""

    dst_path: str = os.path.join(FILES_DIR, dst_file)
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

    with zipfile.ZipFile(dst_path, 'w') as zip_file:
        for filename in src_files:
            zip_file.write(filename)

    return dst_path


def is_s3_client(aid: str) -> bool:
    return aid == S3_CLIENT_AID


def get_report_period() -> tuple[str, str]:
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    return first_day_of_previous_month.strftime('%Y-%m-%d'), last_day_of_previous_month.strftime('%Y-%m-%d')


def get_blast_period() -> tuple[str, str]:
    month = get_previous_month()
    start_date = f"{month}-01"
    year, mth = month.split("-")
    next_month = str(value + 1 if (value := int(mth)) != 12 else 1)
    end_date = f"{year}-{next_month.zfill(2)}-01"
    return start_date, end_date