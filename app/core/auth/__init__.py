from flask import Blueprint
from flask_restful import Api

from .views import LoginView, ResetPassword

auth_bp = Blueprint("auth", __name__)
api = Api(auth_bp)

api.add_resource(LoginView, "/login")
api.add_resource(ResetPassword, "/reset-password")
