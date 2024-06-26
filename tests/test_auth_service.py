import pytest
from app.application.auth_service import ALGORITHM, SECRET_KEY, AuthService
from jose import jwt
@pytest.mark.asyncio
async def test_should_return_False_on_call_authenticate_user(mock_user_service_adapter, admin_user):
	test_auth_service = AuthService(user_repo = mock_user_service_adapter)
	user = await test_auth_service.authenticate_user("adminuser", "Master1")
	assert user == False

@pytest.mark.asyncio
async def test_should_return_an_admin_user_on_call_authenticate_user(mock_user_service_adapter, admin_user):
	test_auth_service = AuthService(user_repo = mock_user_service_adapter)
	user = await test_auth_service.authenticate_user("adminuser", "Master")
	assert user == admin_user

def test_should_return_a_token_on_call_create_access_token(mock_user_service_adapter):
	auth_service = AuthService(user_repo = mock_user_service_adapter)
	data = {"sub": "testuser", "roles": ["users"]}
	created_token = auth_service.create_access_token(data)
	payload = jwt.decode(created_token, SECRET_KEY, algorithms=[ALGORITHM])
	username: str = payload.get("sub")
	roles: list = payload.get("roles", [])
	assert username == "testuser"
	assert roles == ["users"]

def test_should_a_hashed_password():
	auth_service = AuthService(user_repo = None)
	password = "Master"
	hashed_password = auth_service.get_password_hash(password)
	assert auth_service.verify_password(password, hashed_password) == True
	assert auth_service.verify_password("master", hashed_password) == False
	assert auth_service.verify_password("Master", hashed_password) == True
	assert auth_service.verify_password("Master1", hashed_password) == False
