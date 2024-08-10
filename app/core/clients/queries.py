from typing import List, Dict, Union

from ...config.extensions import db

from ..models.user import ApiClient, BlastClient, ESMEClient
from ..utils.enums import ClientType

ModelClient = Union[ApiClient, BlastClient, ESMEClient]


class Client:
    def __init__(self, client_type: str = "") -> None:
        self._Model = {
            ClientType.API.value: ApiClient,
            ClientType.BLAST.value: BlastClient,
        }.get(client_type, ESMEClient)

    @staticmethod
    def get_all() -> Dict[str, List[ModelClient]]:
        return ({
            ClientType.API.value: ApiClient.query.all(),
            ClientType.BLAST.value: BlastClient.query.all(),
            ClientType.ESME.value: ESMEClient.query.all()
        })

    def create(self, data: Dict) -> ModelClient:
        client = self._Model(**data)
        client.save()
        return client

    def get_client(self, id: int) -> ModelClient:
        return self._Model.query.get_or_404(ident=id, description="Client not found")

    def delete_client(self, id: int) -> None:
        client = self.get_client(id)
        db.session.delete(client)
        db.session.commit()

    def update_client(self, id: int, data: Dict) -> ModelClient:
        db.session.query(self._Model).filter_by(id=id).update(data)
        db.session.commit()
        return self.get_client(id)
