import httpx
from typing import List
from app.domain.models.client import Client
from app.domain.repositories.client_repository import ClientRepository
from app.infrastructure.config import settings

class ClientServiceAdapter(ClientRepository):
  async def fetch_clients(self) -> List[Client]:
    async with httpx.AsyncClient() as client:
      response = await client.get(settings.client_service_url)
      response.raise_for_status()
      clients_data = response.json()
      return [Client(**client) for client in clients_data]
