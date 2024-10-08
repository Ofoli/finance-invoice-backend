from enum import Enum


class ClientType(Enum):
    API = "api"
    BLAST = "blast"
    ESME = "esme"


class BlastClientLevel(Enum):
    USER = "user"
    RESELLER = "reseller"


class ReportType(Enum):
    SMSAPI = 0
    SMSWEB = 1
    SMPP = 2
    EMAILAPI = 3
    EMAILWEB = 4
