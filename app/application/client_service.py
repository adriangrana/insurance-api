from typing import Optional
from app.domain.exceptions import UserNotFoundException
from app.domain.repositories.client_repository import ClientRepository
from app.domain.models.client import Client

class ClientService:
  def __init__(self, client_repo: ClientRepository):
    self.client_repo = client_repo

  async def get_user_by_id(self, user_id: str) -> Optional[Client]:
    clients = await self.client_repo.fetch_clients()
    for client in clients:
      if client.id == user_id:
        return client
    raise UserNotFoundException(f"User with id {user_id} not found")

  async def get_user_by_name(self, user_name: str) -> Optional[Client]:
    clients = await self.client_repo.fetch_clients()
    for client in clients:
      if client.name == user_name:
        return client
    raise UserNotFoundException(f"User with name {user_name} not found")
