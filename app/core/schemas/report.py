from marshmallow import fields
from app.config.extensions import ma


class EmailReportCallbackDataSchema(ma.Schema):
    month = fields.String(required=True)
    api_reports = fields.List(fields.Dict(), required=True)
    web_reports = fields.List(fields.Dict(), required=True)
