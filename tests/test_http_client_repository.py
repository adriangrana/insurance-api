import pytest
from app.infrastructure.http.http_client_repository import ClientServiceAdapter

@pytest.mark.asyncio
async def test_should_return_an_Client_on_call_fetch_clients(httpx_mock, test_client):
  httpx_mock.add_response(json=[test_client.model_dump()])
  adapter = ClientServiceAdapter()
  clients = await adapter.fetch_clients()

  assert len(clients) == 1
  assert clients[0].id == test_client.id
  assert clients[0].name == test_client.name
  assert clients[0].email == test_client.email
  assert clients[0].role == test_client.role

