from flask import Blueprint
from flask_restful import Api

from .views import AuthUsersView
from .constants import USERS_URL

users_bp = Blueprint("users", __name__)
api = Api(users_bp)

api.add_resource(AuthUsersView, USERS_URL)
