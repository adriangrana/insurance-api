from typing import List, Optional
from app.domain.repositories.client_repository import ClientRepository
from app.domain.repositories.policy_repository import PolicyRepository
from app.domain.exceptions import PolicyNotFoundException, UserNotFoundException
from app.domain.models.client import Client
from app.domain.models.policy import Policy

class PolicyService:
  def __init__(self, policy_repo: PolicyRepository, client_repo: ClientRepository):
    self.policy_repo = policy_repo
    self.client_repo = client_repo

  async def get_policies_by_username(self, user_name: str) -> List[Policy]:
    clients = await self.client_repo.fetch_clients()
    user = next((client for client in clients if client.name == user_name), None)
    if user:
      policies = await self.policy_repo.fetch_policies()
      return [policy for policy in policies if policy.client_id == user.id]
    raise UserNotFoundException(f"User with name {user_name} not found")

  async def get_user_by_policy_number(self, policy_id: str) -> Optional[Client]:
    policies = await self.policy_repo.fetch_policies()
    policy = next((policy for policy in policies if policy.id == policy_id), None)
    if policy:
      clients = await self.client_repo.fetch_clients()
      return next((client for client in clients if client.id == policy.client_id), None)
    raise PolicyNotFoundException(f"Policy with id {policy_id} not found")
