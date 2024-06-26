from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.testclient import TestClient
import pytest
from app.domain.models.user import User
from app.infrastructure.controllers.auth import get_current_user, router as auth_router
from app.infrastructure.database.mongo_user_repository import UserServiceAdapter
from app.main import app

client = TestClient(app)
app.include_router(auth_router)

def test_should_return_200_on_login_for_access_token(mocker, test_user):
	mocker.patch("app.application.auth_service.AuthService.authenticate_user", return_value=test_user)
	response = client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
	assert response.status_code == 200
	assert "access_token" in response.json()
	assert response.json()["token_type"] == "bearer"

def test_should_return_401_on_login_for_access_token(mocker):
	mocker.patch("app.application.auth_service.AuthService.authenticate_user", return_value=False)
	try:
		client.post("/auth/token", data={"username": "testuser", "password": "testpassword"})
	except Exception as e:
		assert e.status_code == 401
		assert e.detail == "Could not validate credentials"
		assert e.headers == {"WWW-Authenticate": "Bearer"}

@pytest.mark.asyncio
async def test_get_current_user(mocker, token, test_user):
	mocker.patch("app.infrastructure.database.mongo_user_repository.UserServiceAdapter.find_user_by_username", return_value=test_user)
	credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
	user_repo = UserServiceAdapter()
	user = await get_current_user(credentials=credentials, user_repo=user_repo)
	assert user.username == "testuser"
	assert user.roles == ["users"]
