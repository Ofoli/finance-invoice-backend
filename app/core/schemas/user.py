from marshmallow import fields, validate, ValidationError
from app.config.extensions import ma

from ..utils.enums import ClientType

from ..models.user import AuthUser, ApiClient, BlastClient, ESMEClient


def should_be_nalo_email(email: str):
    if not email.endswith("@nalosolutions.com"):
        raise ValidationError("Should be a NALO email")


def validate_client_type(client_type: str):
    if client_type not in [ctype.value for ctype in ClientType]:
        raise ValidationError("Invalid client_type")


class AuthUserSchema(ma.SQLAlchemyAutoSchema):

    email = fields.Email(required=True, validate=should_be_nalo_email)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=12))

    class Meta:  # type: ignore
        model = AuthUser
        exclude = ["created_at", "updated_at"]


class ClientTypeSchema(ma.SQLAlchemyAutoSchema):
    client_type = fields.String(required=True, validate=validate_client_type)


class ApiClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:  # type: ignore
        model = ApiClient


class BlastClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:  # type: ignore
        model = BlastClient


class EsmeClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:  # type: ignore
        model = ESMEClient


class LoginSchema(ma.Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class ResetPasswordSchema(ma.Schema):
    password = fields.String(required=True)
    new_password = fields.String(required=True, validate=validate.Length(min=12))
