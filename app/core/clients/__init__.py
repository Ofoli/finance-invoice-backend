from flask import Blueprint
from flask_restful import Api

from .view import ClientsView

client_bp = Blueprint("auth", __name__)
api = Api(client_bp)

api.add_resource(ClientsView, "/")
