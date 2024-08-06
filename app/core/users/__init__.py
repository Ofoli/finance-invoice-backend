from flask import Blueprint
from flask_restful import Api

from .views import AuthUsersView, AuthUserView

users_bp = Blueprint("users", __name__)
api = Api(users_bp)

api.add_resource(AuthUsersView, "/")
api.add_resource(AuthUserView, "/<int:id>")
