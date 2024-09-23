from enum import Enum


class ClientType(Enum):
    API = "api"
    BLAST = "blast"
    ESME = "esme"


class BlastClientLevel(Enum):
    USER = "user"
    RESELLER = "reseller"


class Service(Enum):
    SMS = "sms"
    EMAIL = "email"
