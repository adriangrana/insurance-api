import pytest
from app.application.client_service import ClientService
from app.domain.models.client import Client
from app.infrastructure.http.http_client_repository import ClientServiceAdapter

@pytest.mark.asyncio
async def test_should_throw_a_UserNotFoundException_on_call_get_user_by_id(mocker, test_client):
  adapter = ClientServiceAdapter()
  mocker.patch.object(adapter, "fetch_clients", return_value=[test_client])
  service = ClientService(client_repo=adapter)
  try:
    await service.get_user_by_id("test-id")
  except Exception as e:
    assert e.__class__.__name__ == "UserNotFoundException"
    assert str(e) == "User with id test-id not found"

@pytest.mark.asyncio
async def test_should_return_a_client_on_call_get_user_by_id(mocker, test_client):
  adapter = ClientServiceAdapter()
  mocker.patch.object(adapter, "fetch_clients", return_value=[test_client])
  service = ClientService(client_repo=adapter)
  client = await service.get_user_by_id(test_client.id)
  assert client == test_client

@pytest.mark.asyncio
async def test_should_throw_a_UserNotFoundException_on_call_get_user_by_name(mocker, test_client):
  adapter = ClientServiceAdapter()
  mocker.patch.object(adapter, "fetch_clients", return_value=[test_client])
  service = ClientService(client_repo=adapter)
  try:
    await service.get_user_by_name("unknown-name")
  except Exception as e:
    assert e.__class__.__name__ == "UserNotFoundException"
    assert str(e) == "User with name unknown-name not found"

@pytest.mark.asyncio
async def test_should_return_a_client_on_call_get_user_by_name(mocker, test_client):
  adapter = ClientServiceAdapter()
  mocker.patch.object(adapter, "fetch_clients", return_value=[test_client])
  service = ClientService(client_repo=adapter)
  client = await service.get_user_by_name(test_client.name)
  assert client == test_client

