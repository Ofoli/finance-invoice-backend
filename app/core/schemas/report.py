from marshmallow import fields
from marshmallow import ValidationError

from app.config.extensions import ma


from app.core.utils.enums import ReportType, ClientType


def _validate_service(service: str):
    if int(service) not in [rtype.value for rtype in ReportType]:
        raise ValidationError("Invalid service")


def validate_client_service(client_service: str) -> bool:
    return client_service in [ctype.value for ctype in ClientType]


class EmailReportCallbackDataSchema(ma.Schema):
    month = fields.String(required=True)
    api_reports = fields.List(fields.Dict(), required=True)
    web_reports = fields.List(fields.Dict(), required=True)


class EtzReportCallbackDataSchema(ma.Schema):
    sent_files_path = fields.String(required=True)
    stat_files_path = fields.String(required=True)


class MonthlyReportSchema(ma.Schema):
    user = fields.Integer(required=True)
    service = fields.String(required=True, validate=_validate_service)
    start_date = fields.String(required=True)
    end_date = fields.String(required=True)
