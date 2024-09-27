from marshmallow import fields
from app.config.extensions import ma


class EmailReportCallbackDataSchema(ma.Schema):
    month = fields.String(required=True)
    api_reports = fields.List(fields.Dict(), required=True)
    web_reports = fields.List(fields.Dict(), required=True)


class EtzReportCallbackDataSchema(ma.Schema):
    sent_files_path = fields.String(required=True)
    stat_files_path = fields.String(required=True)
