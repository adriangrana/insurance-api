from sqlite3 import adapters
import pytest
from app.application.policy_service import PolicyService
from app.domain.models.policy import Policy
from app.infrastructure.http.http_client_repository import ClientServiceAdapter
from app.infrastructure.http.http_policy_repository import PolicyServiceAdapter

@pytest.mark.asyncio
async def test_should_throw_a_UserNotFoundException_get_policies_by_username(mocker, test_policy, test_client):
  policyAdapter = PolicyServiceAdapter()
  clientAdapter = ClientServiceAdapter()
  mocker.patch.object(policyAdapter, "fetch_policies", return_value=[test_policy])
  mocker.patch.object(clientAdapter, "fetch_clients", return_value=[test_client])
  service = PolicyService(client_repo=clientAdapter, policy_repo=policyAdapter)
  try:
    await service.get_policies_by_username("test-name")
  except Exception as e:
    assert e.__class__.__name__ == "UserNotFoundException"
    assert str(e) == "User with name test-name not found"

@pytest.mark.asyncio
async def test_should_return_a_policies_get_policies_by_username(mocker, test_client, test_policy):
  policyAdapter = PolicyServiceAdapter()
  clientAdapter = ClientServiceAdapter()
  mocker.patch.object(policyAdapter, "fetch_policies", return_value=[test_policy])
  mocker.patch.object(clientAdapter, "fetch_clients", return_value=[test_client])
  service = PolicyService(client_repo=clientAdapter, policy_repo=policyAdapter)
  policies = await service.get_policies_by_username(test_client.name)
  assert policies == [test_policy]

@pytest.mark.asyncio
async def test_should_throw_a_UserNotFoundException_get_user_by_policy_number(mocker, test_policy, test_client):
  policyAdapter = PolicyServiceAdapter()
  clientAdapter = ClientServiceAdapter()
  mocker.patch.object(policyAdapter, "fetch_policies", return_value=[test_policy])
  mocker.patch.object(clientAdapter, "fetch_clients", return_value=[test_client])
  service = PolicyService(client_repo=clientAdapter, policy_repo=policyAdapter)
  try:
    await service.get_user_by_policy_number("test-name")
  except Exception as e:
    assert e.__class__.__name__ == "PolicyNotFoundException"
    assert str(e) == "Policy with id test-name not found"

@pytest.mark.asyncio
async def test_should_return_a_policies_get_user_by_policy_number(mocker, test_client, test_policy):
  policyAdapter = PolicyServiceAdapter()
  clientAdapter = ClientServiceAdapter()
  mocker.patch.object(policyAdapter, "fetch_policies", return_value=[test_policy])
  mocker.patch.object(clientAdapter, "fetch_clients", return_value=[test_client])
  service = PolicyService(client_repo=clientAdapter, policy_repo=policyAdapter)
  users = await service.get_user_by_policy_number(test_policy.id)
  assert users == test_client