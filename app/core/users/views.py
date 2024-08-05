from http import HTTPStatus
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..schemas.user import AuthUserSchema

from ..utils.response import Response
from .queries import get_all_users, get_user, get_user_by_email, create_user


class AuthUsersView(Resource):
    schema = AuthUserSchema

    def get(self):
        users = get_all_users()
        return Response().success(self.schema(many=True).dump(users))

    def post(self):
        try:
            validated_data = self.schema().load(request.get_json())
            user = get_user_by_email(validated_data["email"])

            if user is not None:
                error = "User with this email already exist"
                return Response(HTTPStatus.BAD_REQUEST).failed(error)

            new_user = create_user(validated_data)
            return Response().success(self.schema().dump(new_user))
        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)


class AuthUserView(Resource):
    schema = AuthUserSchema

    def get(self, id):
        user = get_user(id)
        if user is None:
            error = "User not found"
            return Response(HTTPStatus.NOT_FOUND).failed(error)
        return Response().success(self.schema().dump(user))
