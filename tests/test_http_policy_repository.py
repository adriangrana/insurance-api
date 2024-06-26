import pytest
from app.infrastructure.http.http_policy_repository import PolicyServiceAdapter

@pytest.mark.asyncio
async def test_should_return_an_policy_on_call_fetch_policies(httpx_mock, test_policy):
  httpx_mock.add_response(json=[test_policy.model_dump()])
  adapter = PolicyServiceAdapter()
  policies = await adapter.fetch_policies()

  assert len(policies) == 1
  assert policies[0] == test_policy

