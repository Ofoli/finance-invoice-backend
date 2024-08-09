from flask import Blueprint
from flask_restful import Api

from .view import ClientsView, ClientView

client_bp = Blueprint("auth", __name__)
api = Api(client_bp)

api.add_resource(ClientsView, "/")
api.add_resource(ClientView, "/<str:client_type>/<int:id>")
