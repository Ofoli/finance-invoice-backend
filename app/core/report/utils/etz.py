import os
import logging
import zipfile

from typing import List, Optional, Tuple, Dict
from werkzeug.datastructures.file_storage import FileStorage

from app.core.constants import APP_LOGGER

from ..constants import ETZ_SENT_FILES_DIR, ETZ_STAT_FILES_DIR, ETZ_REPORT_FILES_DIR
from .process_log import SentSmsLog, StatSmsLog, SmsLog
from .enums import FILE_KINDS
from .misc import create_csv_report

logger = logging.getLogger(APP_LOGGER)

Report = Dict[str, int]


def save_etz_file(zfile: FileStorage) -> None:
    filename = str(zfile.filename)
    dst_dir = ETZ_SENT_FILES_DIR if "sent" in filename else ETZ_STAT_FILES_DIR
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, filename)
    zfile.save(dst=dst_path)


def generate_dump_report() -> Tuple[str, Report]:
    network_report: Report = {}
    dump_report_paths = []
    zipped_stat_files = os.listdir(ETZ_STAT_FILES_DIR)

    for sent_zfile_path in os.listdir(ETZ_SENT_FILES_DIR):
        key = os.path.basename(sent_zfile_path).split("_").pop()
        stat_zfile_path = _get_stat_zfile(zipped_stat_files, key)

        if stat_zfile_path is None:
            logger.error("zipped stat_log {} not found for {}".format(sent_zfile_path, stat_zfile_path))
            continue

        dump_report: List[dict] = []
        dump_report_filename: str = f"report_{key}.csv"
        hashed_sent_logs: Dict[str, SentSmsLog] = _create_logs_hash(sent_zfile_path, kind=FILE_KINDS.SENT)
        hashed_stat_logs: Dict[str, StatSmsLog] = _create_logs_hash(stat_zfile_path, kind=FILE_KINDS.STAT)

        for fid, sent_sms in hashed_sent_logs.items():
            stat_sms: StatSmsLog = hashed_stat_logs.get(fid, StatSmsLog(sent_date=sent_sms.date))
            network_count = network_report.get(sent_sms.network, 0)
            network_report[sent_sms.network] = network_count + sent_sms.page_count
            dump_report.append(
                dict(
                    sent_date=sent_sms.date,
                    username=sent_sms.username,
                    sender=sent_sms.sender,
                    msisdn=sent_sms.msisdn,
                    network=sent_sms.network,
                    message=sent_sms.message,
                    page_count=sent_sms.page_count,
                    status=stat_sms.status,
                    delivered_date=stat_sms.date,
                )
            )
        dump_report_paths.append(f"{ETZ_REPORT_FILES_DIR}/{dump_report_filename}")
        create_csv_report(dump_report, filename=dump_report_filename, dst_dir=ETZ_REPORT_FILES_DIR)

    zipped_file_path = os.path.join(ETZ_REPORT_FILES_DIR, "etz_report.zip")
    _zip_etz_report_files(dump_report_paths, zipped_file_path)

    return zipped_file_path, network_report


def save_etz_network_report(report: dict) -> None: ...


def _zip_etz_report_files(file_paths: List[str], dst_path: str) -> None:
    with zipfile.ZipFile(dst_path, "w") as zipf:
        for file_pth in file_paths:
            zipf.write(file_pth, os.path.basename(file_pth))


def _get_stat_zfile(zpaths: List[str], key: str) -> Optional[str]:
    return [zpath for zpath in zpaths].pop()


def _create_logs_hash(file_path: str, kind: FILE_KINDS) -> Dict:
    logs_hash: Dict[str, SmsLog] = {}

    try:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            filename = zip_ref.namelist()[0]
            with zip_ref.open(filename) as log_file:
                for line in log_file:
                    decoded_line = line.decode("utf-8").strip()
                    log: SmsLog = (
                        SentSmsLog(decoded_line) if kind.value == "sent" else StatSmsLog(log_line=decoded_line)
                    )
                    logs_hash[log.fid] = log

    except zipfile.BadZipFile:
        logger.error({"error": "failed to read zipped file", "message": f"{file_path} is not a valid zip file."})
    except Exception as e:
        logger.error({"error": "failed to read zipped file", "message": {e}})

    return logs_hash
