from flask import Blueprint
from flask_restful import Api

from .view import GetAllClientsView, CreateClientView, ClientView

client_bp = Blueprint("client", __name__)
api = Api(client_bp)

api.add_resource(GetAllClientsView, "/")
api.add_resource(CreateClientView, "/<client_type>")
api.add_resource(ClientView, "/<client_type>/<int:id>")
