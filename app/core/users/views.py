from http import HTTPStatus
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..models.user import AuthUser
from ..schemas.user import AuthUserSchema

from ..utils.response import Response


class AuthUsersView(Resource):
    schema = AuthUserSchema

    def get(self):
        users = AuthUser.query.all()
        return Response().success(self.schema(many=True).dump(users))

    def post(self):
        try:
            validated_data = self.schema().load(request.get_json())
            new_user = AuthUser(**validated_data)
            new_user.set_password(validated_data.get("password"))
            new_user.save()
            return Response().success(self.schema().dump(new_user))
        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)
