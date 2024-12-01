import csv
import os
import zipfile
from datetime import datetime, timedelta

from sqlalchemy import Column

from app.core.constants import FILES_DIR
from app.core.notifications.email import AttachmentEmailNotification
from app.core.report.constants import (
    EMAIL_CLIENT_AID,
    FINANCE_EMAIL,
    NALO_RESELLER_PREFIX,
    S3_CLIENT_AID,
    SUPPORT_EMAIL,
)
from app.core.utils.enums import ServiceType


def send_report_email(service: ServiceType, files: list[str]) -> str:
    month = get_previous_month()
    response = AttachmentEmailNotification(
        subject=f"POSTPAID CLIENT {service.name} REPORT - {month}",
        destination=FINANCE_EMAIL,
        template="invoice_report.html",
        template_data={},
        attachment_file_paths=files,
        cc=[SUPPORT_EMAIL],
    ).send()

    return response


def extract_reseller_prefix(username: str) -> str:
    first, second, *_ = username.split("_")
    return f"{first}_{second}"


def get_previous_month() -> str:
    current_date = datetime.now()
    previous_month = current_date.replace(day=1) - timedelta(days=1)
    return previous_month.strftime("%Y-%m")


def create_csv_report(data: list, filename: str, dst_dir: str = FILES_DIR) -> str:
    if len(data) == 0:
        return ""

    os.makedirs(FILES_DIR, exist_ok=True)
    filepath: str = os.path.join(dst_dir, filename)

    with open(filepath, mode="w", newline="") as file:
        headers = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    return filepath


def zip_blast_reports(src_files: list[str], dst_file: str) -> str:
    if len(src_files) == 0:
        return ""

    os.makedirs(FILES_DIR, exist_ok=True)
    dst_path: str = os.path.join(FILES_DIR, dst_file)

    with zipfile.ZipFile(dst_path, "w") as zip_file:
        for filename in src_files:
            zip_file.write(filename)

    return dst_path


def is_s3_client(aid: Column[str]) -> bool:
    return str(aid) == S3_CLIENT_AID


def is_nalo_reseller(prefix: Column[str]) -> bool:
    return str(prefix) == NALO_RESELLER_PREFIX


def is_sms_client(key: str | int) -> bool:
    return str(key) != EMAIL_CLIENT_AID


def get_report_period() -> tuple[str, str]:
    today = datetime.today()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
    return first_day_of_previous_month.strftime("%Y-%m-%d"), last_day_of_previous_month.strftime(
        "%Y-%m-%d"
    )


def get_blast_period() -> tuple[str, str]:
    month = get_previous_month()
    start_date = f"{month}-01"
    year, mth = month.split("-")
    next_month = str(value + 1 if (value := int(mth)) != 12 else 1)
    end_date = f"{year}-{next_month.zfill(2)}-01"
    return start_date, end_date


def get_year_period() -> tuple[str, str]:
    today = datetime.today()
    one_year_ago = today - timedelta(days=365)
    one_day_ahead = today + timedelta(days=1)
    return one_year_ago.strftime("%Y-%m-%d"), one_day_ahead.strftime("%Y-%m-%d")
