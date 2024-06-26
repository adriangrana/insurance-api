from typing import List
from ..models.client import Client

class ClientRepository:
    async def fetch_clients(self) -> List[Client]:
        raise NotImplementedError