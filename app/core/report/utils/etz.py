import os
from werkzeug.datastructures.file_storage import FileStorage

from ..constants import ETZ_SENT_FILES_DIR, ETZ_STAT_FILES_DIR


def save_etz_file(zfile: FileStorage) -> None:
    filename = str(zfile.filename)
    dst_dir = ETZ_SENT_FILES_DIR if "sent" in filename else ETZ_STAT_FILES_DIR
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, filename)
    zfile.save(dst=dst_path)


def generate_dump_report(sent_dir_path: str, stat_dir_path: str) -> str: ...
