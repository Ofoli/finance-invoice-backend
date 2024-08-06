from marshmallow import fields, validate, ValidationError
from ...config.extensions import ma


from ..models.user import AuthUser, ApiClient, BlastClient, ESMEClient


def should_be_nalo_email(email: str):
    if not email.endswith("@nalosolutions.com"):
        raise ValidationError("Should be a NALO email")


class AuthUserSchema(ma.SQLAlchemyAutoSchema):

    email = fields.Email(required=True, validate=should_be_nalo_email)
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=12)
    )

    class Meta:  # type: ignore
        model = AuthUser


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
