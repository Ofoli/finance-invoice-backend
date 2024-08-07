from http import HTTPStatus
from flask import request
from marshmallow import ValidationError

from app.core.models.user import AuthUser

from ..utils.response import Response
from ..utils.auth import IsAuthedUserMixin
from ..schemas.user import AuthUserSchema

from .queries import get_all_users, get_user, get_user_by_email, create_user


class AuthUsersView(IsAuthedUserMixin):
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


class AuthUserView(IsAuthedUserMixin):
    schema = AuthUserSchema

    def get(self, id):
        user = get_user(id)
        return Response().success(self.schema().dump(user))

    def patch(self, id):
        user: AuthUser = get_user(id)
        fullname = request.get_json().get("fullname")
        if not fullname:
            error = "fullname is required"
            return Response(HTTPStatus.BAD_REQUEST).failed(error)

        user.fullname = fullname
        user.save()
        return Response().success(self.schema().dump(user))
