import pytest
from unittest.mock import AsyncMock
from app.domain.models.user import User
from app.infrastructure.database.mongo_user_repository import UserServiceAdapter

@pytest.mark.asyncio
async def test_should_return_an_user_on_call_find_user_by_username(mock_db, test_user_admin):
  adapter = UserServiceAdapter(mydb=mock_db)
  adapter.collection.find_one = AsyncMock(return_value=test_user_admin.model_dump())
  user = await adapter.find_user_by_username(test_user_admin.username)
  assert user.username == test_user_admin.username
  assert user.email == test_user_admin.email
  assert user.hashed_password == test_user_admin.hashed_password
  assert user.roles == test_user_admin.roles


@pytest.mark.asyncio
async def test_should_return_None_on_call_find_user_by_username(mock_db, test_user_admin):
  adapter = UserServiceAdapter(mydb=mock_db)
  adapter.collection.find_one = AsyncMock(return_value=None)
  user = await adapter.find_user_by_username(test_user_admin.username)
  assert user == None


@pytest.mark.asyncio
async def test_should_create_user(mock_db, test_user_admin):
  adapter = UserServiceAdapter(mydb=mock_db)
  adapter.collection.insert_one = AsyncMock()
  await adapter.create_user(test_user_admin)
  adapter.collection.insert_one.assert_called_once_with(test_user_admin.model_dump())
  adapter.collection.insert_one.assert_awaited_once_with(test_user_admin.model_dump())