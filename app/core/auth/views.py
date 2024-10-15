from typing import Any

from flask import request
from http import HTTPStatus
from flask_restful import Resource
from marshmallow import ValidationError

from ..schemas.user import LoginSchema, ResetPasswordSchema
from ..utils.http import Response
from ..utils.auth import IsAuthedUserMixin

from .utils import Auth


class LoginView(Resource):
    schema = LoginSchema

    def post(self):
        try:
            validated_data: Any = self.schema().load(request.get_json())
            return Auth.login_user(
                email=validated_data["email"], password=validated_data["password"]
            )

        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)


class ResetPassword(IsAuthedUserMixin):
    schema = ResetPasswordSchema

    def post(self):
        try:
            validated_data: Any = self.schema().load(request.get_json())
            return Auth.reset_password(
                user=self.user,
                password=validated_data["password"],
                new_password=validated_data["new_password"],
            )

        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)
