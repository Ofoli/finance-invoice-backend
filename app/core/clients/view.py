from http import HTTPStatus
from typing import List, Any
from flask import request, abort
from marshmallow import ValidationError

from ..utils.enums import ClientType
from ..utils.response import Response
from ..utils.auth import IsAuthedUserMixin
from ..schemas.user import ApiClientSchema, EsmeClientSchema, BlastClientSchema, ClientTypeSchema

from .queries import Client
ClientSchema = ApiClientSchema | EsmeClientSchema | BlastClientSchema


class BaseClientView(IsAuthedUserMixin):
    def _get_schema(self, client_type: str) -> ClientSchema:
        schemas = {
            ClientType.API.value: ApiClientSchema,
            ClientType.BLAST.value: BlastClientSchema,
        }
        return schemas.get(client_type, EsmeClientSchema)


class ClientsView(BaseClientView):
    def get(self):
        clients: List[Any] = Client.get_all()
        return Response().success(clients)

    def post(self):
        try:
            data = request.get_json()
            client_type = ClientTypeSchema().load(data)
            schema = self._get_schema(client_type)
            validated_data = schema().load(data)  # type: ignore
            client = schema().dump(Client(client_type).create(validated_data))  # type: ignore
            return Response(HTTPStatus.CREATED).success(client)
        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)


class ClientView(BaseClientView):

    def _check_type(self, client_type):
        if not client_type in [ctype.value for ctype in ClientType]:
            abort(HTTPStatus.BAD_REQUEST, "Invalid client_type in url")

    def get(self, client_type: str, id: int):
        self._check_type(client_type)
        schema = self._get_schema(client_type)
        client = Client(client_type).get_client(id)
        return Response().success(schema().dump(client))  # type: ignore

    def patch(self, client_type: str, id: int):
        self._check_type(client_type)
        schema = self._get_schema(client_type)

        try:
            validated_data = schema().load(request.get_json())  # type: ignore
            updated_client = Client(
                client_type).update_client(id, validated_data)
            return Response().success(schema().dump(updated_client))  # type: ignore
        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)

    def delete(self, client_type: str, id: int):
        self._check_type(client_type)
        Client(client_type).delete_client(id)
        return Response(HTTPStatus.NO_CONTENT).success(dict())
