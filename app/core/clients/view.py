from http import HTTPStatus
from typing import List, Optional, Any
from flask import request
from marshmallow import ValidationError

from ..utils.enums import ClientType
from ..utils.response import Response
from ..utils.auth import IsAuthedUserMixin
from ..schemas.user import ApiClientSchema, EsmeClientSchema, BlastClientSchema, ClientTypeSchema

from .queries import Client
ClientSchema = ApiClientSchema | EsmeClientSchema | BlastClientSchema


class ClientsView(IsAuthedUserMixin):
    def _get_schema(self, client_type: str) -> ClientSchema:
        schemas = {
            ClientType.API.value: ApiClientSchema,
            ClientType.BLAST.value: BlastClientSchema,
        }
        return schemas.get(client_type, EsmeClientSchema)

    def get(self):
        clients: List[Any] = Client.get_all()
        return Response().success(clients)

    def post(self):
        try:
            data = request.get_json()
            client_type = ClientTypeSchema().load(data)
            schema = self._get_schema(client_type)
            validated_data = schema().load(data)  # type: ignore
            client = Client.create(validated_data, client_type)
            return Response(HTTPStatus.CREATED).success(client)
        except ValidationError as err:
            return Response(HTTPStatus.BAD_REQUEST).failed(err.messages)
