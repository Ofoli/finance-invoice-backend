from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from ..models.user import AuthUser

from ..schemas.user import AuthUserSchema


class AuthUsersView(Resource):
    schema = AuthUserSchema

    def get(self):
        users = AuthUser.query.all()
        return self.schema(many=True).dump(users)

    def post(self):
        data = request.get_json()

        try:
            validated_data = self.schema().load(data)
            return jsonify(validated_data)
        except ValidationError as err:
            return jsonify(err.messages), 400
