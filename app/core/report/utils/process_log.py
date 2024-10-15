import secrets

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Literal, Optional

from ..constants import NETWORKS


class SmsLog(ABC):
    date: str
    fid: str

    @abstractmethod
    def _extract_data(self, log_line: str) -> None:
        """Extracts required fields from log line"""
        pass

    def _extract_value(self, s: str = "", split_key: str = ":") -> str:
        last_element = s.split(split_key)[-1]
        return last_element[:-1]


class SentSmsLog(SmsLog):
    username: str
    sender: str
    msisdn: str
    network: str
    message: str
    page_count: int

    def __init__(self, log_line: str) -> None:
        self._extract_data(log_line=log_line)

    def _extract_data(self, log_line: str) -> None:
        values = log_line.split(" ")
        self.date = f"{values[0]} {values[1]}"
        self.username = self._extract_value(values[6], "_")
        self.fid = value if (value := self._extract_value(values[8])) else secrets.token_hex(10)

        idx_offset: Literal[0, 1] = 1 if "[to:" in values[11] else 0
        sender_text = values[10] if idx_offset == 0 else f"{values[10]} {values[11]}"
        character_count = int(character_count) if (character_count := values[14 + idx_offset].split(":")[1]) else 0

        self.sender = self._extract_value(sender_text)
        self.msisdn = values[11 + idx_offset]
        self.network = SentSmsLog.get_network(self.msisdn)
        self.page_count = SentSmsLog.get_page_count(character_count)
        self.message = SentSmsLog.get_message(log_line, character_count)

    @staticmethod
    def get_network(msisdn: str) -> str:
        prefix = msisdn[:5]
        for name, prefixes in NETWORKS.items():
            if prefix in prefixes:
                return name

        return "FOREIGN"

    @staticmethod
    def get_page_count(character_count: int) -> int:
        if character_count < 161:
            return 1
        elif character_count < 307:
            return 2
        elif character_count < 460:
            return 3
        else:
            return 4

    @staticmethod
    def get_message(log_line: str, character_count: int) -> str:
        search_string = f"msg:{character_count}:"
        start_idx = log_line.find(search_string) + len(search_string)
        return log_line[start_idx : (start_idx + character_count)]  # noqa: E203


class StatSmsLog(SmsLog):
    status: str

    def __init__(self, log_line: Optional[str] = None, sent_date: Optional[str] = None) -> None:
        if sent_date:
            self._form_expired_log(sent_date)

        if log_line:
            self._extract_data(log_line)

    def _extract_data(self, log_line: str) -> None:
        dd, dt, fid, dlr_status = log_line.split(" ")
        self.date = f"{dd} {dt}"
        self.fid = fid
        self.status = dlr_status

    def _form_expired_log(self, sent_date: str) -> None:
        self.date = StatSmsLog.get_expired_date(sent_date)
        self.status = "EXPIRED"

    @staticmethod
    def get_expired_date(sent_date: str) -> str:
        d = datetime.fromisoformat(sent_date)
        new_date = d + timedelta(days=1)
        return new_date.isoformat(sep=" ").split(".")[0]
