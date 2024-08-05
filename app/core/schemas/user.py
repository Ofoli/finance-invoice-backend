from ...config.extensions import ma

from ..models.user import AuthUser, ApiClient, BlastClient, ESMEClient


class AuthUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AuthUser


class ApiClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ApiClient


class BlastClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = BlastClient


class EsmeClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ESMEClient