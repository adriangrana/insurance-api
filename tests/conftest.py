from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient
from app.application.auth_service import ALGORITHM, SECRET_KEY, AuthService
from app.domain.models.client import Client
from app.domain.models.policy import Policy
from app.domain.models.user import User
from app.infrastructure.config import Settings
from app.infrastructure.database.mongo_user_repository import UserServiceAdapter
from app.main import app
from app.infrastructure.controllers.auth import router as auth_router
from app.infrastructure.database.mongodb import   db
from jose import jwt
from pytest_httpx import HTTPXMock

@pytest.fixture
def httpx_mock(httpx_mock: HTTPXMock):
    yield httpx_mock

@pytest.fixture
def client():
	app.include_router(auth_router)
	client = TestClient(app)
	return client

@pytest.fixture
def auth():
	return {"access_token": "test-token", "token_type": "bearer"}

@pytest.fixture
def token():
    data = {"sub": "testuser", "roles": ["users"]}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def admin_token():
    data = {"sub": "testuser", "roles": ["users","admin"]}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture
def test_user():
	return User(
		username="testuser",
		email="testuser@example.com",
		hashed_password="fakehashed",
		roles=["users"]
	)

@pytest.fixture
def test_user_admin():
	return User(
		username="testuseradmin",
		email="testuser@example.com",
		hashed_password="fakehashed",
		roles=["users","admin"]
	)

@pytest.fixture
def test_policy():
	return Policy(
		id= "dde33fe3-b04c-4d4b-994f-c823e4908be5",
		amountInsured= 904.86,
		email= "inesblankenship@quotezart.com",
		inceptionDate= "2015-11-19T05:37:56Z",
		installmentPayment= True,
		clientId= "a0ece5db-cd14-4f21-812f-966633e7be86"
	)


@pytest.fixture
def test_client():
	return Client(
		id="a0ece5db-cd14-4f21-812f-966633e7be86",
		name= "Britney",
		email= "britneyblankenship@quotezart.com",
		role= "admin"
	)

@pytest.fixture
def admin_user():
	return User(
		username="adminuser",
		email="adminuser@example.com",
		hashed_password="$2b$12$4rrT8SrOAHtlqu3PI2ENlOSVShWAfxLgbuvpUXqdHSHQ1nR16HRHq",
		roles=["admin", "users"]
	)


@pytest.fixture
def mock_db():
	mock_client = AsyncMock()
	mock_collection = AsyncMock()
	mock_client[Settings.mongodb_db].users = mock_collection
	with patch.object(db, 'client', mock_client):
		yield db

@pytest.fixture
def mock_user_service_adapter(admin_user, mock_db):
	user_service_adapter = UserServiceAdapter(mydb=mock_db)
	user_service_adapter.find_user_by_username = AsyncMock(return_value=admin_user)
	user_service_adapter.create_user = AsyncMock()
	return user_service_adapter

@pytest.fixture
def test_auth_service(mock_user_service_adapter, admin_user):
	auth_service = AuthService(user_repo=mock_user_service_adapter)
	auth_service.authenticate_user = AsyncMock(return_value=admin_user)
	auth_service.create_access_token = AsyncMock(return_value="test_token")
	return auth_service

@pytest.fixture
def mock_auth_service(mocker, test_auth_service):
	return mocker.patch('app.application.auth_service', return_value=test_auth_service)

@pytest.fixture
def mock_get_current_user(mocker, test_user):
	return mocker.patch('app.infrastructure.controllers.auth.get_current_user', return_value=test_user)

@pytest.fixture
def mock_get_current_admin(mocker, admin_user):
	return mocker.patch('app.infrastructure.controllers.auth.get_current_user', return_value=admin_user)

