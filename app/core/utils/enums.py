from enum import Enum, IntEnum


class ClientType(Enum):
    API = "api"
    BLAST = "blast"
    ESME = "esme"


class BlastClientLevel(Enum):
    USER = "user"
    RESELLER = "reseller"


class ReportType(IntEnum):
    SMSAPI = 0
    SMSWEB = 1
    SMPP = 2
    EMAILAPI = 3
    EMAILWEB = 4
