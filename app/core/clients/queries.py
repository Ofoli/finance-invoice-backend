from ..models.user import ApiClient, BlastClient, ESMEClient
from ..utils.enums import ClientType


class Client:

    @staticmethod
    def get_model(client_type: str):
        return {
            ClientType.API.value: ApiClient,
            ClientType.BLAST.value: BlastClient,
        }.get(client_type, ESMEClient)

    @staticmethod
    def get_all():
        return ApiClient.query.all() + BlastClient.query.all() + ESMEClient.query.all()

    @staticmethod
    def create(data, client_type: str):
        Model = Client.get_model(client_type)
        client = Model(**data)
        client.save()
        return client
