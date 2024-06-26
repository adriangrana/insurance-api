import pytest
from fastapi.testclient import TestClient
from app.application.client_service import ClientService
from app.infrastructure.http.http_client_repository import ClientServiceAdapter
from app.main import app

client = TestClient(app)

def test_should_return_401_on_call_get_user_by_id():
	response = client.get("/users/test-id", headers={"Authorization": "bearer test-token"})
	assert response.status_code == 401

def test_should_return_404_on_call_get_user_by_id(mocker, admin_token, test_user):
	mocker.patch("app.infrastructure.database.mongo_user_repository.UserServiceAdapter.find_user_by_username", return_value=test_user)
	response = client.get("/users/test-id",  headers = {"Authorization": f"Bearer {admin_token}"})
	assert response.status_code == 404

def test_should_return_200_on_call_get_user_by_id(mocker, admin_token, test_client,test_user_admin):
	mocker.patch("app.infrastructure.database.mongo_user_repository.UserServiceAdapter.find_user_by_username", return_value=test_user_admin)
	response = client.get("/users/"+test_client.id,  headers = {"Authorization": f"Bearer {admin_token}"})
	assert response.status_code == 200

def test_should_return_401_on_call_get_user_by_name():
	response = client.get("/users/name/test-name", headers={"Authorization": "bearer test-token"})
	assert response.status_code == 401

def test_should_return_404_on_call_get_user_by_name(mocker, admin_token, test_user):
	mocker.patch("app.infrastructure.database.mongo_user_repository.UserServiceAdapter.find_user_by_username", return_value=test_user)
	response = client.get("/users/name/test-name",  headers = {"Authorization": f"Bearer {admin_token}"})
	assert response.status_code == 404

def test_should_return_402_on_call_get_user_by_name(mocker, admin_token, test_client,test_user_admin):
	mocker.patch("app.infrastructure.database.mongo_user_repository.UserServiceAdapter.find_user_by_username", return_value=test_user_admin)
	response = client.get("/users/name/"+test_client.name,  headers = {"Authorization": f"Bearer {admin_token}"})
	assert response.status_code == 200

def test_should_return_401_on_call_get_policies_by_username():
	response = client.get("/policies/user/test-name", headers={"Authorization": "bearer test-token"})
	assert response.status_code == 401

def test_should_return_404_on_call_get_policies_by_username(mocker, admin_token, test_user, httpx_mock, test_policy, test_client):
	httpx_mock.add_response(json=[test_client.model_dump()])
	mocker.patch("app.infrastructure.database.mongo_user_repository.UserServiceAdapter.find_user_by_username", return_value=test_user)
	response = client.get("/policies/user/test-name",  headers = {"Authorization": f"Bearer {admin_token}"})
	assert response.status_code == 404

def test_should_return_200_on_call_get_policies_by_username(mocker, admin_token, test_user_admin, httpx_mock, test_policy, test_client):
	httpx_mock.add_response(json=[test_client.model_dump()])
	httpx_mock.add_response(json=[test_policy.model_dump()])
	mocker.patch("app.infrastructure.database.mongo_user_repository.UserServiceAdapter.find_user_by_username", return_value=test_user_admin)
	response = client.get("/policies/user/"+test_client.name,  headers = {"Authorization": f"Bearer {admin_token}"})
	assert response.status_code == 200

def test_should_return_401_on_call_get_user_by_policy_number():
	response = client.get("/users/policy/test-policy-id", headers={"Authorization": "bearer test-token"})
	assert response.status_code == 401


def test_should_return_404_on_call_get_user_by_policy_number(mocker, admin_token, test_user, httpx_mock, test_policy, test_client):
	httpx_mock.add_response(json=[test_policy.model_dump()])
	mocker.patch("app.infrastructure.database.mongo_user_repository.UserServiceAdapter.find_user_by_username", return_value=test_user)
	response = client.get("/users/policy/test-id",  headers = {"Authorization": f"Bearer {admin_token}"})
	assert response.status_code == 404

def test_should_return_200_on_call_get_user_by_policy_number(mocker, admin_token,test_user_admin, httpx_mock, test_policy, test_client):
	httpx_mock.add_response(json=[test_policy.model_dump()])
	httpx_mock.add_response(json=[test_client.model_dump()])
	mocker.patch("app.infrastructure.database.mongo_user_repository.UserServiceAdapter.find_user_by_username", return_value=test_user_admin)
	response = client.get("/users/policy/"+test_policy.id,  headers = {"Authorization": f"Bearer {admin_token}"})
	assert response.status_code == 200

