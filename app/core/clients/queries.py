from typing import Dict, List, Optional, Union

from app.core.models import db
from app.core.models.user import ApiClient, BlastClient, ESMEClient
from app.core.utils.enums import ClientType

ModelClient = Union[ApiClient, BlastClient, ESMEClient]


class Client:
    def __init__(self, client_type: str = "") -> None:
        self._Model = {
            ClientType.API.value: ApiClient,
            ClientType.BLAST.value: BlastClient,
        }.get(client_type, ESMEClient)

    @staticmethod
    def get_api_clients() -> List[ApiClient]:
        return ApiClient.query.all()

    @staticmethod
    def get_esme_clients() -> List[ESMEClient]:
        return ESMEClient.query.all()

    @staticmethod
    def get_all() -> Dict[str, List[ModelClient]]:
        return {
            ClientType.API.value: ApiClient.query.all(),
            ClientType.BLAST.value: BlastClient.query.all(),
            ClientType.ESME.value: ESMEClient.query.all(),
        }

    def create(self, data: Dict) -> ModelClient:
        client = self._Model(**data)
        client.save()
        return client

    def get_client(self, id: int) -> ModelClient:
        return self._Model.query.get_or_404(ident=id, description="Client not found")

    def get_client_by_username(self, username: str) -> Optional[ModelClient]:
        return self._Model.query.filter_by(username=username).first()

    def delete_client(self, id: int) -> None:
        client = self.get_client(id)
        db.session.delete(client)
        db.session.commit()

    def update_client(self, id: int, data: Dict) -> ModelClient:
        db.session.query(self._Model).filter_by(id=id).update(data)
        db.session.commit()
        return self.get_client(id)
